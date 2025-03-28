import streamlit as st
import streamlit_analytics2 as streamlit_analytics

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
                icon="📊"
            ),
            st.Page(
                "streamlit_testing/pages/dashboard/web_metrics/by_page.py",
                title="By page",
                url_path="/web_metrics_by_page",
                icon="📊"
            ),
            st.Page(
                "streamlit_testing/pages/dashboard/web_metrics/page_detail.py",
                title="Page detail",
                url_path="/web_metrics_page_detail",
                icon="📊"
            ),
            st.Page(
                "streamlit_testing/pages/dashboard/web_metrics/by_output.py",
                title="By output",
                url_path="/web_metrics_by_output",
                icon="📊"
            ),
        ],
    },
)

with streamlit_analytics.track():
    pg.run()
