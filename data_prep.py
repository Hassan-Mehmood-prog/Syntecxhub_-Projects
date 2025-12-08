#!/usr/bin/env python3
"""
data_prep.py

Read CSV(s), clean/normalize data, parse dates, handle missing values,
rename columns, and export to .xlsx using pandas + openpyxl.

Usage examples:
  python data_prep.py --input data.csv --output out.xlsx
  python data_prep.py -i data1.csv data2.csv -o results.xlsx --date-cols date,created_at --fillna 0
  python data_prep.py -i data.csv -o out.xlsx --rename "Old Name:old_name,Price:price" --dropna-any

Author: You
"""

import argparse
import logging
from pathlib import Path
import sys
from typing import List, Dict, Optional

import pandas as pd

# --------- Logging setup ----------
logger = logging.getLogger("data_prep")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
logger.addHandler(handler)


# --------- Helpers ----------
def normalize_col_name(name: str) -> str:
    """Normalize column name: strip, lower, replace spaces and special chars with underscore."""
    name = str(name).strip()
    # replace spaces and many punctuation with underscore
    name = (
        name.replace(" ", "_")
        .replace("-", "_")
        .replace("/", "_")
        .replace("\\", "_")
        .replace(".", "_")
    )
    # collapse multiple underscores
    while "__" in name:
        name = name.replace("__", "_")
    return name.lower()


def parse_rename_arg(arg: Optional[str]) -> Dict[str, str]:
    """
    Parse rename argument like: "Old Col:old_col,Price:price"
    Returns mapping {old_normalized: new_name}
    """
    if not arg:
        return {}
    mapping = {}
    pairs = [p.strip() for p in arg.split(",") if p.strip()]
    for pair in pairs:
        if ":" not in pair:
            logger.warning("Ignoring invalid rename pair: %s (expected OLD:NEW)", pair)
            continue
        old, new = pair.split(":", 1)
        mapping[normalize_col_name(old)] = new.strip()
    return mapping


def auto_detect_date_cols(df: pd.DataFrame) -> List[str]:
    """Return list of candidate columns likely to be dates (contain 'date' or 'time' in name)."""
    candidates = []
    for c in df.columns:
        if "date" in c.lower() or "time" in c.lower() or "created" in c.lower() or "updated" in c.lower():
            candidates.append(c)
    return candidates


