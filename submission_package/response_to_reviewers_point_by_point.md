# Point-by-Point Response to Reviewers

Manuscript title: **A Leakage-Controlled Cold-Start Benchmark for Drug-Combination Synergy Classification on DrugComb v1.5**

Journal: **BMC Bioinformatics**

Author: **Xulin Pan**

Dear Editor and Reviewers,

Thank you for the careful evaluation of our manuscript and for the constructive suggestions. We have revised the manuscript and the accompanying submission package to improve reproducibility, clarify the evaluation design, strengthen the evidence for study and tissue confounding, and align the submission more closely with BMC Bioinformatics reporting expectations. Below, we provide a point-by-point response. Reviewer comments are reproduced in bold, followed by our responses and the changes made.

## Summary of Major Revisions

1. We deposited the revised manuscript, derived modeling data package, preprocessing scripts, analysis code, metric outputs, and BMC submission materials in a public GitHub repository: https://github.com/xulinpan/bmc.
2. We revised the Availability of data and materials section to cite Zenodo record 15235991 as the source-data location and the GitHub repository as the public location for the derived data package, code, outputs, and submission materials. We removed dependence on the inaccessible DrugComb web portal and now cite only accessible Zenodo and GitHub links.
3. We added and reported robustness experiments: a no-study ablation, leave-study-out evaluation, and leave-tissue-out evaluation.
4. We clarified the split construction protocol, including the fixed random seed and the selection of held-out whole studies/tissues.
5. We softened claims about molecular structure features and Morgan fingerprints, treating them as future comparators rather than reported results.
6. We revised the manuscript into BMC style, including structured abstract labels, BMC-style sections, and complete declarations.
7. We updated funding to state: National Natural Science Foundation of China (grant No. 11461079).

## Reviewer Comment 1: Data and code availability does not meet BMC policy

**The manuscript should provide open access to the code, analysis scripts, derived data package, and metric outputs needed to reproduce the reported results. The availability statement should not rely on unavailable or "upon request" materials.**

**Response:** We agree. We have deposited the revised submission package in the public GitHub repository https://github.com/xulinpan/bmc. The repository includes the manuscript source and PDF, supplementary scripts, metric outputs, figure-generation scripts, robustness experiment outputs, and a compressed derived modeling data package with checksums. The original DrugComb v1.5 source summary file is cited via Zenodo record 15235991. We revised the Availability of data and materials section to avoid relying on the inaccessible portal and to point readers to the GitHub repository for the submitted data/code package.

**Changes made:**

- Revised the Availability of data and materials section in the manuscript.
- Updated the repository README, dataset README, dataset availability statement, cover letter, submission checklist, and submission guide.
- Refreshed the compressed dataset package and checksum sidecars.
- Verified that the PDF contains the GitHub URL and no longer cites the inaccessible DrugComb portal.

## Reviewer Comment 2: Study confounding should be tested directly

**The manuscript identifies study/platform effects as a possible confounder, but this concern should be evaluated rather than left only as a limitation. A no-study ablation and leave-study-out evaluation are recommended.**

**Response:** We agree. We added a no-study ablation and a leave-study-out evaluation. The no-study ablation showed essentially unchanged standard-split performance, indicating that the main standard-split result is not explained solely by the `study_name` feature. However, the leave-study-out evaluation showed a substantial performance collapse, supporting the manuscript's caution that cross-study transfer is much harder than random or grouped standard splitting suggests.

**Reported results:**

| Regime | Balanced accuracy | Macro-F1 | Macro-AUC |
|---|---:|---:|---:|
| Standard, with study | 0.807 | 0.708 | 0.923 |
| Standard, no study | 0.806 | 0.708 | 0.922 |
| Leave-study-out | 0.332 | 0.312 | 0.421 |

**Changes made:**

- Added the no-study and leave-study-out robustness results to the Results section.
- Added supplementary outputs: `nostudy.json`, `leavestudy.json`, and `review_experiments_summary.md`.
- Updated the Discussion to interpret the leave-study-out collapse as evidence of strong cross-study distribution shift.

## Reviewer Comment 3: Clarify the leave-study-out and leave-tissue-out protocols

**The manuscript should specify how held-out studies and tissues were selected and whether the resulting split sizes were affected by imbalance across studies and tissues.**

**Response:** We agree. The Methods section now states that whole studies and tissues were selected in a fixed random order using seed 42 until the held-out set reached approximately 15% of rows or more. Because DrugComb studies are highly imbalanced in size, the leave-study-out split held out 14 of 26 studies, including NCI-ALMANAC. The remaining rows were split into training and validation sets. We added the same clarification for leave-tissue-out evaluation.

**Changes made:**

- Clarified the split protocol in Methods.
- Added held-out study/tissue counts and test-set sizes in the Results and supplementary summary.
- Included the full split-generation code in `supplementary/experiments_review.py`.

