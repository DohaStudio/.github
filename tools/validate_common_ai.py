#!/usr/bin/env python3
"""DohaStudio Common AI Contract v1 schema and cross-object validator."""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas" / "common-ai" / "v1"
POLICY_FILE = SCHEMA_DIR / "version-policy.json"
SCHEMA_FILES = {
    "music_intent": "music-intent.schema.json",
    "provider_capability": "provider-capability.schema.json",
    "rights_metadata": "rights-metadata.schema.json",
    "training_eligibility": "training-eligibility.schema.json",
    "learning_candidate": "learning-candidate.schema.json",
    "dataset_version": "dataset-version.schema.json",
    "dataset_manifest": "dataset-manifest.schema.json",
    "training_run": "training-run.schema.json",
    "evaluation_run": "evaluation-run.schema.json",
    "model_version": "model-version.schema.json",
    "model_manifest": "model-manifest.schema.json",
}
ID_FIELDS = {
    "music_intent": "intent_id",
    "provider_capability": "capability_id",
    "rights_metadata": "rights_metadata_id",
    "training_eligibility": "training_eligibility_id",
    "learning_candidate": "candidate_id",
    "dataset_manifest": "dataset_manifest_id",
    "training_run": "training_run_id",
    "evaluation_run": "evaluation_run_id",
    "model_manifest": "model_manifest_id",
}
SEMVER = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$"
)
FAIL_CLOSED_RIGHTS = {"unknown", "pending_review", "rejected", "expired", "revoked"}
FAIL_CLOSED_CHECKS = {"fail", "unknown", "missing", "expired", "revoked"}
MANIFEST_KINDS = {"dataset_manifest", "model_manifest"}


