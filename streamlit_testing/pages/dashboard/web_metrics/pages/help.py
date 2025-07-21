import os

import streamlit as st

from streamlit_testing.pages.dashboard.web_metrics.definitions import DEFINITIONS
import streamlit_testing.pages.dashboard.web_metrics.elements as elements

# DRAW PAGE HEADER
st.title("Frequently asked questions")
elements.draw_last_updated_badge("2025-07-21")
st.markdown("\n\n")
st.markdown("\n\n")

# CONVERT DEFINITIONS TO HTML
DEFINITIONS = "\n\n".join(
    f"**{key}**: {value}" for key, value in DEFINITIONS.items()
)

# PAGE CONTENT
with open("streamlit_testing/pages/dashboard/web_metrics/pages/md/help_faqs.md", "r", encoding="utf-8") as file:
    content = file.read()

tab1, tab2 = st.tabs(["FAQs", "Definitions"])

with tab1:
    content = content.replace("{{DS_CONTACT_EMAIL_ADDRESS}}", os.environ["DS_CONTACT_EMAIL_ADDRESS"])
    content = content.replace("{{IFG_WEB_ISSUES_FILE_LINK}}", os.environ["IFG_WEB_ISSUES_FILE_LINK"])
    st.markdown(content, unsafe_allow_html=True)

with tab2:
    st.markdown(DEFINITIONS, unsafe_allow_html=True)
