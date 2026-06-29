"""Prepare DrugComb v1.5 tables for modeling.

This script streams the large DrugComb summary CSV, filters to true drug
combination rows, normalizes common missing-value tokens, and creates:

1. drugcomb_screen_summary_modeling.csv
   Clean combination-level table with response and synergy metrics.
2. drugcomb_synergy_prediction_modeling.csv
   Leaner prediction table with identifiers/categorical descriptors and synergy
   targets, avoiding response-derived metrics as input columns.
3. dataset_profile.txt
   Row counts, study/tissue frequencies, missingness, and checksum context.
"""

from __future__ import annotations

import csv
import hashlib
import math
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "summary_v_1_5.csv"
OUT_DIR = ROOT / "modeling"
SCREEN_OUT = OUT_DIR / "drugcomb_screen_summary_modeling.csv"
PRED_OUT = OUT_DIR / "drugcomb_synergy_prediction_modeling.csv"
PROFILE_OUT = OUT_DIR / "dataset_profile.txt"

MISSING = {"", "NA", "NULL", "\\N", "nan", "NaN", "None"}
NUMERIC_COLUMNS = [
    "ic50_row",
    "ic50_col",
    "ri_row",
    "ri_col",
    "css_row",
    "css_col",
    "css_ri",
    "S_sum",
    "S_mean",
    "S_max",
    "synergy_zip",
    "synergy_loewe",
    "synergy_hsa",
    "synergy_bliss",
    "drug_row_clinical_phase",
    "drug_col_clinical_phase",
]

SCREEN_COLUMNS = [
    "block_id",
    "study_name",
    "tissue_name",
    "cell_line_name",
    "drug_row",
    "drug_col",
    "conc_row_unit",
    "conc_col_unit",
    "ic50_row",
    "ic50_col",
    "ri_row",
    "ri_col",
    "css_row",
    "css_col",
    "css_ri",
    "S_sum",
    "S_mean",
    "S_max",
    "synergy_zip",
    "synergy_loewe",
    "synergy_hsa",
    "synergy_bliss",
    "drug_row_clinical_phase",
    "drug_col_clinical_phase",
    "drug_row_target_name",
    "drug_col_target_name",
    "zip_synergy_label",
    "loewe_synergy_label",
    "hsa_synergy_label",
    "bliss_synergy_label",
    "split",
]

PRED_COLUMNS = [
    "block_id",
    "study_name",
    "tissue_name",
    "cell_line_name",
    "drug_row",
    "drug_col",
    "drug_row_clinical_phase",
    "drug_col_clinical_phase",
    "drug_row_target_name",
    "drug_col_target_name",
    "synergy_zip",
    "synergy_loewe",
    "synergy_hsa",
    "synergy_bliss",
    "zip_synergy_label",
    "loewe_synergy_label",
    "hsa_synergy_label",
    "bliss_synergy_label",
    "split",
]


def clean(value: str | None) -> str:
    if value is None:
        return ""
    value = value.strip()
    return "" if value in MISSING else value


def clean_number(value: str | None) -> str:
    value = clean(value)
    if not value:
        return ""
    try:
        parsed = float(value)
    except ValueError:
        return ""
    if not math.isfinite(parsed):
        return ""
    return f"{parsed:.12g}"


def numeric_or_none(value: str) -> float | None:
    value = clean_number(value)
    if not value:
        return None
    return float(value)


def synergy_label(value: str) -> str:
    parsed = numeric_or_none(value)
    if parsed is None:
        return ""
    if parsed >= 10:
        return "synergistic"
    if parsed <= -10:
        return "antagonistic"
    return "additive"


def deterministic_split(row: dict[str, str]) -> str:
    key = "|".join(
        [
            clean(row.get("study_name")),
            clean(row.get("cell_line_name")),
            clean(row.get("drug_row")),
            clean(row.get("drug_col")),
        ]
    )
    bucket = int(hashlib.md5(key.encode("utf-8")).hexdigest()[:8], 16) % 100
    if bucket < 80:
        return "train"
    if bucket < 90:
        return "validation"
    return "test"


def is_combination(row: dict[str, str]) -> bool:
    return bool(clean(row.get("drug_row"))) and bool(clean(row.get("drug_col")))


