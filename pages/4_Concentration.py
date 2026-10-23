"""Section 4 — cross-domain AI concentration, with source-to-number audit.

From repository root:
    python src/concentration.py
    python -m streamlit run pages/4_Concentration.py
"""
from pathlib import Path
import sys

import altair as alt
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.concentration import (  # noqa: E402
    RAW, PUBLICATIONS_FILENAME, concentration_by_year,
    load_investments, load_patents, load_publications,
)

METRICS_PATH = ROOT / 'data' / 'processed' / 'concentration_metrics.csv'
BALANCED = 'Investments (balanced panel)'
ORDER = ['Publications', 'Patents', 'Investments']


@st.cache_data(show_spinner=False)
def load_metrics(path: str, modified: float) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {
        'domain', 'year', 'hhi', 'top3_share', 'countries_observed',
        'countries_positive', 'observed_total',
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f'Missing metric columns: {sorted(missing)}')
    df['year'] = pd.to_numeric(df['year'], errors='raise').astype(int)
    for col in required - {'domain', 'year'}:
        df[col] = pd.to_numeric(df[col], errors='raise')
    if df[list(required)].isna().any().any() or df.duplicated(['domain', 'year']).any():
        raise ValueError('Missing metric values or duplicate domain/year records')
    if not (df.hhi.between(0, 1).all() and df.top3_share.between(0, 1).all()):
        raise ValueError('HHI and top-3 share must lie between 0 and 1')
    return df.sort_values(['domain', 'year']).reset_index(drop=True)


def line_chart(df: pd.DataFrame, measure: str, title: str, *, percent=False,
               endpoints=True, height=315):
    """Line chart with end labels placed INSIDE the plot to avoid clipping."""
    fmt = '.1%' if percent else (',.0f' if measure == 'countries_observed' else '.3f')
    x = alt.X('year:O', title='Year', sort='ascending', axis=alt.Axis(labelAngle=0))
    y = alt.Y(f'{measure}:Q', title=title, scale=alt.Scale(zero=False),
              axis=alt.Axis(format=fmt))
    color = alt.Color('domain:N', title='Dataset / analysis')
    tooltips = [
        alt.Tooltip('domain:N', title='Dataset'),
        alt.Tooltip('year:O', title='Year'),
        alt.Tooltip(f'{measure}:Q', title=title, format=fmt),
        alt.Tooltip('countries_observed:Q', title='Observed countries', format=',.0f'),
    ]
    base = alt.Chart(df).encode(x=x, y=y, color=color)
    line = base.mark_line(point=True).encode(tooltip=tooltips)
    if not endpoints:
        return line.properties(height=height).interactive()

    last_rows = (df.sort_values('year')
                 .groupby('domain', as_index=False).tail(1).copy())
    end_labels = (alt.Chart(last_rows)
                  .mark_text(align='right', baseline='bottom', dx=-9, dy=-8,
                             fontSize=11, fontWeight='bold')
                  .encode(x=x, y=y, color=color,
                          text=alt.Text(f'{measure}:Q', format=fmt)))
    return (line + end_labels).properties(
        height=height, padding={'left': 10, 'right': 20, 'top': 24, 'bottom': 10}
    ).interactive()


def trend_description(start: float, end: float, measure: str) -> str:
    change = end - start
    if measure == 'hhi':
        magnitude = f'{abs(change):.3f} HHI points'
    else:
        magnitude = f'{abs(change) * 100:.1f} percentage points'
    if abs(change) < 1e-10:
        return 'was unchanged'
    return f'{"increased" if change > 0 else "decreased"} by {magnitude}'


