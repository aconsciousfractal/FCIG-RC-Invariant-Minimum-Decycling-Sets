# Source and Evidence Boundary

The repository is standalone: no parent project, private workflow, or
machine-local path is needed to read the theorem or replay the finite panel.
`MANIFEST_SHA256.txt` authenticates the environment-independent source; the
manifest and article PDF are pinned separately by `RELEASE_SHA256.txt`.

## Imported mathematical facts

| Source | Imported role | Not imported |
| --- | --- | --- |
| Mykkeltveit (1972) | classical binary decycling construction | q-ary RC theorem |
| Champarnaud--Hansel--Perrin (2004) | q-ary ordinary minimum `N_q(k)` | RC invariance |
| Marçais--DeBlasio--Kingsford (2024), Section 4.1 | standard full-alphabet F-move terminology and context | preservation (proved in the paper), connectivity, parity, or spectral midpoint |
| Marçais--Elder--Kingsford (2024) | explicit reverse-complement-constrained motivation and comparison | the theorem proved here |
| Pellow et al. (2023) | geometric-selector and on-demand-membership context | the moved RC-invariant terminal |
| Watkins--Zeitlin (1993) | minimal-polynomial context for cyclotomic real parts | the norm gap or MDS theorem |
| Emiris--Tsigaridas (2005) | standard polynomial-bit real-algebraic sign machinery | the spectral reduction and combinatorial proof |

The paper itself proves weighted covariance, arbitrary-zero-tie acyclicity,
stable-PCR fixed rotations, the exact RC coboundary, legal paired descent,
the spectral ideal, literal RC invariance, the real-weight robustness of the
construction, and the odd obstruction.  The real-weight extension is proved
internally and imports no additional source.

Finite-assurance identities are refreshed after every mathematical-input
change and recorded in the capsule README and `CERTIFIED_SUMMARY.json`. The
binary panel is not cited as authority for the q-ary theorem or the direct
membership complexity bound.

Current mathematical-input identities:

- theorem derivation: `5f64d0091aa0d1b28273f5faa0496191f6f791ee86e8cac83264129081f0a3e1`;
- binary validation protocol: `19ed51233420723178307e606649c8efe8862b09906804af16e0ff4ab98ecfc0`;
- stable binary scientific payload: `3bbec32e9d37706e98db9bb61192d12653a6adb8f419a2f1e816b31cd664d9b5`.
