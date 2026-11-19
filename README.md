## Section 3 - Private AI Investment

**Contributor:** Shubham Doshi

### Research Question

**Group question:** Is AI development becoming concentrated in fewer countries?

**Investment focus:** Is funding received by privately held AI companies becoming concentrated in fewer countries?

### Overview

This section explores the geographic distribution of recorded AI investment using:

- Country rankings by funding amount or share.
- Funding comparisons between selected countries over time.
- The combined share received by the top five countries.

The analysis covers **2016–2025**. All funding amounts use **constant 2021 US dollars**.

**Source:** [Our World in Data — CSET-based investment series](https://ourworldindata.org/grapher/private-investment-in-artificial-intelligence-cset).

The frozen snapshot was downloaded on **20 October 2026**. Its metadata records a source update date of **27 April 2026**.

### Methodology

- Exclude regional and World aggregates from country calculations.
- Calculate country shares using the sum of funding across the selected coverage group.
- Calculate shares before applying country display filters.
- Re-rank countries each year when calculating the top-five share.
- Compare all available countries with a fixed panel of 55 countries observed throughout 2016–2025.
- Retain explicit source zeros and leave missing country-years unavailable.
- Convert source dollars into billions by dividing by 1,000,000,000.

The cleaned dataset contains **837 observations across 119 distinct countries or territories** over the period. Country coverage varies between years.

### Findings

Using all available countries, the top-five share increased from
**82.1% in 2016 to 85.0% in 2025**, an increase of **2.9 percentage points**.

The United States' share increased from **51.3% to 70.1%**.

These results show greater endpoint dominance within recorded funding.
The annual trend fluctuates, and the results do not establish that fewer
countries receive funding.

### Design Decisions

Sorted horizontal bars support country comparisons on a common baseline.
A pie chart was rejected because small slices are harder to compare precisely.

Line charts show changes over time. A bump chart was rejected for funding
shares because rankings can remain unchanged while shares change substantially.

A table provides selected-country trend values without requiring hovering.

### Implementation

- `pages/investments.py` — Dashboard, charts, controls and source verification.
- `src/investments.py` — Data loading, validation and calculations.
- `scripts/prepare_investment_data.py` — Reproducible data preparation.
- `data/processed/ai_investment_country_year_2016_2025.csv` — Cleaned country-year observations.
- `data/processed/coverage_by_year.csv` — Annual coverage and total reconciliation.

The original OWID CSV and companion metadata are preserved in `data/raw/`.

[Full data dictionary, provenance, licences and transformations](docs/investment_data_notes.md).

### How to Run

From the repository root:

```bash
python -m pip install -r requirements.txt
python scripts/prepare_investment_data.py
python -m streamlit run app.py
```

Open the Investments section from the app navigation.

### Verification

Automated checks regenerated both processed CSVs byte-for-byte and matched
all 837 cleaned observations to their original records and unit conversions.

The dashboard's **Verify a number** tab reads the original CSV.

For example, United States, 2025 appears in raw CSV row **855**:

```text
301,022,702,852 / 1,000,000,000 = 301.022702852 billion
Rounded dashboard display = $301.02bn
```

Local checks covered filters and an empty country selection. Deployed checks
confirmed chart loading, year selection, fixed-country coverage, funding-amount
mode and the US 2016 source-verification view.

### Limitations

- Country coverage changes over time and may omit deals or geographies.
- Some transaction amounts are estimated, and recent years may have reporting lags.
- The fixed-country panel checks observation coverage, not reporting completeness.
- Country attribution follows recipient-company headquarters, not investor nationality.
- The series measures external equity funding into privately held AI companies, rather than all AI spending or national AI capability.

### Data and AI Disclosure

ChatGPT assisted with data preparation code, dashboard development, chart
design, testing and documentation. Checks included comparisons with original
CSV records, unit conversions, processed-file regeneration and dashboard testing.

[Detailed AI provenance matrix and verification outcomes](docs/investment_ai_provenance.md).

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
