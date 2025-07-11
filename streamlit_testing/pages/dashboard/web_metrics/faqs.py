import os

import streamlit as st

import streamlit_testing.pages.dashboard.web_metrics.elements as elements

# DRAW PAGE HEADER
st.title("Frequently asked questions")
elements.draw_last_updated_badge("2025-07-11")
st.markdown("\n\n")
st.markdown("\n\n")

# PAGE CONTENT
with open("streamlit_testing/pages/dashboard/web_metrics/md/faqs.md", "r", encoding="utf-8") as file:
    content = file.read()

# Replace hardcoded values with environment variables
content = content.replace("{{DS_CONTACT_EMAIL_ADDRESS}}", os.environ["DS_CONTACT_EMAIL_ADDRESS"])
content = content.replace("{{IFG_WEB_ISSUES_FILE_LINK}}", os.environ["IFG_WEB_ISSUES_FILE_LINK"])

st.markdown(content, unsafe_allow_html=True)
