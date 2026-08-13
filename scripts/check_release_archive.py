#!/usr/bin/env python3
"""Verify an exact, clean release archive rather than a permissive worktree."""

from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "MANIFEST_SHA256.txt"
RELEASE = ROOT / "RELEASE_SHA256.txt"
SELECTED_PDF = "paper/A_Parity_Theorem_for_RC_Invariant_MDS.pdf"
ENVELOPE_FILES = {"MANIFEST_SHA256.txt", "RELEASE_SHA256.txt", SELECTED_PDF}


def parsed_paths(path: Path) -> tuple[set[str], list[str]]:
    seen: set[str] = set()
    failures: list[str] = []
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        try:
            expected, relative = line.split(None, 1)
        except ValueError:
            failures.append(f"{path.name} line {number}: malformed")
            continue
        posix = PurePosixPath(relative)
        if posix.is_absolute() or ".." in posix.parts or relative in seen:
            failures.append(f"{path.name} line {number}: unsafe or duplicate {relative}")
            continue
        seen.add(relative)
        target = ROOT.joinpath(*posix.parts)
        if not target.is_file():
            failures.append(f"{path.name}: missing {relative}")
            continue
        actual = hashlib.sha256(target.read_bytes()).hexdigest().upper()
        if actual != expected.upper():
            failures.append(f"{path.name}: mismatch {relative}")
    return seen, failures


def actual_archive_files() -> set[str]:
    files: set[str] = set()
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if relative.parts[:1] == (".git",) or not path.is_file():
            continue
        files.add(relative.as_posix())
    return files


def main() -> None:
    failures: list[str] = []
    for script in ("check_manifest.py", "check_worktree.py"):
        completed = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / script)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        if completed.returncode != 0:
            detail = (completed.stdout + completed.stderr).strip()
            failures.append(f"{script} failed: {detail}")

    manifest_paths, manifest_failures = parsed_paths(MANIFEST)
    release_paths, release_failures = parsed_paths(RELEASE)
    failures.extend(manifest_failures)
    failures.extend(release_failures)
    if release_paths != {"MANIFEST_SHA256.txt", SELECTED_PDF}:
        failures.append(f"release paths differ: {sorted(release_paths)}")

    expected = manifest_paths | ENVELOPE_FILES
    actual = actual_archive_files()
    for relative in sorted(expected - actual):
        failures.append(f"archive missing {relative}")
    for relative in sorted(actual - expected):
        failures.append(f"archive contains unsealed extra {relative}")

    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        raise SystemExit(1)
    print(f"PASS exact release archive files={len(actual)}")


if __name__ == "__main__":
    main()
