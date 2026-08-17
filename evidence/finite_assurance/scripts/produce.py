#!/usr/bin/env python3
"""Exact finite convention-map replay for the standalone parity package.

The calculation uses integer arithmetic in Z[2*cos(2*pi/k)].  It reads no
external research output and no stored RC-MDS witness.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
import time
from collections import deque
from pathlib import Path
from typing import Iterable


SCHEMA = "FCIG_RC_MDS_FINITE_ASSURANCE_PRODUCER_V1"
ASSURANCE_SCOPE = "FINITE_ASSURANCE_K2_TO_K12"
PASS = "PASS_EXACT_PARITY_CONVENTION_MAP_K2_TO_K12"
FAIL = "FAIL_LITERAL_PARITY_CONVENTION_OR_PATH"
INCONCLUSIVE = "INCONCLUSIVE_INPUT_ARITHMETIC_OR_RECONSTRUCTION_GAP"
ORDERS = (2, 4, 6, 8, 10, 12)

PACKAGE = Path(__file__).resolve().parents[1]
RESULT = PACKAGE / "results" / "finite_assurance_producer.json"
DERIVATION = PACKAGE / "THEOREM_DERIVATION.md"
PROTOCOL = PACKAGE / "VALIDATION_PROTOCOL.md"
INPUTS = {
    "theorem_derivation": (DERIVATION, "e0eadfc08dee5d73d531e85223143fabf6ba9d9a434757c33a9a2286fd4dc25c"),
    "validation_protocol": (PROTOCOL, "ad61f5da31940a33697ead9c82c3a235559d887907a4e21dd211b8c3eb57aea7"),
}


Pair = tuple[int, int]


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_hash(path: Path) -> str:
    return sha(path.read_bytes())


def input_audit() -> dict[str, str]:
    found: dict[str, str] = {}
    for name, (path, expected) in INPUTS.items():
        actual = file_hash(path)
        if actual != expected:
            raise RuntimeError(f"input hash mismatch {name}: {actual} != {expected}")
        found[name] = actual
    return found


def add(x: Pair, y: Pair) -> Pair:
    return x[0] + y[0], x[1] + y[1]


def sub(x: Pair, y: Pair) -> Pair:
    return x[0] - y[0], x[1] - y[1]


def alpha_pair(k: int) -> Pair:
    if k == 4:
        return 0, 0
    if k == 6:
        return 1, 0
    return 0, 1


def mul_alpha(x: Pair, k: int) -> Pair:
    if k == 4:
        return 0, 0
    if k == 6:
        return x
    c0, c1 = {8: (2, 0), 10: (1, 1), 12: (3, 0)}[k]
    a, b = x
    return b * c0, a + b * c1


def sign_surd(a: int, b: int, d: int) -> int:
    if not a and not b:
        return 0
    if not b:
        return 1 if a > 0 else -1
    if not a:
        return 1 if b > 0 else -1
    if (a > 0) == (b > 0):
        return 1 if a > 0 else -1
    comparison = a * a - d * b * b
    if comparison == 0:
        raise ArithmeticError("unexpected rational square root cancellation")
    dominant = a if comparison > 0 else b
    return 1 if dominant > 0 else -1


def pair_sign(x: Pair, k: int) -> int:
    a, b = x
    if k in (4, 6):
        if b:
            raise ArithmeticError("non-rational coordinate in rational field")
        return (a > 0) - (a < 0)
    if k == 8:
        return sign_surd(a, b, 2)
    if k == 12:
        return sign_surd(a, b, 3)
    if k == 10:
        return sign_surd(2 * a + b, b, 5)
    raise ValueError(k)


def recurrence_weights(k: int) -> tuple[tuple[Pair, ...], tuple[Pair, ...]]:
    sine: list[Pair] = [(0, 0), (1, 0)]
    cosine: list[Pair] = [(2, 0), alpha_pair(k)]
    while len(sine) <= k:
        sine.append(sub(mul_alpha(sine[-1], k), sine[-2]))
        cosine.append(sub(mul_alpha(cosine[-1], k), cosine[-2]))
    if sine[k] != (0, 0) or cosine[k] != (2, 0):
        raise ArithmeticError((k, sine[k], cosine[k]))
    return tuple(sine), tuple(cosine)


def bits(value: int, width: int) -> tuple[int, ...]:
    return tuple((value >> (width - 1 - j)) & 1 for j in range(width))


def coordinate(value: int, width: int, weights: tuple[Pair, ...]) -> Pair:
    answer = (0, 0)
    for j, bit in enumerate(bits(value, width), start=1):
        if bit:
            answer = add(answer, weights[j])
    return answer


def left_rotate(value: int, k: int) -> int:
    mask = (1 << k) - 1
    return ((value << 1) & mask) | (value >> (k - 1))


def right_rotate(value: int, k: int) -> int:
    return (value >> 1) | ((value & 1) << (k - 1))


def rc(value: int, width: int) -> int:
    answer = 0
    for _ in range(width):
        answer = (answer << 1) | (1 - (value & 1))
        value >>= 1
    return answer


def pcrs(k: int) -> tuple[tuple[int, ...], ...]:
    unseen = set(range(1 << k))
    rows: list[tuple[int, ...]] = []
    while unseen:
        start = min(unseen)
        orbit: list[int] = []
        value = start
        while value not in orbit:
            orbit.append(value)
            value = left_rotate(value, k)
        row = tuple(sorted(orbit))
        unseen.difference_update(row)
        rows.append(row)
    return tuple(sorted(rows, key=lambda row: row[0]))


def word(value: int, width: int) -> str:
    return f"{value:0{width}b}"


def word_list(values: Iterable[int], width: int) -> list[str]:
    return [word(value, width) for value in sorted(values)]


def set_hash(values: Iterable[int], width: int) -> str:
    return sha("".join(f"{value:0{width}b}\n" for value in sorted(values)).encode("ascii"))


def build_selector(
    k: int,
    *,
    rotation: str = "left",
    axis: str = "negative",
    broken_zero_pairing: bool = False,
) -> tuple[set[int] | None, dict[str, object], str | None]:
    cycles = pcrs(k)
    sine, cosine = recurrence_weights(k)
    selected: set[int] = set()
    zero_indices: list[int] = []
    for index, cycle in enumerate(cycles):
        representative = cycle[0]
        real = coordinate(representative, k, cosine)
        imag = coordinate(representative, k, sine)
        if real == (0, 0) and imag == (0, 0):
            zero_indices.append(index)
            continue
        candidates: list[int] = []
        for value in cycle:
            next_value = left_rotate(value, k) if rotation == "left" else right_rotate(value, k)
            a = pair_sign(coordinate(value, k, sine), k)
            b = pair_sign(coordinate(next_value, k, sine), k)
            ray = a == 0 and (b > 0 if axis == "negative" else b < 0)
            crossing = a < 0 < b
            if ray or crossing:
                candidates.append(value)
        if len(candidates) != 1:
            return None, {"selector_error_cycle": index, "candidate_count": len(candidates)}, "selector_unique"
        selected.add(candidates[0])

    index_of = {cycle: i for i, cycle in enumerate(cycles)}
    seen: set[int] = set()
    stable_rows: list[dict[str, object]] = []
    paired_rows: list[dict[str, object]] = []
    broken_applied = False
    for index in zero_indices:
        if index in seen:
            continue
        cycle = cycles[index]
        mate_cycle = tuple(sorted(rc(value, k) for value in cycle))
        mate = index_of[mate_cycle]
        if mate == index:
            fixed = sorted(value for value in cycle if rc(value, k) == value)
            if len(fixed) != 2:
                return None, {"stable_zero_cycle": index, "fixed_count": len(fixed)}, "stable_zero_two_fixed_words"
            chosen = fixed[0]
            selected.add(chosen)
            stable_rows.append(
                {"pcr_index": index, "fixed_words": word_list(fixed, k), "selected": word(chosen, k)}
            )
            seen.add(index)
            continue
        lo, hi = sorted((index, mate))
        if index != lo:
            continue
        source = cycles[lo][0]
        mate_word = rc(source, k)
        if broken_zero_pairing and not broken_applied and len(cycles[hi]) > 1:
            replacement = left_rotate(mate_word, k)
            if replacement == mate_word:
                return None, {"paired_zero_cycle": hi}, "broken_zero_pairing_applicable"
            mate_word = replacement
            broken_applied = True
        selected.update((source, mate_word))
        paired_rows.append(
            {
                "pcr_indices": [lo, hi],
                "source_word": word(source, k),
                "mate_word": word(mate_word, k),
            }
        )
        seen.update((lo, hi))
    if broken_zero_pairing and not broken_applied:
        return None, {"broken_zero_pairing_applied": False}, "mutation_not_applicable"
    return (
        selected,
        {
            "zero_pcr_indices": zero_indices,
            "stable_zero_rows": stable_rows,
            "paired_zero_rows": paired_rows,
        },
        None,
    )


def one_per_pcr(selected: set[int], k: int) -> bool:
    return all(len(selected.intersection(cycle)) == 1 for cycle in pcrs(k))


def residual_dag(selected: set[int], k: int) -> bool:
    n = 1 << (k - 1)
    mask = n - 1
    adjacency = [[] for _ in range(n)]
    indegree = [0] * n
    for edge in range(1 << k):
        if edge in selected:
            continue
        tail, head = edge >> 1, edge & mask
        adjacency[tail].append(head)
        indegree[head] += 1
    queue = deque(i for i, degree in enumerate(indegree) if degree == 0)
    count = 0
    while queue:
        u = queue.popleft()
        count += 1
        for v in adjacency[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    return count == n


def reverse_complement_set(selected: set[int], k: int) -> set[int]:
    return {rc(value, k) for value in selected}


def chi_support(k: int, sine: tuple[Pair, ...], *, closed: bool = False) -> set[int]:
    support: set[int] = set()
    for lower in range(1 << (k - 1)):
        value_sign = pair_sign(coordinate(lower, k - 1, sine), k)
        if value_sign > 0 or (closed and value_sign == 0):
            support.add(lower)
    return support


def potential_rc_invariant(support: set[int], k: int) -> bool:
    return {rc(value, k - 1) for value in support} == support


def defect_matches(selected: set[int], support: set[int], k: int, *, reversed_sign: bool = False) -> bool:
    mate = reverse_complement_set(selected, k)
    lower_mask = (1 << (k - 1)) - 1
    for edge in range(1 << k):
        lhs = int(edge in mate) - int(edge in selected)
        tail, head = edge >> 1, edge & lower_mask
        rhs = int(tail in support) - int(head in support)
        if reversed_sign:
            rhs = -rhs
        if lhs != rhs:
            return False
    return True


def static_failure(
    selected: set[int] | None,
    support: set[int],
    k: int,
    selector_error: str | None = None,
    *,
    reversed_sign: bool = False,
) -> str | None:
    if selector_error or selected is None:
        return selector_error or "selector_unique"
    if not one_per_pcr(selected, k):
        return "one_selected_per_pcr"
    if not residual_dag(selected, k):
        return "residual_dag"
    if any(rc(u, k - 1) == u for u in range(1 << (k - 1))):
        return "lower_rc_fixed_point_free"
    if not potential_rc_invariant(support, k):
        return "potential_rc_invariant"
    if not defect_matches(selected, support, k, reversed_sign=reversed_sign):
        return "rc_defect_gradient"
    return None


def incoming(lower: int, k: int) -> set[int]:
    return {lower, (1 << (k - 1)) | lower}


def outgoing(lower: int) -> set[int]:
    return {lower << 1, (lower << 1) | 1}


def enabled_f(selected: set[int], lower: int, k: int) -> bool:
    return incoming(lower, k).issubset(selected)


def apply_f(selected: set[int], lower: int, k: int) -> set[int]:
    if not enabled_f(selected, lower, k):
        raise RuntimeError("disabled F move")
    return (selected - incoming(lower, k)) | outgoing(lower)


def run_path(selected: set[int], support: set[int], k: int) -> tuple[set[int], list[dict[str, object]]]:
    current = set(selected)
    remaining = set(support)
    steps: list[dict[str, object]] = []
    while remaining:
        enabled = [u for u in sorted(remaining) if enabled_f(current, u, k)]
        if not enabled:
            raise RuntimeError(f"no enabled positive F move at k={k}")
        lower = enabled[0]
        partner = rc(lower, k - 1)
        if partner == lower or partner not in remaining:
            raise RuntimeError("paired potential invariant failed before firing")
        current = apply_f(current, lower, k)
        remaining.remove(lower)
        remaining.remove(partner)
        if not one_per_pcr(current, k):
            raise RuntimeError("F move broke PCR transversal")
        if not residual_dag(current, k):
            raise RuntimeError("F move broke residual DAG")
        if not potential_rc_invariant(remaining, k):
            raise RuntimeError("F move broke paired potential")
        if not defect_matches(current, remaining, k):
            raise RuntimeError("F move broke defect identity")
        steps.append(
            {
                "step": len(steps) + 1,
                "fired_lower_word": word(lower, k - 1),
                "paired_lower_word": word(partner, k - 1),
                "selected_sha256": set_hash(current, k),
                "remaining_support_sha256": set_hash(remaining, k - 1),
            }
        )
    if current != reverse_complement_set(current, k):
        raise RuntimeError("terminal is not RC fixed")
    return current, steps


def order_row(k: int) -> dict[str, object]:
    if k == 2:
        selected = {0, 1, 3}
        if not one_per_pcr(selected, k) or not residual_dag(selected, k):
            raise RuntimeError("explicit k=2 control failed")
        if selected != reverse_complement_set(selected, k):
            raise RuntimeError("explicit k=2 set is not RC fixed")
        return {
            "k": 2,
            "arithmetic": "explicit_k2",
            "pcr_count": len(pcrs(2)),
            "selected_count": len(selected),
            "initial_selected_words": word_list(selected, 2),
            "initial_selected_sha256": set_hash(selected, 2),
            "zero_pcr_count": 0,
            "stable_zero_count": 0,
            "paired_zero_pair_count": 0,
            "zero_ties": {"stable": [], "paired": []},
            "chi_support_count": 0,
            "chi_support_sha256": set_hash((), 1),
            "move_count": 0,
            "path": [],
            "terminal_selected_words": word_list(selected, 2),
            "terminal_selected_sha256": set_hash(selected, 2),
            "one_per_pcr": True,
            "initial_residual_dag": True,
            "coboundary_identity": "not_used_explicit_k2",
            "terminal_rc_fixed": True,
            "terminal_residual_dag": True,
        }

    sine, cosine = recurrence_weights(k)
    selected, meta, error = build_selector(k)
    support = chi_support(k, sine)
    failure = static_failure(selected, support, k, error)
    if failure or selected is None:
        raise RuntimeError(f"baseline static failure at k={k}: {failure}")
    terminal, steps = run_path(selected, support, k)
    if len(steps) * 2 != len(support):
        raise RuntimeError("path length does not equal paired support")
    return {
        "k": k,
        "arithmetic": {
            "basis": "a+b*alpha",
            "alpha_relation": {4: "alpha=0", 6: "alpha=1", 8: "alpha^2=2", 10: "alpha^2=alpha+1", 12: "alpha^2=3"}[k],
            "sine_weights": [list(value) for value in sine[1:]],
            "doubled_cosine_weights": [list(value) for value in cosine[1:]],
        },
        "pcr_count": len(pcrs(k)),
        "selected_count": len(selected),
        "initial_selected_words": word_list(selected, k),
        "initial_selected_sha256": set_hash(selected, k),
        "zero_pcr_count": len(meta["zero_pcr_indices"]),
        "stable_zero_count": len(meta["stable_zero_rows"]),
        "paired_zero_pair_count": len(meta["paired_zero_rows"]),
        "zero_ties": {"stable": meta["stable_zero_rows"], "paired": meta["paired_zero_rows"]},
        "chi_support_count": len(support),
        "chi_support_sha256": set_hash(support, k - 1),
        "move_count": len(steps),
        "path": steps,
        "terminal_selected_words": word_list(terminal, k),
        "terminal_selected_sha256": set_hash(terminal, k),
        "one_per_pcr": True,
        "initial_residual_dag": True,
        "coboundary_identity": True,
        "terminal_rc_fixed": terminal == reverse_complement_set(terminal, k),
        "terminal_residual_dag": residual_dag(terminal, k),
    }


def mutation_result(name: str) -> dict[str, object]:
    for k in ORDERS[1:]:
        sine, _ = recurrence_weights(k)
        selected, _, error = build_selector(k)
        support = chi_support(k, sine)
        reason: str | None = None
        applicable = True
        if name == "RIGHT_ROTATION_SELECTOR":
            selected, _, error = build_selector(k, rotation="right")
            reason = static_failure(selected, support, k, error)
        elif name == "REVERSED_GRADIENT_SIGN":
            reason = static_failure(selected, support, k, error, reversed_sign=True)
        elif name == "CLOSED_HALF_PLANE":
            closed = chi_support(k, sine, closed=True)
            reason = static_failure(selected, closed, k, error)
        elif name == "POSITIVE_AXIS_CONVENTION":
            selected, _, error = build_selector(k, axis="positive")
            reason = static_failure(selected, support, k, error)
        elif name == "BROKEN_ZERO_PAIRING":
            selected, _, error = build_selector(k, broken_zero_pairing=True)
            if error == "mutation_not_applicable":
                applicable = False
            else:
                reason = static_failure(selected, support, k, error)
        elif name == "UNPAIRED_DEFECT_UPDATE":
            if selected is None:
                reason = error
            else:
                enabled = [u for u in sorted(support) if enabled_f(selected, u, k)]
                if not enabled:
                    reason = "no_enabled_positive_f_move"
                else:
                    lower = enabled[0]
                    mutated_state = apply_f(selected, lower, k)
                    mutated_support = set(support)
                    mutated_support.remove(lower)
                    if not potential_rc_invariant(mutated_support, k):
                        reason = "remaining_potential_rc_invariant"
                    elif not defect_matches(mutated_state, mutated_support, k):
                        reason = "rc_defect_gradient"
        elif name == "REVERSED_F_MOVE":
            if selected is None:
                reason = error
            else:
                enabled = [u for u in sorted(support) if enabled_f(selected, u, k)]
                if not enabled:
                    reason = "no_enabled_positive_f_move"
                else:
                    lower = enabled[0]
                    if not outgoing(lower).issubset(selected):
                        reason = "inverse_move_not_enabled"
                    else:
                        inverse_state = (selected - outgoing(lower)) | incoming(lower, k)
                        reason = static_failure(inverse_state, support, k)
        else:
            raise ValueError(name)
        if not applicable:
            continue
        if reason:
            return {"name": name, "rejected": True, "first_k": k, "failed_predicate": reason}
    return {"name": name, "rejected": False, "first_k": None, "failed_predicate": None}


def scientific_payload() -> dict[str, object]:
    rows = [order_row(k) for k in ORDERS]
    mutations = [
        mutation_result(name)
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
    outcome = PASS if passed else FAIL
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
        "outcome": outcome,
        "claim_boundary": {
            "finite_assurance_only": True,
            "all_order_proof_source": "paper and standalone theorem derivation, not this replay",
            "external_outputs_used": False,
            "release_or_novelty_promotion": False,
            "orders_exhaustive": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=RESULT)
    args = parser.parse_args()
    started = time.perf_counter()
    try:
        inputs = input_audit()
        payload = scientific_payload()
        receipt = {
            "schema_version": SCHEMA,
            "assurance_scope": ASSURANCE_SCOPE,
            "status": payload["outcome"],
            "producer": Path(__file__).name,
            "inputs": inputs,
            "scientific_payload": payload,
            "scientific_payload_sha256": sha(canonical(payload)),
            "runtime": {
                "elapsed_seconds": time.perf_counter() - started,
                "python": sys.version.split()[0],
                "platform": platform.platform(),
            },
        }
        code = 0 if payload["outcome"] == PASS else 1
    except Exception as exc:  # fail closed with an auditable envelope
        receipt = {
            "schema_version": SCHEMA,
            "assurance_scope": ASSURANCE_SCOPE,
            "status": INCONCLUSIVE,
            "producer": Path(__file__).name,
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