## Reviewer Comment 4: Possible tissue leakage in leave-cell-line-out evaluation

**Leaving out cell lines does not necessarily leave out tissues. The manuscript should evaluate whether tissue-level overlap contributes to the cold-cell result.**

**Response:** We agree. We added a leave-tissue-out robustness experiment, which evaluates transfer to entirely held-out tissues. This is a stricter tissue-context transfer test than leave-cell-line-out alone. The leave-tissue-out evaluation produced balanced accuracy 0.431 and macro-F1 0.466, confirming that the loss of performance under unseen biological contexts is not limited to individual cell-line identity.

**Reported result:**

| Regime | Balanced accuracy | Macro-F1 | Macro-AUC |
|---|---:|---:|---:|
| Leave-tissue-out | 0.431 | 0.466 | 0.772 |

**Changes made:**

- Added the leave-tissue-out result to the Results section.
- Added the output file `leavetissue.json`.
- Expanded the Discussion to distinguish standard-split performance from transfer across unseen cellular/tissue contexts.

## Reviewer Comment 5: Avoid overclaiming Morgan-fingerprint or molecular-feature improvements

**The manuscript suggests that molecular features may close the cold-start gap, but no molecular baseline is reported. Claims about molecular features should be softened or supported by additional experiments.**

**Response:** We agree. We revised the manuscript to avoid claiming that molecular fingerprints or molecular/omics features solve the observed cold-start failures. The revised text frames Morgan fingerprints and related molecular representations as natural future comparators. We retained `fingerprint_baseline.py` as a supplementary scaffold for future extension but do not present it as a reported result.

**Changes made:**

- Softened molecular-feature claims in the Discussion and Conclusions.
- Clarified that the current benchmark is a leakage-controlled identity/context baseline rather than a molecular model.
- Kept the optional Morgan-fingerprint script in the supplementary package as a reproducibility scaffold only.

## Reviewer Comment 6: Baseline and hyperparameter transparency

**The manuscript should clarify how model settings were chosen and confirm that test data were not used for tuning.**

**Response:** We agree. We revised the Methods to clarify that model settings were fixed before test evaluation and that validation data, not test data, were used for model selection or early stopping. The supplementary package includes the training scripts and metric outputs used to reproduce the reported results.

**Changes made:**

- Clarified model-training and validation procedures in Methods.
- Included `train_lr.py`, `train_gbm.py`, `analysis.py`, and related JSON outputs in the supplementary package.
- Reiterated that all experiments used fixed random seed 42.

## Reviewer Comment 7: Drug-pair symmetry should be acknowledged

**Drug A/B ordering may introduce avoidable variation. Order-invariant encoding or swapped-pair augmentation should be considered.**

**Response:** We agree. We have not added new swapped-pair experiments in this revision, so we do not claim that this issue has been resolved. Instead, we explicitly identify order-invariant pair encoding and swapped-pair augmentation as immediate future robustness checks. This keeps the limitation transparent and avoids unsupported claims.

**Changes made:**

- Added/retained drug-pair symmetry as a limitation and future robustness check.
- Avoided presenting unperformed swapped-pair experiments as evidence.

## Reviewer Comment 8: BMC Bioinformatics style and reporting requirements

**The manuscript should follow BMC Bioinformatics style, including a structured abstract, standard sections, declarations, abbreviations, funding, and availability statement.**

**Response:** We agree. We revised the manuscript to use BMC-style structure and declarations. The abstract now uses Background, Results, and Conclusions labels. The main text follows Background, Methods, Results, Discussion, and Conclusions. Declarations now include Abbreviations, Ethics approval and consent to participate, Consent for publication, Availability of data and materials, Competing interests, Funding, Authors' contributions, and Acknowledgements.

**Changes made:**

- Revised abstract and section structure.
- Added BMC-style declarations.
- Added funding statement: National Natural Science Foundation of China (grant No. 11461079).
- Updated reference style and added recent references relevant to drug-combination synergy prediction.

## Reviewer Comment 9: Availability of the DrugComb portal

**The DrugComb portal may be inaccessible, so the availability statement should not depend on it.**

**Response:** We agree. We revised the Availability of data and materials statement to cite Zenodo record 15235991 as the source-data location and the GitHub repository https://github.com/xulinpan/bmc as the public location for the derived data package, preprocessing code, analysis code, metric outputs, and submission materials. We removed the inaccessible portal link from the manuscript availability statement and package documentation.

**Changes made:**

- Removed the inaccessible portal link from the availability statement and package documentation.
- Added the GitHub repository URL to the manuscript, cover letter, dataset package documentation, submission checklist, and repository README.
- Verified that the rebuilt PDF text contains the GitHub URL.

## Closing Statement

We believe these revisions substantially strengthen the manuscript's reproducibility, clarify the interpretation of cold-start performance, and better align the submission with BMC Bioinformatics expectations. We thank the reviewers again for their constructive comments.
