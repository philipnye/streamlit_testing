import streamlit as st

# DRAW PAGE HEADER
st.title("Frequently asked questions")

# PAGE CONTENT
with open("streamlit_testing/pages/dashboard/web_metrics/md/faqs.md", "r", encoding="utf-8") as file:
    content = file.read()

st.markdown(content)
