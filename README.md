# The Rise of Artificial Intelligence — Geographic Concentration

**UTS 36104 Data Visualisation and Narratives · Assignment 3 Part 2 · Group 15 Portfolio**

> **Team editing note:** This is the shared README draft for the `docs` branch. Section 4 code and analysis are complete; documentation fields marked **TODO (team)** require confirmation or completion by the team before submission. Remove all TODO notes in the assessed version.

## 1. Research Question

**Is AI development becoming concentrated in fewer countries?**

This is an arguable question: scholarly publications, AI-related patents and private AI investment can exhibit different geographic concentration trends, even over the same period.

## 2. Audience and User Stories

**Persona — TODO (team):** Identify a concrete target reader (e.g., an AI-policy analyst), the decision or understanding the application is intended to support, and why comparing the three domains matters. Choose and confirm the team's actual persona rather than treating the example as established.

**Three user stories — TODO (team):** Write and verify each story in the format **As a [persona], I want [task], so that [decision or understanding]**. Each must have a working path through the deployed app.

1. **TODO:** As a …, I want …, so that … . **App path:** …
2. **TODO:** As a …, I want …, so that … . **App path:** …
3. **TODO:** As a …, I want …, so that … . **App path:** …

## 3. App and Reproducibility

- **Deployed Streamlit URL — TODO (team):** Add the public URL.
- **Repository:** This GitHub repository (insert canonical URL in final version).
- **Assessed commit or release — TODO (team):** Record the final hash/tag in the Canvas PDF, not the temporary working branch hash.
- **Entry point — TODO (team):** Confirm whether the main app is `app.py` and that the shared `requirements.txt` deploys correctly.

Run from the repository root:

```bash
pip install -r requirements.txt
python src/concentration.py
python src/concentration.py --verify
python -m streamlit run pages/4_Concentration.py
```

For the **full team app**, run `streamlit run app.py` **only if `app.py` is the confirmed main entry point**.

## 4. Narrative Structure

### Section 1 — AI Publications

**TODO (Section 1 owner):** Analytical question, data/period, visual forms, interactions, evidence-based finding, limitations and links to code/data.

### Section 2 — AI Patents

**TODO (Section 2 owner):** Analytical question, data/period, visual forms, interactions, evidence-based finding, limitations and links to code/data.

### Section 3 — Private AI Investment

**TODO (Section 3 owner):** Analytical question, data/period, visual forms, interactions, evidence-based finding, limitations and links to code/data.

### Section 4 — AI Geographic Concentration

**Question.** Is AI development becoming concentrated in fewer countries?

**Overview.** This section compares observed country-attributed AI scholarly publications, AI-related patents and private AI investment across the common **2016–2024** period. It measures the *geographic concentration of recorded activity*, not total AI capability.

**Method.** In each domain/year, country share = country value / sum of observed country-attributed values. The **HHI (0–1)** is the sum of squared shares; the **Top-3 share (%)** is the sum of the three largest shares, reselected each year. The dashboard also reports **observed countries (count)**, including recorded zeros. Missing country–years are **not** imputed as zero. For investments, a fixed **55-country** balanced panel (countries observed in every year 2016–2024) is compared with the observed panel. The sensitivity deviation is **observed-panel HHI minus balanced-panel HHI**.

**Results (2016 vs 2024).**

| Domain | HHI 2016 | HHI 2024 | Change (HHI points) |
|---|---:|---:|---:|
| Publications | 0.071 | 0.112 | +0.041 |
| Patents | 0.203 | 0.188 | −0.015 |
| Private investment | 0.295 | 0.458 | +0.163 |

*Values rounded to three decimals; these are endpoint comparisons, not evidence of steady year-by-year movement.* Publication concentration increased, patent concentration fell slightly, and investment concentration rose between endpoints but fluctuated substantially in between. **There is no uniform rise in concentration across all three domains.**

**App features.** Filter datasets and year ranges; inspect HHI, Top-3 and country coverage; compare investment-panel deviations; read filter-responsive conclusions; inspect raw country contributions and download audit CSVs. The dashboard displays source links and processed-data refresh metadata.

**Files and verification.** `pages/4_Concentration.py` renders the UI; `src/concentration.py` builds and validates the metrics; `data/processed/concentration_metrics.csv` contains four domain series over nine years (36 rows); `data/processed/concentration_metadata.json` records the processing timestamp. Local execution of `python src/concentration.py --verify` returned **PASS for all 36 saved rows**; seven filter/empty-state scenarios were manually checked; selected 2024 country-level audits passed. Colour-vision-deficiency simulation was **not performed**.

**Interpretation limits.** The three sources have different definitions, geographic attribution and coverage. Country-attributed counts are not necessarily de-duplicated global item counts; changing coverage can affect HHI; cross-domain HHI magnitudes are not necessarily directly comparable. These data cannot establish causality or directly measure overall AI capability. The 55-country panel is a sensitivity check, not a global correction.

## 5. Data Dictionary and Data Lineage

