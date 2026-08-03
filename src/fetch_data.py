"""
Reusable function to pull data from any OpenFEMA v2 API endpoint.

OpenFEMA caps each API response at 1000 records, so this function
automatically pages through results (using $skip) until everything
matching your filter has been downloaded.

Includes:
- A browser-like User-Agent header (some government APIs reject the
  default Python requests header)
- Automatic retries with backoff if FEMA's server is briefly overloaded
  (503 errors)
- A lightweight "get_count=False" mode for quick schema checks, which
  skips the expensive full-table count operation

Docs: https://www.fema.gov/about/openfema/api
"""

import time
import requests
import pandas as pd

BASE_URL = "https://www.fema.gov/api/open/v2"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "flood-cat-model-nfip-portfolio-project/1.0"
    )
}


def _get_with_retries(url, params, max_retries=4):
    """GET a URL with retries + exponential backoff for transient errors."""
    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.get(url, params=params, headers=HEADERS, timeout=60)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            last_error = e
            wait = 2 ** attempt  # 2s, 4s, 8s, 16s
            print(f"  Request failed ({e}). Retrying in {wait}s "
                  f"(attempt {attempt}/{max_retries})...")
            time.sleep(wait)
    raise last_error


def fetch_openfema(endpoint: str, filter_str: str = None, page_size: int = 1000,
                    get_count: bool = True) -> pd.DataFrame:
    """
    Download records from an OpenFEMA v2 endpoint.

    Parameters
    ----------
    endpoint : str
        e.g. "FimaNfipClaims", "FimaNfipPolicies", "DisasterDeclarationsSummaries"
    filter_str : str, optional
        An OData filter expression, e.g. "(state eq 'TX') and (countyCode eq '48201')"
    page_size : int
        Records per API call. OpenFEMA's max is 1000.
    get_count : bool
        If True (default), fetches the TOTAL matching record count first and
        pages through ALL of them. Use this for real data collection.
        If False, just grabs one page quickly with no count query - use this
        for fast schema checks, since counting an unfiltered multi-million
        row table is slow and can cause 503 errors.

    Returns
    -------
    pandas.DataFrame
    """
    url = f"{BASE_URL}/{endpoint}"

    if not get_count:
        params = {"$top": page_size}
        if filter_str:
            params["$filter"] = filter_str
        print(f"Requesting {endpoint} (quick sample, no count)...")
        payload = _get_with_retries(url, params)
        return pd.DataFrame(payload[endpoint])

    params = {"$top": page_size, "$inlinecount": "allpages"}
    if filter_str:
        params["$filter"] = filter_str

    print(f"Requesting {endpoint} ...")
    payload = _get_with_retries(url, params)

    total = payload["metadata"]["count"]
    records = payload[endpoint]
    print(f"  {total} total matching records. Fetched {len(records)} so far.")

    skip = page_size
    while skip < total:
        page_params = {"$top": page_size, "$skip": skip}
        if filter_str:
            page_params["$filter"] = filter_str
        payload = _get_with_retries(url, page_params)
        records.extend(payload[endpoint])
        print(f"  Fetched {len(records)}/{total}")
        skip += page_size
        time.sleep(0.3)  # be polite to FEMA's servers

    return pd.DataFrame(records)
