# The Rise of Artificial Intelligence — Geographic Concentration

**UTS 36104 · Assignment 3 Part 2 · Group 15**

## Research question and audience

**Research question:** Is AI development becoming concentrated in fewer countries?

**Persona / decision:** An AI policy analyst assessing the geographic distribution of AI research, patenting, and private investment. The dashboard supports decisions about which countries and AI development domains warrant closer policy attention.

**User stories:**

1. As an AI policy analyst, I want to examine AI publication shares and concentration trends across years, so that I can assess whether research output is becoming more geographically concentrated. **App path:** Publications → select year range → inspect publication shares and concentration trends.

2. As an AI policy analyst, I want to compare geographic concentration across publications, patents, and private investment, so that I can identify whether concentration is increasing consistently across AI domains. **App path:** Concentration → select datasets and years → inspect HHI and Top-3 share charts.

3. As an AI policy analyst, I want to compare countries' shares of private AI investment and track the leading five countries over time, so that I can assess whether recorded funding is becoming more geographically concentrated. **App path:** Investments → select year → inspect country rankings and the Top-5 share trend → compare all available countries with the fixed-country panel.



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

### Section 3 — Private AI Investment

- **Question / method:** Assess whether funding received by privately held AI companies is becoming concentrated in fewer countries, using the **OWID/CSET investment series for 2016–2025** in **constant 2021 US dollars**. Calculate country shares and the combined **Top-5 share** using all countries in the selected coverage group before display filters. Exclude regional and World aggregates. Compare all available countries with a **55-country fixed panel** observed in all ten years. Use horizontal bars for country rankings and line charts for funding and share trends. Controls select year, countries, coverage, funding amount or share, and trend period.

- **Finding:** With all available countries, Top-5 share increased from **82.1% in 2016 to 85.0% in 2025**, a rise of **2.9 percentage points**. The United States’ share increased from **51.3% to 70.1%**. The fixed-panel Top-5 share also increased, from **82.2% to 85.5%**. These endpoint comparisons indicate greater dominance within recorded funding, although the annual trend fluctuates.

- **Limitations:** Country coverage varies, some deal values are estimated, and recent years may have reporting lags. Country attribution follows recipient-company headquarters rather than investor nationality. Missing country-years are not treated as zero. The fixed panel checks sensitivity to observation coverage, not reporting completeness. Results do not establish that fewer countries receive funding or measure all AI spending and capability.

- **Files and validation:** `pages/investments.py`; `src/investments.py`; `scripts/prepare_investment_data.py`; `data/processed/ai_investment_country_year_2016_2025.csv` (**837 observations**); `data/processed/coverage_by_year.csv`. Automated checks regenerated both processed CSVs byte-for-byte and matched all cleaned records to their raw observations and unit conversions. US 2025 raw row **855** contains **301,022,702,852** constant 2021 US dollars, displayed as **$301.02bn** after division by one billion. Local checks covered filters and empty selection; deployed checks covered chart loading, year selection, fixed coverage, funding mode and source verification. See the [data dictionary](docs/investment_data_notes.md) and [AI provenance matrix](docs/investment_ai_provenance.md). **Colour-vision-deficiency simulation was not performed as part of these checks.**

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

#### Source and provenance

**Dataset:** Estimated funding raised by privately held AI companies — Field: All.

**Publisher:** Our World in Data (OWID).

**Underlying producer:** Georgetown University's Center for Security and Emerging Technology (CSET), Emerging Technology Observatory (ETO). Investment estimates are derived from Crunchbase. OWID adjusts the values for inflation using US consumer prices.

