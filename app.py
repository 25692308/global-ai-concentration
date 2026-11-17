"""Group 15 landing page with main-content navigation to the four sections."""

from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="The Rise of AI | Group 15",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Resolve script availability from the project root, not the working directory.
ROOT = Path(__file__).resolve().parent

st.title("The Rise of Artificial Intelligence")
st.subheader("Geographic Concentration")
st.caption("UTS 36104 · Data Visualisation and Narratives · Group 15")

st.markdown("### Research question")
st.markdown("**Is AI development becoming concentrated in fewer countries?**")
st.write(
    "Explore geographic patterns in AI scholarly publications, AI-related "
    "patents, and private AI investment, then compare country-level "
    "concentration across these domains."
)

st.markdown("### Explore the narrative")

sections = [
    {
        "title": "01 · AI Publications",
        "description": "Explore where AI scholarly publications are recorded.",
        "path": "pages/1_Publications.py",
    },
    {
        "title": "02 · AI Patents",
        "description": "Explore the distribution of AI-related patent activity.",
        "path": "pages/2_Patents.py",
    },
    {
        "title": "03 · Private AI Investment",
        "description": "Explore where private AI investment is recorded.",
        "path": "pages/investments.py",
    },
    {
        "title": "04 · Geographic Concentration",
        "description": "Compare country shares, HHI, Top-3 shares, and investment coverage.",
        "path": "pages/4_Concentration.py",
    },
]

for row_start in (0, 2):
    columns = st.columns(2, gap="medium")
    for column, section in zip(columns, sections[row_start : row_start + 2]):
        with column:
            with st.container(border=True):
                st.markdown(f"#### {section['title']}")
                st.write(section["description"])
                available = (ROOT / section["path"]).is_file()
                if st.button(
                    "Explore section" if available else "Coming soon",
                    key=section["path"],
                    disabled=not available,
                    use_container_width=True,
                ):
                    st.switch_page(section["path"])

st.markdown("### How to interpret the results")
st.write(
    "Source definitions and country coverage differ across publications, "
    "patents, and investment. These comparisons describe recorded activity, "
    "not overall national AI capability."
)
