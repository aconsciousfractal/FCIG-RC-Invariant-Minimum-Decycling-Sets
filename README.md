# A Parity Theorem for RC-Invariant Minimum Decycling Sets

**Author:** Oleksiy Babanskyy

This repository contains the final standalone article and reproducibility package
for *A Parity Theorem for Reverse-Complement-Invariant Minimum
Decycling Sets in Binary de Bruijn Graphs*.

## Main theorem

For every binary word length `k >= 2`, the directed binary de Bruijn graph
`B(2,k)` has a reverse-complement-invariant ordinary minimum decycling set if
and only if `k` is even.

The odd obstruction is proved for every finite alphabet with a
fixed-point-free complement.  The even construction is binary.  The
all-order proof is deductive; the executable finite panel is assurance for
signs, conventions, and mutations, not a premise of the theorem.

Article PDF:

`paper/A_Parity_Theorem_for_RC_Invariant_MDS.pdf`

## Verification

Python 3.11 or later, standard library only:

```text
python scripts/check_manifest.py
python scripts/check_worktree.py
python scripts/check_release_archive.py
python scripts/check_git_history.py
python scripts/verify.py
python scripts/test_release_hygiene_mutations.py
```

The Git-history check applies to a repository clone; the remaining commands
also work from an exact source archive.  Expected results are a single clean
root commit, exact manifest and archive coverage, safe worktree hygiene, a
six-row finite-assurance PASS for `k=2,4,6,8,10,12`, 612 legal source
firings, 7/7 scientific and 7/7 envelope mutations rejected, and 14/14
package mutations rejected.  The stable scientific payload is
`3bbec32e9d37706e98db9bb61192d12653a6adb8f419a2f1e816b31cd664d9b5`.

The two mathematical implementations are independent: one uses exact
quadratic-ring coordinates plus Kahn DAG traversal; the other uses frozen
exact coordinate tables plus a recursive DFS DAG oracle.  Neither invokes a
network service, SAT/MILP solver, or external witness.

## Repository layout

| Path | Content |
| --- | --- |
| `paper/` | complete LaTeX source and article PDF |
| `evidence/finite_assurance/` | standalone derivation, protocol, and two exact implementations |
| `evidence/theorem/` | proof-versus-computation boundary |
| `scripts/verify.py` | non-writing finite-assurance wrapper |
| `scripts/check_git_history.py` | single-root and full-history privacy check |
| `scripts/check_worktree.py` | checksum, privacy, size, binary, and LFS hygiene |
| `scripts/check_release_archive.py` | exact archive-membership enforcement |
| `scripts/test_release_hygiene_mutations.py` | fourteen re-sealed hostile-package controls |
| `docs/` | claim, source, history, and authorship boundaries |

## Claim and distribution boundary

No novelty, priority, complexity, biological-performance, clinical, or
larger-alphabet even theorem is claimed.  See
`docs/PUBLIC_CLAIM_BOUNDARY.md` before quoting the result.

The author is Oleksiy Babanskyy.  No affiliation, ORCID, DOI, journal venue,
or repository URL is asserted until one is assigned.  Copyright is governed
by the `ALL RIGHTS RESERVED` notice and limited non-commercial verification
permission in `LICENSE`.

## Accessibility

The selected PDF supports text extraction, bookmarks, hyperlinks, and embedded
fonts, but it is not a tagged PDF/PDF-UA artifact. The complete LaTeX source is
included. A destination that requires tagged accessible PDF output will require
a separate accessible export before submission.
