# Generated Results

`python scripts/verify.py` is non-writing by default.  Use
`python scripts/verify.py --output results/verification.json` to retain a local
receipt.  Generated JSON below a `results/` directory is intentionally ignored
by Git and excluded from the source manifest.

Such a receipt is allowed by `check_worktree.py` but deliberately rejected by
`check_release_archive.py`.  Remove generated receipts before packaging a
release archive.
