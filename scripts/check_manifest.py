#!/usr/bin/env python3
"""Independently verify manifest hashes and exact source/evidence coverage."""

from __future__ import annotations

import hashlib
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "MANIFEST_SHA256.txt"
RELEASE = ROOT / "RELEASE_SHA256.txt"
BUILD_SUFFIXES = {
    ".aux", ".bbl", ".blg", ".log", ".out", ".toc", ".fls",
    ".fdb_latexmk", ".synctex.gz",
}


def expected_paths() -> set[str]:
    answer: set[str] = set()
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if not path.is_file() or path in {MANIFEST, RELEASE}:
            continue
        if ".git" in relative.parts or "__pycache__" in relative.parts:
            continue
        if any(part.lower() == "results" for part in relative.parts) and relative.suffix.lower() == ".json":
            continue
        if relative.suffix == ".pdf" or any(relative.name.endswith(suffix) for suffix in BUILD_SUFFIXES):
            continue
        answer.add(relative.as_posix())
    return answer


def main() -> None:
    failures: list[str] = []
    seen: set[str] = set()
    for number, raw in enumerate(MANIFEST.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        try:
            expected, relative = line.split(None, 1)
        except ValueError:
            failures.append(f"line {number}: malformed")
            continue
        posix = PurePosixPath(relative)
        if posix.is_absolute() or ".." in posix.parts or relative in seen:
            failures.append(f"line {number}: unsafe or duplicate path {relative}")
            continue
        seen.add(relative)
        path = ROOT.joinpath(*posix.parts)
        if not path.is_file():
            failures.append(f"missing {relative}")
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest().upper()
        if actual != expected.upper():
            failures.append(f"mismatch {relative}")

    expected_set = expected_paths()
    for relative in sorted(expected_set - seen):
        failures.append(f"unmanifested {relative}")
    for relative in sorted(seen - expected_set):
        failures.append(f"unexpected manifest entry {relative}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        raise SystemExit(1)
    print(f"PASS manifest hashes and coverage {len(seen)}/{len(expected_set)}")


if __name__ == "__main__":
    main()
