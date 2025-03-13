import streamlit as st

st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed",
)

pg = st.navigation(
    {
        "Web traffic": [
            st.Page(
                "streamlit_testing/pages/home.py",
                title="Home",
                icon="🏠"
            ),
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

pg.run()
