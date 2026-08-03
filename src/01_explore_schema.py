"""
STEP A of Phase 2 - run this FIRST.

Pulls a tiny sample (5 rows) from each dataset we need, with NO filter,
just so we can see the real column names before writing filtered queries.

Run:
    python src/01_explore_schema.py
"""

from fetch_data import fetch_openfema

datasets = ["FimaNfipClaims", "FimaNfipPolicies", "DisasterDeclarationsSummaries"]

for ds in datasets:
    print("=" * 70)
    print(ds)
    print("=" * 70)
    df = fetch_openfema(ds, filter_str=None, page_size=5, get_count=False)
    print("\nColumns:")
    print(list(df.columns))
    print("\nFirst row:")
    print(df.iloc[0])
    print("\n")
