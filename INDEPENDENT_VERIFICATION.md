# Independent Verification Guide

## 1. Read the mathematical object

Open `paper/A_Parity_Theorem_for_RC_Invariant_MDS.pdf`. The normalization is
in Section 2, odd nonexistence in Section 3, the weighted q-ary seed and zero
ties in Section 4, the exact coboundary in Section 5, legal descent in Section
6, the direct spectral construction in Section 7, and theorem assembly plus
the DNA corollary in Section 8.

## 2. Audit the delicate proof points

- The complement is an involution with no fixed alphabet symbol.
- The construction-level weight map is real, injective, nonzero, and
  antisymmetric; the polynomial-bit corollary separately assumes integer
  weights with a finite binary encoding.
- PCRs contain distinct rotations, including imprimitive orbits.
- Homopolymer loops are mandatory and literal set overlap is retained in an
  F-move.
- The nonzero selector uses the negative real ray or the strict
  lower-to-upper crossing.
- Arbitrary zero-PCR representatives preserve acyclicity before they are
  chosen equivariantly.
- A stable even PCR has exactly two RC-fixed rotations over every allowed
  alphabet, not only binary.
- The half-plane is open and the gradient is tail minus head.
- One physical firing produces a two-coordinate potential update.
- Strong connectedness and minimum-zero normalization are both used at
  termination.
- The direct set is an ideal because `r_s` increases strictly on every
  residual edge internal to the positive sector.
- Exact integer-weight membership uses algebraic sign determination; no
  floating-point zero test is part of the theorem, and no effective claim is
  made for an unrepresented arbitrary real table.
- The `k=2` construction is separate, and `k=1` is an explicit exception.

## 3. Verify the repository package

From a repository clone:

```text
python scripts/check_git_history.py
```

From either a clone or a fresh exact extraction:

```text
python scripts/check_manifest.py
python scripts/check_worktree.py
python scripts/check_release_archive.py
python scripts/verify.py
python scripts/test_release_hygiene_mutations.py
```

The executable calculation is a binary finite-assurance panel only. The
written proof is authority for the q-ary all-order theorem and direct
membership corollary.

## 4. Evidence boundary

The hashes authenticate bytes. The finite rows check conventions. Neither
function supplies a novelty opinion, an all-order proof, or a biological
benchmark.