def try_parse_dates(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
    """
    Convert listed columns to datetime if possible; errors -> NaT, logged.
    Use pandas.to_datetime with dayfirst=False by default; you can change if needed.
    """
    for c in cols:
        if c not in df.columns:
            logger.warning("Date column '%s' not found in DataFrame columns.", c)
            continue
        try:
            df[c] = pd.to_datetime(df[c], errors="coerce", infer_datetime_format=True)
            logger.info("Parsed dates in column: %s", c)
        except Exception as e:
            logger.warning("Failed to parse dates in column %s: %s", c, e)
    return df


def load_and_concat(files: List[Path]) -> pd.DataFrame:
    """Load CSV files and concatenate into one DataFrame."""
    dfs = []
    for f in files:
        try:
            logger.info("Reading CSV: %s", f)
            df = pd.read_csv(f)
            dfs.append(df)
        except Exception as e:
            logger.error("Failed to read %s: %s", f, e)
            raise
    if not dfs:
        raise ValueError("No dataframes loaded from the provided files.")
    if len(dfs) == 1:
        return dfs[0]
    logger.info("Concatenating %d files", len(dfs))
    return pd.concat(dfs, ignore_index=True)


# --------- Main processing logic ----------
def process_dataframe(
    df: pd.DataFrame,
    date_cols: List[str],
    rename_map: Dict[str, str],
    fillna_value: Optional[str],
    dropna_any: bool,
    dropna_thresh: Optional[int],
    strip_strings: bool = True,
) -> pd.DataFrame:
    # 1. Normalize column names (but keep original mapping for renaming)
    orig_cols = list(df.columns)
    normalized_map = {c: normalize_col_name(c) for c in orig_cols}
    df = df.rename(columns=normalized_map)
    logger.info("Normalized column names.")

    # 2. Apply rename map (rename_map keys are expected normalized)
    if rename_map:
        # only apply renames for columns that exist
        applicable = {k: v for k, v in rename_map.items() if k in df.columns}
        if applicable:
            df = df.rename(columns=applicable)
            logger.info("Applied %d column renames.", len(applicable))
        else:
            logger.warning("No rename mappings matched existing columns.")

    # 3. Trim whitespace for object/string columns
    if strip_strings:
        obj_cols = df.select_dtypes(include=["object"]).columns
        if len(obj_cols) > 0:
            df[obj_cols] = df[obj_cols].apply(lambda s: s.str.strip())
            logger.info("Stripped whitespace from %d string columns.", len(obj_cols))

    # 4. Parse date columns
    if date_cols:
        # first try exact names (normalized), then try auto-detect if 'auto' flag used
        df = try_parse_dates(df, date_cols)

    # 5. Handle missing values
    # - drop rows where all values NaN
    before = len(df)
    df = df.dropna(how="all")
    after = len(df)
    if after < before:
        logger.info("Dropped %d rows that were entirely empty.", before - after)

    if dropna_any:
        before = len(df)
        df = df.dropna(how="any")
        logger.info("Dropped %d rows with any missing values.", before - len(df))

    if dropna_thresh:
        # keep rows with at least 'thresh' non-null values; thresh is an int
        before = len(df)
        df = df.dropna(thresh=dropna_thresh)
        logger.info("Dropped %d rows with less than %d non-null values.", before - len(df), dropna_thresh)

    if fillna_value is not None:
        df = df.fillna(fillna_value)
        logger.info("Filled remaining missing values with: %s", str(fillna_value))

    return df


def export_to_excel(df: pd.DataFrame, output_path: Path):
    try:
        logger.info("Exporting to Excel: %s", output_path)
        # openpyxl engine used automatically by pandas when file ends with .xlsx
        df.to_excel(output_path, index=False)
        logger.info("Export successful.")
    except Exception as e:
        logger.error("Failed to export Excel file: %s", e)
        raise


# --------- CLI ----------
def parse_args():
    p = argparse.ArgumentParser(description="CSV -> cleaned .xlsx exporter")
    p.add_argument(
        "-i",
        "--input",
        required=True,
        nargs="+",
        help="Input CSV file(s). You can pass multiple files (space separated).",
    )
    p.add_argument("-o", "--output", required=True, help="Output .xlsx path (e.g. cleaned.xlsx)")
    p.add_argument(
        "--date-cols",
        help="Comma-separated list of date columns to parse (names should match CSV headers). "
        "Example: created_at,date\n"
        "If omitted, columns with 'date'/'time' in name are auto-detected and parsed.",
    )
    p.add_argument(
        "--rename",
        help='Rename columns mapping like "Old Col:old_col,Price:price". Left side is original header (any case), right side is new column name.',
    )
    p.add_argument("--fillna", help="Fill missing values with this value (applies to all columns).")
    p.add_argument("--dropna-any", action="store_true", help="Drop rows with ANY missing value.")
    p.add_argument(
        "--dropna-thresh",
        type=int,
        help="Drop rows that have fewer than this many non-null values (int).",
    )
    p.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose logging (DEBUG).",
    )
    return p.parse_args()


def main():
    args = parse_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)

    input_files = [Path(p) for p in args.input]
    for f in input_files:
        if not f.exists():
            logger.error("Input file does not exist: %s", f)
            sys.exit(2)

    output_path = Path(args.output)
    if output_path.suffix.lower() != ".xlsx":
        logger.error("Output file must have .xlsx extension.")
        sys.exit(2)

    # parse rename mapping and date columns
    rename_map = parse_rename_arg(args.rename)
    date_cols_flag = []
    if args.date_cols:
        # split by comma and normalize
        date_cols_flag = [c.strip() for c in args.date_cols.split(",") if c.strip()]

    # 1. Load CSV(s)
    try:
        df = load_and_concat(input_files)
    except Exception as e:
        logger.error("Could not load input CSV(s): %s", e)
        sys.exit(3)

    # If no date_cols provided, auto detect by name
    if not date_cols_flag:
        auto = auto_detect_date_cols(df)
        if auto:
            date_cols_flag = auto
            logger.info("Auto-detected date columns: %s", ", ".join(auto))
        else:
            logger.info("No date columns provided or auto-detected.")

    # Normalize rename_map keys: user passed original names; normalize for matching
    rename_map_normalized = {normalize_col_name(k): v for k, v in rename_map.items()}

    # Process the dataframe
    try:
        processed = process_dataframe(
            df,
            date_cols=[normalize_col_name(c) for c in date_cols_flag],
            rename_map=rename_map_normalized,
            fillna_value=args.fillna,
            dropna_any=args.dropna_any,
            dropna_thresh=args.dropna_thresh,
        )
    except Exception as e:
        logger.error("Processing failed: %s", e)
        sys.exit(4)

    # Export to excel
    try:
        export_to_excel(processed, output_path)
    except Exception as e:
        logger.error("Export failed: %s", e)
        sys.exit(5)

    logger.info("All done. Output: %s", output_path)


if __name__ == "__main__":
    main()
