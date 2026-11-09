# Section 3: AI investment data and dictionary

The dashboard tracks estimated external equity funding received by privately held AI-related companies, grouped by recipient headquarters and deal announcement year. It includes venture capital, private equity and mergers and acquisitions. CSET estimates some undisclosed deal values. The series excludes publicly traded recipients, internal corporate spending, debt, grants and crowdfunding. It does not measure all AI spending or the countries where investors are based.

* **Source:** [Our World in Data investment series](https://ourworldindata.org/grapher/private-investment-in-artificial-intelligence-cset), based on Georgetown CSET's Emerging Technology Observatory (ETO) [Country AI Activity Metrics](https://eto.tech/dataset-docs/country-ai-activity-metrics/) and U.S. Bureau of Labor Statistics consumer prices. ETO derives the investment estimates from Crunchbase. OWID adjusts the values for inflation using the US CPI.
* **Files:** [OWID full CSV](https://ourworldindata.org/grapher/private-investment-in-artificial-intelligence-cset.csv?v=1&csvType=full&useColumnShortNames=false) and [metadata JSON](https://ourworldindata.org/grapher/private-investment-in-artificial-intelligence-cset.metadata.json?v=1&csvType=full&useColumnShortNames=false).
* **Snapshot:** Downloaded 20 October 2026. The frozen metadata lists 27 April 2026 as the source update date. All three CSVs cover 2016–2025. The latest observation year is 2025, which is not necessarily complete.
* **Licence and reuse:** The [ETO dataset documentation](https://eto.tech/dataset-docs/country-ai-activity-metrics/#what-are-the-terms-of-use) refers to [ETO's general terms](https://eto.tech/tou), which apply [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) to ETO material unless otherwise specified and flag separate rights for third-party material. See [OWID reuse guidance](https://ourworldindata.org/how-to-use-our-world-in-data) for its processed download. The cleaned and coverage files derive from that download; the project does not grant a separate licence to underlying third-party data.

## Original OWID CSV

**Path:** `data/raw/private-investment-in-artificial-intelligence-cset.csv`. **Key:** `Code` + `Year`. **Coverage:** 2016–2025; latest year 2025; 897 rows. Saved unchanged from the full CSV link above.

|Column|Meaning and unit|
|-|-|
|`Entity`|Country, territory, region, or World name.|
|`Code`|Source geography identifier, including OWID codes for aggregate rows.|
|`Year`|Calendar year of deal announcement.|
|`Estimated funding raised by privately held AI companies - Field: All`|Estimated equity funding received, in constant 2021 US dollars.|

`data/raw/private-investment-in-artificial-intelligence-cset.metadata.json` is the unmodified companion metadata, not a table of observations. Its top-level fields are `chart` (chart description and citation), `columns` (indicator definition, units, coverage and update information), `dateDownloaded` (ISO date), and `activeFilters` (export filters, empty in this snapshot). It has no observation key.

## Cleaned investment observations

**Path:** `data/processed/ai\_investment\_country\_year\_2016\_2025.csv`. **Key:** `country\_code` + `year`. **Coverage:** 2016–2025; latest year 2025; 837 rows across 119 distinct countries or territories. **Input:** Original OWID CSV and its metadata above. This is the table the dashboard reads.

|Column|Meaning and unit|
|-|-|
|`country`|Recipient country or territory name, from `Entity`.|
|`country\_code`|Country or territory code, from `Code`.|
|`year`|Calendar year, from `Year`.|
|`investment\_usd\_2021`|Source amount in constant 2021 US dollars.|
|`investment\_usd\_2021\_bn`|Source amount divided by one billion, expressed in billions of constant 2021 US dollars.|
|`has\_observation\_every\_year`|Boolean: the country has a source row in each year of the snapshot. This describes observation coverage, not reporting completeness.|
|`source\_row`|Row number in the original CSV, counting the header as row 1.|
|`source\_file`|Original CSV filename.|
|`source\_url`|OWID series page URL.|

The preparation script removes 60 regional or World observations, sorts by country code and year, and adds the display unit, coverage flag and provenance fields. It retains original dollar amounts and explicit zeros. It does not fill missing observations or adjust for inflation again.

## Yearly coverage and reconciliation

**Path:** `data/processed/coverage\_by\_year.csv`. **Key:** `year`. **Coverage:** 2016–2025; latest year 2025; ten rows. **Input:** Original OWID CSV above, grouped by year with country observations and the World row kept separate. Used to check coverage and reconcile totals.

|Column|Meaning and unit|
|-|-|
|`year`|Calendar year.|
|`countries\_observed`|Number of distinct countries or territories with a row that year.|
|`country\_sum\_usd\_2021`|Sum of observed country amounts, in constant 2021 US dollars.|
|`owid\_world\_usd\_2021`|OWID World amount, in constant 2021 US dollars.|
|`difference\_usd\_2021`|Country sum minus OWID World amount, in constant 2021 US dollars.|
|`countries\_observed\_all\_years`|Count of countries or territories with a row in every year of the snapshot; 55 for this release.|

## Reproduce and verify

Run `python scripts/prepare\_investment\_data.py` from the repository root. The script uses the checked-in raw snapshot and does not download new data. It regenerates both processed CSVs and writes `data/processed/validation.json`, a generated report with the raw checksum, record counts, coverage and reconciliation results. Both CSVs regenerated byte-for-byte from the checked-in source, and all 837 cleaned rows matched their raw records and unit conversions during the ZIP review.

For a live example, select United States, 2025 in **Verify a number**. The app reads raw row 855, containing 301,022,702,852 constant 2021 US dollars. Dividing by one billion gives 301.022702852 billion, shown as **$301.02bn** on the verification card.

## Interpretation and group use

Annual funding shares use the sum across all countries in the selected coverage group, before ranking or trend filters. Regional and World rows are not added to that denominator. The top five are ranked separately each year. If computing HHI, sum the squares of unrounded country shares from that same denominator; multiply by 10,000 only for the 0–10,000 scale. The 55-country option checks sensitivity to observation coverage; it cannot correct missing deals or coverage bias. Compare compatible years and geography definitions when combining investments with publications and patents.

