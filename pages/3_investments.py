st.caption(f"Coverage: {panel_description}. Shares use the sum of funding in this coverage group, including countries outside the displayed ranking.")
st.caption("Interpretation: source coverage changes across years, recent reporting may be incomplete, and some funding amounts are estimates. A higher top-five share shows greater dominance within recorded funding; it does not establish that fewer countries receive funding.")

explore, verify, sources = st.tabs(["Explore investment", "Verify a number", "Sources and design"])
share_mode = metric == "Share of recorded funding"
field = "share" if share_mode else "investment_usd_2021_bn"
axis_title = "Share of recorded funding" if share_mode else "Funding (billions of constant 2021 US$)"
axis_format = ".0%" if share_mode else ",.0f"

def style_chart(chart):
    return chart.configure_view(strokeWidth=0).configure_axis(labelFontSize=12, titleFontSize=12, gridColor="#e8edf2").configure_legend(labelFontSize=12, titleFontSize=12)

with explore:
    st.subheader(f"1. Country ranking in {selected_year}")
    bars = alt.Chart(ranking.head(top_n)).mark_bar(color="#176b87", cornerRadiusEnd=3).encode(
        x=alt.X(f"{field}:Q", title=axis_title, axis=alt.Axis(format=axis_format), scale=alt.Scale(domain=[0, 1]) if share_mode else alt.Scale(zero=True)),
        y=alt.Y("country:N", sort=alt.SortField(field="investment_usd_2021", order="descending"), title=None),
        tooltip=[alt.Tooltip("country:N", title="Country / territory"), alt.Tooltip("year:O", title="Year"),
                 alt.Tooltip("investment_usd_2021_bn:Q", title="Funding (2021 US$ bn)", format=",.3f"),
                 alt.Tooltip("share:Q", title="Share of coverage-group funding", format=".2%")],
    ).properties(height=max(240, top_n * 25))
    st.altair_chart(style_chart(bars), width="stretch")
    st.caption("Changing the number of bars changes only the display. The share denominator still includes every country in the selected coverage group.")

    st.subheader("2. Follow countries over time")
    choices = sorted(panel["country"].unique().tolist())
    defaults = [name for name in ["United States", "China", "United Kingdom", "Australia"] if name in choices]
    if "inv_compare" not in st.session_state:
        st.session_state["inv_compare"] = defaults
    else:
        st.session_state["inv_compare"] = [name for name in st.session_state["inv_compare"] if name in choices]
    selected_countries = st.multiselect("Compare up to five countries", choices, max_selections=5, key="inv_compare")
    if selected_countries:
        trends = comparison_series(panel, selected_countries, *period)
        observed = trends.dropna(subset=["investment_usd_2021"])
        if observed.empty:
            st.info("No observations are available for these countries in this period.")
        else:
            lines = alt.Chart(observed).mark_line(point=True, strokeWidth=2.5).encode(
                x=alt.X("year:O", title="Year", axis=alt.Axis(labelAngle=0), scale=alt.Scale(domain=list(range(period[0], period[1] + 1)))),
                y=alt.Y(f"{field}:Q", title=axis_title, axis=alt.Axis(format=axis_format), scale=alt.Scale(domain=[0, 1]) if share_mode else alt.Scale(zero=True)),
                color=alt.Color("country:N", title="Country / territory", scale=alt.Scale(scheme="tableau10")),
                detail=alt.Detail("segment:O"),
                tooltip=[alt.Tooltip("country:N", title="Country"), alt.Tooltip("year:O", title="Year"),
                         alt.Tooltip("investment_usd_2021_bn:Q", title="Funding (2021 US$ bn)", format=",.3f"),
                         alt.Tooltip("share:Q", title="Share of coverage-group funding", format=".2%")],
            ).properties(height=310)
            st.altair_chart(style_chart(lines), width="stretch")
            trend_values = observed[
                ["country", "year", "investment_usd_2021_bn", "share"]
            ].sort_values(["country", "year"]).copy()
            trend_values["share"] *= 100
            st.caption("Values for the selected countries and years")
            st.dataframe(
                trend_values,
                hide_index=True,
                width="stretch",
                column_config={
                    "country": "Country or territory",
                    "year": st.column_config.NumberColumn("Year", format="%d"),
                    "investment_usd_2021_bn": st.column_config.NumberColumn(
                        "Funding (constant 2021 US$ bn)", format="%.3f"
                    ),
                    "share": st.column_config.NumberColumn(
                        "Share of recorded funding (%)", format="%.2f"
                    ),
                },
            )
        missing = int(trends["investment_usd_2021"].isna().sum())
        st.caption(f"{missing} selected country-year observations are unavailable. Lines break across missing years; missing observations are not converted to zero. Selecting countries does not change the share denominator.")
    else:
        st.info("Select at least one country to draw the comparison chart.")

    st.subheader("3. How much do the leading five receive?")
    time_summary = summary.loc[summary["year"].between(*period)]
    concentration = alt.Chart(time_summary).mark_line(point=alt.OverlayMarkDef(color="#b65c20", filled=True), color="#b65c20", strokeWidth=3).encode(
        x=alt.X("year:O", title="Year", axis=alt.Axis(labelAngle=0)),
        y=alt.Y("top5_share:Q", title="Top five countries' share", axis=alt.Axis(format=".0%"), scale=alt.Scale(domain=[0, 1])),
        tooltip=[alt.Tooltip("year:O", title="Year"), alt.Tooltip("top5_share:Q", title="Top-five share", format=".2%"),
                 alt.Tooltip("countries_observed:Q", title="Countries / territories recorded")],
    ).properties(height=230)
    st.altair_chart(style_chart(concentration), width="stretch")
    first, last = time_summary.iloc[0], time_summary.iloc[-1]
    if len(time_summary) > 1:
        change = (last["top5_share"] - first["top5_share"]) * 100
        direction = "higher" if change > 0 else "lower" if change < 0 else "unchanged"
        st.markdown(f"In this coverage group, the leading five accounted for **{first['top5_share']:.1%} in {int(first['year'])}** and **{last['top5_share']:.1%} in {int(last['year'])}**. The end share is **{abs(change):.1f} percentage points {direction}**. Intermediate years can move differently.")
    st.caption("The leading five are re-ranked each year. This is concentration in the funding covered by this dataset. Compare both coverage options before making a claim about change.")
    with st.expander("Country values and coverage"):
        st.dataframe(ranking[["country", "year", "investment_usd_2021", "investment_usd_2021_bn", "share"]], hide_index=True, width="stretch",
                     column_config={"share": st.column_config.NumberColumn("Share (fraction)", format="%.4f")})
        st.dataframe(summary[["year", "countries_observed", "recorded_total_bn", "top5_share"]], hide_index=True, width="stretch")
        st.download_button("Download the exact cleaned dataset", data=data_path.read_bytes(), file_name=DATA_FILE, mime="text/csv", key="inv_download")

