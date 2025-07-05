import streamlit as st

# DRAW PAGE HEADER
st.title("Roadmap")

# PAGE CONTENT
with open("streamlit_testing/pages/dashboard/web_metrics/md/roadmap.md", "r", encoding="utf-8") as file:
    content = file.read()

st.markdown(content)
