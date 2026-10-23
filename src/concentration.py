"""Reproducible country-level AI concentration calculations.

Input files are the team's cleaned investment data and OECD.AI patent export.
Missing country-years are never automatically imputed as zero.
"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
AGGREGATE_CODES = {"ALL", "OECD", "EU27"}


def _check_columns(df: pd.DataFrame, required: set[str], label: str) -> None:
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{label}: missing columns {sorted(missing)}")


def _validate_country_year(df: pd.DataFrame, label: str) -> pd.DataFrame:
    df = df.copy()
    if df[["year", "country_code", "value"]].isna().any().any():
        raise ValueError(f"{label}: missing year, country_code, or value")
    df["year"] = pd.to_numeric(df["year"], errors="raise").astype(int)
    df["value"] = pd.to_numeric(df["value"], errors="raise")
    if (df["value"] < 0).any():
        raise ValueError(f"{label}: negative values detected")
    if df.duplicated(["year", "country_code"]).any():
        raise ValueError(f"{label}: duplicate year/country_code combinations")
    return df


def load_patents(path: Path = RAW / "Evolution of AI-related patents by country.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    _check_columns(df, {"year", "Country/territory", "Country/territory_label", "AI_counts"}, "Patents")
    df = df.loc[~df["Country/territory"].isin(AGGREGATE_CODES)].copy()
    df = df.rename(columns={
        "Country/territory": "country_code",
        "Country/territory_label": "country",
        "AI_counts": "value",
    })[["year", "country_code", "country", "value"]]
    df["domain"] = "Patents"
    return _validate_country_year(df, "Patents")


def load_investments(path: Path = RAW / "ai_investment_country_year_2016_2025.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    _check_columns(df, {"year", "country_code", "country", "investment_usd_2021"}, "Investments")
    df = df.rename(columns={"investment_usd_2021": "value"})[
        ["year", "country_code", "country", "value"]
    ]
    df["domain"] = "Investments"
    return _validate_country_year(df, "Investments")


def concentration_by_year(df: pd.DataFrame, start_year: int = 2016, end_year: int = 2024) -> pd.DataFrame:
    """Compute HHI and Top-3 share over observed countries for each domain/year.

    HHI = sum((country value / sum observed values)^2).
    Top-3 share = sum of the three largest observed shares.
    These are observed-country metrics, not necessarily world-coverage metrics.
    """
    _check_columns(df, {"year", "country_code", "value", "domain"}, "Concentration input")
    data = df.loc[df["year"].between(start_year, end_year)].copy()
    if data.duplicated(["domain", "year", "country_code"]).any():
        raise ValueError("Duplicate domain/year/country rows")
    results = []
    for (domain, year), group in data.groupby(["domain", "year"], sort=True):
        if group["value"].isna().any() or (group["value"] < 0).any():
            raise ValueError(f"Invalid values for {domain} {year}")
        total = group["value"].sum()
        if total <= 0:
            raise ValueError(f"No positive total for {domain} {year}")
        shares = group["value"] / total
        results.append({
            "domain": domain,
            "year": int(year),
            "hhi": float((shares ** 2).sum()),
            "top3_share": float(shares.nlargest(3).sum()),
            "countries_observed": int(group["country_code"].nunique()),
            "countries_positive": int((group["value"] > 0).sum()),
            "observed_total": float(total),
        })
    return pd.DataFrame(results).sort_values(["domain", "year"]).reset_index(drop=True)


def investment_balanced_panel(df: pd.DataFrame, start_year: int = 2016, end_year: int = 2024) -> pd.DataFrame:
    """Return only countries with an explicit observation in every selected year."""
    data = df.loc[df["year"].between(start_year, end_year)].copy()
    years = set(range(start_year, end_year + 1))
    if set(data["year"].unique()) != years:
        raise ValueError("Investment data does not contain every requested year")
    counts = data.groupby("country_code")["year"].nunique()
    eligible = counts[counts == len(years)].index
    return data.loc[data["country_code"].isin(eligible)].copy()


def build_outputs(start_year: int = 2016, end_year: int = 2024) -> pd.DataFrame:
    patents = load_patents()
    investments = load_investments()
    combined = pd.concat([patents, investments], ignore_index=True)
    metrics = concentration_by_year(combined, start_year, end_year)
    balanced = investment_balanced_panel(investments, start_year, end_year)
    balanced_metrics = concentration_by_year(balanced, start_year, end_year)
    balanced_metrics["domain"] = "Investments (balanced panel)"
    metrics = pd.concat([metrics, balanced_metrics], ignore_index=True)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(PROCESSED / "concentration_metrics.csv", index=False)
    print(metrics.to_string(index=False))
    print(f"\nSaved: {PROCESSED / 'concentration_metrics.csv'}")
    return metrics



# Optional publications integration (OWID Grapher CSV). Do not silently
# substitute an unverified data source if the publication file is absent.
PUBLICATIONS_FILENAME = 'annual-scholarly-publications-on-artificial-intelligence.csv'
PUBLICATIONS_URL = (
    'https://ourworldindata.org/grapher/'
    'annual-scholarly-publications-on-artificial-intelligence.csv'
    '?v=1&csvType=full&useColumnShortNames=true'
)


def load_publications(
    path: Path = RAW / PUBLICATIONS_FILENAME
) -> pd.DataFrame:
    """Load country-level AI publication counts from OWID."""

    source = pd.read_csv(path)

    required = {
        "entity",
        "code",
        "year",
        "num_articles__field_all",
    }
    _check_columns(source, required, "Publications")

    source = source.rename(columns={
        "entity": "country",
        "code": "country_code",
        "num_articles__field_all": "value",
    })[
        ["year", "country_code", "country", "value"]
    ].copy()

    # Exclude aggregate and non-country codes.
    source["country_code"] = source["country_code"].astype("string")
    source = source.loc[
        source["country_code"].str.fullmatch(
            r"[A-Z]{3}", na=False
        )
    ].copy()

    # Keep valid observations only.
    source = source.dropna(subset=["value"])

    source["domain"] = "Publications"

    return _validate_country_year(source, "Publications")


def build_outputs_complete(start_year: int = 2016, end_year: int = 2024) -> pd.DataFrame:
    """Rebuild metrics, optionally including the team's OWID publication CSV."""
    patents = load_patents()
    investments = load_investments()
    datasets = [patents, investments]
    pub_path = RAW / PUBLICATIONS_FILENAME
    if pub_path.exists():
        datasets.append(load_publications(pub_path))
        print(f'Publications loaded from: {pub_path}')
    else:
        print(f'Publications not yet integrated: place the OWID CSV at {pub_path}')
    metrics = concentration_by_year(pd.concat(datasets, ignore_index=True), start_year, end_year)
    balanced = investment_balanced_panel(investments, start_year, end_year)
    balanced_metrics = concentration_by_year(balanced, start_year, end_year)
    balanced_metrics['domain'] = 'Investments (balanced panel)'
    metrics = pd.concat([metrics, balanced_metrics], ignore_index=True)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(PROCESSED / 'concentration_metrics.csv', index=False)
    print(f'Saved: {PROCESSED / "concentration_metrics.csv"} ({len(metrics)} rows)')
    return metrics

if __name__ == "__main__":
    build_outputs_complete()