with verify:
    st.subheader("Trace a displayed value to its source")
    st.write(f"Choose a country from the {selected_year} ranking. This check reads the original downloaded CSV and compares it with the prepared observation.")
    verify_country = st.selectbox("Country to verify", ranking["country"].tolist(), key="inv_verify_country")
    try:
        trace = trace_observation(panel, verify_country, selected_year)
        st.metric(f"{verify_country}, {selected_year}", f"${trace['value_bn']:,.2f}bn")
        st.caption("Funding received, expressed in billions of constant 2021 US dollars.")
        st.markdown(f"**Original file:** `data/raw/{RAW_FILE}`  \n**Original CSV row:** {trace['source_row']} (header is row 1)")
        st.dataframe(pd.DataFrame([trace["source_record"]]), hide_index=True, width="stretch")
        st.code(f"{trace['value_usd']:,} / 1,000,000,000 = {trace['value_bn']:.9f} billion\nRounded display = {trace['value_bn']:,.2f} billion", language="text")
        st.success("The country, year and dollar amount match the original source row.")
        with st.expander("Verify the country's share"):
            st.code(f"Country funding / sum of all country funding in the selected coverage group\n= {trace['value_usd']:,} / {trace['denominator_usd']:,}\n= {trace['share'] * 100:.6f}%", language="text")
            st.caption(f"Denominator uses {panel_description}. It does not include regional or World rows.")
    except (OSError, ValueError, KeyError, IndexError) as error:
        st.error(f"Source verification could not be completed: {error}")
    st.markdown(f"[Open the source page]({SOURCE_URL}) · [Read the original methodology]({METHOD_URL})")

with sources:
    st.subheader("Sources, scope and limitations")
    st.markdown(f"**Data:** [Our World in Data, CSET-based investment series]({SOURCE_URL}).  \n**Original methodology:** [Emerging Technology Observatory, Georgetown University]({METHOD_URL}).")
    try:
        metadata = load_source_metadata()
        column = next(iter(metadata["columns"].values()))
        st.caption(f"Source last updated: {column['lastUpdated']}. Downloaded snapshot: {metadata['dateDownloaded']}.")
    except (OSError, KeyError, ValueError):
        st.caption("Source metadata is unavailable. Retain the original metadata JSON alongside the raw CSV.")
    st.write("CSET estimates funding from external equity transactions into privately held AI-related companies, including venture capital, private equity and mergers and acquisitions. Some transaction values are estimated when undisclosed. Country attribution follows recipient-company headquarters.")
    st.write("The series excludes recipients listed on public exchanges, internal corporate R&D and infrastructure spending, grants, debt and crowdfunding. It does not measure all AI investment or the nationality of the investors.")
    st.write("OWID has already adjusted values into constant 2021 US dollars using the US CPI. Preparation retains those values, removes regional/global rows, standardises columns and divides by one billion for the display unit.")
    st.warning(f"Coverage varies by year. The full snapshot contains {data['country_code'].nunique()} countries or territories across {min(years)}–{max(years)}, with {fixed_count} observed every year. The fixed-country option controls observation coverage, not reporting completeness. Recent years may be incomplete; the OWID CSV does not retain CSET's completeness flags. Missing rows remain unavailable.")
    st.subheader("Why these chart forms?")
    st.markdown("**Country comparison: sorted horizontal bars (Magnitude).** They place countries on a common zero baseline and allow precise comparisons. A pie chart was rejected because many small slices and angle comparisons make country differences harder to judge.")
    st.markdown("**Change over time: line charts (Change over time).** Ordered years reveal shifts and reversals. A bump chart was rejected for the funding-share trend because rankings alone can stay the same while funding shares change substantially.")
    st.caption("Citation: Center for Security and Emerging Technology (2026); U.S. Bureau of Labor Statistics (2026), with processing by Our World in Data. See docs/investment_data_notes.md for the full source record.")
