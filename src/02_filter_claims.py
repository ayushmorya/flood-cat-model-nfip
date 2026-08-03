"""
STEP B of Phase 2 - run this AFTER you've manually downloaded the file below.

Manual download (do this in your browser first):
    https://www.fema.gov/about/reports-and-data/openfema/FimaNfipClaims.parquet

Save it into: data/raw/FimaNfipClaims.parquet

This script then loads that national file, filters it down to just our
study county, and saves a small, fast, ready-to-use CSV into data/processed/.

Run:
    python src/02_filter_claims.py
"""

import os
import pandas as pd

# ---- CONFIG: change these to study a different county ----
STATE = "TX"
COUNTY_FIPS = "48201"   # Harris County, TX (Houston)
OUTPUT_NAME = "nfip_claims_harris_tx.csv"
# ------------------------------------------------------------

RAW_PATH = "../data/raw/FimaNfipClaims.parquet"
OUT_PATH = f"../data/processed/{OUTPUT_NAME}"

print("Loading national claims file (this may take a minute)...")
df = pd.read_parquet(RAW_PATH)

print(f"\nLoaded {len(df):,} total rows nationwide.")
print("\nColumns available:")
print(list(df.columns))

# Try to find the right state/county columns automatically and show what we used
state_col = "state" if "state" in df.columns else None
county_col = "countyCode" if "countyCode" in df.columns else None

if state_col is None or county_col is None:
    print("\n[!] Could not find 'state' / 'countyCode' columns automatically.")
    print("    Please check the column list above and tell Claude the correct names.")
else:
    filtered = df[(df[state_col] == STATE) & (df[county_col] == COUNTY_FIPS)]
    print(f"\nFiltered to {STATE}, county FIPS {COUNTY_FIPS}: {len(filtered):,} rows")

    os.makedirs("../data/processed", exist_ok=True)
    filtered.to_csv(OUT_PATH, index=False)
    print(f"Saved to {OUT_PATH}")

    if "yearOfLoss" in filtered.columns:
        print("\nClaims by year:")
        print(filtered["yearOfLoss"].value_counts().sort_index())
