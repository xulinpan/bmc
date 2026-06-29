"""Create the BMC Bioinformatics data-availability package.

Run from the repository root or from this folder:

    python make_dataset_package.py

The archive includes the derived modeling CSV plus metadata and the derivation script.
"""

from __future__ import annotations

import zipfile
from pathlib import Path


THIS_DIR = Path(__file__).resolve().parent
MODELING_DIR = THIS_DIR.parent
DRUGCOMB_DIR = MODELING_DIR.parent
OUT_ZIP = MODELING_DIR / "BMC_Bioinformatics_dataset_PanXulin.zip"

FILES = [
    (THIS_DIR / "README.md", "README.md"),
    (THIS_DIR / "DATA_AVAILABILITY_STATEMENT.txt", "DATA_AVAILABILITY_STATEMENT.txt"),
    (THIS_DIR / "metadata" / "DATA_DICTIONARY.md", "metadata/DATA_DICTIONARY.md"),
    (THIS_DIR / "metadata" / "dataset_profile.txt", "metadata/dataset_profile.txt"),
    (THIS_DIR / "metadata" / "checksums.tsv", "metadata/checksums.tsv"),
    (THIS_DIR / "scripts" / "prepare_modeling_dataset.py", "scripts/prepare_modeling_dataset.py"),
    (THIS_DIR / "make_dataset_package.py", "scripts/make_dataset_package.py"),
    (MODELING_DIR / "drugcomb_synergy_prediction_modeling.csv", "data/drugcomb_synergy_prediction_modeling.csv"),
]


def main() -> None:
    missing = [str(path) for path, _ in FILES if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing required files:\n" + "\n".join(missing))

    with zipfile.ZipFile(OUT_ZIP, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for src, arcname in FILES:
            print(f"adding {arcname}")
            zf.write(src, arcname)

    with zipfile.ZipFile(OUT_ZIP) as zf:
        bad = zf.testzip()
    if bad is not None:
        raise RuntimeError(f"Zip integrity check failed at {bad}")

    print(f"created {OUT_ZIP}")


if __name__ == "__main__":
    main()