@dataclass(frozen=True, order=True)
class ValidationIssue:
    code: str
    object_kind: str
    object_id: str | None
    path: str
    rule: str
    message: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ContractValidator:
    """Load the v1 registry and validate objects without external resources."""

    def __init__(self, schema_dir: Path = SCHEMA_DIR) -> None:
        self.schema_dir = schema_dir
        self.policy = self._read_json(POLICY_FILE)
        self.schemas = {
            kind: self._read_json(schema_dir / filename)
            for kind, filename in SCHEMA_FILES.items()
        }
        self.envelope = self._read_json(schema_dir / "common-envelope.schema.json")
        resources = [self.envelope, *self.schemas.values()]
        self.registry = Registry().with_resources(
            (schema["$id"], Resource.from_contents(schema)) for schema in resources
        )
        self.validators = {
            kind: Draft202012Validator(
                schema, registry=self.registry, format_checker=FormatChecker()
            )
            for kind, schema in self.schemas.items()
        }

    @staticmethod
    def _read_json(path: Path) -> Any:
        return json.loads(path.read_text(encoding="utf-8"))

    @staticmethod
    def _path(parts: Iterable[Any]) -> str:
        values = list(parts)
        return "$" + "".join(
            f"[{part}]" if isinstance(part, int) else f".{part}" for part in values
        )

    @staticmethod
    def _object_id(obj: Any) -> str | None:
        return obj.get("object_id") if isinstance(obj, dict) else None

    @staticmethod
    def _approval_status(value: Any) -> str | None:
        if isinstance(value, dict):
            return value.get("status")
        return value if isinstance(value, str) else None

    @staticmethod
    def _parse_time(value: str | None) -> datetime | None:
        if not value:
            return None
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            return None
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)

    def issue(
        self,
        code: str,
        obj: Any,
        path: str,
        rule: str,
        message: str,
        *,
        kind: str | None = None,
    ) -> ValidationIssue:
        actual_kind = kind or (
            obj.get("schema_name", "unknown") if isinstance(obj, dict) else "unknown"
        )
        return ValidationIssue(
            code, actual_kind, self._object_id(obj), path, rule, message
        )

    def check_registry(self) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        ids: set[str] = set()
        registry_schemas = {"common_envelope": self.envelope, **self.schemas}
        for kind, schema in sorted(registry_schemas.items()):
            try:
                Draft202012Validator.check_schema(schema)
            except Exception as exc:  # jsonschema emits safe schema text only
                issues.append(
                    self.issue(
                        "INVALID_SCHEMA", {}, "$", "meta-schema", str(exc), kind=kind
                    )
                )
            schema_id = schema.get("$id")
            if not isinstance(schema_id, str) or schema_id in ids:
                issues.append(
                    self.issue(
                        "SCHEMA_ID_CONFLICT",
                        {},
                        "$.$id",
                        "unique schema id",
                        "Schema $id is missing or duplicated.",
                        kind=kind,
                    )
                )
            ids.add(schema_id)
            try:
                resolver = self.registry.resolver(schema_id)
                resolver.lookup(schema_id)
            except Exception:
                issues.append(
                    self.issue(
                        "BROKEN_SCHEMA_REFERENCE",
                        {},
                        "$.$id",
                        "registry lookup",
                        "Schema resource is not resolvable from the local registry.",
                        kind=kind,
                    )
                )
                continue
            for reference in sorted(set(self._references(schema))):
                try:
                    resolver.lookup(reference)
                except Exception:
                    issues.append(
                        self.issue(
                            "BROKEN_SCHEMA_REFERENCE",
                            {},
                            "$.$ref",
                            "local reference lookup",
                            f"Schema reference is not resolvable: {reference}",
                            kind=kind,
                        )
                    )
        return sorted(issues)

    def _version_issues(
        self, obj: dict[str, Any], expected_kind: str | None
    ) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        kind = obj.get("schema_name")
        version = obj.get("schema_version")
        if not isinstance(kind, str):
            issues.append(
                self.issue(
                    "MISSING_REQUIRED_FIELD",
                    obj,
                    "$.schema_name",
                    "required",
                    "schema_name is required.",
                )
            )
            return issues
        if expected_kind and kind != expected_kind:
            issues.append(
                self.issue(
                    "OBJECT_SCHEMA_KIND_MISMATCH",
                    obj,
                    "$.schema_name",
                    "expected schema kind",
                    f"Expected {expected_kind}; received {kind}.",
                )
            )
        if kind not in self.schemas:
            issues.append(
                self.issue(
                    "OBJECT_SCHEMA_KIND_MISMATCH",
                    obj,
                    "$.schema_name",
                    "registered schema kind",
                    f"No v1 schema is registered for {kind}.",
                )
            )
            return issues
        if not isinstance(version, str):
            issues.append(
                self.issue(
                    "MISSING_REQUIRED_FIELD",
                    obj,
                    "$.schema_version",
                    "required",
                    "schema_version is required.",
                )
            )
            return issues
        match = SEMVER.fullmatch(version)
        if not match:
            issues.append(
                self.issue(
                    "INVALID_SCHEMA_VERSION",
                    obj,
                    "$.schema_version",
                    "semantic version",
                    "schema_version must be SemVer.",
                )
            )
            return issues
        major, minor = int(match.group(1)), int(match.group(2))
        if major != self.policy["supported_major"]:
            issues.append(
                self.issue(
                    "UNSUPPORTED_SCHEMA_VERSION",
                    obj,
                    "$.schema_version",
                    "supported major",
                    f"Schema major {major} is unsupported.",
                )
            )
        maximum = self.policy["maximum_minor"]
        if minor < self.policy["minimum_minor"] or (
            maximum is not None and minor > maximum
        ):
            issues.append(
                self.issue(
                    "UNSUPPORTED_SCHEMA_VERSION",
                    obj,
                    "$.schema_version",
                    "supported minor",
                    f"Schema minor {minor} is outside the supported range.",
                )
            )
        if version in self.policy["deprecated_versions"]:
            issues.append(
                self.issue(
                    "DEPRECATED_SCHEMA_VERSION",
                    obj,
                    "$.schema_version",
                    "deprecated version",
                    f"Schema version {version} is deprecated.",
                )
            )
        return issues

    def _schema_issue(self, obj: dict[str, Any], error: Any) -> ValidationIssue:
        code_by_validator = {
            "required": "MISSING_REQUIRED_FIELD",
            "enum": "INVALID_ENUM_VALUE",
            "const": "SCHEMA_CONSTRAINT_VIOLATION",
            "additionalProperties": "UNKNOWN_FIELD",
            "unevaluatedProperties": "UNKNOWN_FIELD",
            "format": "INVALID_FORMAT",
            "pattern": "INVALID_FORMAT",
            "minItems": "EMPTY_REQUIRED_COLLECTION",
            "uniqueItems": "DUPLICATE_ITEM",
        }
        code = code_by_validator.get(error.validator, "SCHEMA_VALIDATION_ERROR")
        if error.validator == "const" and list(error.path) == ["schema_name"]:
            code = "OBJECT_SCHEMA_KIND_MISMATCH"
        return self.issue(
            code,
            obj,
            self._path(error.absolute_path),
            str(error.validator),
            error.message,
        )

    @staticmethod
    def _forbidden_keys(value: Any, forbidden: set[str]) -> set[str]:
        found: set[str] = set()
        if isinstance(value, dict):
            for key, child in value.items():
                if key.lower() in forbidden:
                    found.add(key)
                found.update(ContractValidator._forbidden_keys(child, forbidden))
        elif isinstance(value, list):
            for child in value:
                found.update(ContractValidator._forbidden_keys(child, forbidden))
        return found

    @staticmethod
    def _references(value: Any) -> Iterable[str]:
        if isinstance(value, dict):
            reference = value.get("$ref")
            if isinstance(reference, str):
                yield reference
            for child in value.values():
                yield from ContractValidator._references(child)
        elif isinstance(value, list):
            for child in value:
                yield from ContractValidator._references(child)

    def validate_object(
        self, obj: Any, expected_kind: str | None = None
    ) -> list[ValidationIssue]:
        if not isinstance(obj, dict):
            return [
                self.issue(
                    "SCHEMA_VALIDATION_ERROR",
                    obj,
                    "$",
                    "type",
                    "Contract object must be a JSON object.",
                )
            ]
        issues = self._version_issues(obj, expected_kind)
        kind = obj.get("schema_name")
        if kind not in self.validators or any(
            issue.code
            in {
                "OBJECT_SCHEMA_KIND_MISMATCH",
                "UNSUPPORTED_SCHEMA_VERSION",
                "INVALID_SCHEMA_VERSION",
            }
            for issue in issues
        ):
            return sorted(set(issues))
        for error in sorted(
            self.validators[kind].iter_errors(obj),
            key=lambda item: (list(item.absolute_path), item.message),
        ):
            issues.append(self._schema_issue(obj, error))
        id_field = ID_FIELDS.get(kind)
        if id_field and obj.get(id_field) != obj.get("object_id"):
            issues.append(
                self.issue(
                    "OBJECT_ID_MISMATCH",
                    obj,
                    f"$.{id_field}",
                    "canonical object identity",
                    f"{id_field} must equal object_id.",
                )
            )
        if kind == "music_intent" and set(obj.get("preserve", [])) & set(
            obj.get("replace", [])
        ):
            issues.append(
                self.issue(
                    "INTENT_CONFLICT",
                    obj,
                    "$.preserve",
                    "preserve/replace disjointness",
                    "preserve and replace must not contain the same path.",
                )
            )
        if kind == "provider_capability":
            forbidden = {
                "endpoint",
                "credential",
                "api_key",
                "access_token",
                "refresh_token",
                "model_path",
                "storage_path",
            }
            found = self._forbidden_keys(obj, forbidden)
            if found:
                issues.append(
                    self.issue(
                        "PROVIDER_BOUNDARY_VIOLATION",
                        obj,
                        "$",
                        "provider discovery boundary",
                        f"Forbidden provider execution fields: {', '.join(sorted(found))}.",
                    )
                )
        if kind == "training_eligibility":
            if self._forbidden_keys(obj, {"runtime_allowed"}):
                issues.append(
                    self.issue(
                        "TRAINING_ELIGIBILITY_RUNTIME_AUTHORITY",
                        obj,
                        "$",
                        "candidate-only eligibility",
                        "TrainingEligibility must not contain runtime_allowed.",
                    )
                )
            if obj.get("training_allowed"):
                checks = obj.get("checks", {})
                if any(value != "pass" for value in checks.values()):
                    issues.append(
                        self.issue(
                            "TRAINING_ELIGIBILITY_FAILURE",
                            obj,
                            "$.checks",
                            "all candidate checks pass",
                            "training_allowed requires every canonical check to pass.",
                        )
                    )
        return sorted(set(issues))

    @staticmethod
    def _rights_allowed(rights: dict[str, Any], purpose: str) -> bool:
        if rights.get("rights_status") in FAIL_CLOSED_RIGHTS:
            return False
        if rights.get("rights_status") not in {"approved", "approved_limited"}:
            return False
        retention = rights.get("retention_allowed")
        retention_allowed = (
            retention.get("allowed") if isinstance(retention, dict) else retention
        )
        if not retention_allowed:
            return False
        if purpose == "training":
            return rights.get("training_allowed") is True
        if purpose == "runtime":
            return (
                rights.get("analysis_allowed") is True
                and rights.get("derivative_generation_allowed") is True
            )
        return False

    def _manifest_identity_issues(
        self, manifest: dict[str, Any], version: dict[str, Any]
    ) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        if manifest.get("schema_name") == "dataset_manifest":
            expected_kind = "dataset_version"
            pairs = [
                ("source_dataset_version_id", version.get("object_id")),
                ("source_dataset_version_checksum", version.get("content_fingerprint")),
                ("dataset_id", version.get("dataset_id")),
                ("dataset_version", version.get("dataset_version")),
            ]
        else:
            expected_kind = "model_version"
            pairs = [
                ("source_model_version_id", version.get("object_id")),
                ("model_id", version.get("model_id")),
                ("model_version", version.get("model_version")),
            ]
        if version.get("schema_name") != expected_kind:
            issues.append(
                self.issue(
                    "MANIFEST_IDENTITY_MISMATCH",
                    manifest,
                    "$",
                    "Manifest/Version kind identity",
                    f"Manifest requires an authoritative {expected_kind} source.",
                )
            )
        for field, expected in pairs:
            if expected is not None and manifest.get(field) != expected:
                issues.append(
                    self.issue(
                        "MANIFEST_IDENTITY_MISMATCH",
                        manifest,
                        f"$.{field}",
                        "Version/Manifest identity",
                        f"{field} does not match the authoritative Version.",
                    )
                )
        return issues

    def validate_transition(self, previous: Any, current: Any) -> list[ValidationIssue]:
        issues = self.validate_object(previous) + self.validate_object(current)
        if not isinstance(previous, dict) or not isinstance(current, dict):
            return sorted(set(issues))
        if previous.get("schema_name") not in MANIFEST_KINDS or previous.get(
            "schema_name"
        ) != current.get("schema_name"):
            return sorted(set(issues))
        if previous.get("object_id") != current.get("object_id"):
            if current.get("supersedes") != previous.get("object_id"):
                issues.append(
                    self.issue(
                        "INVALID_REFERENCE",
                        current,
                        "$.supersedes",
                        "manifest replacement lineage",
                        "A replacement Manifest must reference the previous Manifest with supersedes.",
                    )
                )
            return sorted(set(issues))
        if previous.get("manifest_status") == "issued" and previous != current:
            issues.append(
                self.issue(
                    "ISSUED_MANIFEST_MUTATION",
                    current,
                    "$",
                    "issued Manifest immutability",
                    "An issued Manifest cannot change while retaining its ID.",
                )
            )
            changed = sorted(
                key
                for key in set(previous) | set(current)
                if previous.get(key) != current.get(key)
            )
            if any("checksum" in key or key.startswith("source_") for key in changed):
                issues.append(
                    self.issue(
                        "IMMUTABLE_FIELD_CHANGED",
                        current,
                        "$",
                        "immutable identity fields",
                        f"Immutable fields changed: {', '.join(changed)}.",
                    )
                )
        return sorted(set(issues))

    def _dataset_gate_issues(
        self,
        dataset: dict[str, Any],
        by_kind: dict[str, list[dict[str, Any]]],
        by_id: dict[str, dict[str, Any]],
        evaluated_at: datetime,
    ) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        if (
            dataset.get("status") != "frozen"
            or dataset.get("approved") is not True
            or dataset.get("frozen") is not True
            or dataset.get("training_allowed") is not True
        ):
            issues.append(
                self.issue(
                    "DATASET_ELIGIBILITY_FAILURE",
                    dataset,
                    "$",
                    "frozen approved DatasetVersion",
                    "Training requires an approved, frozen, training-allowed DatasetVersion.",
                )
            )
        split = dataset.get("split_manifest", {})
        split_names = ("train", "validation", "test")
        split_sets = {name: set(split.get(name, [])) for name in split_names}
        union = set().union(*split_sets.values()) if split_sets else set()
        for left, right in (
            ("train", "validation"),
            ("train", "test"),
            ("validation", "test"),
        ):
            overlap = split_sets[left] & split_sets[right]
            if overlap:
                issues.append(
                    self.issue(
                        "SPLIT_LEAKAGE",
                        dataset,
                        "$.split_manifest",
                        "record split isolation",
                        f"Candidate IDs overlap between {left} and {right}: {', '.join(sorted(overlap))}.",
                    )
                )
        groups = split.get("group_keys", {})
        seen_groups: dict[str, str] = {}
        for split_name in split_names:
            for candidate_id in split_sets[split_name]:
                group = groups.get(candidate_id)
                if group and group in seen_groups and seen_groups[group] != split_name:
                    issues.append(
                        self.issue(
                            "SPLIT_LEAKAGE",
                            dataset,
                            "$.split_manifest.group_keys",
                            "lineage group isolation",
                            f"Group {group} appears in {seen_groups[group]} and {split_name}.",
                        )
                    )
                elif group:
                    seen_groups[group] = split_name
        if dataset.get("candidate_count") != len(union):
            issues.append(
                self.issue(
                    "DATASET_ELIGIBILITY_FAILURE",
                    dataset,
                    "$.candidate_count",
                    "candidate set cardinality",
                    "candidate_count must equal the unique split candidate count.",
                )
            )
        candidates = {
            item.get("candidate_id"): item
            for item in by_kind.get("learning_candidate", [])
        }
        eligibility = {
            (item.get("candidate_id"), item.get("usage_purpose")): item
            for item in by_kind.get("training_eligibility", [])
        }
        for candidate_id in sorted(union):
            candidate = candidates.get(candidate_id)
            if candidate is None:
                issues.append(
                    self.issue(
                        "INVALID_REFERENCE",
                        dataset,
                        "$.split_manifest",
                        "candidate reference",
                        f"Candidate {candidate_id} does not exist.",
                    )
                )
                continue
            decision = eligibility.get((candidate_id, dataset.get("usage_purpose")))
            if decision is None:
                issues.append(
                    self.issue(
                        "DATASET_ELIGIBILITY_FAILURE",
                        dataset,
                        "$.usage_purpose",
                        "purpose-matched TrainingEligibility",
                        f"Candidate {candidate_id} has no eligibility for this purpose.",
                    )
                )
                continue
            expires = self._parse_time(decision.get("expires_at"))
            checks = decision.get("checks", {})
            if (
                decision.get("decision") != "eligible"
                or decision.get("approved") is not True
                or decision.get("training_allowed") is not True
                or any(value in FAIL_CLOSED_CHECKS for value in checks.values())
                or (expires is not None and expires <= evaluated_at)
            ):
                issues.append(
                    self.issue(
                        "DATASET_ELIGIBILITY_FAILURE",
                        decision,
                        "$",
                        "eligible unexpired candidate decision",
                        f"Candidate {candidate_id} is not eligible for Dataset inclusion.",
                    )
                )
            rights = by_id.get(decision.get("rights_metadata_id"))
            if rights is None or not self._rights_allowed(rights, "training"):
                issues.append(
                    self.issue(
                        "RIGHTS_FAILURE",
                        decision,
                        "$.rights_metadata_id",
                        "training rights fail-closed",
                        f"Candidate {candidate_id} lacks valid training rights.",
                    )
                )
        manifest = by_id.get(dataset.get("dataset_manifest_id"))
        if manifest is None or manifest.get("schema_name") != "dataset_manifest":
            issues.append(
                self.issue(
                    "DATASET_MANIFEST_MISSING",
                    dataset,
                    "$.dataset_manifest_id",
                    "issued DatasetManifest",
                    "DatasetManifest does not exist.",
                )
            )
        else:
            if manifest.get("manifest_status") != "issued":
                issues.append(
                    self.issue(
                        "DATASET_MANIFEST_NOT_ISSUED",
                        manifest,
                        "$.manifest_status",
                        "issued DatasetManifest",
                        "DatasetManifest must be issued.",
                    )
                )
            issues.extend(self._manifest_identity_issues(manifest, dataset))
        if (
            dataset.get("rights_summary", {}).get("status") != "pass"
            or dataset.get("rights_summary", {}).get("exception_count") != 0
        ):
            issues.append(
                self.issue(
                    "DATASET_ELIGIBILITY_FAILURE",
                    dataset,
                    "$.rights_summary",
                    "aggregate rights summary",
                    "Dataset rights summary must pass with zero exceptions.",
                )
            )
        return issues

    def _runtime_issues(
        self,
        model: dict[str, Any],
        by_kind: dict[str, list[dict[str, Any]]],
        by_id: dict[str, dict[str, Any]],
        integrity: dict[str, str],
        evaluated_at: datetime,
    ) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        training = by_id.get(model.get("training_run_id"))
        if (
            training is None
            or training.get("schema_name") != "training_run"
            or training.get("status") != "succeeded"
        ):
            issues.append(
                self.issue(
                    "LINEAGE_INCOMPLETE",
                    model,
                    "$.training_run_id",
                    "successful TrainingRun lineage",
                    "A successful TrainingRun is required.",
                )
            )
        elif training:
            dataset_ref = training.get("dataset_version_ref", {}).get("object_id")
            dataset = by_id.get(dataset_ref)
            if dataset is None:
                issues.append(
                    self.issue(
                        "INVALID_REFERENCE",
                        training,
                        "$.dataset_version_ref",
                        "DatasetVersion reference",
                        "TrainingRun DatasetVersion does not exist.",
                    )
                )
            else:
                issues.extend(
                    self._dataset_gate_issues(dataset, by_kind, by_id, evaluated_at)
                )
        evaluations = [by_id.get(item) for item in model.get("evaluation_run_ids", [])]
        if not evaluations or any(item is None for item in evaluations):
            issues.append(
                self.issue(
                    "MISSING_EVALUATION",
                    model,
                    "$.evaluation_run_ids",
                    "EvaluationRun presence",
                    "Every referenced EvaluationRun must exist.",
                )
            )
        else:
            for evaluation in evaluations:
                if evaluation.get("status") != "completed":
                    issues.append(
                        self.issue(
                            "MISSING_EVALUATION",
                            evaluation,
                            "$.status",
                            "completed EvaluationRun",
                            "EvaluationRun must be completed.",
                        )
                    )
                if self._approval_status(evaluation.get("approval")) != "approved":
                    issues.append(
                        self.issue(
                            "UNAPPROVED_EVALUATION",
                            evaluation,
                            "$.approval",
                            "approved EvaluationRun",
                            "EvaluationRun must be approved.",
                        )
                    )
                if training and evaluation.get("training_run_id") != training.get(
                    "training_run_id"
                ):
                    issues.append(
                        self.issue(
                            "INVALID_REFERENCE",
                            evaluation,
                            "$.training_run_id",
                            "TrainingRun lineage",
                            "EvaluationRun references a different TrainingRun.",
                        )
                    )
                if evaluation.get("rights_review") != "eligible":
                    issues.append(
                        self.issue(
                            "RIGHTS_FAILURE",
                            evaluation,
                            "$.rights_review",
                            "runtime rights review",
                            "Evaluation rights review must be eligible.",
                        )
                    )
        if self._approval_status(model.get("approval")) != "approved":
            issues.append(
                self.issue(
                    "UNAPPROVED_MODEL",
                    model,
                    "$.approval",
                    "approved ModelVersion",
                    "ModelVersion must be approved.",
                )
            )
        if (
            model.get("status") != "runtime_allowed"
            or model.get("runtime_allowed") is not True
        ):
            issues.append(
                self.issue(
                    "RUNTIME_PROMOTION_INVARIANT_FAILURE",
                    model,
                    "$.runtime_allowed",
                    "runtime promotion state",
                    "ModelVersion must explicitly be in runtime_allowed state.",
                )
            )
        if model.get("deprecated") is not False or model.get("status") == "deprecated":
            issues.append(
                self.issue(
                    "DEPRECATED_MODEL",
                    model,
                    "$.deprecated",
                    "non-deprecated model",
                    "Deprecated models cannot be promoted.",
                )
            )
        if model.get("runtime", {}).get("compatibility") != "pass":
            issues.append(
                self.issue(
                    "INCOMPATIBLE_RUNTIME",
                    model,
                    "$.runtime.compatibility",
                    "runtime compatibility",
                    "Runtime compatibility must pass.",
                )
            )
        manifest = by_id.get(model.get("model_manifest_id"))
        if manifest is None or manifest.get("schema_name") != "model_manifest":
            issues.append(
                self.issue(
                    "MODEL_MANIFEST_MISSING",
                    model,
                    "$.model_manifest_id",
                    "issued ModelManifest",
                    "ModelManifest does not exist.",
                )
            )
        else:
            if manifest.get("manifest_status") != "issued":
                issues.append(
                    self.issue(
                        "MODEL_MANIFEST_NOT_ISSUED",
                        manifest,
                        "$.manifest_status",
                        "issued ModelManifest",
                        "ModelManifest must be issued.",
                    )
                )
            issues.extend(self._manifest_identity_issues(manifest, model))
            if integrity.get(manifest.get("object_id")) != "valid":
                issues.append(
                    self.issue(
                        "MANIFEST_INTEGRITY_FAILURE",
                        manifest,
                        "$.manifest_checksum",
                        "declared integrity evidence",
                        "ModelManifest integrity evidence must be valid.",
                    )
                )
            if set(manifest.get("evaluation_run_ids", [])) != set(
                model.get("evaluation_run_ids", [])
            ):
                issues.append(
                    self.issue(
                        "MANIFEST_IDENTITY_MISMATCH",
                        manifest,
                        "$.evaluation_run_ids",
                        "evaluation lineage identity",
                        "ModelManifest and ModelVersion EvaluationRun IDs differ.",
                    )
                )
        rights = by_id.get(model.get("rights_policy_eligibility_id"))
        if (
            rights is None
            or rights.get("schema_name") != "rights_metadata"
            or not self._rights_allowed(rights, "runtime")
        ):
            issues.append(
                self.issue(
                    "RIGHTS_FAILURE",
                    model,
                    "$.rights_policy_eligibility_id",
                    "runtime rights fail-closed",
                    "Runtime rights/policy evidence is missing or ineligible.",
                )
            )
        compatible = False
        for capability in by_kind.get("provider_capability", []):
            if (
                capability.get("status") == "available"
                and model.get("object_id") in capability.get("model_version_ids", [])
                and set(model.get("supported_capability_ids", []))
                & {capability.get("capability_id")}
            ):
                compatible = True
        if not compatible:
            issues.append(
                self.issue(
                    "INCOMPATIBLE_RUNTIME",
                    model,
                    "$.supported_capability_ids",
                    "ProviderCapability compatibility evidence",
                    "No available ProviderCapability declares this model.",
                )
            )
        return issues

    def validate_scenario(self, scenario: Any) -> list[ValidationIssue]:
        if not isinstance(scenario, dict):
            return [
                self.issue(
                    "SCENARIO_INVALID",
                    scenario,
                    "$",
                    "scenario object",
                    "Scenario must be a JSON object.",
                )
            ]
        scenario = copy.deepcopy(scenario)
        defaults = scenario.get("envelope_defaults", {})
        if defaults:
            scenario["objects"] = [
                {**defaults, **obj} for obj in scenario.get("objects", [])
            ]
            for transition in scenario.get("transitions", []):
                transition["previous"] = {**defaults, **transition.get("previous", {})}
                transition["current"] = {**defaults, **transition.get("current", {})}
        issues: list[ValidationIssue] = []
        objects = scenario.get("objects", [])
        transitions = scenario.get("transitions", [])
        for obj in objects:
            issues.extend(self.validate_object(obj))
        for transition in transitions:
            issues.extend(
                self.validate_transition(
                    transition.get("previous"), transition.get("current")
                )
            )
        by_kind: dict[str, list[dict[str, Any]]] = {}
        by_id: dict[str, dict[str, Any]] = {}
        for obj in objects:
            if not isinstance(obj, dict):
                continue
            by_kind.setdefault(obj.get("schema_name", "unknown"), []).append(obj)
            object_id = obj.get("object_id")
            if object_id in by_id and by_id[object_id] != obj:
                issues.append(
                    self.issue(
                        "MANIFEST_IDENTITY_MISMATCH",
                        obj,
                        "$.object_id",
                        "unique immutable identity",
                        "The same object_id identifies different payloads.",
                    )
                )
            elif object_id:
                by_id[object_id] = obj
        evaluated_at = self._parse_time(scenario.get("evaluated_at")) or datetime.now(
            timezone.utc
        )
        for dataset in by_kind.get("dataset_version", []):
            if dataset.get("training_allowed") or dataset.get("status") == "frozen":
                issues.extend(
                    self._dataset_gate_issues(dataset, by_kind, by_id, evaluated_at)
                )
        integrity = scenario.get("manifest_integrity", {})
        for model in by_kind.get("model_version", []):
            if model.get("runtime_allowed"):
                issues.extend(
                    self._runtime_issues(model, by_kind, by_id, integrity, evaluated_at)
                )
        for manifest in by_kind.get("dataset_manifest", []):
            source = by_id.get(manifest.get("source_dataset_version_id"))
            if source:
                issues.extend(self._manifest_identity_issues(manifest, source))
        for manifest in by_kind.get("model_manifest", []):
            source = by_id.get(manifest.get("source_model_version_id"))
            if source:
                issues.extend(self._manifest_identity_issues(manifest, source))
        for kind, source_field in (
            ("dataset_manifest", "source_dataset_version_id"),
            ("model_manifest", "source_model_version_id"),
        ):
            issued_by_source: dict[str, list[dict[str, Any]]] = {}
            for manifest in by_kind.get(kind, []):
                if manifest.get("manifest_status") == "issued":
                    issued_by_source.setdefault(manifest.get(source_field), []).append(
                        manifest
                    )
            for source_id, manifests in issued_by_source.items():
                if len(manifests) < 2:
                    continue
                manifest_ids = {item.get("object_id") for item in manifests}
                linked = sum(
                    item.get("supersedes") in manifest_ids for item in manifests
                )
                if linked != len(manifests) - 1:
                    issues.append(
                        self.issue(
                            "MANIFEST_IDENTITY_MISMATCH",
                            manifests[-1],
                            f"$.{source_field}",
                            "single issued Manifest lineage",
                            f"Conflicting issued Manifests reference Version {source_id}.",
                        )
                    )
        for transition in transitions:
            current = transition.get("current", {})
            previous = transition.get("previous", {})
            if current.get("object_id") != previous.get("object_id") and current.get(
                "supersedes"
            ) != previous.get("object_id"):
                issues.append(
                    self.issue(
                        "INVALID_REFERENCE",
                        current,
                        "$.supersedes",
                        "replacement lineage",
                        "Replacement records must reference the prior immutable record.",
                    )
                )
        return sorted(set(issues))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--object", type=Path)
    group.add_argument("--scenario", type=Path)
    group.add_argument("--check-registry", action="store_true")
    parser.add_argument("--kind", choices=sorted(SCHEMA_FILES))
    args = parser.parse_args(argv)
    validator = ContractValidator()
    if args.check_registry:
        issues = validator.check_registry()
    elif args.object:
        issues = validator.validate_object(load_json(args.object), args.kind)
    else:
        issues = validator.validate_scenario(load_json(args.scenario))
    print(
        json.dumps(
            {"valid": not issues, "errors": [item.to_dict() for item in issues]},
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(main())
