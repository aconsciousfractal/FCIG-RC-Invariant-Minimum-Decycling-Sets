param(
    [string]$PdfLaTeX = "pdflatex",
    [string]$BibTeX = "bibtex",
    [switch]$Clean
)

$ErrorActionPreference = "Stop"
$PaperDirectory = (Resolve-Path (Join-Path $PSScriptRoot "..\paper")).Path
$SelectedPdf = Join-Path $PaperDirectory "A_Parity_Theorem_for_RC_Invariant_MDS.pdf"

Push-Location $PaperDirectory
try {
    if ($Clean) {
        @("main.aux", "main.bbl", "main.blg", "main.log", "main.out", "main.pdf", "main.toc") |
            ForEach-Object {
                $Artifact = Join-Path $PaperDirectory $_
                if (Test-Path -LiteralPath $Artifact) {
                    Remove-Item -LiteralPath $Artifact -Force
                }
            }
    }

    & $PdfLaTeX --version
    if ($LASTEXITCODE -ne 0) { throw "Unable to execute pdfLaTeX" }
    & $BibTeX --version
    if ($LASTEXITCODE -ne 0) { throw "Unable to execute BibTeX" }

    & $PdfLaTeX -interaction=nonstopmode -halt-on-error main.tex
    if ($LASTEXITCODE -ne 0) { throw "Initial pdfLaTeX pass failed" }

    & $BibTeX main
    if ($LASTEXITCODE -ne 0) { throw "BibTeX pass failed" }

    & $PdfLaTeX -interaction=nonstopmode -halt-on-error main.tex
    if ($LASTEXITCODE -ne 0) { throw "Second pdfLaTeX pass failed" }

    & $PdfLaTeX -interaction=nonstopmode -halt-on-error main.tex
    if ($LASTEXITCODE -ne 0) { throw "Final pdfLaTeX pass failed" }

    Copy-Item -LiteralPath (Join-Path $PaperDirectory "main.pdf") -Destination $SelectedPdf -Force
    Get-FileHash -Algorithm SHA256 -LiteralPath $SelectedPdf

    if ($Clean) {
        @("main.aux", "main.bbl", "main.blg", "main.log", "main.out", "main.pdf", "main.toc") |
            ForEach-Object {
                $Artifact = Join-Path $PaperDirectory $_
                if (Test-Path -LiteralPath $Artifact) {
                    Remove-Item -LiteralPath $Artifact -Force
                }
            }
    }
}
finally {
    Pop-Location
}
