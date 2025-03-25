import os

import pandas as pd
from sqlalchemy import engine, exc
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder

from streamlit_testing.pages.dashboard.web_traffic.utils import apply_locale_string

import ds_utils.database_operations as dbo

# HANDLE DIRECT ACCESS
if "url" not in st.query_params:
    st.write("""
        Direct access to this page not developed yet - please navigate here using one of the links
        in the table on the 'By page' page
    """)
    st.stop()

# DISABLE SIDEBAR
st.markdown(
    """
        <style>
            div[data-testid="stSidebarCollapsedControl"]{
                display: none;
            }
            section[data-testid="stSidebar"][aria-expanded="true"]{
                display: none;
            }
        </style>
    """,
    unsafe_allow_html=True
)

# CONNECT TO DATABASE
connection = dbo.connect_sql_db(
    driver="pyodbc",
    driver_version=os.environ["ODBC_DRIVER"],
    dialect="mssql",
    server=os.environ["ODBC_SERVER"],
    database=os.environ["ODBC_DATABASE"],
    authentication=os.environ["ODBC_AUTHENTICATION"],
    username=os.environ["AZURE_CLIENT_ID"],
    password=os.environ["AZURE_CLIENT_SECRET"],
)

# LOAD DATA
with open("streamlit_testing/sql/dashboard/page_detail.sql", "r") as file:
    script = file.read()

script_content_metadata = script.split(';')[0]
script_web_traffic = script.split(';')[1]

script_content_metadata = script_content_metadata.replace("''", "'" + st.query_params["url"] + "'")
script_web_traffic = script_web_traffic.replace("''", "'" + st.query_params["url"] + "'")


@st.cache_data(show_spinner="Loading data...")
def load_data(script: str, _connection: engine.base.Engine) -> pd.DataFrame:
    """Load data from database"""

    try:
        df = pd.read_sql_query(
            sql=script,
            con=_connection,
        )
    except exc.DBAPIError:
        df = pd.read_sql_query(
            sql=script,
            con=_connection,
        )

    return df


df_content_metadata = load_data(script_content_metadata, connection)
df_web_traffic = load_data(script_web_traffic, connection)

# DRAW PAGE HEADER
st.title(df_content_metadata["page_title"].iloc[0])
st.subheader(df_content_metadata["authors"].iloc[0])
st.markdown("https://www.instituteforgovernment.org.uk" + df_content_metadata["partial"].iloc[0])

# DRAW OUTPUT WIDGETS
st.dataframe(
    df_content_metadata[[
        "type", "published_date", "updated_date_alternative", "research_areas", "tags"
    ]].T,
)

tab1, tab2, tab3 = st.tabs(["Metrics", "Traffic sources", "Search terms"])

with tab1:
    metric = st.selectbox(
        label="Metric",
        options=[
            "activeUsers",
            "engagedSessions",
            "screenPageViews",
            "sessions",
            "userEngagementDuration",
        ],
        index=0,
        key="metric",
    )

    start_date = st.date_input(
        label="Start date",
        value=df_web_traffic["date"].min(),
        min_value=df_web_traffic["date"].min(),
        max_value=df_web_traffic["date"].max(),
        key="start_date",
    )
    end_date = st.date_input(
        label="End date",
        value=df_web_traffic["date"].max(),
        min_value=df_web_traffic["date"].min(),
        max_value=df_web_traffic["date"].max(),
        key="end_date",
    )

    # EDIT DATA
    df_web_traffic = df_web_traffic[
        (df_web_traffic["date"] >= start_date) &
        (df_web_traffic["date"] <= end_date)
    ]

    st.line_chart(
        data=df_web_traffic,
        x="date",
        y=metric,
        use_container_width=True,
        x_label=""
    )

    grid_builder = GridOptionsBuilder.from_dataframe(df_web_traffic)
    grid_options = grid_builder.build()

    grid_options["pagination"] = True
    grid_options["paginationPageSize"] = 25

    grid_options["defaultColDef"] = {
        "filter": True,
    }

    column_defs = {column_def["field"]: column_def for column_def in grid_options["columnDefs"]}

    metrics = [
        "activeUsers",
        "engagedSessions",
        "screenPageViews",
        "sessions",
        "userEngagementDuration",
    ]
    for metric in metrics:
        column_defs[metric]["valueFormatter"] = apply_locale_string

    AgGrid(
        df_web_traffic,
        key="ag",
        update_on=[],
        gridOptions=grid_options,
        allow_unsafe_jscode=True,
    )

with tab2:
    st.markdown("Not yet developed")
with tab3:
    st.markdown("Not yet developed")
