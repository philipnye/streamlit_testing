import os

import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, StAggridTheme

from streamlit_testing.config.ag_grid_theme import AG_GRID_THEME_BASE, AG_GRID_THEME_DEFAULTS
import streamlit_testing.pages.dashboard.web_metrics.elements as elements
from streamlit_testing.pages.dashboard.web_metrics.utils import set_metrics

# HANDLE DIRECT ACCESS
if "url" not in st.query_params:
    elements.raise_page_not_found_message()
    st.stop()

# DISABLE SIDEBAR
elements.disable_sidebar()

# SET METRIC TYPE
METRIC_TYPE = "download"
(
    METRICS_RAW, METRICS_DISPLAY, METRIC_AGGREGATIONS, METRIC_CALCULATIONS, DEFAULT_METRIC
) = set_metrics(METRIC_TYPE)

# CONNECT TO DATABASE
connection = elements.connect_database()

# LOAD DATE RANGE DATA
with open("streamlit_testing/sql/dashboard/web_metrics/date_range.sql", "r") as file:
    script_date_range = file.read()

df_date_range = elements.load_data(
    script_date_range,
    connection,
)

# LOAD PUBLICATION DATA
with open("streamlit_testing/sql/dashboard/web_metrics/publication_detail.sql", "r") as file:
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
st.title("Publication: _" + df_content_metadata["Publication title"].iloc[0] + "_")
elements.draw_latest_data_badge(df_date_range["max_date"][0])
st.markdown("\n\n")
st.markdown("\n\n")

if df_content_metadata["Author"].iloc[0]:
    st.subheader(df_content_metadata["Author"].iloc[0])
else:
    st.subheader("_No author_")
st.markdown("https://www.instituteforgovernment.org.uk" + df_content_metadata["Link"].iloc[0])
st.markdown("\n\n")

content_metadata = ["Content type", "Publication type", "Published date", "Updated date", "Team", "Topic"]

for date_col in ["Published date", "Updated date"]:
    df_content_metadata[date_col] = pd.to_datetime(
        df_content_metadata[date_col]
    ).dt.strftime("%d %B %Y")

df_content_metadata = df_content_metadata.fillna("")

st.markdown(
    df_content_metadata[content_metadata].T.reset_index().style.set_table_styles([
        {"selector": "tr", "props": [("border", "none")]},
        {"selector": "td", "props": [("border", "none")]},
        {"selector": "td:first-child", "props": [
            ("font-weight", "bold"),
            ("padding-left", "0"),
        ]},
    ]).hide(axis=0).hide(axis=1).to_html(), unsafe_allow_html=True
)
st.markdown("\n\n")

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
        start_date=start_date,
        end_date=end_date,
        metrics=list(METRICS_DISPLAY.keys()),
        default_metric=DEFAULT_METRIC,
    )

    df_metrics["Date"] = pd.to_datetime(
        df_metrics["Date"]
    ).dt.strftime("%Y-%m-%d")

    # DRAW TABLE
    column_defs, grid_options = elements.set_table_defaults(
        df=df_metrics,
        metrics=METRICS_DISPLAY,
        sort_columns="Date",
        sort_order="asc",
    )

    column_defs = elements.format_date_cols(
        column_defs,
        ["Date"]
    )

    for metric, formatter in METRICS_DISPLAY.items():
        column_defs[metric]["valueFormatter"] = formatter

    AgGrid(
        df_metrics,
        key="ag",
        license_key=os.environ["AG_GRID_LICENCE_KEY"],
        enable_enterprise_modules="enterpriseOnly",
        update_on=[],
        gridOptions=grid_options,
        allow_unsafe_jscode=True,
        theme=StAggridTheme(base=AG_GRID_THEME_BASE).withParams(**AG_GRID_THEME_DEFAULTS),
        height=elements.calculate_ag_grid_height(len(df_metrics)),
    )

with tab2:
    st.markdown("Not yet developed")
with tab3:
    st.markdown("Not yet developed")
