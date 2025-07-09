import streamlit as st

import streamlit_testing.pages.dashboard.web_metrics.elements as elements

# DRAW PAGE HEADER
st.title("Frequently asked questions")
elements.draw_last_updated_badge("2025-07-09")
st.markdown("\n\n")
st.markdown("\n\n")

# PAGE CONTENT
with open("streamlit_testing/pages/dashboard/web_metrics/md/faqs.md", "r", encoding="utf-8") as file:
    content = file.read()

st.markdown(content)
