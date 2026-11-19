# The Rise of Artificial Intelligence — Geographic Concentration

**UTS 36104 · Assignment 3 Part 2 · Group 15**  
**Status:** Shared draft on `docs`; all `TODO` entries must be completed before assessment.

## Research question and audience

**Question:** Is AI development becoming concentrated in fewer countries?

**Persona / decision — TODO (team):** [Name a specific audience and what this app helps them understand or decide.]

**User stories — TODO (team):** Confirm each can be completed in the deployed app.
1. As a [persona], I want [task], so that [purpose]. **App path:** [page/filter/chart].
2. As a [persona], I want [task], so that [purpose]. **App path:** [page/filter/chart].
3. As a [persona], I want [task], so that [purpose]. **App path:** [page/filter/chart].

**App URL — TODO:** [Deployed Streamlit URL]  
**Repository URL — TODO:** https://github.com/25692308/global-ai-concentration  
**Final assessed commit/tag — TODO:** [Use the team-approved version; include it in the Canvas PDF]

## Student sections

- Section 1 : Hoa Nhung Dao (25979079)
- Section 2 : Phenphan Viriyathamakul (26506028)
- Section 3 : Shubham Doshi (25683145)
- Section 4 : Myeongjin Han (25692308)

### Section 1 — AI Publications

- **Question**  Is AI research output becoming concentrated in a small number of countries?
- **Method:** 
**Source URL:** https://ourworldindata.org/grapher/annual-scholarly-publications-on-artificial-intelligence.csv?v=1&csvType=full&useColumnShortNames=true

**Dataset:** Annual Scholarly Publications on Artificial Intelligence (2024 edition)

**Publisher:** Our World in Data

**Licence:** CC BY 4.0

**Measures:** Total AI publications, active countries, Top-5 publication share, concentration change, publication share by country, publication growth, and a Growth + Scale Score for emerging research hubs. Visualisations include KPI cards, a Treemap, a 100% Stacked Area Chart, a Multi-Line Chart, and a Horizontal Bar Chart. A year-range filter controls all metrics and visualisations. The Top-5 publishing countries are identified using publication counts in the selected end year.

- **Finding:** AI research output remains highly concentrated among a relatively small number of countries despite publication activity being recorded across nearly 190 countries in the dataset. Across different year selections, the five largest publishing countries consistently account for a substantial share of global AI publications, and the concentration analysis generally shows an increasing share held by leading countries over time.

For example, when the period 2019–2024 is selected, the dashboard shows 2,009,712 publications across 187 active countries, while the five largest publishing countries account for 55.4% of publications during the selected period. In 2024 alone, the top five countries contribute 58.54% of global AI publications, with China accounting for 27.53%, India 12.31%, and the United States 12.01% of worldwide AI publications.

However, the Fastest Growing AI Research Countries analysis indicates that several countries outside today's leading publishing nations are recording strong publication growth. This suggests that while AI research output is becoming increasingly concentrated among current leaders, new AI research hubs continue to emerge and expand their presence in the global research landscape.

- **Limitations:** Publication counts measure research output rather than research quality, impact, or commercial adoption. The dataset may underrepresent research published exclusively in non-English languages, and coverage of some Chinese journals is incomplete. Multi-country publications may be attributed to multiple countries through author affiliations. Publication counts alone do not capture all dimensions of national AI capability.

- **Files:** 
\pages/1_Publications.py\ — Dashboard layout, KPI cards, filters, visualisations, and source verification interface.
\src/publications.py\ — Data loading, cleaning, KPI calculations, publication-share calculations, concentration metrics, trend analysis, and Growth + Scale scoring.
\data/raw/publications.csv\ — Original Annual Scholarly Publications on Artificial Intelligence dataset downloaded from Our World in Data.
\data/processed/publications.csv\ — Processed country-year publication dataset used by the dashboard.

- **Validation:** Publication-share values displayed in the Treemap were independently recalculated using:

Country Publications ÷ Global Publications × 100

and matched the dashboard output. For the 2019–2024 selection, the dashboard reported 2,009,712 Global AI Publications, 187 Active Countries, 55.4% Top-5 Share, and +5.6 percentage-point Concentration Change. The Concentration Over Time chart was verified by recalculating annual publication shares for the five largest publishing countries and confirming that the 2024 combined Top-5 share was 58.54%, while all remaining countries accounted for 41.46%. Country-level publication shares were also checked against source records, including China (27.53%), India (12.31%), and the United States (12.01%) in 2024.

Publication Trends were spot-checked against selected country-year records from the source dataset. Year-range filtering was tested across all KPI cards and all four dashboard sections to confirm that metrics, charts, and derived calculations updated consistently. Dashboard outputs matched the underlying source dataset and transformation logic for all tested cases.

### Section 2 — AI Patents

