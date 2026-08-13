#!/usr/bin/env python3
"""Build the separate manifest/PDF release checksum layer."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "MANIFEST_SHA256.txt"
PDF = ROOT / "paper" / "A_Parity_Theorem_for_RC_Invariant_MDS.pdf"
OUTPUT = ROOT / "RELEASE_SHA256.txt"


def main() -> None:
    rows = []
    for path in (MANIFEST, PDF):
        digest = hashlib.sha256(path.read_bytes()).hexdigest().upper()
        rows.append(f"{digest}  {path.relative_to(ROOT).as_posix()}")
    OUTPUT.write_text("\n".join(rows) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {OUTPUT.name} with 2 entries")


if __name__ == "__main__":
    main()