def prepare() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    total_rows = 0
    combo_rows = 0
    written_rows = 0
    skipped_missing_zip = 0
    missing_counts: Counter[str] = Counter()
    study_counts: Counter[str] = Counter()
    tissue_counts: Counter[str] = Counter()
    split_counts: Counter[str] = Counter()
    label_counts: dict[str, Counter[str]] = defaultdict(Counter)

    with SOURCE.open("r", encoding="utf-8", newline="") as src, SCREEN_OUT.open(
        "w", encoding="utf-8", newline=""
    ) as screen_f, PRED_OUT.open("w", encoding="utf-8", newline="") as pred_f:
        reader = csv.DictReader(src)
        screen_writer = csv.DictWriter(screen_f, fieldnames=SCREEN_COLUMNS)
        pred_writer = csv.DictWriter(pred_f, fieldnames=PRED_COLUMNS)
        screen_writer.writeheader()
        pred_writer.writeheader()

        for row in reader:
            total_rows += 1
            if not is_combination(row):
                continue
            combo_rows += 1

            cleaned: dict[str, str] = {}
            for key in row:
                if key in NUMERIC_COLUMNS:
                    cleaned[key] = clean_number(row[key])
                else:
                    cleaned[key] = clean(row[key])

            if not cleaned.get("synergy_zip"):
                skipped_missing_zip += 1
                continue

            cleaned["zip_synergy_label"] = synergy_label(cleaned["synergy_zip"])
            cleaned["loewe_synergy_label"] = synergy_label(cleaned["synergy_loewe"])
            cleaned["hsa_synergy_label"] = synergy_label(cleaned["synergy_hsa"])
            cleaned["bliss_synergy_label"] = synergy_label(cleaned["synergy_bliss"])
            cleaned["split"] = deterministic_split(cleaned)

            screen_writer.writerow({col: cleaned.get(col, "") for col in SCREEN_COLUMNS})
            pred_writer.writerow({col: cleaned.get(col, "") for col in PRED_COLUMNS})

            written_rows += 1
            study_counts[cleaned.get("study_name", "Unknown") or "Unknown"] += 1
            tissue_counts[cleaned.get("tissue_name", "Unknown") or "Unknown"] += 1
            split_counts[cleaned["split"]] += 1
            for label_col in [
                "zip_synergy_label",
                "loewe_synergy_label",
                "hsa_synergy_label",
                "bliss_synergy_label",
            ]:
                label_counts[label_col][cleaned[label_col] or "missing"] += 1
            for col in SCREEN_COLUMNS:
                if not cleaned.get(col):
                    missing_counts[col] += 1

    lines = [
        "DrugComb v1.5 modeling dataset profile",
        "",
        f"source_file: {SOURCE}",
        f"screen_summary_file: {SCREEN_OUT}",
        f"synergy_prediction_file: {PRED_OUT}",
        "",
        f"raw_rows_scanned: {total_rows}",
        f"combination_rows: {combo_rows}",
        f"modeling_rows_written: {written_rows}",
        f"combination_rows_skipped_missing_synergy_zip: {skipped_missing_zip}",
        "",
        "split_counts:",
    ]
    lines.extend(f"  {key}: {split_counts[key]}" for key in ["train", "validation", "test"])
    lines.append("")
    lines.append("zip_synergy_label_counts:")
    lines.extend(f"  {key}: {value}" for key, value in label_counts["zip_synergy_label"].most_common())
    lines.append("")
    lines.append("top_studies:")
    lines.extend(f"  {key}: {value}" for key, value in study_counts.most_common(30))
    lines.append("")
    lines.append("top_tissues:")
    lines.extend(f"  {key}: {value}" for key, value in tissue_counts.most_common(30))
    lines.append("")
    lines.append("missing_counts_in_written_screen_table:")
    lines.extend(f"  {key}: {missing_counts[key]}" for key in SCREEN_COLUMNS if missing_counts[key])
    lines.append("")
    lines.append("notes:")
    lines.append("  synergy labels use common thresholds: >= 10 synergistic, <= -10 antagonistic, otherwise additive.")
    lines.append("  split is deterministic by study, cell line, and drug pair to reduce near-duplicate leakage.")
    lines.append("  prediction table excludes response-derived columns such as CSS, RI, S_* and IC50 from features.")

    PROFILE_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    prepare()