- **Question / method:** Which countries lead AI patenting, and how has their share of world AI patents changed from 2010 to 2024? Data: OECD AI patent indicators (PCT-based, by priority year), 2010–2024 on the page. Measures: patent counts, country share of the world total (`ALL`), and rank among five countries. The five countries are the highest 2024 counts after excluding aggregate rows (`ALL`, `OECD`, `EU27`). Charts: metric tiles (2024 counts and change since 2010), a line chart of annual counts, a stacked area chart of shares, a rank table with a year slider, and a share table with CSV download. Filter: country multiselect.
- **Finding / limitations:** From 2010 to 2024, the United States' share fell from 30.9% to 28.9%, while China's rose from 4.9% to 27.3%. Japan's fell from 31.4% to 10.7%, and Korea's rose from 4.1% to 10.7%. China ranked first in 2020 and 2021. The United States ranked first in 2011, 2013–2019, and 2022–2024. Japan ranked first in 2010 and 2012. Limitations: patents measure filed inventions, not research quality or commercial value; patent rules differ between offices; recent years may be estimates; rankings compare only the five countries shown; the source includes territories; and the page covers 2010–2024, whereas Section 4 covers 2016–2024.
- **Files and validation:** `pages/2_Patents.py`; `src/patents.py` (`render_patent_view`); source `Evolution_of_AI-related_patents_by_country.csv`; processed output `data/processed/processed.csv`. Checks completed: shares for 2010 and 2024 were recalculated from the source and match the page; ranks were spot-checked for 2010, 2014, 2020, 2021, and 2022; aggregate rows were excluded.
  
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

### Section 4 — Geographic Concentration

- **Question / method:** Compare the geographic concentration of the country-attributed publications, patents and private-investment inputs shared with Students 1–3, using **2016–2024** as the common period. For each domain/year, compute a country's share of observed values, **HHI = sum of squared shares (0–1)** and **Top-3 share = sum of the three largest shares (0–1)**. Report observed-country counts; do not treat missing country-years as zero. Compare observed-investment HHI against a **55-country balanced panel** (countries recorded in all nine years). Deviation = observed HHI − balanced-panel HHI.
- **Finding:** HHI changed from **0.071 to 0.112** (publications), **0.203 to 0.188** (patents), and **0.295 to 0.458** (investment) between 2016 and 2024 (rounded). These endpoint changes show **no uniform increase across all three domains**; investment values fluctuate within the period.
- **Limitations:** Source definitions, country coverage and attribution vary; country-attributed totals need not equal unique global totals. Neither HHI nor Top-3 establishes causality or measures all AI capability. Balanced-panel comparison is a coverage sensitivity check, not proof of global completeness.
- **Files and validation:** `pages/4_Concentration.py`; `src/concentration.py`; `data/processed/concentration_metrics.csv` (36 domain-year rows); `data/processed/concentration_metadata.json` (processing timestamp). The app supports dataset/year filters, charts, country-level auditing and CSV downloads. **`python src/concentration.py --verify` passed all 36 rows**; seven filter cases and selected 2024 raw-country audits passed. **Colour-vision-deficiency simulation was not performed.**

## Data dictionary and lineage

Each student should document **every dataset used by their section**, including source and exact URL, licence, **all columns with units**, primary key, full time range and latest observation, and preprocessing steps. Shared source datasets should have one definitive entry in the final version; Student 4 documents how it reuses them and the outputs it creates.

### Section 1 — Publications data

**Source URL:** https://ourworldindata.org/grapher/annual-scholarly-publications-on-artificial-intelligence.csv?v=1&csvType=full&useColumnShortNames=true

**Licence:** CC BY 4.0

**Raw file:** \data/raw/publications.csv\

**Processed file:** \data/processed/publications.csv\

**Columns:**
- \entity\: country name
- \code\: ISO 3-letter country code
- \year\: observation year
- \num_articles__field_all\: number of AI-related scholarly publications (count)

**Primary key:** (\code\, \year\)

**Coverage / latest:** 2016–2024; latest observation 2024

**Transforms:** Read the raw file \publications.csv\ from \data/raw/\. Rename columns from \entity\, \code\, \year\, and \num_articles__field_all\ to \country\, \code\, \year\, and \publications\. Remove rows with missing country codes and exclude OWID aggregate regions to retain country-level observations only. The processed file preserves the same country-year publication records for dashboard use.

### Section 2 — Patents data

- **Source URL:** `https://oecd.ai/en/trends-and-data`
- **Licence:** `Creative Commons Attribution 4.0`
- **Raw file:** `Evolution_of_AI-related_patents_by_country.csv` (3,570 data rows)
- **Columns:**
  - `AI_counts`: number of AI-related patents (count)
  - `Country/territory`: ISO3 code, for example `USA` or `CHN`; aggregates are `ALL`, `OECD`, `EU27`
  - `Country/territory_label`: country or territory name
  - `sector`: always `AI`
  - `year`: priority year
