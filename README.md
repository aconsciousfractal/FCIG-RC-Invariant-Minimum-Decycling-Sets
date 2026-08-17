# A Parity Theorem for RC-Invariant Minimum Decycling Sets

**Author:** Oleksiy Babanskyy

This repository contains the final standalone article and mathematical
reproducibility package for *A Parity Theorem for Reverse-Complement-Invariant
Minimum Decycling Sets in q-ary de Bruijn Graphs*.

## Main theorem

Let `A` be any finite nonempty alphabet with a fixed-point-free involutive
complement, and let `q = |A|`. For every integer `k >= 2`, the directed de
Bruijn graph `B(q,k)` has a literal reverse-complement-invariant ordinary
minimum decycling set if and only if `k` is even.

Consequences include:

- the binary theorem for `0 <-> 1`;
- the DNA theorem for `A <-> T` and `C <-> G`;
- exact even-order cardinality
  `N_q(k) = (1/k) sum_{d|k} phi(d) q^(k/d)`;
- an odd-order symmetry premium of at least two;
- a family of deterministic direct spectral selectors indexed by injective
  antisymmetric real weight maps;
- polynomial-bit word membership for the integer-weight specialization, in
  addition to a finite legal full-alphabet firing descent.

For DNA, one concrete weight choice is
`s(A),s(C),s(G),s(T) = -2,-1,1,2`. The theorem is graph-theoretic: it does
not assert a quantitative window guarantee or biological performance.

Article PDF:

`paper/A_Parity_Theorem_for_RC_Invariant_MDS.pdf`

## Proof architecture

The odd obstruction uses a primitive PCR joining two RC-fixed lower states.
For even `k >= 4`, injective antisymmetric real alphabet weights define a
weighted cyclotomic seed. Arbitrary choices on zero-embedding PCRs are proved acyclic,
so the ties can be made RC-equivariant. The exact edgewise identity

```text
1_RC(M) - 1_M = nabla chi
```

turns the symmetry defect into a nonnegative integral potential. Legal
full-alphabet source firings remove it two coordinates at a time. A second
construction selects a self-dual spectral ideal directly and gives
word-by-word membership without materializing the firing path. For a
finitely encoded integer weight table, that membership rule has polynomial
Turing bit complexity. The case
`k=2` is handled by a complement-reversing total order.

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

The exact executable panel is intentionally narrower than the theorem: it
checks the binary specialization at `k=2,4,6,8,10,12`, including 612 legal
firings, 7/7 scientific mutations, and 7/7 envelope mutations. It is
convention assurance only; the written proof is the all-order and q-ary
authority. The direct q-ary membership theorem is mathematical content, not
a software release in this repository.

## Repository layout

| Path | Content |
| --- | --- |
| `paper/` | complete LaTeX source and article PDF |
| `evidence/finite_assurance/` | standalone theorem derivation plus the binary exact panel |
| `evidence/theorem/` | proof-versus-computation boundary |
| `scripts/verify.py` | non-writing finite-assurance wrapper |
| `scripts/check_git_history.py` | distributable-history privacy check |
| `scripts/check_worktree.py` | checksum, privacy, size, binary, and LFS hygiene |
| `scripts/check_release_archive.py` | exact archive-membership enforcement |
| `docs/` | claim, source, history, and authorship boundaries |

## Claim and distribution boundary

The public mathematical claims are the q-ary parity theorem, its binary and
DNA corollaries, the exact firing count for the exhibited monotone descent,
and the direct polynomial-bit membership theorem. No exact odd premium,
shortest-path result, longest-residual-path bound, biological-performance,
clinical, or blanket novelty/priority claim is made. See
`docs/PUBLIC_CLAIM_BOUNDARY.md`.

The author is Oleksiy Babanskyy (ORCID `0009-0001-6176-6208`). No affiliation,
DOI, or journal venue is asserted. The repository is distributed under the MIT
license; its third-party boundary is stated in `LICENSE_SCOPE.md`.

## Accessibility

The selected PDF supports text extraction, bookmarks, hyperlinks, and
embedded fonts, but it is not a tagged PDF/PDF-UA artifact. The complete
LaTeX source is included. A venue requiring tagged accessible PDF output will
need a separate accessible export.
