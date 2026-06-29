# BMC Bioinformatics Submission Package

This repository contains the BMC Bioinformatics submission materials for:

**A Leakage-Controlled Cold-Start Benchmark for Drug-Combination Synergy Classification on DrugComb v1.5**

Author: Xulin Pan

## Repository Contents

- `submission_package/`
  - BMC Bioinformatics manuscript source, compiled PDF, figures, supplementary scripts, review-response material, cover letter and submission checklist.
- `dataset_package/`
  - Compressed derived modeling dataset archive: `BMC_Bioinformatics_dataset_PanXulin.zip`
  - Checksum sidecars: `.sha256` and `.md5`
  - Dataset README, data dictionary, dataset profile and preprocessing script.

## Data Note

The uncompressed derived modeling table is approximately 912 MB and is stored inside the compressed dataset archive. The original DrugComb v1.5 source file is not redistributed here; it is publicly available from the DrugComb portal and Zenodo record 15235991.

## Integrity

Verify the dataset archive before use:

```powershell
Get-FileHash .\dataset_package\BMC_Bioinformatics_dataset_PanXulin.zip -Algorithm SHA256
Get-Content .\dataset_package\BMC_Bioinformatics_dataset_PanXulin.zip.sha256
```

The archive was checked locally with Python `zipfile.ZipFile.testzip()` before repository staging.
