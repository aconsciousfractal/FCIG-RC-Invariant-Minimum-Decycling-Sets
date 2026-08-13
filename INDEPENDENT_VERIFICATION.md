# Independent Verification Guide

## 1. Read the mathematical object

Open `paper/A_Parity_Theorem_for_RC_Invariant_MDS.pdf`.  The normalization is
in Section 2, odd nonexistence in Section 3, the binary cyclotomic seed and tie
theorem in Section 4, the exact half-plane coboundary in Section 5, legal
defect descent in Section 6, and the parity composition in Section 7.

## 2. Verify the repository and package

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

The history checker requires exactly one root commit and rejects recoverable
non-public workflow identifiers. The manifest checker authenticates source/evidence
coverage.  The worktree checker permits an explicitly requested generated
receipt but rejects privacy, size, archive, binary, cache, and LFS hazards.
The archive checker is stricter: it requires the exact sealed file set and
therefore rejects every generated receipt.  The verifier itself is
non-writing unless `--output` is supplied.

## 3. Audit the delicate proof points

- PCRs are sets of distinct rotations, including imprimitive orbits.
- Homopolymer loops are mandatory and literal set overlap is retained in a
  source move.
- The odd proof separately excludes a setwise RC-stable odd PCR.
- Rotation indices use `r -> s-r`; position indices use `i -> s-1-i`.
- Zero-embedding PCR representatives are arbitrary for acyclicity and only
  afterward chosen RC-equivariantly.
- The half-plane is open; the negative-real-axis convention is load-bearing.
- One source is fired at a time.  “Paired” refers to the forced
  two-coordinate potential update, not a simultaneous move.
- The minimum-zero normalization and connectedness of the lower graph are
  required at the termination step.
- Finite rows do not discharge an all-order quantifier.

## 4. Evidence boundary

The written proof is the authority for the all-order theorem.  The executable
panel checks exact finite conventions and mutations only.  Its hashes certify
artifact identity, not mathematical truth or novelty.
