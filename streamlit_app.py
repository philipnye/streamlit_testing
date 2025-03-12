import streamlit as st

pg = st.navigation(
    {
        "Web traffic": [
            st.Page(
                "home.py",
                title="Home",
                icon="🏠"
            ),
            st.Page(
                "dashboard_web_summary.py",
                title="Summary",
                icon="📊"
            ),
            st.Page(
                "dashboard_web_bypage.py",
                title="By page",
                icon="📊"
            ),
            st.Page(
                "dashboard_web_pagedetail.py",
                title="Page detail",
                icon="📊"
            )
        ],
    },
)

pg.run()
