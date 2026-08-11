from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.validate_common_ai import ContractValidator, load_json  # noqa: E402


FIXTURES = ROOT / "tests" / "fixtures" / "common-ai" / "v1"
SCHEMAS = ROOT / "schemas" / "common-ai" / "v1"


def materialize(scenario: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(scenario)
    defaults = result.pop("envelope_defaults", {})
    result["objects"] = [{**defaults, **item} for item in result.get("objects", [])]
    for transition in result.get("transitions", []):
        transition["previous"] = {**defaults, **transition["previous"]}
        transition["current"] = {**defaults, **transition["current"]}
    return result


def mutate(document: Any, mutation: dict[str, Any]) -> None:
    tokens = [
        token.replace("~1", "/").replace("~0", "~")
        for token in mutation["path"].split("/")[1:]
    ]
    target = document
    for token in tokens[:-1]:
        target = target[int(token)] if isinstance(target, list) else target[token]
    leaf = tokens[-1]
    if mutation["op"] == "remove":
        if isinstance(target, list):
            target.pop(int(leaf))
        else:
            del target[leaf]
    elif mutation["op"] == "append":
        target[int(leaf)].append(copy.deepcopy(mutation["value"])) if isinstance(
            target, list
        ) else target[leaf].append(copy.deepcopy(mutation["value"]))
    elif mutation["op"] == "set":
        if isinstance(target, list):
            target[int(leaf)] = copy.deepcopy(mutation["value"])
        else:
            target[leaf] = copy.deepcopy(mutation["value"])
    else:
        raise AssertionError(f"unsupported mutation: {mutation['op']}")


class CommonAIContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = ContractValidator()

    def test_schema_registry_is_valid(self) -> None:
        self.assertEqual([], self.validator.check_registry())

    def test_common_envelope_fixture(self) -> None:
        envelope = load_json(SCHEMAS / "common-envelope.schema.json")
        fixture = load_json(FIXTURES / "valid" / "common-envelope.json")
        errors = list(
            Draft202012Validator(
                envelope,
                registry=self.validator.registry,
                format_checker=FormatChecker(),
            ).iter_errors(fixture)
        )
        self.assertEqual([], errors)

    def test_every_runtime_object_passes_its_schema(self) -> None:
        scenario = materialize(
            load_json(FIXTURES / "scenarios" / "runtime-promotion.json")
        )
        self.assertGreaterEqual(len(scenario["objects"]), 15)
        for item in scenario["objects"]:
            with self.subTest(
                schema_name=item["schema_name"], object_id=item["object_id"]
            ):
                self.assertEqual([], self.validator.validate_object(item))

    def test_valid_cross_object_scenarios(self) -> None:
        for name in (
            "runtime-promotion.json",
            "manifest-supersession.json",
            "model-manifest-supersession.json",
        ):
            with self.subTest(name=name):
                scenario = load_json(FIXTURES / "scenarios" / name)
                self.assertEqual([], self.validator.validate_scenario(scenario))

    def test_invalid_catalog(self) -> None:
        catalog_path = FIXTURES / "invalid" / "cases.json"
        catalog = load_json(catalog_path)
        groups = (
            ("cases", catalog["base_scenario"]),
            ("transition_cases", catalog["transition_base"]),
        )
        count = 0
        for key, relative_base in groups:
            for case in catalog[key]:
                count += 1
                with self.subTest(case=case["name"]):
                    case_base = case.get("base_scenario", relative_base)
                    base = load_json((catalog_path.parent / case_base).resolve())
                    scenario = materialize(base)
                    for change in case["mutations"]:
                        mutate(scenario, change)
                    if "expected_kind" in case:
                        issues = self.validator.validate_object(
                            scenario["objects"][case["object_index"]],
                            case["expected_kind"],
                        )
                    else:
                        issues = self.validator.validate_scenario(scenario)
                    codes = {issue.code for issue in issues}
                    self.assertIn(case["expected_code"], codes, sorted(codes))
        self.assertGreaterEqual(count, 32)

    def test_error_output_is_deterministic_and_sanitized(self) -> None:
        scenario = materialize(
            load_json(FIXTURES / "scenarios" / "runtime-promotion.json")
        )
        scenario["objects"][0]["unexpected"] = True
        first = self.validator.validate_scenario(scenario)
        second = self.validator.validate_scenario(scenario)
        self.assertEqual(first, second)
        encoded = json.dumps([item.to_dict() for item in first])
        self.assertNotIn(str(ROOT), encoded)
        self.assertNotIn("Traceback", encoded)

    def test_conflicting_issued_manifest_identity_is_rejected(self) -> None:
        scenario = materialize(
            load_json(FIXTURES / "scenarios" / "runtime-promotion.json")
        )
        conflicting = copy.deepcopy(scenario["objects"][13])
        conflicting["object_id"] = "dataset_manifest_conflict"
        conflicting["dataset_manifest_id"] = "dataset_manifest_conflict"
        conflicting["manifest_checksum"] = (
            "sha256:eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
        )
        scenario["objects"].append(conflicting)
        codes = {issue.code for issue in self.validator.validate_scenario(scenario)}
        self.assertIn("MANIFEST_IDENTITY_MISMATCH", codes)

    def test_forward_minor_uses_extensions_only(self) -> None:
        scenario = materialize(
            load_json(FIXTURES / "scenarios" / "runtime-promotion.json")
        )
        item = scenario["objects"][0]
        item["schema_version"] = "1.2.3"
        item["extensions"] = {"org.dohastudio.test": {"future_field": True}}
        self.assertEqual([], self.validator.validate_object(item))
        item["future_field"] = True
        self.assertIn(
            "UNKNOWN_FIELD",
            {issue.code for issue in self.validator.validate_object(item)},
        )
        del item["future_field"]
        item["extensions"] = {"unnamespaced": True}
        self.assertIn(
            "INVALID_FORMAT",
            {issue.code for issue in self.validator.validate_object(item)},
        )

    def test_authority_boundary_regressions(self) -> None:
        similarity = (
            ROOT / "docs" / "specifications" / "05-similarity-report.md"
        ).read_text(encoding="utf-8")
        architecture = (
            ROOT / "docs" / "architecture" / "common-ai-contracts.md"
        ).read_text(encoding="utf-8")
        self.assertNotIn("SimilarityReport MUST stop product execution", similarity)
        for phrase in ("does not execute policy", "API error", "fail-closed"):
            self.assertIn(phrase, similarity)
        for phrase in ("REST", "SSE", "Adapter Loader", "Compatibility Layer"):
            self.assertIn(phrase, architecture)


if __name__ == "__main__":
    unittest.main()