def render_narrative(view: pd.DataFrame) -> None:
    """Interpret ONLY the actual years/domains selected by the user."""
    st.markdown('### What do these trends tell us?')
    st.caption('The following comparisons update with the dataset and year filters.')
    for domain in ORDER:
        rows = view.loc[view.domain == domain].sort_values('year')
        if rows.empty:
            continue
        first, last = rows.iloc[0], rows.iloc[-1]
        if len(rows) == 1:
            st.markdown(
                f'**{domain} ({int(last.year)}):** HHI = {last.hhi:.3f}; '
                f'Top-3 share = {last.top3_share:.1%}. '
                'Select at least two years to assess a trend.'
            )
            continue
        st.markdown(
            f'**{domain} ({int(first.year)}–{int(last.year)}):** '
            f'HHI {trend_description(first.hhi, last.hhi, "hhi")} '
            f'({first.hhi:.3f} → {last.hhi:.3f}), while the top-three share '
            f'{trend_description(first.top3_share, last.top3_share, "top3_share")} '
            f'({first.top3_share:.1%} → {last.top3_share:.1%}).'
        )
    st.info(
        'Interpretation: The measures describe geographic concentration in '
        'the observed country-attributed values, not all dimensions of AI capability. '
        'An endpoint comparison does not imply a steady year-by-year trend.'
    )
    st.caption(
        'Comparability limitation: Publications, patents and investments have '
        'different definitions, country coverage and attribution methods. '
        'Their absolute HHI levels should not be treated as directly comparable. '
        'Missing country-years are not assumed to be zero.'
    )


@st.cache_data(show_spinner=False)
def audit_source(domain: str, year: int, mtime: float):
    loaders = {
        'Patents': load_patents,
        'Investments': load_investments,
        'Publications': load_publications,
    }
    source = loaders[domain]()
    rows = source.loc[
        source.year == year,
        ['country', 'country_code', 'year', 'value', 'domain'],
    ].copy()
    if rows.empty:
        raise ValueError(f'No raw country data for {domain} {year}')
    total = rows.value.sum()
    if total <= 0:
        raise ValueError('Observed total must be positive')
    rows['share'] = rows.value / total
    rows['hhi_contribution'] = rows.share ** 2
    rows = rows.sort_values(
        ['value', 'country_code'], ascending=[False, True]
    ).reset_index(drop=True)
    rows['rank'] = range(1, len(rows) + 1)
    recomputed = concentration_by_year(source, year, year).iloc[0]
    return rows, recomputed


st.set_page_config(page_title='AI Concentration Analysis', layout='wide')
st.title('Section 4 · AI Concentration Analysis')
st.markdown('**Research question:** Is AI development becoming concentrated in fewer countries?')
st.write(
    'Compare geographic concentration in AI publications, patents, and '
    'private investment using country-attributed measures.'
)

if not METRICS_PATH.exists():
    st.error('Metrics not found. From the project root, run: `python src/concentration.py`')
    st.stop()
try:
    metrics = load_metrics(str(METRICS_PATH), METRICS_PATH.stat().st_mtime)
except (ValueError, pd.errors.ParserError) as e:
    st.error(f'Invalid metrics file: {e}')
    st.stop()

available = [x for x in ORDER if x in set(metrics.domain)]
if not available:
    st.error('No domain metrics available.')
    st.stop()

with st.sidebar:
    st.header('Concentration filters')
    selected = st.multiselect('Datasets', available, default=available)
    low, high = int(metrics.year.min()), int(metrics.year.max())
    years = st.slider('Year range', low, high, (low, high)) if low < high else (low, high)
    st.caption('Investment sensitivity is shown separately below.')

if not selected:
    st.info('Choose at least one dataset.')
    st.stop()
view = metrics.loc[
    metrics.domain.isin(selected) & metrics.year.between(*years)
].copy()
if view.empty:
    st.warning('No data for the selected years and datasets.')
    st.stop()

st.caption(
    'Shares use each domain/year’s sum of observed country-attributed values; '
    'this is not necessarily a global unique-item denominator.'
)
st.subheader('Latest available concentration')
cols = st.columns(len(selected))
for col, domain in zip(cols, selected):
    rows = view.loc[view.domain == domain].sort_values('year')
    with col:
        if rows.empty:
            st.info(f'No {domain} data in the selected range.')
            continue
        r = rows.iloc[-1]
        st.markdown(f'**{domain} · {int(r.year)}**')
        st.metric('HHI (0–1)', f'{r.hhi:.3f}')
        st.metric('Top-3 country share', f'{r.top3_share:.1%}')
        st.caption(f'Observed countries: {int(r.countries_observed)}')

