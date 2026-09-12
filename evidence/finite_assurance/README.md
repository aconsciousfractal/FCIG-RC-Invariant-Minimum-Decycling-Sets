# Exact Binary Finite-Assurance Capsule

This self-contained directory contains a readable theorem derivation, the
validation protocol, and two nonidentical exact implementations.

The derivation separates the proof-level real-weight family from the
integer-weight polynomial-bit membership corollary.  The executable binary
panel continues to exercise the same integer specialization and its
scientific payload is therefore unchanged.

- `THEOREM_DERIVATION.md` — q-ary all-order derivation, SHA-256
  `5f64d0091aa0d1b28273f5faa0496191f6f791ee86e8cac83264129081f0a3e1`;
- `VALIDATION_PROTOCOL.md` — SHA-256
  `19ed51233420723178307e606649c8efe8862b09906804af16e0ff4ab98ecfc0`;
- `scripts/produce.py` — exact quadratic-ring coordinates and Kahn DAG test;
- `scripts/validate.py` — literal exact tables and independent DFS DAG test.

Run the two inner programs only in a disposable copy because their defaults
write receipts inside this capsule:

```text
python scripts/produce.py
python scripts/validate.py
```

The repository-level `scripts/verify.py` is the recommended non-writing
entrypoint; it creates the disposable copy automatically.

Expected stable scientific payload:

`3bbec32e9d37706e98db9bb61192d12653a6adb8f419a2f1e816b31cd664d9b5`.

The executable panel checks the binary specialization at
`k=2,4,6,8,10,12` and rejects seven scientific plus seven envelope
mutations. It does not implement the direct q-ary selector. It is convention
assurance, not an all-order premise or a novelty certificate.