- [Source page](https://ourworldindata.org/grapher/private-investment-in-artificial-intelligence-cset)
- [Full CSV download](https://ourworldindata.org/grapher/private-investment-in-artificial-intelligence-cset.csv?v=1&csvType=full&useColumnShortNames=false)
- [Metadata download](https://ourworldindata.org/grapher/private-investment-in-artificial-intelligence-cset.metadata.json?v=1&csvType=full&useColumnShortNames=false)
- [Original methodology](https://eto.tech/dataset-docs/country-ai-activity-metrics/)

**Downloaded snapshot:** 20 October 2026.  
**Source update recorded in the metadata:** 27 April 2026.  
**Time coverage:** 2016–2025.  
**Latest observation:** 2025; reporting completeness is not confirmed.  
**Funding unit:** Constant 2021 US dollars.

The measure covers external equity funding received by privately held
AI-related companies, including venture capital, private equity and
mergers and acquisitions. Country attribution follows recipient-company
headquarters, and the year follows the deal announcement.

#### Licence and reuse

Reuse follows [OWID's guidance](https://ourworldindata.org/how-to-use-our-world-in-data),
[ETO's terms](https://eto.tech/tou) and applicable third-party restrictions.

ETO's general terms specify CC BY-NC 4.0 unless otherwise stated and identify
separate rights for third-party material. This project does not grant a
separate licence to the underlying data.

#### Original source CSV

**File:** `data/raw/private-investment-in-artificial-intelligence-cset.csv`  
**Primary key:** `Code` + `Year`.  
**Coverage:** 2016–2025; latest year 2025.  
**Size:** 897 observations, including country, regional and World records.  
**Transformation:** Preserved unchanged from the downloaded OWID CSV.

| Column | Meaning and unit |
|---|---|
| `Entity` | Country, territory, region or World name. |
| `Code` | Source geography identifier, including OWID aggregate codes. |
| `Year` | Calendar year of deal announcement. |
| `Estimated funding raised by privately held AI companies - Field: All` | Estimated funding received, in constant 2021 US dollars. |

#### Source metadata

**File:** `data/raw/private-investment-in-artificial-intelligence-cset.metadata.json`.

Preserved unchanged from the downloaded metadata. This is a descriptive
JSON object, not a table of observations, so it has no observation primary key.

| Field | Meaning |
|---|---|
| `chart` | Chart description, source and citation information. |
| `columns` | Indicator definition, units, time coverage and update information. |
| `dateDownloaded` | Download date in ISO format. |
| `activeFilters` | Export filters; empty in this snapshot. |

#### Cleaned country-year observations

**File:** `data/processed/ai_investment_country_year_2016_2025.csv`  
**Primary key:** `country_code` + `year`.  
**Coverage:** 2016–2025; latest year 2025.  
**Size:** 837 observations across 119 distinct countries or territories.

This is an unbalanced panel: not every country has an observation in every
year. A fixed panel contains 55 countries observed in all ten years.

| Column | Meaning and unit |
|---|---|
| `country` | Recipient country or territory name, from `Entity`. |
| `country_code` | Country or territory identifier, from `Code`. |
| `year` | Calendar year, from `Year`. |
| `investment_usd_2021` | Original funding amount in constant 2021 US dollars. |
| `investment_usd_2021_bn` | Original amount divided by 1,000,000,000, in billions of constant 2021 US dollars. |
| `has_observation_every_year` | Boolean indicating whether the country has a source observation in every year from 2016 to 2025. This measures observation coverage, not reporting completeness. |
| `source_row` | Original CSV row number, counting the header as row 1. |
| `source_file` | Original source CSV filename. |
| `source_url` | OWID source-page URL. |

**Transformation:** Remove 60 regional and World observations, rename
identifiers, sort country-year records, retain source dollar amounts and
add the billions, coverage and provenance fields.

#### Annual coverage and reconciliation

**File:** `data/processed/coverage_by_year.csv`  
**Primary key:** `year`.  
**Coverage:** 2016–2025; latest year 2025.  
**Size:** Ten annual observations.

| Column | Meaning and unit |
|---|---|
| `year` | Calendar year. |
| `countries_observed` | Number of distinct countries or territories with a source observation that year. |
| `country_sum_usd_2021` | Sum of observed country funding, in constant 2021 US dollars. |
| `owid_world_usd_2021` | Separate OWID World amount, in constant 2021 US dollars. |
| `difference_usd_2021` | Country sum minus the World amount, in constant 2021 US dollars. |
| `countries_observed_all_years` | Number of countries observed in every year of the snapshot: 55. |

**Transformation:** Group the original country observations by year,
calculate country counts and funding totals, and compare these totals
with the separately retained World record. World funding is not added
to country funding.

#### Reproducible preparation

**Script:** `scripts/prepare_investment_data.py`.

From the repository root, run:

```bash
python scripts/prepare_investment_data.py
```

The script uses Python's standard library and reads the packaged raw CSV
and metadata. It regenerates both processed CSVs and writes
`data/processed/validation.json`, containing validation results, coverage
information and the raw-data checksum.

Preparation retains explicit source zeros. Missing country-years remain
absent. No values are imputed, and inflation adjustment is not applied again.

#### Use and limitations

Annual country shares use the sum of funding across the selected coverage
group before display filters are applied. Regional and World records are
excluded from this denominator.

Changing coverage, estimated deal amounts and reporting lags can affect
comparisons. The fixed-country panel checks sensitivity to observation
coverage; it does not establish complete global coverage.

The data do not measure all AI spending, investor nationality or overall
national AI capability.

[Detailed investment data notes](docs/investment_data_notes.md).

### Section 4 — Concentration derived data

**Input reuse:** `src/concentration.py` reads the shared publications, patents and country-year investment CSVs from `data/raw/`. It normalises the columns to `year`, `country_code`, `country`, `value`, without assuming identical country coverage. Publications retain three-uppercase-letter codes and nonmissing values; patents exclude `ALL`, `OECD`, `EU27`; investments use `investment_usd_2021` (constant 2021 USD). All input values must be nonnegative with unique country-year keys.

| Output / provenance | Columns and units | Key; coverage/latest | Transformation |
|---|---|---|---|
| `data/processed/concentration_metrics.csv` — computed from the shared source CSVs using `src/concentration.py` | `domain` (category), `year` (year), `hhi` (0–1), `top3_share` (0–1), `countries_observed` (count), `countries_positive` (count), `observed_total` (publication/patent count or constant 2021 USD, depending on domain) | (`domain`, `year`); 2016–2024/latest 2024; 36 rows | Compute country shares, HHI, Top-3, observed totals and counts; add the balanced-investment series |
| `data/processed/concentration_metadata.json` — generated by the same script | `processed_at_utc` (ISO-8601 UTC timestamp), `first_year`, `last_year` (years), `domains` (list of categories) | One object per generated file; latest observation covered is 2024 | Write the processing timestamp and selected range after generating metrics; **not** the publisher's update date |

**Student 4 verification:** From the repository root run `python src/concentration.py` then `python src/concentration.py --verify`. The second command checks all saved domain-year values against source-based calculations (within numerical tolerance). The original shared inputs must be included in the assessed repository commit.


## AI provenance matrix

| Artefact | Who | Tool | Request | Output | Verification | Outcome |
|---|---|---|---|---|---|---|
| Section 1 | Student 1 (Hoa Nhung Dao) | Microsoft Copilot | Brainstorm dashboard structure, visualisation selection, storytelling flow, KPI design, verification approach, README documentation, and Python/Streamlit code suggestions for data processing and dashboard implementation. | Dashboard layout, KPI calculations, Treemap, Stacked Area Chart, Multi-Line Chart, Growth + Scale methodology, validation workflow, content. | Publication shares were recalculated from the source dataset and matched dashboard outputs. Top-5 Share and Concentration Change metrics were verified against source publication totals. Country-level publication shares (including China, India, and the United States in 2024) were spot-checked against the original dataset. Year-range filtering was tested across all KPI cards and visualisations. | Reviewed, modified, and verified before inclusion in the dashboard. |
| Section 2 | Student 2 (Phenphan Viriyathamakul) | Claude (Anthropic) | Troubleshooting a Streamlit run error (missing `plotly` dependency); Git/GitHub guidance for branches, pull, push, and deployment; drafting README text and the data dictionary | Terminal commands, troubleshooting steps, README draft text | Shares for 2010 and 2024 recalculated from the source CSV and matched the page; ranks spot-checked for 2010, 2014, 2020, 2021, 2022; app run locally after installing plotly 7.1.0 | Reviewed, Checked before upload in the dashboard |
| Section 3 | Student 3 (Shubham Doshi) | ChatGPT (OpenAI) | Data preparation, dashboard development and README assistance | Processing code, charts and documentation | Regenerated processed CSVs; checked 837 records against raw data; verified US 2025 funding ($301.02bn) and tested filters | Data checks matched; tested controls worked. [Detailed provenance](docs/investment_ai_provenance.md) |
| Section 4 | Student 4 (Myeongjin Han) | ChatGPT (OpenAI) | Code assistance and academic writing refinement | Code and wording suggestions | Reproduction checks (36/36 rows) and dashboard testing (7 cases) | Reviewed, modified and verified |



## Data and AI disclosure

This project uses publicly available datasets covering AI scholarly publications, AI-related patents, and private AI investment. Data sources, licences, processing methods, limitations, and validation procedures are documented in the relevant sections of this repository.

Team members used AI assistants, including Microsoft Copilot, Claude, and ChatGPT, to support selected tasks such as Python and Streamlit development, debugging, visualisation planning, data preparation, and documentation.

The AI provenance matrix records each member's reported AI use, including the tool, request, output, verification approach, and outcome. The team remains responsible for reviewing AI-assisted material, verifying analytical results, and ensuring the accuracy of the submitted work.


## Reproducibility and application

### Installation

Install the required Python dependencies from the repository root:

```bash
pip install -r requirements.txt
```

The deployed Streamlit application uses Python 3.12.

### Run the application

```bash
streamlit run app.py
```

### Reproduce concentration metrics

```bash
python src/concentration.py
python src/concentration.py --verify
```

Other data preparation procedures and verification methods are documented in the corresponding sections and scripts.

### Application and source code

- [Deployed Streamlit application](https://global-ai-concentration-group15.streamlit.app/)
- [GitHub repository](https://github.com/25692308/global-ai-concentration)
