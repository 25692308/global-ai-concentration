## Section 4 - AI Concentration Analysis

### Research Question

Is AI development becoming concentrated in fewer countries?

### Overview

This section investigates geographic concentration across three dimensions of AI development:

- AI scholarly publications
- AI-related patents
- Private AI investment

The analysis covers 2016–2024 and uses the Herfindahl–Hirschman Index (HHI) and the combined share of the top three countries.

### Methodology

For each dataset and year, country shares are calculated using the total observed country-attributed values.

- **Country share:** Country value divided by the observed total.
- **HHI:** Sum of squared country shares. Higher values indicate greater concentration.
- **Top-3 share:** Combined share of the three countries with the largest recorded values.
- **Country coverage:** Number of countries with recorded observations, including recorded zeros.

A balanced-panel sensitivity analysis is also performed for investment data, retaining only countries observed in every year from 2016 to 2024.

Missing country-year observations are not automatically treated as zero.

### Implementation

- `pages/4_Concentration.py` — Interactive Streamlit visualisations, filters, interpretation and data audit.
- `src/concentration.py` — Data loading, validation and concentration calculations.
- `data/processed/concentration_metrics.csv` — Calculated concentration indicators.

### How to Run

From the repository root:

```bash
pip install -r requirements.txt
python src/concentration.py
streamlit run app.py
```

The calculation script expects the required source CSV files in `data/raw/`.

### Verification

HHI, Top-3 shares, observed country counts and totals were independently recalculated from country-level data and compared with the processed metrics.

The dashboard also provides a country-level audit table and downloadable CSV for inspecting individual calculations.

### Limitations

- Publications, patents and investments use different definitions and country-attribution methods.
- Observed country totals do not necessarily represent unique global totals.
- Changes in country coverage may influence concentration measures.
- The balanced-panel analysis checks sensitivity to coverage changes but does not guarantee complete global representation.
- Results should not be interpreted as a comprehensive measure of AI capability.