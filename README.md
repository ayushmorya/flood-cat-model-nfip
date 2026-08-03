# Residential Flood Loss Model — NFIP Portfolio Analysis

A simplified catastrophe (cat) model for residential flood risk, built on real
U.S. National Flood Insurance Program (NFIP) claims and policy data.

This project reconstructs the four core modules of a real catastrophe model —
**Hazard, Exposure, Vulnerability, and Financial** — and produces the
industry-standard outputs analysts use every day: **AAL (Average Annual
Loss)**, an **EP (Exceedance Probability) curve**, and **PML (Probable
Maximum Loss)** at key return periods.

> Status: 🚧 In progress — built step by step, phase by phase. See roadmap below.

---

## Why this project

Off-the-shelf vendor cat models (RMS, Verisk/AIR, CoreLogic) require paid
licenses. This project shows the same conceptual workflow using 100% public,
free data — proving hands-on understanding of how a cat model is actually
built, not just how to describe one.

## Data sources

| Dataset | Source | Used for |
|---|---|---|
| FIMA NFIP Redacted Claims (v2) | OpenFEMA (bulk Parquet download) | Hazard, Vulnerability, and Financial modules — this single dataset includes building value, coverage, deductible, damage amount, flood zone, and cause of loss per claim |

Study area: **Harris County, Texas** (FIPS 48201) — chosen for its long, dense flood claim history (1978-present, 170,803 claims), including Hurricane Harvey (2017).

> Note: an earlier plan also used the separate NFIP Policies dataset for
> exposure. It was dropped in favor of using the Claims dataset's own
> building value/coverage fields — a simplification known in the industry
> as burn-cost / historical loss analysis. This also avoided downloading
> an 80-million-row national file for a single-county study.

## Project roadmap

- [x] **Phase 1** — Environment & repo setup
- [x] **Phase 2** — Data collection (NFIP claims, Harris County TX, 1978-present)
- [ ] **Phase 3** — Data cleaning & exploratory analysis
- [ ] **Phase 4** — Hazard module (empirical return periods)
- [ ] **Phase 5** — Vulnerability module (damage ratios by flood zone)
- [ ] **Phase 6** — Financial module (deductibles, limits, payouts)
- [ ] **Phase 7** — AAL / EP curve / PML calculation
- [ ] **Phase 8** — Model validation & backtesting
- [ ] **Phase 9** — Packaging, visuals, and (optional) Streamlit app

## Repository structure

```
flood-cat-model-nfip/
 ├── data/
 │   ├── raw/          # downloaded NFIP/NOAA files (not pushed to GitHub - large)
 │   └── processed/    # cleaned, merged datasets used by notebooks
 ├── notebooks/         # one notebook per phase, in order
 ├── src/                # reusable Python functions
 ├── outputs/figures/   # saved charts (EP curve, damage curves, etc.)
 └── requirements.txt
```

## How to run this project

```bash
git clone <your-repo-url>
cd flood-cat-model-nfip
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook
```

## Key results

*(To be filled in after Phase 7 — AAL, EP curve chart, PML at 20/50/100-year
return periods will go here.)*

## Methodology & limitations

*(To be filled in after Phase 8 — this section is what interviewers read
most closely. Be explicit about simplifications: this model uses empirical
historical resampling rather than a physically modeled hazard grid; a
production-grade model would use flood depth rasters and engineering-based
depth-damage curves.)*

## Author

*(Your name, LinkedIn, and a one-line note that this is a self-directed
learning project built to demonstrate cat modeling fundamentals.)*
