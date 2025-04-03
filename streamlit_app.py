import streamlit as st

st.set_page_config(
    layout="wide",
)

pg = st.navigation(
    {
        "Web traffic": [
            st.Page(
                "streamlit_testing/pages/dashboard/web_metrics/summary.py",
                title="Summary",
                url_path="/web_metrics_summary",
            ),
            st.Page(
                "streamlit_testing/pages/dashboard/web_metrics/by_page.py",
                title="By page",
                url_path="/web_metrics_by_page",
            ),
            st.Page(
                "streamlit_testing/pages/dashboard/web_metrics/page_detail.py",
                title="Page detail",
                url_path="/web_metrics_page_detail",
            ),
            st.Page(
                "streamlit_testing/pages/dashboard/web_metrics/by_output.py",
                title="By output",
                url_path="/web_metrics_by_output",
            ),
        ],
    },
)

# HIDE PAGES IN SIDEBAR
st.markdown(
    """
        <style>
            a[href$="web_metrics_page_detail"]{
                display: none;
            }
        </style>
    """,
    unsafe_allow_html=True
)

pg.run()
