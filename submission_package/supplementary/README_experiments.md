# Review Experiments: Reproducibility Notes

All commands are intended to run from this `supplementary/` folder. The scripts auto-locate
`drugcomb_synergy_prediction_modeling.csv` in the parent `modeling/` folder. Alternatively, set:

```bash
DRUGCOMB_DATA=/path/to/drugcomb_synergy_prediction_modeling.csv
```

Requirements:

```bash
pip install lightgbm scikit-learn pyarrow scipy pandas numpy
```

For the optional molecular baseline:

```bash
pip install rdkit
```

## Identity-Only Robustness Experiments

These experiments address the main BMC review risks around study confounding and cross-context transfer.
They use the same identity-and-context feature set as the manuscript.

```bash
python experiments_review.py prep
python experiments_review.py nostudy leavestudy leavetissue
```

Outputs are already included in `review_experiments_output/`:

- `nostudy.json`
- `leavestudy.json`
- `leavetissue.json`
- `review_experiments_summary.md`

Reported results, LightGBM with seed 42:

| Regime | Bal. acc. | Macro-F1 | Macro-AUC |
|---|---:|---:|---:|
| Standard, with study | 0.807 | 0.708 | 0.923 |
| Standard, no study | 0.806 | 0.708 | 0.922 |
| Leave-study-out (14/26 studies, n_test=406267) | 0.332 | 0.312 | 0.421 |
| Leave-tissue-out (7/17 tissues, n_test=111231) | 0.431 | 0.466 | 0.772 |

## Figure Regeneration

```bash
python regen_figures_300dpi.py
```

This regenerates the manuscript figures into `../manuscript/figures/`.

## Optional Morgan-Fingerprint Baseline

This comparator is included as a reproducibility scaffold for future work and was not used for the
reported benchmark results. It requires a drug-to-SMILES table.

```bash
python fetch_drug_smiles.py --drugcomb drugcomb_drugs.csv --out drug_smiles.csv
python fingerprint_baseline.py --smiles drug_smiles.csv --mode struct_ctx --regime standard
python fingerprint_baseline.py --smiles drug_smiles.csv --mode struct_ctx --regime colddrug
python fingerprint_baseline.py --smiles drug_smiles.csv --mode struct_ctx --regime coldcell
```

The script writes `fingerprint_<mode>_<regime>.json` files comparable with the identity-only metrics.
