"""Public API for DohaStudio Common AI Contract Schema v1."""

from __future__ import annotations

from typing import Any

from .__about__ import __version__
from .resources import (
    ContractResourceError,
    build_registry,
    get_schema,
    read_resource,
    resource_names,
    schema_names,
)
from .validator import ContractValidator, ValidationIssue


def contract_policy_version() -> str:
    """Return the executable contract policy version, separate from package version."""

    return str(read_resource("version-policy.json")["policy_version"])


def validate_contract(
    instance: Any, expected_kind: str | None = None
) -> tuple[ValidationIssue, ...]:
    """Validate one contract object and return canonical deterministic issues."""

    return tuple(ContractValidator().validate_object(instance, expected_kind))


def validate_scenario(scenario: Any) -> tuple[ValidationIssue, ...]:
    """Validate one cross-object scenario using only packaged resources."""

    return tuple(ContractValidator().validate_scenario(scenario))


__all__ = [
    "ContractResourceError",
    "ContractValidator",
    "ValidationIssue",
    "__version__",
    "build_registry",
    "contract_policy_version",
    "get_schema",
    "read_resource",
    "resource_names",
    "schema_names",
    "validate_contract",
    "validate_scenario",
]
