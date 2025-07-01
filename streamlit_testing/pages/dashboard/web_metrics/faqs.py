import streamlit as st

# DRAW PAGE HEADER
st.title("Frequently asked questions")

# FAQ CONTENT
with open("streamlit_testing/pages/dashboard/web_metrics/md/faqs.md", "r") as file:
    faq_content = file.read()

st.markdown(faq_content)
