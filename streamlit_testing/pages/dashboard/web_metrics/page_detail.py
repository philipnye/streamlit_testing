import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder

import streamlit_testing.pages.dashboard.web_metrics.elements as elements
from streamlit_testing.pages.dashboard.web_metrics.utils import (
    format_date, compare_dates,
    set_metrics
)

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
(
    METRICS_RAW, METRICS_DISPLAY, METRIC_AGGREGATIONS, METRIC_CALCULATIONS, DEFAULT_METRIC
) = set_metrics(METRIC_TYPE)

# CONNECT TO DATABASE
connection = elements.connect_database()

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
st.title(df_content_metadata["Page title"].iloc[0])
st.subheader(df_content_metadata["Authors"].iloc[0])
st.markdown("https://www.instituteforgovernment.org.uk" + df_content_metadata["URL"].iloc[0])

# DRAW OUTPUT WIDGETS
st.dataframe(
    df_content_metadata[[
        "Content type", "Published date", "Updated date", "Research areas", "Tags"
    ]].T,
)

tab1, tab2, tab3 = st.tabs(["Metrics", "Traffic sources", "Search terms"])

with tab1:
    start_date, end_date = elements.draw_date_range_inputs(
        min_date=df_web_traffic["Date"].min(),
        max_date=df_web_traffic["Date"].max(),
    )

    # EDIT DATA
    df_web_traffic = df_web_traffic[
        (df_web_traffic["Date"] >= start_date) &
        (df_web_traffic["Date"] <= end_date)
    ]

    df_web_traffic = elements.calculate_derived_metrics(df_web_traffic, METRIC_CALCULATIONS)

    df_web_traffic = df_web_traffic[
        ["Date"] + list(METRICS_DISPLAY.keys())
    ]

    elements.draw_line_chart_section(
        df=df_web_traffic,
        x="Date",
        metrics=list(METRICS_DISPLAY.keys()),
        default_metric=DEFAULT_METRIC,
    )

    df_web_traffic["Date"] = pd.to_datetime(
        df_web_traffic["Date"]
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

    column_defs["Date"]["Content type"] = "Date"
    column_defs["Date"]["cellClass"] = "ag-right-aligned-cell"
    column_defs["Date"]["headerClass"] = "ag-right-aligned-header"
    column_defs["Date"]["valueFormatter"] = format_date
    column_defs["Date"]["comparator"] = compare_dates
    column_defs["Date"]["sort"] = "asc"

    for metric, formatter in METRICS_DISPLAY.items():
        column_defs[metric]["valueFormatter"] = formatter

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
