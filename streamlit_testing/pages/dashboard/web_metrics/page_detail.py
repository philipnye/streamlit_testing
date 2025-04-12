import pandas as pd
import streamlit as st
from st_aggrid import AgGrid

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
elements.disable_sidebar()

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

df_content_metadata = elements.load_data(
    script_content_metadata,
    connection,
    (st.query_params["url"], )
)

if df_content_metadata.empty:
    elements.raise_page_not_found_message()
    st.stop()

# DRAW PAGE HEADER
st.title(df_content_metadata["Page title"].iloc[0])
st.subheader(df_content_metadata["Authors"].iloc[0])
st.markdown("https://www.instituteforgovernment.org.uk" + df_content_metadata["URL"].iloc[0])

st.dataframe(
    df_content_metadata[[
        "Content type", "Published date", "Updated date", "Research areas", "Tags"
    ]].T,
)

# DRAW DATE RANGE INPUTS
with open("streamlit_testing/sql/dashboard/web_metrics/date_range.sql", "r") as file:
    script_date_range = file.read()

df_date_range = elements.load_data(
    script_date_range,
    connection,
)

date_range_option, start_date, end_date = elements.draw_date_range_inputs(
    min_date=df_date_range["min_date"][0],
    max_date=df_date_range["max_date"][0],
)

# DRAW TABS
tab1, tab2, tab3 = st.tabs(["Metrics", "Traffic sources", "Search terms"])

with tab1:

    # LOAD DATA
    script_metrics = script.split(';')[1]

    df_metrics = elements.load_data(
        script_metrics,
        connection,
        (st.query_params["url"], start_date, end_date)
    )

    # EDIT DATA
    df_metrics = elements.calculate_derived_metrics(df_metrics, METRIC_CALCULATIONS)

    df_metrics = df_metrics[
        ["Date"] + list(METRICS_DISPLAY.keys())
    ]

    # DRAW LINE CHART SECTION
    selected_metric = elements.draw_line_chart_section(
        df=df_metrics,
        x="Date",
        metrics=list(METRICS_DISPLAY.keys()),
        default_metric=DEFAULT_METRIC,
    )

    df_metrics["Date"] = pd.to_datetime(
        df_metrics["Date"]
    ).dt.strftime("%Y-%m-%d")

    # DRAW TABLE
    column_defs, grid_options = elements.set_table_defaults(
        df_metrics,
        DEFAULT_METRIC,
        METRICS_DISPLAY,
    )

    column_defs["Date"]["Content type"] = "Date"
    column_defs["Date"]["cellClass"] = "ag-right-aligned-cell"
    column_defs["Date"]["headerClass"] = "ag-right-aligned-header"
    column_defs["Date"]["valueFormatter"] = format_date
    column_defs["Date"]["comparator"] = compare_dates
    column_defs["Date"]["sort"] = "asc"

    for metric, formatter in METRICS_DISPLAY.items():
        column_defs[metric]["valueFormatter"] = formatter

    AgGrid(
        df_metrics,
        key="ag",
        update_on=[],
        gridOptions=grid_options,
        allow_unsafe_jscode=True,
    )

with tab2:
    st.markdown("Not yet developed")
with tab3:
    st.markdown("Not yet developed")
