"""
data_cleaning.py
Loads Supermarket-data.csv, performs cleaning checks, and saves a clean copy.
"""

import pandas as pd
import numpy as np
import os

RAW_PATH = "Supermarket-data.csv"
CLEAN_PATH = "data/supermarket_clean.csv"


def load_and_clean(raw_path: str = RAW_PATH, clean_path: str = CLEAN_PATH) -> pd.DataFrame:
    # ── 1. Load ──────────────────────────────────────────────────────────────
    df = pd.read_csv(raw_path)
    print(f"Loaded {len(df):,} rows × {len(df.columns)} columns")

    # ── 2. Inspect missing values ─────────────────────────────────────────
    missing = df.isnull().sum()
    if missing.any():
        print("\nMissing values detected:")
        print(missing[missing > 0])
        df.dropna(inplace=True)
        print(f"Rows after dropping NaNs: {len(df):,}")
    else:
        print("[OK] No missing values")

    # ── 3. Remove duplicates ─────────────────────────────────────────────
    dupes = df.duplicated().sum()
    if dupes:
        print(f"Removing {dupes} duplicate rows")
        df.drop_duplicates(inplace=True)
    else:
        print("[OK] No duplicate rows")

    # ── 4. Data types ────────────────────────────────────────────────────
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df.dropna(subset=["Date"], inplace=True)

    numeric_cols = ["Quantity", "Unit Price", "Rating", "Sales"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df.dropna(subset=numeric_cols, inplace=True)

    # ── 5. Validate / recalculate Sales ──────────────────────────────────
    df["Calculated_Sales"] = df["Quantity"] * df["Unit Price"]
    mismatch = (df["Sales"].round(2) != df["Calculated_Sales"].round(2)).sum()
    if mismatch:
        print(f"[WARN] {mismatch} rows where Sales != Qty x Unit Price - recalculating")
        df["Sales"] = df["Calculated_Sales"]
    else:
        print("[OK] Sales column matches Quantity x Unit Price")
    df.drop(columns=["Calculated_Sales"], inplace=True)

    # ── 6. Derived columns ───────────────────────────────────────────────
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    df["Month_Name"] = df["Date"].dt.strftime("%b %Y")
    df["DayOfWeek"] = df["Date"].dt.day_name()

    # ── 7. Save clean copy ───────────────────────────────────────────────
    os.makedirs(os.path.dirname(clean_path), exist_ok=True)
    df.to_csv(clean_path, index=False)
    print(f"\n[OK] Clean dataset saved -> {clean_path}  ({len(df):,} rows)")
    return df


if __name__ == "__main__":
    df = load_and_clean()
    print("\n--- Sample ---")
    print(df.head(3).to_string())
    print("\n--- dtypes ---")
    print(df.dtypes)
