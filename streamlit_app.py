import streamlit as st

st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
)

if not st.user.is_logged_in:
    st.header("Please log in to access this page")
    st.button("Log in", on_click=st.login)
    st.stop()

st.sidebar.button("Log out", type="tertiary", on_click=st.logout)

pg = st.navigation(
    {
        "Analytics dashboard": [
            st.Page(
                "streamlit_testing/pages/dashboard/web_metrics/pages/home.py",
                title="Home",
                url_path="/web_metrics_home",
            ),
            st.Page(
                "streamlit_testing/pages/dashboard/web_metrics/pages/summary.py",
                title="Summary",
                url_path="/web_metrics_summary",
            ),
            st.Page(
                "streamlit_testing/pages/dashboard/web_metrics/pages/publications.py",
                title="Publications",
                url_path="/web_metrics_publications",
            ),
            st.Page(
                "streamlit_testing/pages/dashboard/web_metrics/pages/publication_detail.py",
                title="Publication detail",
                url_path="/web_metrics_publication_detail",
            ),
            st.Page(
                "streamlit_testing/pages/dashboard/web_metrics/pages/pages.py",
                title="Pages",
                url_path="/web_metrics_pages",
            ),
            st.Page(
                "streamlit_testing/pages/dashboard/web_metrics/pages/page_detail.py",
                title="Page detail",
                url_path="/web_metrics_page_detail",
            ),
            st.Page(
                "streamlit_testing/pages/dashboard/web_metrics/pages/roadmap.py",
                title="Roadmap",
                url_path="/web_metrics_roadmap",
            ),
            st.Page(
                "streamlit_testing/pages/dashboard/web_metrics/pages/faqs.py",
                title="FAQs",
                url_path="/web_metrics_faqs",
            ),
        ],
    },
)

# APPLY CUSTOM CSS
# Hide pages in sidebar
st.markdown(
    """
        <style>
            a[href$="web_metrics_summary"] {
                display: none;
            }
        </style>
        <style>
            a[href$="web_metrics_page_detail"] {
                display: none;
            }
        </style>
        <style>
            a[href$="web_metrics_publication_detail"] {
                display: none;
            }
        </style>
    """,
    unsafe_allow_html=True
)


# RUN PAGE
pg.run()