st.subheader('1. How has concentration changed?')
st.altair_chart(line_chart(view, 'hhi', 'HHI (0–1)'), use_container_width=True)
st.caption(
    'End labels show the latest selected value for each series. '
    'Higher HHI indicates greater concentration among observed country-attributed values.'
)

st.subheader('2. How much do the top three countries account for?')
st.altair_chart(
    line_chart(view, 'top3_share', 'Top-3 country share', percent=True),
    use_container_width=True,
)
st.caption(
    'The top three countries are recalculated independently each year. '
    'A country can enter or leave the top three.'
)

render_narrative(view)

st.subheader('3. How does country coverage change?')
st.altair_chart(
    line_chart(view, 'countries_observed', 'Observed countries', height=245),
    use_container_width=True,
)
st.caption(
    'Recorded zeros count as observed; absent country–years are not imputed as zero. '
    'This plot reports source coverage, not the number of countries with positive values.'
)

st.subheader('4. Investment coverage sensitivity')
if {'Investments', BALANCED}.issubset(set(metrics.domain)):
    sensitivity = metrics.loc[
        metrics.domain.isin(['Investments', BALANCED])
        & metrics.year.between(*years)
    ].copy()
    # Short, presentation-friendly legend names; underlying metrics remain unchanged.
    sensitivity_plot = sensitivity.copy()
    sensitivity_plot['domain'] = sensitivity_plot['domain'].replace({
        'Investments': 'Observed panel',
        BALANCED: 'Balanced panel',
    })
    st.altair_chart(
        line_chart(sensitivity_plot, 'hhi', 'Investment HHI (0–1)', endpoints=False),
        use_container_width=True,
    )
    wide = sensitivity.pivot(index='year', columns='domain', values='hhi').dropna()
    if not wide.empty:
        wide['difference'] = wide['Investments'] - wide[BALANCED]
        last = wide.iloc[-1]
        c1, c2, c3 = st.columns(3)
        c1.metric(f'Observed panel HHI · {int(wide.index[-1])}', f'{last["Investments"]:.6f}')
        c2.metric(f'Balanced panel HHI · {int(wide.index[-1])}', f'{last[BALANCED]:.6f}')
        c3.metric(
            'HHI difference', f'{last["difference"]:+.6f}',
            help='Observed-panel HHI minus balanced-panel HHI.',
        )
        st.caption(
            f'Maximum absolute HHI difference in selected years: '
            f'{wide.difference.abs().max():.6f}.'
        )
        with st.expander('View year-by-year sensitivity differences'):
            st.dataframe(
                wide.reset_index().rename(columns={'year': 'Year'}),
                hide_index=True, use_container_width=True,
            )
    st.caption(
        'Balanced panel includes only countries observed in every year of the '
        'original 2016–2024 period. It does not change when the year slider changes. '
        'Similar results are a robustness check, not proof of complete global coverage.'
    )
else:
    st.info('Balanced-panel investment metrics are unavailable.')

st.subheader('5. Verify a number — from raw country values')
verify_domain = st.selectbox('Dataset to inspect', selected, key='verify_domain')
subset = view.loc[view.domain == verify_domain].sort_values('year')
verify_year = st.selectbox(
    'Year to inspect', subset.year.astype(int).tolist(), index=len(subset) - 1,
)
reported = subset.loc[subset.year == verify_year].iloc[0]
source_path = {
    'Patents': RAW / 'Evolution of AI-related patents by country.csv',
    'Investments': RAW / 'ai_investment_country_year_2016_2025.csv',
    'Publications': RAW / PUBLICATIONS_FILENAME,
}[verify_domain]

if not source_path.exists():
    st.error(f'Raw source file not found: {source_path.name}. Cannot independently verify this metric.')
