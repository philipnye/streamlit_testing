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

# APPLY CUSTOM CSS
# Hide pages in sidebar
st.markdown(
    """
        <style>
            a[href$="web_metrics_page_detail"] {
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
                display: none;
            }
        </style>
    """,
    unsafe_allow_html=True
)

pg.run()