**Team requirement:** Complete entries for **every** raw, intermediate and processed dataset used by the full app. For each file identify the source and exact URL, applicable licence, all columns and units, primary key, full time coverage, latest observed period and transformations. Do not state unverified third-party reuse terms as confirmed.

### Section 1–3 datasets — TODO (team)

| Dataset | Source / exact URL | Licence | Columns + units | Primary key | Coverage / latest observation | Transform / derived file |
|---|---|---|---|---|---|---|
| Section 1 inputs | TODO | TODO | TODO | TODO | TODO | TODO |
| Section 2 inputs | TODO | TODO | TODO | TODO | TODO | TODO |
| Section 3 inputs | TODO | TODO | TODO | TODO | TODO | TODO |

### Section 4 input and output datasets

**A. Publications — `data/raw/annual-scholarly-publications-on-artificial-intelligence.csv`**

- **Source/URL:** Our World in Data, *Annual scholarly publications on artificial intelligence* (CSET underlying data); https://ourworldindata.org/grapher/annual-scholarly-publications-on-artificial-intelligence
- **Licence:** **TODO (team verify):** inspect the original dataset's attribution and third-party reuse terms; OWID hosting does not itself establish a universal licence for externally sourced data.
- **Original file:** 1,613 rows; columns: `entity` (country/entity name, text), `code` (entity code, text), `year` (calendar year), `num_articles__field_all` (scholarly publications, count).
- **Primary key:** `(entity, year)` in the source; transformed analytics expect unique `(year, country_code)`.
- **Full file coverage/latest:** 2016–2024; latest 2024. There are 63 rows without `code`; rows without a three-letter uppercase code are excluded (including these 63 rows).
- **Transform:** rename `entity→country`, `code→country_code`, `num_articles__field_all→value`; retain codes matching three uppercase letters; remove missing values; validate nonnegative values and unique country–year keys; aggregate shares, HHI and Top-3 by year. **Note:** code-shape filtering alone is not a verified geopolitical country list.

**B. Patents — `data/raw/Evolution of AI-related patents by country.csv`**

- **Source/URL:** OECD.AI export; https://oecd.ai/en/data . **TODO (team):** record the precise export URL/date and applicable dataset-specific reuse licence.
- **Original file:** 3,570 rows; columns: `AI_counts` (AI-related patent count), `Country/territory` (country/aggregate code), `Country/territory_label` (name), `sector` (categorical label), `year` (calendar year).
- **Primary key:** `(Country/territory, sector, year)` for the original export (no duplicates found in the uploaded CSV); processed country-year keys `(year, country_code)`.
- **Full file coverage/latest:** 1995–2024; latest 2024. Analysis restricts to 2016–2024.
- **Transform:** drop aggregate codes `ALL`, `OECD`, `EU27` (90 records in this export); rename `Country/territory→country_code`, `Country/territory_label→country`, `AI_counts→value`; select year/country/value; validate and compute shares, HHI and Top-3. Units are **patent counts**.

**C. Private AI investment — `data/raw/ai_investment_country_year_2016_2025.csv`**

- **Source/URL:** Team-prepared country/year input derived from OWID/CSET, https://ourworldindata.org/grapher/private-investment-in-artificial-intelligence-cset . **TODO (Section 3 owner):** document the upstream raw export, exact preparation script and reuse licence before final assessment.
- **Original file:** 837 rows; coverage 2016–2025; latest 2025. Section 4 analysis uses **2016–2024**.
- **Columns/units:** `country` (name), `country_code` (code), `year` (calendar year), `investment_usd_2021` (constant 2021 USD), `investment_usd_2021_bn` (billion constant 2021 USD), `has_observation_every_year` (Boolean), `source_row` (source-row reference), `source_file` (source filename), `source_url` (source URL).
- **Primary key:** `(year, country_code)`.
- **Transform:** load `investment_usd_2021` as `value`, validate nonnegative country-year records; restrict to 2016–2024; compute domain-year shares, HHI, Top-3, coverage and totals. For balanced panel retain countries observed in **all nine years**; compute sensitivity values without replacing missing years by zeros.

**D. Investment coverage diagnostic — `data/raw/coverage_by_year.csv` (if retained in the team data package)**

- **Role:** a 10-row companion diagnostic, not read directly by Section 4's current Streamlit page or its metric-builder.
- **Source/URL and licence:** derivative of the team's investment input and OWID world total; **TODO (team)** confirm exact upstream export/process and terms.
- **Columns/units:** `year` (calendar year), `countries_observed` (count), `country_sum_usd_2021` (constant 2021 USD), `owid_world_usd_2021` (constant 2021 USD), `difference_usd_2021` (constant 2021 USD), `countries_observed_all_years` (count).
- **Primary key:** `year`; coverage 2016–2025, latest 2025.
- **Transform:** compare summed country-year investment with source world totals; the script producing this diagnostic must be documented if this file forms part of the assessed data package.

**E. Calculated metrics — `data/processed/concentration_metrics.csv`**