else:
    try:
        country_rows, recomputed = audit_source(
            verify_domain, int(verify_year), source_path.stat().st_mtime,
        )
    except (ValueError, KeyError, pd.errors.ParserError) as e:
        st.error(f'Unable to audit the raw data: {e}')
    else:
        st.latex(
            r's_{i,t}=\frac{x_{i,t}}{\sum_j x_{j,t}},\quad '
            r'HHI_t=\sum_i s_{i,t}^2,\quad '
            r'Top3_t=\sum_{i\in\mathrm{Top3}_t}s_{i,t}'
        )
        st.write(
            f'**{verify_domain} · {verify_year}** — observed country total: '
            f'**{country_rows.value.sum():,.2f}**; '
            f'observed countries: **{len(country_rows)}**.'
        )
        st.write(
            'Country contributions are ranked by their recorded value. '
            'The full downloadable table contains every observed country.'
        )
        # Presentation-only formatting; country_rows and the CSV export stay exact.
        display = country_rows[
            ['rank', 'country', 'country_code', 'value', 'share', 'hhi_contribution']
        ].head(10).copy()
        if verify_domain == 'Investments':
            display['value'] = display['value'] / 1_000_000_000
            value_label = 'Investment (USD bn)'
            value_format = '%.2f'
        else:
            value_label = 'Value'
            value_format = '%.0f'
        display = display.rename(columns={'value': value_label})
        st.dataframe(
            display, hide_index=True, use_container_width=True,
            column_config={
                value_label: st.column_config.NumberColumn(
                    value_label, format=value_format,
                    help=('Billions of constant 2021 US dollars.'
                          if verify_domain == 'Investments'
                          else 'Original country-level recorded value.'),
                ),
                'share': st.column_config.NumberColumn('Country share', format='%.5f'),
                'hhi_contribution': st.column_config.NumberColumn(
                    'HHI contribution', format='%.6f'
                ),
            },
        )
        hhi_calc = country_rows.hhi_contribution.sum()
        top3_calc = country_rows.head(3).share.sum()
        a, b = st.columns(2)
        a.metric('Recomputed HHI = Σ country share²', f'{hhi_calc:.6f}')
        b.metric('Recomputed Top-3 share = Σ top 3 shares', f'{top3_calc:.2%}')
        matches = (
            abs(hhi_calc - reported.hhi) < 1e-9
            and abs(top3_calc - reported.top3_share) < 1e-9
            and abs(country_rows.value.sum() - reported.observed_total)
            < max(1e-6, abs(reported.observed_total) * 1e-10)
        )
        if matches:
            st.success(
                'PASS — independently recomputed values match the processed CSV '
                f'(HHI {reported.hhi:.6f}; Top-3 {reported.top3_share:.2%}).'
            )
        else:
            st.error(
                'MISMATCH — raw recomputation differs from processed metrics. '
                'Regenerate metrics and inspect preprocessing before presenting these numbers.'
            )
        st.download_button(
            'Download full country contribution audit (CSV)',
            country_rows.to_csv(index=False).encode('utf-8'),
            file_name=f'concentration_audit_{verify_domain.lower()}_{verify_year}.csv',
            mime='text/csv',
        )

with st.expander('Data sources, methodology and limitations'):
    st.markdown('''
**Publications:** Our World in Data, *Annual scholarly publications on artificial intelligence*.
Country-attributed publications may be counted in more than one country when authors
have affiliations across countries.
[OWID data](https://ourworldindata.org/grapher/annual-scholarly-publications-on-artificial-intelligence).

**Patents:** OECD.AI, AI-related PCT applications by priority date and inventor location.
The pipeline excludes `ALL`, `OECD`, and `EU27` aggregate rows.
[OECD.AI](https://oecd.ai/en/data) ·
[Methodology](https://www.oecd.org/en/publications/identifying-emerging-ai-technologies-using-patent-data_d17e9a1a-en.html).

**Investments:** Our World in Data / CSET, estimated funding raised by privately held
AI companies in constant 2021 USD.
[OWID data](https://ourworldindata.org/grapher/private-investment-in-artificial-intelligence-cset).

**Scope and interpretation:** HHI uses the 0–1 scale. Values are shares of
*observed, country-attributed totals*, not necessarily shares of a unique global total.
Country coverage, data definitions, and attribution methods differ by domain.
Missing country–years are not automatically zeros. The balanced panel is a
sensitivity analysis, not a correction for all source limitations.
Differences between domains should be interpreted cautiously.
''')

st.subheader('Processed metrics')
st.dataframe(view, hide_index=True, use_container_width=True)
st.download_button(
    'Download selected metrics (CSV)',
    view.to_csv(index=False).encode('utf-8'),
    file_name='concentration_metrics_filtered.csv', mime='text/csv',
)
