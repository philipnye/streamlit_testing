import os

import streamlit as st
from st_aggrid import AgGrid, StAggridTheme

from streamlit_testing.config.ag_grid_theme import AG_GRID_THEME_BASE, AG_GRID_THEME_DEFAULTS
import streamlit_testing.pages.dashboard.web_metrics.config as config
import streamlit_testing.pages.dashboard.web_metrics.elements as elements
from streamlit_testing.pages.dashboard.web_metrics.utils import format_integer, set_metrics

# SET METRIC TYPE
METRIC_TYPE = "web_traffic"
(
    METRICS_RAW, METRICS_DISPLAY, METRIC_AGGREGATIONS, METRIC_CALCULATIONS, DEFAULT_METRIC
) = set_metrics(METRIC_TYPE)

# CONNECT TO DATABASE
connection = elements.connect_database()

# DRAW PAGE HEADER
st.title("Summary")

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

# DRAW BREAKDOWNS INPUT
breakdowns = st.pills(
    label="Choose breakdown",
    options=config.BREAKDOWNS,
    selection_mode="multi",
    default=config.DEFAULT_BREAKDOWNS,
    key="breakdowns",
)

# Sort breakdowns for consistent ordering
breakdowns.sort(key=lambda x: config.BREAKDOWNS.index(x))

# LOAD PAGE DATA
with open("streamlit_testing/sql/dashboard/web_metrics/summary.sql", "r") as file:
    script = file.read()

df = elements.load_data(
    script,
    connection,
    (start_date, end_date)
)

# EDIT DATA
df_grouped_by_day = df[["Date"] + METRICS_RAW].drop_duplicates().groupby("Date").sum().reset_index()

if breakdowns == []:
    df.insert(0, "Category", "All pages")
    df_grouped = df[["Category", "Link"] + METRICS_RAW].drop_duplicates().groupby("Category").agg(
        Pages=("Link", "nunique"),
        **METRIC_AGGREGATIONS
    ).reset_index()
else:
    df_grouped = df[breakdowns + ["Link"] + METRICS_RAW].drop_duplicates().groupby(
        breakdowns,
        dropna=False
    ).agg(
        Pages=("Link", "nunique"),
        **METRIC_AGGREGATIONS
    ).reset_index()

df_grouped_by_day = elements.fill_missing_dates(df_grouped_by_day, start_date, end_date, "Date", METRICS_RAW)
df_grouped_by_day = elements.calculate_derived_metrics(df_grouped_by_day, METRIC_CALCULATIONS)
df_grouped = elements.calculate_derived_metrics(df_grouped, METRIC_CALCULATIONS)

if breakdowns == []:
    df_grouped = df_grouped[
        ["Category", "Pages"] + list(METRICS_DISPLAY.keys())
    ]
else:
    df_grouped = df_grouped[
        breakdowns + ["Pages"] + list(METRICS_DISPLAY.keys())
    ]

# DRAW LINE CHART SECTION
selected_metric = elements.draw_line_chart_section(
    df=df_grouped_by_day,
    x="Date",
    start_date=start_date,
    end_date=end_date,
    metrics=list(METRICS_DISPLAY.keys()),
    default_metric=DEFAULT_METRIC,
)

# DRAW TABLE
column_defs, grid_options = elements.set_table_defaults(
    df=df_grouped,
    metrics=METRICS_DISPLAY,
    sort_columns=breakdowns if breakdowns else None,
    sort_order="asc",
    pin_columns=breakdowns if breakdowns else None
)

column_defs["Pages"]["valueFormatter"] = format_integer

for metric, formatter in METRICS_DISPLAY.items():
    column_defs[metric]["valueFormatter"] = formatter

AgGrid(
    df_grouped,
    key="ag",
    license_key=os.environ["AG_GRID_LICENCE_KEY"],
    enable_enterprise_modules="enterpriseOnly",
    update_on=[],
    gridOptions=grid_options,
    allow_unsafe_jscode=True,
    theme=StAggridTheme(base=AG_GRID_THEME_BASE).withParams(**AG_GRID_THEME_DEFAULTS),
    height=elements.calculate_ag_grid_height(len(df_grouped)),
)
