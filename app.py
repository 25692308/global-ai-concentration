"""Minimal shared entrypoint for the uploaded starter repository."""
import streamlit as st

st.set_page_config(page_title="Global AI Concentration", layout="wide")
st.caption("ASSIGNMENT 3 / DATA NARRATIVE STUDIO")
st.title("Global AI Concentration")
st.markdown("## Is AI development becoming concentrated in fewer countries?")
st.write("Explore publications, patents and investment as different views of geographical concentration. Each section contributes evidence toward the same question.")
st.page_link("pages/investments.py", label="Open the Investments dashboard", icon="📊")
st.caption("This starter includes the investment contribution. The other sections can be integrated through the existing pages and modules.")
