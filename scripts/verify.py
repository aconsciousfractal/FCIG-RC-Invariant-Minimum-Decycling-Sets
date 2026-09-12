#!/usr/bin/env python3
"""Standalone exact finite-assurance replay for the RC-MDS parity package."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CAPSULE = ROOT / "evidence" / "finite_assurance"
PASS_INNER = "PASS_EXACT_PARITY_CONVENTION_MAP_K2_TO_K12"
PASS_OUTER = "PASS_STANDALONE_PACKAGE_VERIFICATION_FINAL"
EXPECTED_PAYLOAD = "3bbec32e9d37706e98db9bb61192d12653a6adb8f419a2f1e816b31cd664d9b5"
EXPECTED_PDF = "dad06bffc30130678a060e46b33c665b9a0ef07567d652da3aa0aafbba97588d"
EXPECTED_INPUTS = {
    "THEOREM_DERIVATION.md": "5f64d0091aa0d1b28273f5faa0496191f6f791ee86e8cac83264129081f0a3e1",
    "VALIDATION_PROTOCOL.md": "19ed51233420723178307e606649c8efe8862b09906804af16e0ff4ab98ecfc0",
}
EXPECTED_ROWS = [
    [2, 3, 0, 0, 0, 0, 0],
    [4, 6, 3, 1, 1, 2, 1],
    [6, 14, 5, 1, 2, 10, 5],
    [8, 36, 6, 2, 2, 52, 26],
    [10, 108, 9, 1, 4, 220, 110],
    [12, 352, 19, 5, 7, 940, 470],
]


def canonical(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def add(checks: list[dict[str, object]], name: str, passed: bool, detail: object) -> None:
    checks.append({"name": name, "passed": bool(passed), "detail": detail})


def execute(script: Path, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script)],
        cwd=cwd,
        text=True,
        capture_output=True,
        timeout=240,
        check=False,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        "--out",
        dest="output",
        type=Path,
        default=None,
        help="optional receipt path; omitted means no repository-tree write",
    )
    args = parser.parse_args()
    started = time.perf_counter()
    checks: list[dict[str, object]] = []
    error: str | None = None
    producer: dict[str, object] = {}
    validation: dict[str, object] = {}

    try:
        input_rows: dict[str, dict[str, object]] = {}
        for name, expected in EXPECTED_INPUTS.items():
            path = CAPSULE / name
            actual = file_hash(path) if path.is_file() else None
            input_rows[name] = {"expected": expected, "actual": actual, "match": actual == expected}
        add(checks, "frozen_input_hashes", all(row["match"] for row in input_rows.values()), input_rows)

        pdf = ROOT / "paper" / "A_Parity_Theorem_for_RC_Invariant_MDS.pdf"
        actual_pdf = file_hash(pdf) if pdf.is_file() else None
        add(checks, "article_pdf", actual_pdf == EXPECTED_PDF, {"expected": EXPECTED_PDF, "actual": actual_pdf})

        with tempfile.TemporaryDirectory(prefix="fcig_rc_mds_verify_") as temporary:
            work = Path(temporary) / "finite_assurance"
            shutil.copytree(CAPSULE, work)
            producer_run = execute(work / "scripts" / "produce.py", work)
            validator_run = execute(work / "scripts" / "validate.py", work)
            add(
                checks,
                "producer_process",
                producer_run.returncode == 0,
                {"returncode": producer_run.returncode},
            )
            add(
                checks,
                "independent_validator_process",
                validator_run.returncode == 0,
                {"returncode": validator_run.returncode},
            )
            producer_path = work / "results" / "finite_assurance_producer.json"
            validation_path = work / "results" / "finite_assurance_validation.json"
            producer = json.loads(producer_path.read_text(encoding="utf-8"))
            validation = json.loads(validation_path.read_text(encoding="utf-8"))

        payload = producer.get("scientific_payload", {})
        declared = producer.get("scientific_payload_sha256")
        recomputed = hashlib.sha256(canonical(payload)).hexdigest()
        add(
            checks,
            "producer_payload_identity",
            producer.get("status") == PASS_INNER
            and declared == EXPECTED_PAYLOAD
            and recomputed == EXPECTED_PAYLOAD,
            {"status": producer.get("status"), "declared": declared, "recomputed": recomputed},
        )

        rows = [
            [
                row.get(key)
                for key in (
                    "k",
                    "pcr_count",
                    "zero_pcr_count",
                    "stable_zero_count",
                    "paired_zero_pair_count",
                    "chi_support_count",
                    "move_count",
                )
            ]
            for row in payload.get("order_rows", [])
        ]
        add(checks, "six_exact_order_rows", rows == EXPECTED_ROWS, {"rows": rows})

        aggregate = payload.get("aggregate", {})
        scientific_mutations = payload.get("mutation_results", [])
        add(
            checks,
            "legal_firing_total",
            aggregate.get("total_f_moves_k4_to_k12") == 612,
            {"actual": aggregate.get("total_f_moves_k4_to_k12"), "expected": 612},
        )
        add(
            checks,
            "scientific_mutations",
            len(scientific_mutations) == 7
            and all(row.get("rejected") is True for row in scientific_mutations),
            {"count": len(scientific_mutations), "rejected": sum(row.get("rejected") is True for row in scientific_mutations)},
        )

        vp = validation.get("validation_payload", {})
        envelope_mutations = vp.get("envelope_mutations", [])
        add(
            checks,
            "independent_exact_match",
            validation.get("status") == PASS_INNER
            and vp.get("producer_payload_hash_valid") is True
            and vp.get("exact_scientific_payload_match") is True
            and vp.get("independent_scientific_payload_sha256") == EXPECTED_PAYLOAD,
            {
                "status": validation.get("status"),
                "producer_hash_valid": vp.get("producer_payload_hash_valid"),
                "exact_match": vp.get("exact_scientific_payload_match"),
                "independent_payload": vp.get("independent_scientific_payload_sha256"),
            },
        )
        add(
            checks,
            "envelope_mutations",
            len(envelope_mutations) == 7
            and all(row.get("rejected") is True for row in envelope_mutations),
            {"count": len(envelope_mutations), "rejected": sum(row.get("rejected") is True for row in envelope_mutations)},
        )

        summary = json.loads((CAPSULE / "CERTIFIED_SUMMARY.json").read_text(encoding="utf-8"))
        add(
            checks,
            "shipped_summary",
            summary.get("order_rows") == EXPECTED_ROWS
            and summary.get("total_legal_f_moves") == 612
            and summary.get("stable_scientific_payload_sha256") == EXPECTED_PAYLOAD,
            {"schema": summary.get("schema")},
        )
    except Exception as exc:  # fail closed and still write a useful envelope
        error = f"{type(exc).__name__}: {exc}"
        add(checks, "execution_completed", False, {"error": error})

    passed = bool(checks) and all(row["passed"] for row in checks)
    result = {
        "schema": "FCIG_RC_MDS_STANDALONE_VERIFICATION_V2",
        "status": PASS_OUTER if passed else "FAIL_STANDALONE_PACKAGE_VERIFICATION",
        "pass": passed,
        "publication_status": "OUT_OF_SCOPE_NOT_ASSERTED",
        "claim_boundary": "BINARY_FINITE_CONVENTION_ASSURANCE_ONLY_QARY_ALL_ORDER_THEOREM_IS_PROOF_ONLY",
        "checks": checks,
        "checks_passed": sum(bool(row["passed"]) for row in checks),
        "checks_total": len(checks),
        "orders": [2, 4, 6, 8, 10, 12],
        "order_rows": EXPECTED_ROWS if passed else [],
        "total_legal_f_moves": 612 if passed else None,
        "scientific_mutations_rejected": 7 if passed else None,
        "envelope_mutations_rejected": 7 if passed else None,
        "stable_scientific_payload_sha256": EXPECTED_PAYLOAD,
        "selected_pdf_sha256": EXPECTED_PDF,
        "runtime_seconds": time.perf_counter() - started,
    }
    if error is not None:
        result["error"] = error
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    print(json.dumps({key: result[key] for key in ("status", "pass", "checks_passed", "checks_total")}, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
