#!/usr/bin/env python3
"""Re-seal and reject fourteen hostile worktree/archive mutations."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parent.parent
Mutation = Callable[[Path], None]
BS = chr(92)


def write_text(root: Path, relative: str, value: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8", newline="\n")


def mutations() -> list[tuple[str, Mutation]]:
    return [
        (
            "yaml_private_path",
            lambda root: write_text(
                root, "rogue.yaml", "source: " + "C:" + BS + "Temp" + BS + "private.txt\n"
            ),
        ),
        (
            "extensionless_private_path",
            lambda root: write_text(root, "ROGUE", "source: /" + "home/reviewer/private.txt\n"),
        ),
        (
            "environment_secret",
            lambda root: write_text(root, ".env", "API_TOKEN=" + "sk-" + "A" * 32 + "\n"),
        ),
        (
            "fine_grained_token",
            lambda root: write_text(root, "rogue.txt", "token=" + "github_" + "pat_" + "A" * 32 + "\n"),
        ),
        (
            "raw_transcript",
            lambda root: write_text(root, "transcript.txt", "SYSTEM" + ": hidden instructions\n"),
        ),
        (
            "unc_path",
            lambda root: write_text(
                root,
                "unc.txt",
                "path=" + BS + BS + "server" + BS + "share" + BS + "private\n",
            ),
        ),
        (
            "windows_temp_path",
            lambda root: write_text(
                root, "temp.txt", "path=" + "C:" + BS + "Temp" + BS + "private\n"
            ),
        ),
        ("tar_archive", lambda root: (root / "rogue.tar").write_bytes(b"archive")),
        ("uppercase_zip", lambda root: (root / "rogue.ZIP").write_bytes(b"archive")),
        (
            "lowercase_external_directory",
            lambda root: write_text(root, "external/raw.txt", "private drop\n"),
        ),
        (
            "large_cache_file",
            lambda root: (
                (root / "__pycache__").mkdir(parents=True, exist_ok=True),
                (root / "__pycache__" / "large.bin").write_bytes(b"x" * (6 * 1024 * 1024)),
            ),
        ),
        (
            "invalid_utf8_text",
            lambda root: (root / "invalid.md").write_bytes(b"valid\n\xff\xfe"),
        ),
        (
            "additional_pdf",
            lambda root: (root / "private.pdf").write_bytes(
                (root / "paper" / "A_Parity_Theorem_for_RC_Invariant_MDS.pdf").read_bytes()
                + b"\nprivate metadata "
                + b"C:"
                + BS.encode("ascii")
                + b"Temp"
                + BS.encode("ascii")
                + b"review\n"
            ),
        ),
        (
            "generated_result_json",
            lambda root: write_text(
                root,
                "results/verification.json",
                '{"generated": true, "not_part_of_release_archive": true}\n',
            ),
        ),
    ]


def run(script: Path, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script)],
        cwd=cwd,
        text=True,
        capture_output=True,
        timeout=60,
        check=False,
    )


def main() -> int:
    rows: list[dict[str, object]] = []
    with tempfile.TemporaryDirectory(prefix="fcig_rc_mds_hygiene_") as temporary:
        scratch = Path(temporary)
        for index, (name, mutate) in enumerate(mutations()):
            work = scratch / f"case_{index:02d}"
            shutil.copytree(ROOT, work, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            mutate(work)
            manifest_build = run(work / "scripts" / "build_manifest.py", work)
            release_build = run(work / "scripts" / "build_release.py", work)
            manifest_check = run(work / "scripts" / "check_manifest.py", work)
            worktree_check = run(work / "scripts" / "check_worktree.py", work)
            archive_check = run(work / "scripts" / "check_release_archive.py", work)
            sealed = (
                manifest_build.returncode == 0
                and release_build.returncode == 0
                and manifest_check.returncode == 0
            )
            if name == "generated_result_json":
                rejected = sealed and worktree_check.returncode == 0 and archive_check.returncode != 0
            else:
                rejected = sealed and worktree_check.returncode != 0 and archive_check.returncode != 0
            rows.append(
                {
                    "name": name,
                    "rejected": rejected,
                    "manifest_exit": manifest_check.returncode,
                    "worktree_exit": worktree_check.returncode,
                    "archive_exit": archive_check.returncode,
                }
            )

    passed = len(rows) == 14 and all(bool(row["rejected"]) for row in rows)
    result = {
        "status": "PASS_RELEASE_HYGIENE_MUTATIONS_14_OF_14" if passed else "FAIL_RELEASE_HYGIENE_MUTATIONS",
        "pass": passed,
        "mutations_rejected": sum(bool(row["rejected"]) for row in rows),
        "mutations_total": len(rows),
        "rows": rows,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
