"""Verify an installed wheel or sdist without importing repository source."""

from __future__ import annotations

import json
import os
import socket
import tempfile
from pathlib import Path

import dohastudio_common_ai as api

VALID_INTENT = json.loads(
    """{
      "schema_version": "1.0.0",
      "created_at": "2026-08-11T00:00:00Z",
      "created_by": "actor_test",
      "producer": {"name": "synthetic-fixture", "version": "1.0.0"},
      "schema_name": "music_intent",
      "object_id": "intent_1",
      "intent_id": "intent_1",
      "operation": "planning",
      "target": {"project_id": "project_1"},
      "instruction": "Create a synthetic plan",
      "preserve": ["lyrics"],
      "replace": ["arrangement"],
      "constraints": [],
      "priority": "normal",
      "requested_capability": "lyrics_generation"
    }"""
)


def main() -> None:
    assert api.__version__ == "0.1.0"
    assert api.contract_policy_version() == "1.0.0"
    assert len(api.schema_names()) == 12
    assert len(api.resource_names()) == 13

    schema = api.get_schema("music_intent")
    assert schema == api.get_schema(schema["$id"])
    assert api.ContractValidator().check_registry() == []
    assert api.validate_contract(VALID_INTENT, "music_intent") == ()

    invalid = {**VALID_INTENT, "unexpected": "sensitive-value"}
    first = api.validate_contract(invalid, "music_intent")
    second = api.validate_contract(invalid, "music_intent")
    assert first and first == second
    encoded = json.dumps([issue.to_dict() for issue in first])
    assert "sensitive-value" not in encoded
    assert "Traceback" not in encoded

    socket.create_connection = lambda *args, **kwargs: (_ for _ in ()).throw(
        AssertionError("network attempted")
    )
    assert api.ContractValidator().check_registry() == []

    original = Path.cwd()
    with tempfile.TemporaryDirectory() as directory:
        os.chdir(directory)
        try:
            assert len(api.schema_names()) == 12
            assert api.get_schema("model_manifest")["$id"].endswith(
                "model-manifest.schema.json"
            )
        finally:
            os.chdir(original)

    print(
        f"installed package PASS version={api.__version__} "
        f"schemas={len(api.schema_names())}"
    )


if __name__ == "__main__":
    main()
