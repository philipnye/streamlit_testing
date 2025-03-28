import os

import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder

import streamlit_testing.pages.dashboard.web_metrics.elements as elements
from streamlit_testing.pages.dashboard.web_metrics.utils import (
    apply_locale_string, format_date, format_date_comparator,
    set_metrics
)

import ds_utils.database_operations as dbo

# HANDLE DIRECT ACCESS
if "url" not in st.query_params:
    elements.raise_page_not_found_message()
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

# SET METRIC TYPE
METRIC_TYPE = "web_traffic"
METRICS, METRIC_AGGREGATIONS, DEFAULT_METRIC = set_metrics(METRIC_TYPE)

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
with open("streamlit_testing/sql/dashboard/web_metrics/page_detail.sql", "r") as file:
    script = file.read()

script_content_metadata = script.split(';')[0]
script_web_traffic = script.split(';')[1]

script_content_metadata = script_content_metadata.replace("''", "'" + st.query_params["url"] + "'")
script_web_traffic = script_web_traffic.replace("''", "'" + st.query_params["url"] + "'")

df_content_metadata = elements.load_data(script_content_metadata, connection)

if df_content_metadata.empty:
    elements.raise_page_not_found_message()
    st.stop()

df_web_traffic = elements.load_data(script_web_traffic, connection)

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
    start_date, end_date = elements.draw_date_range_inputs(
        min_date=df_web_traffic["date"].min(),
        max_date=df_web_traffic["date"].max(),
    )

    # EDIT DATA
    df_web_traffic = df_web_traffic[
        (df_web_traffic["date"] >= start_date) &
        (df_web_traffic["date"] <= end_date)
    ]

    elements.draw_line_chart_section(
        df=df_web_traffic,
        x="date",
        metrics=METRICS,
        default_metric=DEFAULT_METRIC,
    )

    df_web_traffic["date"] = pd.to_datetime(
        df_web_traffic["date"]
    ).dt.strftime("%Y-%m-%d")

    grid_builder = GridOptionsBuilder.from_dataframe(df_web_traffic)
    grid_options = grid_builder.build()

    grid_options["pagination"] = True
    grid_options["paginationPageSize"] = 25
    grid_options["defaultColDef"] = {
        "filter": True,
        "filterParams": {
            "excelMode": "windows",
        },
    }

    column_defs = {column_def["field"]: column_def for column_def in grid_options["columnDefs"]}

    column_defs["date"]["type"] = "date"
    column_defs["date"]["cellClass"] = "ag-right-aligned-cell"
    column_defs["date"]["headerClass"] = "ag-right-aligned-header"
    column_defs["date"]["valueFormatter"] = format_date
    column_defs["date"]["comparator"] = format_date_comparator
    column_defs["date"]["sort"] = "asc"

    for metric in METRICS:
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