- **Source:** generated from A–C by `src/concentration.py`.
- **Columns/units:** `domain` (category), `year` (calendar year), `hhi` (dimensionless 0–1), `top3_share` (fraction 0–1), `countries_observed` (count), `countries_positive` (count), `observed_total` (publication/patent counts or constant 2021 USD, according to `domain`).
- **Primary key:** `(domain, year)`; coverage **2016–2024**, latest **2024**, four series × nine years = **36 rows**.
- **Transform:** compute each country's share of the observed country-attributed total, square and sum shares for HHI, sum top-three shares; calculate coverage counts and observed totals. Add a separately labelled balanced-investment series.

**F. Processing metadata — `data/processed/concentration_metadata.json`**

- **Source:** written by `src/concentration.py` when regenerating metrics. **Record type:** one metadata object, rather than yearly observations.
- **Fields/units:** `processed_at_utc` (UTC ISO-8601 timestamp), `first_year`, `last_year` (years), `domains` (array of labels). Primary identifier: the single file/version associated with the committed generated metrics. Latest data period: 2024; latest *processing timestamp* is recorded separately.
- **Transform:** generate only after successful processing; do not mistake processing time for the source publisher's release date.

## 6. AI Provenance Matrix

**Required columns:** artefact; who; tool; what was asked; what came back; how it was verified (a test that *could have failed*); outcome. Each team member must contribute at least one substantive row. The following are the **Section 4 member's** records; add team members' rows before assessment.

| Artefact | Who | Tool | What was asked | What came back | How it was verified | Outcome |
|---|---|---|---|---|---|---|
| `src/concentration.py` | Myeongjin Han | ChatGPT (OpenAI) | Suggest HHI/Top-3 calculations, data validation and investment balanced-panel checks | Pipeline and source-audit suggestions | `python src/concentration.py --verify` passed **36/36** rows; missing/mismatched inputs would fail | Reviewed, modified and adopted |
| `pages/4_Concentration.py` | Myeongjin Han | ChatGPT (OpenAI) | Refine Streamlit charts, narrative and filters | UI/code and test suggestions | Manually tested seven filter cases, including empty selection and one year; unexpected state could fail | Reviewed, modified and adopted |
| 2024 country-level audit | Myeongjin Han | ChatGPT (OpenAI) | Suggest source-to-number validation of displayed HHI and Top-3 values | Recalculation/audit approach | Checked Publications, Patents and Investments against country-level values; dashboard displayed PASS; mismatches show errors | Adopted after local verification |
| Section 4 documentation | Myeongjin Han | ChatGPT (OpenAI) | Draft methodology, dictionary and provenance text | Suggested document structure and descriptions | Compared text with source CSV headers, source-linked documentation, code and observed checks; licence/upstream lineage uncertainties were flagged | Edited; pending team source/licence confirmation |
| **TODO (member 2)** | TODO | TODO | TODO | TODO | TODO | TODO |
| **TODO (member 3)** | TODO | TODO | TODO | TODO | TODO | TODO |
| **TODO (member 4)** | TODO | TODO | TODO | TODO | TODO | TODO |
| **TODO (member 5, if applicable)** | TODO | TODO | TODO | TODO | TODO | TODO |

## 7. Data and AI Disclosure Statement — TODO (team finalisation)

**Draft to verify against the team's actual work:** This project uses publicly cited third-party datasets and documented transformations for the analyses presented. Generative AI tools, including ChatGPT (OpenAI), assisted with selected coding, debugging, testing suggestions and writing. Team members reviewed and modified relevant suggestions and checked calculations and application behaviour against source data. The AI provenance matrix above records substantive uses and potentially failing verification checks. Unverified data rights or upstream preparation processes must be resolved and documented before final assessment. **TODO (team):** Include all other tools used, contributors' checks, any applicable limitations, and the actual data licensing arrangements.

## 8. Final Team Submission Checklist — TODO (team)

- [ ] README has one agreed research question, a named persona with decision, and **three walk-through user stories**.
- [ ] Four or more labelled charts across at least three Visual Vocabulary families; each value readable without hovering.
- [ ] Colour-vision-deficiency check completed or risk explicitly acknowledged (Rubric 18).
- [ ] Two or more responsive interactions; empty filter message; 1366×768 layout with vertical scrolling only.
- [ ] Public deployed app opens within five seconds; visible source links and actual last processed refresh time.
- [ ] Every dataset has source, precise URL, licence, columns with units, primary key, coverage, latest observation and transforms; source samples and app-read processed files are in the repository.
- [ ] Every group member has a verified provenance row and the final disclosure is accurate.
- [ ] All assessed processed outputs regenerate from source samples using documented steps.
- [ ] Final merged commit/release runs, app URL works, and the **Canvas PDF** has the app URL, repository URL and full assessed commit hash or release tag.

**Submission:** One PDF per group, due **Friday 20 November 2026, 11:59 pm**. Everything else must be present in the repository at the assessed commit.
