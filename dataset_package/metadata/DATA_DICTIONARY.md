# Data Dictionary

File: `data/drugcomb_synergy_prediction_modeling.csv`

Rows: `739,964`

## Identifier and Context Columns

- `block_id`: DrugComb experiment/block identifier.
- `study_name`: Source study or screening campaign.
- `tissue_name`: Tissue or disease-context label associated with the cell line.
- `cell_line_name`: Cell line used in the drug-combination experiment.
- `drug_row`: First drug in the DrugComb pair orientation.
- `drug_col`: Second drug in the DrugComb pair orientation.

## Drug Annotation Columns

- `drug_row_clinical_phase`: Clinical-development phase for `drug_row`; numeric DrugComb annotation.
- `drug_col_clinical_phase`: Clinical-development phase for `drug_col`; numeric DrugComb annotation.
- `drug_row_target_name`: Semicolon-separated target names for `drug_row`; blank if unavailable.
- `drug_col_target_name`: Semicolon-separated target names for `drug_col`; blank if unavailable.

## Synergy Score Columns

- `synergy_zip`: ZIP synergy score. This is the primary regression target in the manuscript.
- `synergy_loewe`: Loewe synergy score.
- `synergy_hsa`: Highest Single Agent synergy score.
- `synergy_bliss`: Bliss independence synergy score.

## Synergy Label Columns

Each label is derived independently from the corresponding synergy score:

- `zip_synergy_label`
- `loewe_synergy_label`
- `hsa_synergy_label`
- `bliss_synergy_label`

Label thresholds:

- `synergistic`: score >= 10
- `antagonistic`: score <= -10
- `additive`: otherwise

The manuscript's classification target is `zip_synergy_label`.

## Split Column

- `split`: Predefined grouped split with values `train`, `validation` and `test`.

The split is deterministic by study, cell line and drug pair, intended to reduce near-duplicate
pair-context leakage between partitions. Cold-start splits in the manuscript are generated from this
table by holding out drugs, cell lines, studies or tissues.

## Notes for Reuse

For leakage-controlled pre-treatment prediction, use only columns available before a combination assay:
drug identity, cell-line/tissue/study context, clinical phase and target annotations. Do not use any
synergy-score or synergy-label columns as model inputs.
