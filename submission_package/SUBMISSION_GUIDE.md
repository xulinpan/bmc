# BMC Bioinformatics — Submission Guide

**Manuscript:** A Leakage-Controlled Cold-Start Benchmark for Drug-Combination Synergy Classification on DrugComb v1.5
**Author:** Xulin Pan · Article type: Research article

This package is complete and LaTeX-based. Below is what to upload, how to build it, and the few
author-only steps remaining before submission.

---

## 1. What to upload to BMC (the editorial system)

| Upload slot | File |
|---|---|
| Manuscript (LaTeX source) | `manuscript/main.tex` (uses `\documentclass{bmcart}`) |
| Figures (separate files) | `manuscript/figures/fig1…fig11` (PNG, 300 DPI) |
| Cover letter | `cover_letter_bmc_bioinformatics.txt` |
| Supplementary / Additional files | `supplementary/` (scripts + metric JSON), zipped, if the portal requests |

BMC's submission system **already contains `bmcart.cls`**, so you upload `main.tex` directly — you do
**not** need to supply the class file to them. `manuscript/main_article.pdf` is your human-readable
preview of the same content.

---

## 2. File manifest

```
bmc_bioinformatics_submission/
├── SUBMISSION_GUIDE.md                  ← this file
├── PEER_REVIEW_BMC_Bioinformatics.md    ← reviewer-style critique + revision status
├── cover_letter_bmc_bioinformatics.txt
├── submission_checklist.txt             ← pre-submission action items
├── README_submission_package.md
├── manuscript/
│   ├── main.tex                         ← BMC bmcart submission source (canonical)
│   ├── main_article.tex                 ← same content, article class (compiles anywhere)
│   ├── main_article.pdf                 ← compiled 15-page preview
│   └── figures/                         ← 7 figures used in the text, 300 DPI
└── supplementary/
    ├── README_experiments.md
    ├── prep.py, train_lr.py, train_gbm.py, analysis.py, figures.py, figures2.py
    ├── experiments_review.py            ← no-study / leave-study-out / leave-tissue-out
    ├── regen_figures_300dpi.py
    ├── fingerprint_baseline.py, fetch_drug_smiles.py, drug_smiles_demo.csv
    ├── *.json                           ← metric outputs
    └── review_experiments_output/       ← robustness-experiment results + summary
```

`main.tex` and `main_article.tex` are kept byte-for-byte consistent in content; they differ only in the
document-class wrapper (BMC `bmcart` vs standard `article`).

---

## 3. How to compile

**Option A — official BMC format (`main.tex`).** Open the "BioMed Central article" template on Overleaf
(it bundles `bmcart.cls`), upload `main.tex` and the `figures/` folder, and compile. Locally, place
`bmcart.cls` next to `main.tex` and run `pdflatex main.tex` twice. The bibliography is inline
(`thebibliography`), so no BibTeX pass is required.

**Option B — preview anywhere (`main_article.tex`).** Standard `article` class, no external files:

```bash
cd manuscript
pdflatex main_article.tex
pdflatex main_article.tex
```

This is how `main_article.pdf` was produced (15 pages, verified: no undefined references or citations).

---

## 4. Author-only steps before submission (see `submission_checklist.txt`)

1. **Deposit the code (required by BMC before acceptance).** Create a public GitHub repo, mint a Zenodo
   DOI from a tagged release, add an OSI license, and update the *Availability of data and materials*
   statement to cite the URL + DOI. The statement currently says the code is supplied as supplementary
   material and will be deposited before final submission — that commitment must be fulfilled.
2. Confirm the corresponding-author affiliation and email, and the NSFC grant formatting.
3. (Optional, strengthens the paper) run the full Morgan-fingerprint molecular baseline — see
   `supplementary/README_experiments.md`.

---

## 5. Status vs. the peer-review report

- **Leakage control, cold-start framing, imbalance-aware metrics** — in place.
- **No-study ablation, leave-study-out, leave-tissue-out** — run and integrated (Results "Robustness
  experiments" table). Removing study barely changes performance (0.807→0.806); leave-study-out falls to
  chance (0.332); leave-tissue-out collapses (0.431).
- **Molecular baseline** — implemented and validated end-to-end; full run is the author's next step.
- **Open-code deposit** — the one mandatory item outstanding (step 1 above).
```
