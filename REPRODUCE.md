# Reproduce

## Requirements

- Python 3.11 or later;
- standard library only for package verification;
- a TeX distribution with `pdflatex` and `bibtex` only for rebuilding the PDF.

No Python package installation, network access, or external solver is required.

## Integrity and archive checks

From the repository root:

```text
python scripts/check_manifest.py
python scripts/check_worktree.py
python scripts/check_release_archive.py
```

`MANIFEST_SHA256.txt` covers environment-independent source, evidence,
documentation, and provenance.  It excludes itself, `RELEASE_SHA256.txt`, the
selected PDF, generated JSON receipts, and LaTeX build products.
`RELEASE_SHA256.txt` separately pins the manifest and article PDF, avoiding a
hash cycle.  The archive checker then requires the actual file set to be
exactly the manifest set plus those three envelope objects; an ignored receipt
therefore cannot slip into a distributable archive.

## Exact binary-specialization replay

```text
python scripts/verify.py
```

The no-argument command writes no file.  To retain a local receipt:

```text
python scripts/verify.py --output results/verification.json
```

The wrapper executes both implementations in a temporary copy.  Successful
output has `pass=true`, six rows, 612 firings, 7/7 scientific mutations, 7/7
envelope mutations, and stable scientific payload
`3bbec32e9d37706e98db9bb61192d12653a6adb8f419a2f1e816b31cd664d9b5`.
The calculation is finite binary assurance only; the q-ary all-order theorem
and direct membership corollary are proved in the paper.

## Adversarial package panel

```text
python scripts/test_release_hygiene_mutations.py
```

The script operates only in temporary copies.  It re-seals the checksum layers
after fourteen hostile mutations.  Thirteen must fail worktree and archive
hygiene; the generated-receipt control must pass worktree hygiene but fail
exact archive membership.

## Build the paper

The reference environment uses MiKTeX 25.12 / pdfTeX 1.40.28 and BibTeX 0.99e.
For a manual build, start at the repository root and run:

```text
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf A_Parity_Theorem_for_RC_Invariant_MDS.pdf
```

The final command copies the generated `paper/main.pdf` byte-for-byte to the
selected article path.  The source suppresses PDF date/trailer variability.
Windows users may instead run this helper from the repository root:

```text
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/build_paper.ps1 -Clean
```

The current article-PDF digest is the second pin in `RELEASE_SHA256.txt`.
The source fixes author and document metadata and suppresses volatile PDF
date/trailer fields so independent clean builds can be compared bytewise.

## Git-history hygiene

From a repository clone, run:

```text
python scripts/check_git_history.py
```

This verifies that the distributable history consists of one root commit and
that no deleted non-public workflow material remains reachable. It is intentionally
separate from archive verification because a source archive has no `.git`
directory.
