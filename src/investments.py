"""Investment data and calculations shared by the Investments page.

This module has no Streamlit dependency. All shares use the complete chosen
country panel for each year, before display filters are applied.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = "ai_investment_country_year_2016_2025.csv"
RAW_FILE = "private-investment-in-artificial-intelligence-cset.csv"
VALUE_COLUMN = "Estimated funding raised by privately held AI companies - Field: All"
SOURCE_URL = "https://ourworldindata.org/grapher/private-investment-in-artificial-intelligence-cset"
METHOD_URL = "https://eto.tech/dataset-docs/country-ai-activity-metrics/"
ALL_COUNTRIES = "All available countries"
FIXED_COUNTRIES = "Countries observed every year"


def load_investments(root: Path = ROOT) -> pd.DataFrame:
    """Load the prepared CSV and reject ambiguous or inconsistent inputs."""
    path = Path(root) / "data" / "processed" / DATA_FILE
    if not path.is_file():
        raise FileNotFoundError(f"Upload {DATA_FILE} into data/processed/.")
    frame = pd.read_csv(path)
    required = {"country", "country_code", "year", "investment_usd_2021", "source_row", "source_file"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"The investment CSV is missing columns: {', '.join(sorted(missing))}")
    if frame.empty or frame[list(required)].isna().any().any():
        raise ValueError("The investment CSV is empty or contains missing required values.")
    if not frame["country_code"].astype(str).str.fullmatch(r"[A-Z]{3}").all():
        raise ValueError("Use the country-only CSV; regional and World rows are not allowed.")
    frame["year"] = pd.to_numeric(frame["year"], errors="raise")
    if not (frame["year"] % 1 == 0).all():
        raise ValueError("Years must be whole numbers.")
    frame["year"] = frame["year"].astype(int)
    frame["investment_usd_2021"] = pd.to_numeric(frame["investment_usd_2021"], errors="raise")
    if not np.isfinite(frame["investment_usd_2021"]).all() or (frame["investment_usd_2021"] < 0).any():
        raise ValueError("Funding amounts must be finite and non-negative.")
    if frame.duplicated(["country_code", "year"]).any():
        raise ValueError("There are duplicate country-year observations.")
    if frame.groupby("country_code")["country"].nunique().gt(1).any():
        raise ValueError("A country code is linked to more than one country name.")
    billions = frame["investment_usd_2021"] / 1_000_000_000
    if "investment_usd_2021_bn" in frame and not np.allclose(
        pd.to_numeric(frame["investment_usd_2021_bn"], errors="raise"), billions, rtol=0, atol=1e-9
    ):
        raise ValueError("The billions column does not match the original dollar values.")
    frame["investment_usd_2021_bn"] = billions
    year_count = frame["year"].nunique()
    counts = frame.groupby("country_code")["year"].nunique()
    consistent_codes = counts[counts.eq(year_count)].index
    frame["has_observation_every_year"] = frame["country_code"].isin(consistent_codes)
    return frame.sort_values(["year", "country_code"]).reset_index(drop=True)


def select_panel(frame: pd.DataFrame, basis: str) -> pd.DataFrame:
    if basis == ALL_COUNTRIES:
        return frame.copy()
    if basis == FIXED_COUNTRIES:
        return frame.loc[frame["has_observation_every_year"]].copy()
    raise ValueError(f"Unknown country-coverage choice: {basis}")


def annual_summary(frame: pd.DataFrame) -> pd.DataFrame:
    """Summarise the entire panel. Top-five membership is re-ranked annually."""
    records = []
    for year, group in frame.groupby("year", sort=True):
        ranked = group.sort_values(["investment_usd_2021", "country"], ascending=[False, True])
        total = int(ranked["investment_usd_2021"].sum())
        leader = ranked.iloc[0]
        records.append({
            "year": int(year), "recorded_total_usd_2021": total,
            "recorded_total_bn": total / 1_000_000_000,
            "countries_observed": int(group["country_code"].nunique()),
            "leader": leader["country"],
            "leader_share": float(leader["investment_usd_2021"] / total) if total else np.nan,
            "top5_share": float(ranked.head(5)["investment_usd_2021"].sum() / total) if total else np.nan,
        })
    return pd.DataFrame(records)


def country_values(frame: pd.DataFrame, year: int) -> pd.DataFrame:
    selected = frame.loc[frame["year"].eq(year)].copy()
    total = selected["investment_usd_2021"].sum()
    selected["share"] = selected["investment_usd_2021"] / total if total else np.nan
    return selected.sort_values(["investment_usd_2021", "country"], ascending=[False, True])


def comparison_series(frame: pd.DataFrame, countries: list[str], start: int, end: int) -> pd.DataFrame:
    """Retain missing country-years and break lines across gaps explicitly."""
    names = list(dict.fromkeys(countries))
    grid = pd.MultiIndex.from_product([names, range(start, end + 1)], names=["country", "year"])
    series = frame.set_index(["country", "year"])[["investment_usd_2021", "investment_usd_2021_bn"]].reindex(grid).reset_index()
    totals = frame.groupby("year")["investment_usd_2021"].sum()
    series["share"] = series["investment_usd_2021"] / series["year"].map(totals).replace(0, np.nan)
    series["segment"] = series.groupby("country", sort=False)["investment_usd_2021"].transform(lambda values: values.isna().cumsum())
    return series


def load_source_metadata(root: Path = ROOT) -> dict:
    path = Path(root) / "data" / "raw" / RAW_FILE.replace(".csv", ".metadata.json")
    return json.loads(path.read_text(encoding="utf-8"))


def trace_observation(frame: pd.DataFrame, country: str, year: int, root: Path = ROOT) -> dict:
    """Trace a prepared observation back to its exact original CSV row."""
    matches = frame.loc[frame["country"].eq(country) & frame["year"].eq(year)]
    if len(matches) != 1:
        raise ValueError("No unique observation exists for that country and year.")
    observation = matches.iloc[0]
    if observation["source_file"] != RAW_FILE:
        raise ValueError("Unexpected source filename in the prepared data.")
    with (Path(root) / "data" / "raw" / RAW_FILE).open(encoding="utf-8-sig", newline="") as handle:
        original = list(csv.DictReader(handle))
    source_row = int(observation["source_row"])
    if not 2 <= source_row <= len(original) + 1:
        raise ValueError("Source-row reference is outside the original CSV.")
    source = original[source_row - 2]
    if (source["Entity"] != country or source["Code"] != observation["country_code"]
            or int(source["Year"]) != year
            or int(source[VALUE_COLUMN]) != int(observation["investment_usd_2021"])):
        raise ValueError("The prepared observation does not match its original source row.")
    total = int(frame.loc[frame["year"].eq(year), "investment_usd_2021"].sum())
    value = int(source[VALUE_COLUMN])
    return {"source_row": source_row, "source_record": source, "value_usd": value,
            "value_bn": value / 1_000_000_000, "denominator_usd": total,
            "share": value / total if total else np.nan, "country": country, "year": year}
