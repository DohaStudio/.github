"""Compare built distribution resources with the authority source byte-for-byte."""

from __future__ import annotations

import argparse
import hashlib
import tarfile
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "schemas" / "common-ai" / "v1"
EXPECTED = {path.name for path in SOURCE.glob("*.json")}


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def verify_wheel(path: Path) -> None:
    with zipfile.ZipFile(path) as archive:
        resources = {
            PurePosixPath(name).name: name
            for name in archive.namelist()
            if "/resources/v1/" in name and name.endswith(".json")
        }
        assert set(resources) == EXPECTED
        for filename, member in resources.items():
            assert digest(archive.read(member)) == digest(
                (SOURCE / filename).read_bytes()
            )
        assert not any(
            part in name
            for name in archive.namelist()
            for part in ("__pycache__", ".pyc", ".venv", "/dist/", "/build/")
        )


def verify_sdist(path: Path) -> None:
    with tarfile.open(path, "r:gz") as archive:
        resources = {
            PurePosixPath(name).name: name
            for name in archive.getnames()
            if "/schemas/common-ai/v1/" in name and name.endswith(".json")
        }
        assert set(resources) == EXPECTED
        for filename, member in resources.items():
            extracted = archive.extractfile(member)
            assert extracted is not None
            assert digest(extracted.read()) == digest((SOURCE / filename).read_bytes())
        assert not any(
            part in name
            for name in archive.getnames()
            for part in ("__pycache__", ".pyc", ".venv", "/dist/", "/build/")
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--wheel", type=Path, required=True)
    parser.add_argument("--sdist", type=Path, required=True)
    arguments = parser.parse_args()
    verify_wheel(arguments.wheel)
    verify_sdist(arguments.sdist)
    print(f"distribution resources PASS count={len(EXPECTED)}")


if __name__ == "__main__":
    main()
