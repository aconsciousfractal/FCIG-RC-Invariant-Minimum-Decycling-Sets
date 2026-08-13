# Source and Evidence Lock

The repository is standalone: verification needs no parent project.  Its
complete environment-independent source/evidence identity is
`MANIFEST_SHA256.txt`; the article PDF and manifest are independently pinned
by `RELEASE_SHA256.txt`.

Finite-assurance identities are recorded here after every mathematical-input
change:

- theorem derivation:
  `1cefda36038cac5d74c9cc18f85bd6461c1e5aede7f06d95fcef1cc4df20e39d`;
- validation protocol:
  `67ef1020f7364e25e96519f8247b8cd01f955e6c50ec2133733c0a52bb1705e6`;
- stable scientific payload:
  `3bbec32e9d37706e98db9bb61192d12653a6adb8f419a2f1e816b31cd664d9b5`.

No parent-repository commit, non-public workflow state, machine-local path, or
deleted workflow artifact is part of the source identity. A clone can verify the
single-root public history with `python scripts/check_git_history.py`; a
source extraction can verify the sealed file set with
`python scripts/check_release_archive.py`.

The paper imports only the ordinary minimum cardinality/construction and the
valid source-move preservation result identified in the bibliography.  Modern
RC-constrained work is compared explicitly but is not imported as proof of the
parity theorem.
