# AI investment data for Assignment 3, Section 3

## Dataset and provenance

Dataset: Estimated funding raised by privately held AI companies, Field: All.
Publisher: Our World in Data (OWID).
Underlying producer: Georgetown University's Center for Security and Emerging Technology (CSET), Emerging Technology Observatory (ETO). ETO derives investment metrics from Crunchbase. OWID adjusts the values for inflation using the US CPI.

Data page: https://ourworldindata.org/grapher/private-investment-in-artificial-intelligence-cset
Full CSV: https://ourworldindata.org/grapher/private-investment-in-artificial-intelligence-cset.csv?v=1&csvType=full&useColumnShortNames=false
Metadata: https://ourworldindata.org/grapher/private-investment-in-artificial-intelligence-cset.metadata.json?v=1&csvType=full&useColumnShortNames=false
Original methodology: https://eto.tech/dataset-docs/country-ai-activity-metrics/

Downloaded: 20 October 2026. OWID indicator last updated: 27 April 2026.

## Contents checked

The frozen full CSV contains 897 observations covering 2016–2025. There are 119 distinct countries or territories across the period and six regional/global aggregates. The country-only table contains 837 observations. Coverage varies: 69 country observations in 2016 and 92 in 2025. Only 55 countries have an observation in every year. This is an unbalanced panel, not 119 countries in every year.

## What the measure means

Estimated annual equity funding received by privately held AI-related companies, including venture capital, private equity, and mergers and acquisitions. Recipient country follows company headquarters, and the year is the deal-announcement year. Some undisclosed transaction amounts are estimated by the original provider. The series excludes recipients listed on public stock exchanges, internal corporate spending, grants, debt and crowdfunding. Investors can include corporations and sovereign wealth funds. It does not measure all AI spending or funding originating from investors in each country.

OWID values are in constant 2021 US dollars. The original ETO tables use millions of dollars; do not apply that unit to this OWID CSV.

## Files and reproducible preparation

- raw/: downloaded OWID CSV and metadata, preserved unchanged.
- processed/ai_investment_country_year_2016_2025.csv: country-only observations with documented units and source-row references.
- processed/coverage_by_year.csv: annual coverage and country-sum reconciliation against the reported World aggregate.
- processed/validation.json: checks, retrieval date and raw-data SHA-256.
- prepare_investment_data.py: rerun with Python 3 using its standard library.

Preparation renames identifiers, retains source dollar amounts, sorts country-year records, excludes the six OWID aggregate codes and adds a billions column by dividing by 1,000,000,000. No country values are imputed, re-estimated or inflation-adjusted again. Explicit source zeros remain zero. Missing country-years stay absent. Every prepared row identifies its original CSV row, counting the header as row 1.

## Use in the dashboard and concentration section

Use the country-only table for country rankings and concentration calculations. Calculate annual shares using a clearly stated denominator, such as the sum of available country observations. Label the result as a share of funding recorded in this dataset. Do not add World or regional rows to country rows. Small differences of a few dollars between country sums and the World row arise from integer rounding.

For HHI, use unrounded fractions of the SAME annual denominator and sum their squares. Multiply by 10,000 only if using the 0–10,000 scale. Do not use only the displayed top ten countries. For comparisons over time, inspect coverage changes and run a fixed-country sensitivity check with has_observation_every_year=true; that flag concerns observation presence, not reporting completeness. Reported source zeros may have a different interpretation from absent rows. Recent years can have reporting lags. The OWID extract does not retain the original ETO completeness flags, so do not describe 2025 as confirmed complete. The source notes limited geographical coverage, particularly in Africa. Comparing different indicators also requires compatible years and country definitions.

## Verification example for the recording

The United States, 2025, appears in raw CSV row 855 with a value of 301022702852 constant 2021 US dollars. The prepared billions column is 301.022702852, calculated by division by 1,000,000,000. A dashboard display rounded to two decimals should show 301.02 billion constant 2021 US dollars. Show the source row and this conversion on screen.

## Citation

Center for Security and Emerging Technology (2026); U.S. Bureau of Labor Statistics (2026), with major processing by Our World in Data. Estimated funding raised by privately held AI companies – Field: All [dataset]. Accessed 20 October 2026. https://ourworldindata.org/grapher/private-investment-in-artificial-intelligence-cset

Retain the full downloaded metadata when sharing. OWID-produced material is available under CC BY; underlying third-party data remain subject to the original providers' terms. See the data page and ETO terms for details.
