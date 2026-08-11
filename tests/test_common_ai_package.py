from __future__ import annotations

import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from dohastudio_common_ai import (  # noqa: E402
    ContractResourceError,
    ContractValidator,
    __version__,
    build_registry,
    contract_policy_version,
    get_schema,
    read_resource,
    resource_names,
    schema_names,
    validate_contract,
)

SCHEMAS = ROOT / "schemas" / "common-ai" / "v1"
FIXTURES = ROOT / "tests" / "fixtures" / "common-ai" / "v1"


class AuthorityResourceRoot:
    def joinpath(self, *parts: str) -> Path:
        if parts[:2] != ("resources", "v1") or len(parts) != 3:
            raise AssertionError("unexpected package resource lookup")
        return SCHEMAS / parts[2]


def authority_resources():
    return patch(
        "dohastudio_common_ai.resources.files",
        return_value=AuthorityResourceRoot(),
    )


class CommonAIPackageTests(unittest.TestCase):
    def test_package_metadata_versions_are_separate(self) -> None:
        self.assertEqual("0.1.0", __version__)
        with authority_resources():
            self.assertEqual("1.0.0", contract_policy_version())

    def test_schema_and_resource_enumeration_is_deterministic(self) -> None:
        self.assertEqual(12, len(schema_names()))
        self.assertEqual(tuple(sorted(schema_names())), schema_names())
        self.assertEqual(13, len(resource_names()))
        self.assertEqual(tuple(sorted(resource_names())), resource_names())

    def test_every_declared_resource_exists_in_authority_source(self) -> None:
        for name in resource_names():
            with self.subTest(name=name):
                self.assertTrue((SCHEMAS / name).is_file())

    def test_schema_lookup_by_name_and_id(self) -> None:
        with authority_resources():
            by_name = get_schema("music_intent")
            by_id = get_schema(by_name["$id"])
        self.assertEqual(by_name, by_id)

    def test_unknown_schema_and_traversal_fail_closed(self) -> None:
        with authority_resources():
            for value in ("unknown", "../version-policy.json", "/tmp/schema.json"):
                with self.subTest(value=value):
                    with self.assertRaises(ContractResourceError):
                        get_schema(value)
                    with self.assertRaises(ContractResourceError):
                        read_resource(value)

    def test_missing_resource_has_sanitized_error(self) -> None:
        class MissingRoot:
            def joinpath(self, *parts: str) -> Path:
                return Path(tempfile.gettempdir()) / "missing-common-ai-resource"

        with patch("dohastudio_common_ai.resources.files", return_value=MissingRoot()):
            with self.assertRaisesRegex(
                ContractResourceError,
                "Common AI Contract resource is unavailable",
            ) as caught:
                read_resource("music-intent.schema.json")
        self.assertNotIn(str(ROOT), str(caught.exception))

    def test_registry_contains_all_twelve_schema_ids(self) -> None:
        with authority_resources():
            registry = build_registry()
            ids = [get_schema(name)["$id"] for name in schema_names()]
        for schema_id in ids:
            with self.subTest(schema_id=schema_id):
                registry.resolver(schema_id).lookup(schema_id)

    def test_local_references_resolve_offline(self) -> None:
        validator = ContractValidator(_schema_dir=SCHEMAS)
        self.assertEqual([], validator.check_registry())

    def test_valid_fixture_passes_public_validation(self) -> None:
        scenario = json.loads(
            (FIXTURES / "scenarios" / "runtime-promotion.json").read_text(
                encoding="utf-8"
            )
        )
        fixture = {**scenario["envelope_defaults"], **scenario["objects"][0]}
        with authority_resources():
            issues = validate_contract(fixture, "music_intent")
        self.assertEqual((), issues)

    def test_invalid_fixture_is_deterministic_and_sanitized(self) -> None:
        scenario = json.loads(
            (FIXTURES / "scenarios" / "runtime-promotion.json").read_text(
                encoding="utf-8"
            )
        )
        defaults = scenario.pop("envelope_defaults")
        item = {**defaults, **scenario["objects"][0], "unexpected": "secret-value"}
        with authority_resources():
            first = validate_contract(item)
            second = validate_contract(item)
        self.assertEqual(first, second)
        encoded = json.dumps([issue.to_dict() for issue in first])
        self.assertNotIn("secret-value", encoded)
        self.assertNotIn(str(ROOT), encoded)
        self.assertNotIn("Traceback", encoded)

    def test_import_has_no_output_or_filesystem_mutation(self) -> None:
        before = set(ROOT.iterdir())
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured), contextlib.redirect_stderr(captured):
            __import__("dohastudio_common_ai")
        self.assertEqual("", captured.getvalue())
        self.assertEqual(before, set(ROOT.iterdir()))

    def test_current_working_directory_is_irrelevant(self) -> None:
        original = Path.cwd()
        with tempfile.TemporaryDirectory() as temporary:
            os.chdir(temporary)
            try:
                with authority_resources():
                    self.assertEqual(12, len(schema_names()))
                    schema = get_schema("music_intent")
                    self.assertEqual(
                        "music_intent", schema["properties"]["schema_name"]["const"]
                    )
            finally:
                os.chdir(original)

    def test_separator_variants_are_not_resource_names(self) -> None:
        with authority_resources():
            for value in (
                "resources/v1/music-intent.schema.json",
                "resources\\v1\\music-intent.schema.json",
            ):
                with self.subTest(value=value):
                    with self.assertRaises(ContractResourceError):
                        read_resource(value)

    def test_fresh_interpreter_import_is_silent(self) -> None:
        environment = dict(os.environ)
        environment["PYTHONPATH"] = str(ROOT / "src")
        result = subprocess.run(
            [sys.executable, "-c", "import dohastudio_common_ai"],
            cwd=tempfile.gettempdir(),
            env=environment,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("", result.stdout)
        self.assertEqual("", result.stderr)
