import os

import pandas as pd
import streamlit as st
from st_aggrid import AgGrid

from streamlit_testing.config.ag_grid_theme import ag_grid_theme
import streamlit_testing.pages.dashboard.web_metrics.config as config
import streamlit_testing.pages.dashboard.web_metrics.elements as elements
from streamlit_testing.pages.dashboard.web_metrics.utils import (set_metrics)

# SET METRIC TYPE
METRIC_TYPE = "web_traffic"
(
    METRICS_RAW, METRICS_DISPLAY, METRIC_AGGREGATIONS, METRIC_CALCULATIONS, DEFAULT_METRIC
) = set_metrics(METRIC_TYPE)

# CONNECT TO DATABASE
connection = elements.connect_database()

# DRAW PAGE HEADER
st.title("By page")

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

# LOAD DATA
with open("streamlit_testing/sql/dashboard/web_metrics/by_page.sql", "r") as file:
    script = file.read()

df = elements.load_data(
    script,
    connection,
    (start_date, end_date)
)

# EDIT DATA
df_by_day = df[["Date"] + METRICS_RAW].groupby("Date").sum().reset_index()
df_by_day = elements.calculate_derived_metrics(df_by_day, METRIC_CALCULATIONS)

df_by_page = elements.group_df(
    df=df[config.METRICS_BY_PAGE + METRICS_RAW],
    group_by=config.METRICS_BY_PAGE,
)

df_by_page = elements.calculate_derived_metrics(df_by_page, METRIC_CALCULATIONS)

df_by_page = df_by_page[config.METRICS_BY_PAGE + list(METRICS_DISPLAY.keys())]

df_by_page["Published date"] = pd.to_datetime(
    df_by_page["Published date"]
).dt.strftime("%Y-%m-%d")
df_by_page["Updated date"] = pd.to_datetime(
    df_by_page["Updated date"]
).dt.strftime("%Y-%m-%d")

# DRAW LINE CHART SECTION
selected_metric = elements.draw_line_chart_section(
    df=df_by_day,
    x="Date",
    metrics=list(METRICS_DISPLAY.keys()),
    default_metric=DEFAULT_METRIC,
)

# DRAW TABLE
column_defs, grid_options = elements.set_table_defaults(
    df=df_by_page,
    metrics=METRICS_DISPLAY,
    sort_columns=DEFAULT_METRIC,
    sort_order="desc",
    pin_columns=["Page title"]
)

column_defs = elements.create_internal_link(
    column_defs,
    "Page title",
)
column_defs = elements.create_external_link(
    column_defs,
    "URL",
)
column_defs = elements.format_date_cols(
    column_defs,
    ["Published date", "Updated date"]
)

for metric, formatter in METRICS_DISPLAY.items():
    column_defs[metric]["valueFormatter"] = formatter

AgGrid(
    df_by_page,
    key="ag",
    license_key=os.environ["AG_GRID_LICENCE_KEY"],
    update_on=[],
    gridOptions=grid_options,
    allow_unsafe_jscode=True,
    theme=ag_grid_theme
)
