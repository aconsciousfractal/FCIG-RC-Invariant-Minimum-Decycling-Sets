# Exact Finite-Assurance Capsule

This self-contained directory contains a readable theorem derivation, the
validation protocol, and two nonidentical exact implementations.

- `THEOREM_DERIVATION.md` — SHA-256
  `1cefda36038cac5d74c9cc18f85bd6461c1e5aede7f06d95fcef1cc4df20e39d`;
- `VALIDATION_PROTOCOL.md` — SHA-256
  `67ef1020f7364e25e96519f8247b8cd01f955e6c50ec2133733c0a52bb1705e6`;
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

The finite panel checks exact conventions at `k=2,4,6,8,10,12` and rejects
seven scientific plus seven envelope mutations.  It is assurance for the
proof, not an all-order premise or a novelty certificate.
