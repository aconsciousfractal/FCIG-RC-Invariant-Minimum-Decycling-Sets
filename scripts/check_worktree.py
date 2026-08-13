#!/usr/bin/env python3
"""Verify checksum pins and fail closed on unsafe worktree material.

Generated JSON receipts below a results directory are permitted here because
they are useful during local verification.  The archive checker imposes exact
file membership and rejects them from a distributable package.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parent.parent
CHECKSUMS = ROOT / "RELEASE_SHA256.txt"
SELECTED_PDF = "paper/A_Parity_Theorem_for_RC_Invariant_MDS.pdf"
REQUIRED_RELEASE = {
    "MANIFEST_SHA256.txt",
    SELECTED_PDF,
}
REQUIRED_FILES = {
    ".gitattributes", ".gitignore", "CITATION.cff", "LICENSE",
    "LICENSE_SCOPE.md", "README.md", "INDEPENDENT_VERIFICATION.md", "REPRODUCE.md",
    "MANIFEST_SHA256.txt", "RELEASE_SHA256.txt", "requirements.txt",
    "scripts/verify.py", "scripts/check_git_history.py", "scripts/build_manifest.py", "scripts/check_manifest.py",
    "scripts/build_release.py", "scripts/check_worktree.py",
    "scripts/check_release_archive.py", "scripts/build_paper.ps1",
    "scripts/test_release_hygiene_mutations.py",
    "docs/PUBLIC_CLAIM_BOUNDARY.md", "docs/SOURCE_LOCK.md",
    "docs/RESEARCH_HISTORY.md", "docs/AUTHORSHIP.md",
    "evidence/finite_assurance/THEOREM_DERIVATION.md",
    "evidence/finite_assurance/VALIDATION_PROTOCOL.md",
    "evidence/finite_assurance/CERTIFIED_SUMMARY.json",
    "evidence/finite_assurance/README.md",
    "evidence/finite_assurance/scripts/produce.py",
    "evidence/finite_assurance/scripts/validate.py",
    "evidence/theorem/README.md", "results/README.md",
    "paper/main.tex", "paper/abstract.tex", "paper/macros.tex", "paper/refs.bib",
    "paper/sections/01_introduction.tex",
    "paper/sections/02_normalization_and_prior_work.tex",
    "paper/sections/03_odd_order_obstruction.tex",
    "paper/sections/04_mykkeltveit_seed_and_zero_ties.tex",
    "paper/sections/05_half_plane_coboundary.tex",
    "paper/sections/06_legal_descent_and_even_existence.tex",
    "paper/sections/07_binary_parity_theorem.tex",
    "paper/sections/08_exact_validation_and_reproducibility.tex",
    "paper/sections/09_boundaries_and_outlook.tex",
    "paper/appendices/A_convention_dictionary.tex",
    "paper/appendices/B_technical_lemmas.tex",
    "paper/appendices/C_finite_validation_tables.tex",
    SELECTED_PDF,
}
FORBIDDEN_ENDINGS = {
    ".aux", ".bbl", ".blg", ".log", ".out", ".toc", ".pyc", ".pyo",
    ".fls", ".fdb_latexmk", ".synctex.gz", ".zip", ".7z", ".tar",
    ".tar.gz", ".tgz", ".rar",
}
TEXT_SUFFIXES = {
    ".md", ".txt", ".tex", ".bib", ".py", ".ps1", ".cff", ".json",
    ".yaml", ".yml", ".toml", ".ini", ".cfg", ".env",
}
TEXT_NAMES = {".gitignore", ".gitattributes", "LICENSE"}
PRIVATE_PATTERNS = {
    "windows_absolute_path": re.compile(r"(?i)\b[A-Z]:[\\/][A-Za-z0-9_. -]"),
    "windows_unc_path": re.compile(r"\\\\[A-Za-z0-9._$-]+[\\/][A-Za-z0-9._$-]+"),
    "unix_private_path": re.compile(r"/(?:Users|home)/[^/\s]+/"),
    "codex_private": re.compile(
        r"(?i)\." + "codex" + r"|<" + "heartbeat" + r">|automation_" + "id"
        + r"|agent_" + "name" + r"|sub" + "agent"
    ),
    "parent_project_path": re.compile(
        "FRAME" + "WORK/04-SOFT" + "WARE|paper_" + "projects/"
    ),
    "private_key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "github_token": re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    "github_fine_token": re.compile("github_" + "pat_" + r"[A-Za-z0-9_]{20,}"),
    "openai_like_token": re.compile(r"sk-[A-Za-z0-9]{20,}"),
    "aws_key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "raw_transcript_role": re.compile(r"(?m)^\s*(?:SYSTEM|USER|ASSISTANT)\s*:"),
}


def main() -> None:
    failures: list[str] = []
    seen: set[str] = set()
    for number, raw in enumerate(CHECKSUMS.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        try:
            expected, relative = line.split(None, 1)
        except ValueError:
            failures.append(f"release line {number}: malformed")
            continue
        posix = PurePosixPath(relative)
        if posix.is_absolute() or ".." in posix.parts or relative in seen:
            failures.append(f"release line {number}: unsafe or duplicate {relative}")
            continue
        seen.add(relative)
        path = ROOT.joinpath(*posix.parts)
        if not path.is_file():
            failures.append(f"missing release object {relative}")
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest().upper()
        if actual != expected.upper():
            failures.append(f"release mismatch {relative}")
    if seen != REQUIRED_RELEASE:
        failures.append(f"release paths differ: expected={sorted(REQUIRED_RELEASE)} actual={sorted(seen)}")

    all_files: set[str] = set()
    largest = 0
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        rel = relative.as_posix()
        lower_parts = tuple(part.lower() for part in relative.parts)
        if lower_parts[:1] == (".git",):
            continue
        if path.is_symlink():
            failures.append(f"symlink forbidden {rel}")
            continue
        if "external" in lower_parts:
            failures.append(f"raw external directory included {rel}")
        if "__pycache__" in lower_parts:
            failures.append(f"cache directory forbidden {rel}")
        if path.is_dir():
            continue
        if not path.is_file():
            continue
        all_files.add(rel)
        size = path.stat().st_size
        largest = max(largest, size)
        if size > 5 * 1024 * 1024:
            failures.append(f"file exceeds 5 MiB {rel}: {size}")
        lower_name = relative.name.lower()
        if any(lower_name.endswith(suffix) for suffix in FORBIDDEN_ENDINGS):
            failures.append(f"forbidden generated/archive file {rel}")
        if lower_name == ".env" or lower_name.startswith(".env."):
            failures.append(f"environment file forbidden {rel}")
        data = path.read_bytes()
        first = data[:160]
        if first.startswith(b"version https://git-lfs.github.com/spec/v1"):
            failures.append(f"Git LFS pointer forbidden {rel}")
        suffix = relative.suffix.lower()
        if suffix == ".pdf":
            if rel != SELECTED_PDF:
                failures.append(f"additional PDF forbidden {rel}")
            text = "\n".join(
                chunk.decode("ascii")
                for chunk in re.findall(rb"[\x20-\x7e]{4,}", data)
            )
        elif suffix in TEXT_SUFFIXES or relative.name in TEXT_NAMES or not suffix:
            try:
                text = data.decode("utf-8", errors="strict")
            except UnicodeDecodeError as exc:
                failures.append(f"invalid UTF-8 text {rel}: byte {exc.start}")
                continue
        else:
            failures.append(f"unsupported binary/file type {rel}")
            continue
        for name, pattern in PRIVATE_PATTERNS.items():
            if pattern.search(text):
                failures.append(f"{name} in {rel}")
    for required in sorted(REQUIRED_FILES - all_files):
        failures.append(f"required file missing {required}")
    if "ALL RIGHTS RESERVED" not in (ROOT / "LICENSE").read_text(encoding="utf-8"):
        failures.append("all-rights-reserved licence notice missing")
    readme = (ROOT / "README.md").read_text(encoding="utf-8").lower()
    if "final standalone article" not in readme or "reproducibility package" not in readme:
        failures.append("final-package identity missing from README")
    if "oleksiy babanskyy" not in readme:
        failures.append("author identity missing from README")

    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        raise SystemExit(1)
    print(f"PASS worktree checksum pins 2/2; hygiene files={len(all_files)} largest_bytes={largest}")


if __name__ == "__main__":
    main()
