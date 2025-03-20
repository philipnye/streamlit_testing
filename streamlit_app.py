import streamlit as st
import streamlit_analytics2 as streamlit_analytics

st.set_page_config(
    layout="wide",
)

pg = st.navigation(
    {
        "Web traffic": [
            st.Page(
                "streamlit_testing/pages/dashboard/web_traffic/summary.py",
                title="Summary",
                url_path="/web_traffic_summary",
                icon="📊"
            ),
            st.Page(
                "streamlit_testing/pages/dashboard/web_traffic/by_page.py",
                title="By page",
                url_path="/web_traffic_by_page",
                icon="📊"
            ),
            st.Page(
                "streamlit_testing/pages/dashboard/web_traffic/page_detail.py",
                title="Page detail",
                url_path="/web_traffic_page_detail",
                icon="📊"
            )
        ],
    },
)

with streamlit_analytics.track():
    pg.run()