- **Primary key:** (`Country/territory`, `year`), because `sector` is constant.
- **Coverage / latest:** 1995–2024; latest observation 2024
- **Transforms:** `Read the raw file `Evolution_of_AI-related_patents_by_country.csv` from `data/raw/` without modifying it. Use `ALL` as the world total and exclude `OECD` and `EU27` from rankings. Keep the five countries with the most patents in 2024 (United States, China, Japan, Korea, Germany) for 2010–2024. Calculate share as count ÷ `ALL`, and Others as `ALL` minus the five countries. Save to `data/processed/processed.csv`.`

### Section 3 — Investment data

**TODO:** [Source URL; licence; raw and processed filenames; full columns/units; primary key; coverage/latest; upstream transformation script and derived files].

### Section 4 — Concentration derived data

**Input reuse:** `src/concentration.py` reads the shared publications, patents and country-year investment CSVs from `data/raw/`. It normalises the columns to `year`, `country_code`, `country`, `value`, without assuming identical country coverage. Publications retain three-uppercase-letter codes and nonmissing values; patents exclude `ALL`, `OECD`, `EU27`; investments use `investment_usd_2021` (constant 2021 USD). All input values must be nonnegative with unique country-year keys. **Source licences and upstream investment-data lineage must be confirmed in Students 1–3's definitive entries.**

| Output / provenance | Columns and units | Key; coverage/latest | Transformation |
|---|---|---|---|
| `data/processed/concentration_metrics.csv` — computed from the shared source CSVs using `src/concentration.py` | `domain` (category), `year` (year), `hhi` (0–1), `top3_share` (0–1), `countries_observed` (count), `countries_positive` (count), `observed_total` (publication/patent count or constant 2021 USD, depending on domain) | (`domain`, `year`); 2016–2024/latest 2024; 36 rows | Compute country shares, HHI, Top-3, observed totals and counts; add the balanced-investment series |
| `data/processed/concentration_metadata.json` — generated by the same script | `processed_at_utc` (ISO-8601 UTC timestamp), `first_year`, `last_year` (years), `domains` (list of categories) | One object per generated file; latest observation covered is 2024 | Write the processing timestamp and selected range after generating metrics; **not** the publisher's update date |

**Student 4 verification:** From the repository root run `python src/concentration.py` then `python src/concentration.py --verify`. The second command checks all saved domain-year values against source-based calculations (within numerical tolerance). The original shared inputs must be included in the assessed repository commit.


## AI provenance matrix

| Artefact | Who | Tool | Request | Output | Verification | Outcome |
|---|---|---|---|---|---|---|
| Section 1 | Student 1 (Hoa Nhung Dao) | Microsoft Copilot | Brainstorm dashboard structure, visualisation selection, storytelling flow, KPI design, verification approach, README documentation, and Python/Streamlit code suggestions for data processing and dashboard implementation. | Dashboard layout, KPI calculations, Treemap, Stacked Area Chart, Multi-Line Chart, Growth + Scale methodology, validation workflow, content. | Publication shares were recalculated from the source dataset and matched dashboard outputs. Top-5 Share and Concentration Change metrics were verified against source publication totals. Country-level publication shares (including China, India, and the United States in 2024) were spot-checked against the original dataset. Year-range filtering was tested across all KPI cards and visualisations. | Reviewed, modified, and verified before inclusion in the dashboard. |
| Section 2 | Student 2 (Phenphan Viriyathamakul) | Claude (Anthropic) | Troubleshooting a Streamlit run error (missing `plotly` dependency); Git/GitHub guidance for branches, pull, push, and deployment; drafting README text and the data dictionary | Terminal commands, troubleshooting steps, README draft text | Shares for 2010 and 2024 recalculated from the source CSV and matched the page; ranks spot-checked for 2010, 2014, 2020, 2021, 2022; app run locally after installing plotly 7.1.0 |
| Section 3 | Student 3 | TODO | TODO | TODO | TODO | TODO |
| Section 4 | Student 4 (Myeongjin Han) | ChatGPT (OpenAI) | Code assistance and academic writing refinement | Code and wording suggestions | Reproduction checks (36/36 rows) and dashboard testing (7 cases) | Reviewed, modified and verified |



## Data and AI disclosure

**Team draft — verify before submission.** This project uses publicly sourced datasets and documented transformations. ChatGPT assisted Student 4 with coding, debugging, chart design, testing suggestions and documentation. Suggested material was reviewed and tested before use. The table above records substantive AI uses and checks. **TODO (team):** Add other members' actual AI tools and verification practices; confirm source licences and upstream processing before finalising this statement.

## Run and submit

Install dependencies:

```bash
pip install -r requirements.txt
```

**Section 4 data reproduction:**

```bash
python src/concentration.py
python src/concentration.py --verify
```

**Team app (TODO: confirm after integration):**

```bash
streamlit run app.py
```

**Before submission — team:** Complete TODOs; check all 30 rubric items including at least four charts from three Visual Vocabulary families, readable labels, responsive/empty-state interactions, accessible colour use, 1366×768 layout, under-five-second deployed loading, sources/refresh display, full data regeneration, and the final assessed commit. **Canvas submission is one PDF per group**, containing the deployed app URL, repository URL and full assessed commit hash or release tag; no separate report is required.
