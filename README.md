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

- Section 1 : student Name (student id)
- Section 2 : Phenphan Viriyathamakul (26506028)
- Section 3 : student Name (student id)
- Section 4 : Myeongjin Han (25692308)

Each student should complete the same fields: **question / method / finding / limitations / files and validation**.

### Section 1 — AI Publications

- **Question / method — TODO:** [Data, years, measures, charts and filters]
- **Finding / limitations — TODO:** [Evidence-based interpretation and limitations]
- **Files and validation — TODO:** [Code paths, processed output and actual tests]

### Section 2 — AI Patents

- **Question / method:** Which countries lead AI patenting, and how has their share of world AI patents changed from 2010 to 2024? Data: OECD AI patent indicators (PCT-based, by priority year), 2010–2024 on the page. Measures: patent counts, country share of the world total (`ALL`), and rank among five countries. The five countries are the highest 2024 counts after excluding aggregate rows (`ALL`, `OECD`, `EU27`). Charts: metric tiles (2024 counts and change since 2010), a line chart of annual counts, a stacked area chart of shares, a rank table with a year slider, and a share table with CSV download. Filter: country multiselect.
- **Finding / limitations:** From 2010 to 2024, the United States' share fell from 30.9% to 28.9%, while China's rose from 4.9% to 27.3%. Japan's fell from 31.4% to 10.7%, and Korea's rose from 4.1% to 10.7%. China ranked first in 2020 and 2021. The United States ranked first in 2011, 2013–2019, and 2022–2024. Japan ranked first in 2010 and 2012. Limitations: patents measure filed inventions, not research quality or commercial value; patent rules differ between offices; recent years may be estimates; rankings compare only the five countries shown; the source includes territories; and the page covers 2010–2024, whereas Section 4 covers 2016–2024.
- **Files and validation:** `pages/2_Patents.py`; `src/patents.py` (`render_patent_view`); source `Evolution_of_AI-related_patents_by_country.csv`; processed output `data/processed/processed.csv`. Checks completed: shares for 2010 and 2024 were recalculated from the source and match the page; ranks were spot-checked for 2010, 2014, 2020, 2021, and 2022; aggregate rows were excluded. Not yet completed: `<TODO: automated tests>`, deployed-app loading time, 1366×768 layout, and colour-vision check.
  
### Section 3 — Private AI Investment

- **Question / method — TODO:** [Data, years, measures, charts and filters]
- **Finding / limitations — TODO:** [Evidence-based interpretation and limitations]
- **Files and validation — TODO:** [Code paths, processed output and actual tests]

### Section 4 — Geographic Concentration

- **Question / method:** Compare the geographic concentration of the country-attributed publications, patents and private-investment inputs shared with Students 1–3, using **2016–2024** as the common period. For each domain/year, compute a country's share of observed values, **HHI = sum of squared shares (0–1)** and **Top-3 share = sum of the three largest shares (0–1)**. Report observed-country counts; do not treat missing country-years as zero. Compare observed-investment HHI against a **55-country balanced panel** (countries recorded in all nine years). Deviation = observed HHI − balanced-panel HHI.
- **Finding:** HHI changed from **0.071 to 0.112** (publications), **0.203 to 0.188** (patents), and **0.295 to 0.458** (investment) between 2016 and 2024 (rounded). These endpoint changes show **no uniform increase across all three domains**; investment values fluctuate within the period.
- **Limitations:** Source definitions, country coverage and attribution vary; country-attributed totals need not equal unique global totals. Neither HHI nor Top-3 establishes causality or measures all AI capability. Balanced-panel comparison is a coverage sensitivity check, not proof of global completeness.
- **Files and validation:** `pages/4_Concentration.py`; `src/concentration.py`; `data/processed/concentration_metrics.csv` (36 domain-year rows); `data/processed/concentration_metadata.json` (processing timestamp). The app supports dataset/year filters, charts, country-level auditing and CSV downloads. **`python src/concentration.py --verify` passed all 36 rows**; seven filter cases and selected 2024 raw-country audits passed. **Colour-vision-deficiency simulation was not performed.**

## Data dictionary and lineage

Each student should document **every dataset used by their section**, including source and exact URL, licence, **all columns with units**, primary key, full time range and latest observation, and preprocessing steps. Shared source datasets should have one definitive entry in the final version; Student 4 documents how it reuses them and the outputs it creates.

### Section 1 — Publications data

**TODO:** [Source URL; licence; raw and processed filenames; full columns/units; primary key; coverage/latest; transforms].

### Section 2 — Patents data

**TODO:** [Source URL; licence; raw and processed filenames; full columns/units; primary key; coverage/latest; transforms].

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
| Section 1 | Student 1 | TODO | TODO | TODO | TODO | TODO |
| Section 2 | Student 2 | TODO | TODO | TODO | TODO | TODO |
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
