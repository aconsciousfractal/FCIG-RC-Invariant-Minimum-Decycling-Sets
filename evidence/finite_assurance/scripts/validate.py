#!/usr/bin/env python3
"""Independent exact validator for the standalone parity package.

This module does not import the producer.  Its cyclotomic coordinates are
literal exact tables, and its residual-DAG test uses DFS rather than the
producer's Kahn traversal.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import platform
import sys
import time
from pathlib import Path
from typing import Iterable


SCHEMA = "FCIG_RC_MDS_FINITE_ASSURANCE_VALIDATION_V1"
PRODUCER_SCHEMA = "FCIG_RC_MDS_FINITE_ASSURANCE_PRODUCER_V1"
ASSURANCE_SCOPE = "FINITE_ASSURANCE_K2_TO_K12"
PASS = "PASS_EXACT_PARITY_CONVENTION_MAP_K2_TO_K12"
FAIL = "FAIL_LITERAL_PARITY_CONVENTION_OR_PATH"
INCONCLUSIVE = "INCONCLUSIVE_INPUT_ARITHMETIC_OR_RECONSTRUCTION_GAP"
ORDERS = (2, 4, 6, 8, 10, 12)

PACKAGE = Path(__file__).resolve().parents[1]
INPUT = PACKAGE / "results" / "finite_assurance_producer.json"
OUTPUT = PACKAGE / "results" / "finite_assurance_validation.json"
DERIVATION = PACKAGE / "THEOREM_DERIVATION.md"
PROTOCOL = PACKAGE / "VALIDATION_PROTOCOL.md"
FROZEN_INPUTS = {
    "theorem_derivation": (DERIVATION, "5f64d0091aa0d1b28273f5faa0496191f6f791ee86e8cac83264129081f0a3e1"),
    "validation_protocol": (PROTOCOL, "19ed51233420723178307e606649c8efe8862b09906804af16e0ff4ab98ecfc0"),
}


Pair = tuple[int, int]

SINE: dict[int, tuple[Pair, ...]] = {
    4: ((0, 0), (1, 0), (0, 0), (-1, 0), (0, 0)),
    6: ((0, 0), (1, 0), (1, 0), (0, 0), (-1, 0), (-1, 0), (0, 0)),
    8: ((0, 0), (1, 0), (0, 1), (1, 0), (0, 0), (-1, 0), (0, -1), (-1, 0), (0, 0)),
    10: ((0, 0), (1, 0), (0, 1), (0, 1), (1, 0), (0, 0), (-1, 0), (0, -1), (0, -1), (-1, 0), (0, 0)),
    12: ((0, 0), (1, 0), (0, 1), (2, 0), (0, 1), (1, 0), (0, 0), (-1, 0), (0, -1), (-2, 0), (0, -1), (-1, 0), (0, 0)),
}

COSINE: dict[int, tuple[Pair, ...]] = {
    4: ((2, 0), (0, 0), (-2, 0), (0, 0), (2, 0)),
    6: ((2, 0), (1, 0), (-1, 0), (-2, 0), (-1, 0), (1, 0), (2, 0)),
    8: ((2, 0), (0, 1), (0, 0), (0, -1), (-2, 0), (0, -1), (0, 0), (0, 1), (2, 0)),
    10: ((2, 0), (0, 1), (-1, 1), (1, -1), (0, -1), (-2, 0), (0, -1), (1, -1), (-1, 1), (0, 1), (2, 0)),
    12: ((2, 0), (0, 1), (1, 0), (0, 0), (-1, 0), (0, -1), (-2, 0), (0, -1), (-1, 0), (0, 0), (1, 0), (0, 1), (2, 0)),
}


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_hash(path: Path) -> str:
    return sha(path.read_bytes())


def audit_inputs() -> dict[str, str]:
    found: dict[str, str] = {}
    for name, (path, expected) in FROZEN_INPUTS.items():
        actual = file_hash(path)
        if actual != expected:
            raise AssertionError(("input_hash", name, actual, expected))
        found[name] = actual
    return found


def exact_sign(value: Pair, k: int) -> int:
    a, b = value
    if k in (4, 6):
        if b:
            raise AssertionError(("rational_basis", k, value))
        return (a > 0) - (a < 0)
    if k == 10:
        a, b, d = 2 * a + b, b, 5
    else:
        d = 2 if k == 8 else 3
    if a == b == 0:
        return 0
    if b == 0:
        return 1 if a > 0 else -1
    if a == 0:
        return 1 if b > 0 else -1
    if (a > 0) == (b > 0):
        return 1 if a > 0 else -1
    delta = abs(a) * abs(a) - d * abs(b) * abs(b)
    if delta == 0:
        raise AssertionError(("irrational_cancellation", k, value))
    leading = a if delta > 0 else b
    return 1 if leading > 0 else -1


def digits(value: int, width: int) -> tuple[int, ...]:
    text = f"{value:0{width}b}"
    return tuple(int(char) for char in text)


def dot(value: int, width: int, table: tuple[Pair, ...]) -> Pair:
    a = b = 0
    for position, digit in enumerate(digits(value, width), start=1):
        if digit:
            a += table[position][0]
            b += table[position][1]
    return a, b


def rotate_left(value: int, width: int) -> int:
    text = f"{value:0{width}b}"
    return int(text[1:] + text[0], 2)


def rotate_right(value: int, width: int) -> int:
    text = f"{value:0{width}b}"
    return int(text[-1] + text[:-1], 2)


def reverse_complement(value: int, width: int) -> int:
    text = f"{value:0{width}b}"
    return int("".join("1" if char == "0" else "0" for char in reversed(text)), 2)


def cycles(width: int) -> tuple[tuple[int, ...], ...]:
    unique = {
        tuple(sorted({
            int((f"{value:0{width}b}"[shift:] + f"{value:0{width}b}"[:shift]), 2)
            for shift in range(width)
        }))
        for value in range(1 << width)
    }
    return tuple(sorted(unique, key=lambda row: row[0]))


def binary(value: int, width: int) -> str:
    return f"{value:0{width}b}"


def binary_list(values: Iterable[int], width: int) -> list[str]:
    return [binary(value, width) for value in sorted(values)]


def collection_hash(values: Iterable[int], width: int) -> str:
    payload = "".join(binary(value, width) + "\n" for value in sorted(values))
    return sha(payload.encode("ascii"))


def independent_selector(
    k: int,
    *,
    rotation: str = "left",
    axis: str = "negative",
    broken_zero_pairing: bool = False,
) -> tuple[set[int] | None, dict[str, object], str | None]:
    rows = cycles(k)
    sine, cosine = SINE[k], COSINE[k]
    chosen: set[int] = set()
    zero: list[int] = []
    for index, row in enumerate(rows):
        z = row[0]
        if dot(z, k, sine) == (0, 0) and dot(z, k, cosine) == (0, 0):
            zero.append(index)
            continue
        candidates: list[int] = []
        for value in row:
            neighbor = rotate_left(value, k) if rotation == "left" else rotate_right(value, k)
            first = exact_sign(dot(value, k, sine), k)
            second = exact_sign(dot(neighbor, k, sine), k)
            axis_hit = first == 0 and (second > 0 if axis == "negative" else second < 0)
            if axis_hit or first < 0 < second:
                candidates.append(value)
        if len(candidates) != 1:
            return None, {"selector_error_cycle": index, "candidate_count": len(candidates)}, "selector_unique"
        chosen.add(candidates[0])

    lookup = {row: index for index, row in enumerate(rows)}
    consumed: set[int] = set()
    stable: list[dict[str, object]] = []
    paired: list[dict[str, object]] = []
    altered = False
    for index in zero:
        if index in consumed:
            continue
        row = rows[index]
        mate_row = tuple(sorted(reverse_complement(value, k) for value in row))
        mate = lookup[mate_row]
        if mate == index:
            fixed = sorted(value for value in row if reverse_complement(value, k) == value)
            if len(fixed) != 2:
                return None, {"stable_zero_cycle": index, "fixed_count": len(fixed)}, "stable_zero_two_fixed_words"
            chosen.add(fixed[0])
            stable.append({"pcr_index": index, "fixed_words": binary_list(fixed, k), "selected": binary(fixed[0], k)})
            consumed.add(index)
        else:
            low, high = sorted((index, mate))
            if index != low:
                continue
            source = rows[low][0]
            mate_word = reverse_complement(source, k)
            if broken_zero_pairing and not altered and len(rows[high]) > 1:
                mate_word = rotate_left(mate_word, k)
                altered = True
            chosen.update((source, mate_word))
            paired.append({"pcr_indices": [low, high], "source_word": binary(source, k), "mate_word": binary(mate_word, k)})
            consumed.update((low, high))
    if broken_zero_pairing and not altered:
        return None, {"broken_zero_pairing_applied": False}, "mutation_not_applicable"
    return chosen, {"zero_pcr_indices": zero, "stable_zero_rows": stable, "paired_zero_rows": paired}, None


def transversal(chosen: set[int], k: int) -> bool:
    for row in cycles(k):
        count = sum(value in chosen for value in row)
        if count != 1:
            return False
    return True


def dag_by_dfs(chosen: set[int], k: int) -> bool:
    n = 1 << (k - 1)
    tail_mask = n - 1
    adjacency: list[list[int]] = [[] for _ in range(n)]
    for edge in range(1 << k):
        if edge not in chosen:
            adjacency[edge >> 1].append(edge & tail_mask)
    color = [0] * n

    def visit(start: int) -> bool:
        color[start] = 1
        for target in adjacency[start]:
            if color[target] == 1:
                return False
            if color[target] == 0 and not visit(target):
                return False
        color[start] = 2
        return True

    return all(color[node] != 0 or visit(node) for node in range(n))


def rc_set(chosen: set[int], k: int) -> set[int]:
    return {reverse_complement(value, k) for value in chosen}


def half_plane(k: int, *, closed: bool = False) -> set[int]:
    answer: set[int] = set()
    for lower in range(1 << (k - 1)):
        sign = exact_sign(dot(lower, k - 1, SINE[k]), k)
        if sign > 0 or (closed and sign == 0):
            answer.add(lower)
    return answer


def support_is_rc(support: set[int], k: int) -> bool:
    return {reverse_complement(value, k - 1) for value in support} == support


def bridge(chosen: set[int], support: set[int], k: int, *, reverse_sign: bool = False) -> bool:
    image = rc_set(chosen, k)
    mask = (1 << (k - 1)) - 1
    for edge in range(1 << k):
        defect = int(edge in image) - int(edge in chosen)
        gradient = int((edge >> 1) in support) - int((edge & mask) in support)
        if reverse_sign:
            gradient = -gradient
        if defect != gradient:
            return False
    return True


def first_failure(
    chosen: set[int] | None,
    support: set[int],
    k: int,
    error: str | None = None,
    *,
    reverse_sign: bool = False,
) -> str | None:
    if error or chosen is None:
        return error or "selector_unique"
    if not transversal(chosen, k):
        return "one_selected_per_pcr"
    if not dag_by_dfs(chosen, k):
        return "residual_dag"
    if any(reverse_complement(u, k - 1) == u for u in range(1 << (k - 1))):
        return "lower_rc_fixed_point_free"
    if not support_is_rc(support, k):
        return "potential_rc_invariant"
    if not bridge(chosen, support, k, reverse_sign=reverse_sign):
        return "rc_defect_gradient"
    return None


def incoming_edges(lower: int, k: int) -> set[int]:
    return {lower, lower | (1 << (k - 1))}


def outgoing_edges(lower: int) -> set[int]:
    return {2 * lower, 2 * lower + 1}


def is_enabled(chosen: set[int], lower: int, k: int) -> bool:
    return incoming_edges(lower, k) <= chosen


def fire(chosen: set[int], lower: int, k: int) -> set[int]:
    if not is_enabled(chosen, lower, k):
        raise AssertionError(("disabled_fire", k, lower))
    answer = set(chosen)
    answer.difference_update(incoming_edges(lower, k))
    answer.update(outgoing_edges(lower))
    return answer


def replay_path(chosen: set[int], support: set[int], k: int) -> tuple[set[int], list[dict[str, object]]]:
    state, q = set(chosen), set(support)
    trace: list[dict[str, object]] = []
    while q:
        candidates = [u for u in sorted(q) if is_enabled(state, u, k)]
        if not candidates:
            raise AssertionError(("no_enabled_positive", k, len(trace)))
        u = candidates[0]
        mate = reverse_complement(u, k - 1)
        if mate == u or mate not in q:
            raise AssertionError(("unpaired_support", k, u, mate))
        state = fire(state, u, k)
        q.difference_update((u, mate))
        if not transversal(state, k):
            raise AssertionError(("path_transversal", k, len(trace)))
        if not dag_by_dfs(state, k):
            raise AssertionError(("path_dag", k, len(trace)))
        if not support_is_rc(q, k):
            raise AssertionError(("path_support_rc", k, len(trace)))
        if not bridge(state, q, k):
            raise AssertionError(("path_bridge", k, len(trace)))
        trace.append(
            {
                "step": len(trace) + 1,
                "fired_lower_word": binary(u, k - 1),
                "paired_lower_word": binary(mate, k - 1),
                "selected_sha256": collection_hash(state, k),
                "remaining_support_sha256": collection_hash(q, k - 1),
            }
        )
    if state != rc_set(state, k):
        raise AssertionError(("terminal_rc", k))
    return state, trace


def reconstruct_row(k: int) -> dict[str, object]:
    if k == 2:
        chosen = {0, 1, 3}
        if not transversal(chosen, 2) or not dag_by_dfs(chosen, 2) or chosen != rc_set(chosen, 2):
            raise AssertionError("k2 explicit control")
        return {
            "k": 2,
            "arithmetic": "explicit_k2",
            "pcr_count": len(cycles(2)),
            "selected_count": len(chosen),
            "initial_selected_words": binary_list(chosen, 2),
            "initial_selected_sha256": collection_hash(chosen, 2),
            "zero_pcr_count": 0,
            "stable_zero_count": 0,
            "paired_zero_pair_count": 0,
            "zero_ties": {"stable": [], "paired": []},
            "chi_support_count": 0,
            "chi_support_sha256": collection_hash((), 1),
            "move_count": 0,
            "path": [],
            "terminal_selected_words": binary_list(chosen, 2),
            "terminal_selected_sha256": collection_hash(chosen, 2),
            "one_per_pcr": True,
            "initial_residual_dag": True,
            "coboundary_identity": "not_used_explicit_k2",
            "terminal_rc_fixed": True,
            "terminal_residual_dag": True,
        }
    chosen, meta, error = independent_selector(k)
    support = half_plane(k)
    failed = first_failure(chosen, support, k, error)
    if failed or chosen is None:
        raise AssertionError(("baseline", k, failed))
    terminal, trace = replay_path(chosen, support, k)
    if 2 * len(trace) != len(support):
        raise AssertionError(("path_length", k))
    return {
        "k": k,
        "arithmetic": {
            "basis": "a+b*alpha",
            "alpha_relation": {4: "alpha=0", 6: "alpha=1", 8: "alpha^2=2", 10: "alpha^2=alpha+1", 12: "alpha^2=3"}[k],
            "sine_weights": [list(value) for value in SINE[k][1:]],
            "doubled_cosine_weights": [list(value) for value in COSINE[k][1:]],
        },
        "pcr_count": len(cycles(k)),
        "selected_count": len(chosen),
        "initial_selected_words": binary_list(chosen, k),
        "initial_selected_sha256": collection_hash(chosen, k),
        "zero_pcr_count": len(meta["zero_pcr_indices"]),
        "stable_zero_count": len(meta["stable_zero_rows"]),
        "paired_zero_pair_count": len(meta["paired_zero_rows"]),
        "zero_ties": {"stable": meta["stable_zero_rows"], "paired": meta["paired_zero_rows"]},
        "chi_support_count": len(support),
        "chi_support_sha256": collection_hash(support, k - 1),
        "move_count": len(trace),
        "path": trace,
        "terminal_selected_words": binary_list(terminal, k),
        "terminal_selected_sha256": collection_hash(terminal, k),
        "one_per_pcr": True,
        "initial_residual_dag": True,
        "coboundary_identity": True,
        "terminal_rc_fixed": terminal == rc_set(terminal, k),
        "terminal_residual_dag": dag_by_dfs(terminal, k),
    }


def mutation(name: str) -> dict[str, object]:
    for k in ORDERS[1:]:
        chosen, _, error = independent_selector(k)
        support = half_plane(k)
        reason: str | None = None
        applicable = True
        if name == "RIGHT_ROTATION_SELECTOR":
            chosen, _, error = independent_selector(k, rotation="right")
            reason = first_failure(chosen, support, k, error)
        elif name == "REVERSED_GRADIENT_SIGN":
            reason = first_failure(chosen, support, k, error, reverse_sign=True)
        elif name == "CLOSED_HALF_PLANE":
            reason = first_failure(chosen, half_plane(k, closed=True), k, error)
        elif name == "POSITIVE_AXIS_CONVENTION":
            chosen, _, error = independent_selector(k, axis="positive")
            reason = first_failure(chosen, support, k, error)
        elif name == "BROKEN_ZERO_PAIRING":
            chosen, _, error = independent_selector(k, broken_zero_pairing=True)
            if error == "mutation_not_applicable":
                applicable = False
            else:
                reason = first_failure(chosen, support, k, error)
        elif name == "UNPAIRED_DEFECT_UPDATE":
            if chosen is None:
                reason = error
            else:
                candidates = [u for u in sorted(support) if is_enabled(chosen, u, k)]
                if not candidates:
                    reason = "no_enabled_positive_f_move"
                else:
                    u = candidates[0]
                    state = fire(chosen, u, k)
                    q = set(support)
                    q.remove(u)
                    reason = "remaining_potential_rc_invariant" if not support_is_rc(q, k) else (
                        "rc_defect_gradient" if not bridge(state, q, k) else None
                    )
        elif name == "REVERSED_F_MOVE":
            if chosen is None:
                reason = error
            else:
                candidates = [u for u in sorted(support) if is_enabled(chosen, u, k)]
                if not candidates:
                    reason = "no_enabled_positive_f_move"
                else:
                    u = candidates[0]
                    if not outgoing_edges(u) <= chosen:
                        reason = "inverse_move_not_enabled"
                    else:
                        inverse = (chosen - outgoing_edges(u)) | incoming_edges(u, k)
                        reason = first_failure(inverse, support, k)
        else:
            raise ValueError(name)
        if not applicable:
            continue
        if reason:
            return {"name": name, "rejected": True, "first_k": k, "failed_predicate": reason}
    return {"name": name, "rejected": False, "first_k": None, "failed_predicate": None}


def independent_payload() -> dict[str, object]:
    rows = [reconstruct_row(k) for k in ORDERS]
    mutations = [
        mutation(name)
        for name in (
            "RIGHT_ROTATION_SELECTOR",
            "REVERSED_GRADIENT_SIGN",
            "CLOSED_HALF_PLANE",
            "POSITIVE_AXIS_CONVENTION",
            "BROKEN_ZERO_PAIRING",
            "UNPAIRED_DEFECT_UPDATE",
            "REVERSED_F_MOVE",
        )
    ]
    passed = all(row["terminal_rc_fixed"] and row["terminal_residual_dag"] for row in rows)
    passed = passed and all(row["rejected"] for row in mutations)
    return {
        "governed_orders": list(ORDERS),
        "order_rows": rows,
        "aggregate": {
            "total_zero_pcrs_k4_to_k12": sum(int(row["zero_pcr_count"]) for row in rows[1:]),
            "total_chi_support_k4_to_k12": sum(int(row["chi_support_count"]) for row in rows[1:]),
            "total_f_moves_k4_to_k12": sum(int(row["move_count"]) for row in rows[1:]),
            "scientific_mutations_rejected": sum(int(row["rejected"]) for row in mutations),
        },
        "mutation_results": mutations,
        "outcome": PASS if passed else FAIL,
        "claim_boundary": {
            "finite_assurance_only": True,
            "all_order_proof_source": "paper and standalone theorem derivation, not this replay",
            "external_outputs_used": False,
            "release_or_novelty_promotion": False,
            "orders_exhaustive": False,
        },
    }


def assess_producer_envelope(
    producer: dict[str, object], expected: dict[str, object]
) -> dict[str, bool]:
    """Run the real hash, schema, status and exact-payload decision path."""
    schema_valid = producer.get("schema_version") == PRODUCER_SCHEMA
    assurance_valid = producer.get("assurance_scope") == ASSURANCE_SCOPE
    actual = producer.get("scientific_payload")
    payload_present = isinstance(actual, dict)
    hash_valid = bool(
        payload_present
        and producer.get("scientific_payload_sha256") == sha(canonical(actual))
    )
    exact_match = bool(payload_present and actual == expected)
    status_valid = producer.get("status") == PASS
    expected_outcome_valid = expected.get("outcome") == PASS
    passed = all(
        (
            schema_valid,
            assurance_valid,
            payload_present,
            hash_valid,
            exact_match,
            status_valid,
            expected_outcome_valid,
        )
    )
    return {
        "schema_valid": schema_valid,
        "assurance_valid": assurance_valid,
        "payload_present": payload_present,
        "hash_valid": hash_valid,
        "exact_match": exact_match,
        "status_valid": status_valid,
        "expected_outcome_valid": expected_outcome_valid,
        "passed": passed,
    }


def envelope_mutations(
    producer: dict[str, object], expected: dict[str, object]
) -> list[dict[str, object]]:
    """Apply, rehash, serialize and adjudicate seven hostile receipts."""
    trials: list[tuple[str, dict[str, object]]] = []

    def trial(name: str) -> dict[str, object]:
        candidate = copy.deepcopy(producer)
        trials.append((name, candidate))
        payload = candidate.get("scientific_payload")
        if not isinstance(payload, dict):
            raise AssertionError("mutation base lacks scientific payload")
        return payload

    trial("ORDER_COUNT")["order_rows"][1]["pcr_count"] += 1  # type: ignore[index,operator]
    trial("SELECTED_WORD")["order_rows"][1]["initial_selected_words"][0] = "1111"  # type: ignore[index]
    trial("ZERO_TIE")["order_rows"][1]["zero_ties"]["stable"][0]["selected"] = "0000"  # type: ignore[index]
    trial("PATH_STEP")["order_rows"][1]["path"][0]["fired_lower_word"] = "111"  # type: ignore[index]
    trial("SCIENTIFIC_MUTATION_VERDICT")["mutation_results"][0]["rejected"] = False  # type: ignore[index]
    trial("OUTCOME")["outcome"] = FAIL
    trial("CLAIM_BOUNDARY")["claim_boundary"]["release_or_novelty_promotion"] = True  # type: ignore[index]

    results: list[dict[str, object]] = []
    for name, candidate in trials:
        payload = candidate["scientific_payload"]
        candidate["scientific_payload_sha256"] = sha(canonical(payload))
        reparsed = json.loads(json.dumps(candidate, sort_keys=True))
        assessment = assess_producer_envelope(reparsed, expected)
        results.append(
            {
                "name": name,
                "payload_hash_recomputed": assessment["hash_valid"],
                "rejected": not assessment["passed"],
                "exact_match": assessment["exact_match"],
            }
        )
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=INPUT)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    started = time.perf_counter()
    try:
        inputs = audit_inputs()
        producer = json.loads(args.input.read_text(encoding="utf-8"))
        actual = producer.get("scientific_payload")
        if not isinstance(actual, dict):
            raise AssertionError("missing producer scientific payload")
        expected = independent_payload()
        expected_hash = sha(canonical(expected))
        assessment = assess_producer_envelope(producer, expected)
        mutations = envelope_mutations(producer, expected)
        passed = assessment["passed"] and all(row["rejected"] for row in mutations)
        validation_payload = {
            "producer_receipt_sha256": file_hash(args.input),
            "producer_payload_hash_valid": assessment["hash_valid"],
            "producer_scientific_payload_sha256": producer.get("scientific_payload_sha256"),
            "independent_scientific_payload_sha256": expected_hash,
            "exact_scientific_payload_match": assessment["exact_match"],
            "independent_order_count": len(expected["order_rows"]),
            "independent_total_f_moves": expected["aggregate"]["total_f_moves_k4_to_k12"],
            "independent_scientific_mutations_rejected": expected["aggregate"]["scientific_mutations_rejected"],
            "envelope_mutations": mutations,
            "outcome": PASS if passed else FAIL,
            "claim_boundary": expected["claim_boundary"],
        }
        receipt = {
            "schema_version": SCHEMA,
            "assurance_scope": ASSURANCE_SCOPE,
            "status": validation_payload["outcome"],
            "validator": Path(__file__).name,
            "inputs": inputs,
            "validation_payload": validation_payload,
            "validation_payload_sha256": sha(canonical(validation_payload)),
            "runtime": {
                "elapsed_seconds": time.perf_counter() - started,
                "python": sys.version.split()[0],
                "platform": platform.platform(),
            },
        }
        code = 0 if passed else 1
    except Exception as exc:
        receipt = {
            "schema_version": SCHEMA,
            "assurance_scope": ASSURANCE_SCOPE,
            "status": INCONCLUSIVE,
            "validator": Path(__file__).name,
            "error": f"{type(exc).__name__}: {exc}",
            "runtime": {"elapsed_seconds": time.perf_counter() - started, "python": sys.version.split()[0]},
        }
        code = 2
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": receipt["status"], "output": str(args.output)}, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
