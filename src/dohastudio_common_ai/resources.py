"""Offline access to the packaged Common AI Contract v1 resources."""

from __future__ import annotations

import json
from importlib.resources import files
from types import MappingProxyType
from typing import Any

from referencing import Registry, Resource

SCHEMA_FILES = MappingProxyType(
    {
        "common_envelope": "common-envelope.schema.json",
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
)
_RESOURCE_FILES = frozenset({*SCHEMA_FILES.values(), "version-policy.json"})


class ContractResourceError(LookupError):
    """A requested packaged contract resource is unknown or unavailable."""


def schema_names() -> tuple[str, ...]:
    """Return canonical schema names in deterministic order."""

    return tuple(sorted(SCHEMA_FILES))


def resource_names() -> tuple[str, ...]:
    """Return packaged JSON resource names in deterministic order."""

    return tuple(sorted(_RESOURCE_FILES))


def _resource(name: str):
    if name not in _RESOURCE_FILES:
        raise ContractResourceError("Unknown Common AI Contract resource.")
    resource = files("dohastudio_common_ai").joinpath("resources", "v1", name)
    if not resource.is_file():
        raise ContractResourceError("Common AI Contract resource is unavailable.")
    return resource


def read_resource(name: str) -> dict[str, Any]:
    """Read one allowed UTF-8 JSON resource without exposing its filesystem path."""

    try:
        value = json.loads(_resource(name).read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ContractResourceError(
            "Common AI Contract resource could not be read."
        ) from exc
    if not isinstance(value, dict):
        raise ContractResourceError("Common AI Contract resource is invalid.")
    return value


def get_schema(name_or_id: str) -> dict[str, Any]:
    """Return a schema by canonical name or exact schema identifier."""

    filename = SCHEMA_FILES.get(name_or_id)
    if filename is not None:
        return read_resource(filename)
    for candidate in SCHEMA_FILES.values():
        schema = read_resource(candidate)
        if schema.get("$id") == name_or_id:
            return schema
    raise ContractResourceError("Unknown Common AI Contract schema.")


def build_registry() -> Registry:
    """Build the complete offline registry from the twelve packaged schemas."""

    schemas = [read_resource(name) for name in SCHEMA_FILES.values()]
    return Registry().with_resources(
        (schema["$id"], Resource.from_contents(schema)) for schema in schemas
    )
