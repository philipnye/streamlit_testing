import streamlit as st

st.set_page_config(
    layout="wide",
)

if not st.user.is_logged_in:
    st.header("Please log in to access this page")
    st.button("Log in", on_click=st.login)
    st.stop()

st.sidebar.button("Log out", type="tertiary", on_click=st.logout)

pg = st.navigation(
    {
        "Web traffic": [
            st.Page(
                "streamlit_testing/pages/dashboard/web_metrics/home.py",
                title="Home",
                url_path="/web_metrics_home",
            ),
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
            st.Page(
                "streamlit_testing/pages/dashboard/web_metrics/faqs.py",
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
            a[href$="web_metrics_page_detail"] {
                display: none;
            }
        </style>
        <style>
            a[href$="summary"] {
                display: none;
            }
        </style>
    """,
    unsafe_allow_html=True
)

# Disable watermark
# NB: Done as a workaround until this issue is fixed: https://github.com/PablocFonseca/streamlit-aggrid/issues/313
st.markdown(
    """
        <style>
            div.ag-watermark {
                display: none !important;
                opacity: 0 !important;
            }
            div.ag-watermark::before {
                display: none !important;
                opacity: 0 !important;
            }
        </style>
    """,
    unsafe_allow_html=True
)

pg.run()
