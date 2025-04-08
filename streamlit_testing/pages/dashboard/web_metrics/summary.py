import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder

import streamlit_testing.pages.dashboard.web_metrics.elements as elements
from streamlit_testing.pages.dashboard.web_metrics.utils import format_integer, set_metrics

# SET METRIC TYPE
METRIC_TYPE = "web_traffic"
(
    METRICS_RAW, METRICS_DISPLAY, METRIC_AGGREGATIONS, METRIC_CALCULATIONS, DEFAULT_METRIC
) = set_metrics(METRIC_TYPE)

# CONNECT TO DATABASE
connection = elements.connect_database()

# LOAD DATA
with open("streamlit_testing/sql/dashboard/web_metrics/date_range.sql", "r") as file:
    script_date_range = file.read()
with open("streamlit_testing/sql/dashboard/web_metrics/summary.sql", "r") as file:
    script = file.read()

df_date_range = elements.load_data(
    script_date_range,
    connection,
)

# DRAW PAGE HEADER
st.title("Summary")

# DRAW INPUT WIDGETS
# Controls
date_range_option, start_date, end_date = elements.draw_date_range_inputs(
    min_date=df_date_range["min_date"][0],
    max_date=df_date_range["max_date"][0],
)

breakdowns = st.pills(
    label="Choose breakdown",
    options=[
        "Content type",
        "Publication type",
        "Research area",
        "Tag",
        "Author",
        "Published date: year",
        "Published date: month",
        "Published date: day",
        "Updated date: year",
        "Updated date: month",
        "Updated date: day",
    ],
    selection_mode="multi",
    default="Content type",
    key="breakdowns",
)

# EDIT DATA
df = elements.load_data(
    script,
    connection,
    (start_date, end_date)
)

df_grouped_by_day = df[["Date"] + METRICS_RAW].drop_duplicates().groupby("Date").sum().reset_index()

if breakdowns == []:
    df.insert(0, "Category", "All pages")
    df_grouped = df[["Category", "URL"] + METRICS_RAW].drop_duplicates().groupby("Category").agg(
        Pages=("URL", "nunique"),
        **METRIC_AGGREGATIONS
    ).reset_index()
else:
    df_grouped = df[breakdowns + ["URL"] + METRICS_RAW].drop_duplicates().groupby(breakdowns).agg(
        Pages=("URL", "nunique"),
        **METRIC_AGGREGATIONS
    ).reset_index()

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

# DRAW OUTPUT WIDGETS
# Chart
elements.draw_line_chart_section(
    df=df_grouped_by_day,
    x="Date",
    metrics=list(METRICS_DISPLAY.keys()),
    default_metric=DEFAULT_METRIC,
)

# Table
grid_builder = GridOptionsBuilder.from_dataframe(df_grouped)
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
if breakdowns != []:
    for breakdown in breakdowns:
        column_defs[breakdown]["pinned"] = "left"
    column_defs[breakdowns[0]]["sort"] = "asc"

column_defs["Pages"]["valueFormatter"] = format_integer

for metric, formatter in METRICS_DISPLAY.items():
    column_defs[metric]["valueFormatter"] = formatter

AgGrid(
    df_grouped,
    key="ag",
    update_on=[],
    gridOptions=grid_options,
    allow_unsafe_jscode=True,
)
