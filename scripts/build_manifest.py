#!/usr/bin/env python3
"""Build the deterministic source/evidence SHA-256 manifest."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "MANIFEST_SHA256.txt"
RELEASE = ROOT / "RELEASE_SHA256.txt"
BUILD_SUFFIXES = {
    ".aux", ".bbl", ".blg", ".log", ".out", ".toc", ".fls",
    ".fdb_latexmk", ".synctex.gz",
}


def included(path: Path) -> bool:
    relative = path.relative_to(ROOT)
    if not path.is_file() or path in {OUTPUT, RELEASE}:
        return False
    if ".git" in relative.parts or "__pycache__" in relative.parts:
        return False
    if any(part.lower() == "results" for part in relative.parts) and relative.suffix.lower() == ".json":
        return False
    if relative.suffix == ".pdf" or any(relative.name.endswith(suffix) for suffix in BUILD_SUFFIXES):
        return False
    return True


def main() -> None:
    files = sorted(
        (path for path in ROOT.rglob("*") if included(path)),
        key=lambda path: path.relative_to(ROOT).as_posix(),
    )
    lines = [
        "# SHA-256 manifest for FCIG-RC-Invariant-Minimum-Decycling-Sets",
        "# PDF, release checksums, JSON below any results directory and LaTeX build products are excluded.",
    ]
    for path in files:
        digest = hashlib.sha256(path.read_bytes()).hexdigest().upper()
        lines.append(f"{digest}  {path.relative_to(ROOT).as_posix()}")
    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {OUTPUT.name} with {len(files)} entries")


if __name__ == "__main__":
    main()
