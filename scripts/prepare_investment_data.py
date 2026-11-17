"""Prepare country-year investment data from the frozen OWID CSET CSV.

Run from the project root: python scripts/prepare_investment_data.py
Uses only the Python standard library. Does not download or refresh the source.
"""
from pathlib import Path
import csv
import hashlib
import json
from decimal import Decimal

ROOT = Path(__file__).resolve().parents[1] / "data"
RAW = ROOT / "raw" / "private-investment-in-artificial-intelligence-cset.csv"
METADATA = RAW.with_suffix(".metadata.json")
SOURCE_URL = "https://ourworldindata.org/grapher/private-investment-in-artificial-intelligence-cset"
rows = list(csv.DictReader(RAW.open(encoding="utf-8-sig", newline="")))
value_column = "Estimated funding raised by privately held AI companies - Field: All"
aggregate_codes = {"OWID_ASI", "OWID_EUR", "OWID_NAM", "OWID_OCE", "OWID_SAM", "OWID_WRL"}
years = sorted({int(row["Year"]) for row in rows})
country_rows = [(line, row) for line, row in enumerate(rows, start=2) if row["Code"] not in aggregate_codes]
assert all(len(row["Code"]) == 3 and row["Code"].isalpha() for _, row in country_rows)
assert len(country_rows) == len({(row["Code"], row["Year"]) for _, row in country_rows}), "Duplicate country-year"
assert all(row[value_column] != "" and Decimal(row[value_column]) >= 0 for _, row in country_rows)
country_years = {}
for _, row in country_rows:
    country_years.setdefault(row["Code"], set()).add(int(row["Year"]))
complete_panel = {code for code, present in country_years.items() if present == set(years)}
metadata = json.loads(METADATA.read_text(encoding="utf-8"))
column_metadata = metadata["columns"][value_column]
processed = ROOT / "processed"
processed.mkdir(exist_ok=True)
fields = ["country", "country_code", "year", "investment_usd_2021", "investment_usd_2021_bn", "has_observation_every_year", "source_row", "source_file", "source_url"]
with (processed / "ai_investment_country_year_2016_2025.csv").open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=fields)
    writer.writeheader()
    for line, row in sorted(country_rows, key=lambda item: (item[1]["Code"], int(item[1]["Year"]))):
        value = Decimal(row[value_column])
        writer.writerow({"country": row["Entity"], "country_code": row["Code"], "year": int(row["Year"]), "investment_usd_2021": str(value), "investment_usd_2021_bn": format(value / Decimal(1000000000), ".9f"), "has_observation_every_year": str(row["Code"] in complete_panel).lower(), "source_row": line, "source_file": RAW.name, "source_url": SOURCE_URL})
coverage = []
for year in years:
    subset = [row for _, row in country_rows if int(row["Year"]) == year]
    country_sum = sum((Decimal(row[value_column]) for row in subset), Decimal(0))
    world = next(Decimal(row[value_column]) for row in rows if row["Entity"] == "World" and int(row["Year"]) == year)
    difference = country_sum - world
    assert abs(difference) <= len(subset), "Country sum and World differ beyond integer-rounding tolerance"
    coverage.append({"year": year, "countries_observed": len(subset), "country_sum_usd_2021": str(country_sum), "owid_world_usd_2021": str(world), "difference_usd_2021": str(difference), "countries_observed_all_years": len(complete_panel)})
with (processed / "coverage_by_year.csv").open("w", encoding="utf-8", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(coverage[0]))
    writer.writeheader()
    writer.writerows(coverage)
validation = {"raw_sha256": hashlib.sha256(RAW.read_bytes()).hexdigest(), "raw_rows": len(rows), "country_rows": len(country_rows), "distinct_countries_or_territories": len(country_years), "years": years, "countries_observed_every_year": len(complete_panel), "aggregate_rows_excluded": len(rows) - len(country_rows), "duplicate_country_years": 0, "negative_values": 0, "blank_values_in_present_rows": 0, "explicit_zero_values_retained": sum(Decimal(row[value_column]) == 0 for _, row in country_rows), "missing_country_years": "Not filled or converted to zero", "unit": column_metadata["unit"], "source_last_updated": column_metadata["lastUpdated"], "retrieval_date": metadata.get("dateDownloaded"), "source_url": SOURCE_URL, "world_reconciliation": coverage}
(processed / "validation.json").write_text(json.dumps(validation, indent=2) + "\n", encoding="utf-8")
print(json.dumps({key: value for key, value in validation.items() if key != "world_reconciliation"}, indent=2))
