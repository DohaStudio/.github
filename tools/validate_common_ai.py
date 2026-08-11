#!/usr/bin/env python3
"""Compatibility CLI for the packaged Common AI Contract validator."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src"
if str(SOURCE) not in sys.path:
    sys.path.insert(0, str(SOURCE))

from dohastudio_common_ai.validator import (  # noqa: E402
    ContractValidator as PackageContractValidator,
)
from dohastudio_common_ai.validator import (
    ValidationIssue,
    input_load_issue,
    load_json,
)
from dohastudio_common_ai.validator import (
    main as package_main,
)

SCHEMA_DIR = ROOT / "schemas" / "common-ai" / "v1"


class ContractValidator(PackageContractValidator):
    """Repository-compatible validator backed by the authority source tree."""

    def __init__(self, schema_dir: Path = SCHEMA_DIR) -> None:
        super().__init__(_schema_dir=schema_dir)


def main(argv: list[str] | None = None) -> int:
    """Run the historical CLI against the repository authority resources."""

    return package_main(argv, schema_dir=SCHEMA_DIR)


__all__ = [
    "ContractValidator",
    "ValidationIssue",
    "input_load_issue",
    "load_json",
    "main",
]


if __name__ == "__main__":
    sys.exit(main())
