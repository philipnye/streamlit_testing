import os

import pandas as pd
from sqlalchemy import engine, exc
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder

import streamlit_testing.pages.dashboard.web_traffic.elements as elements
from streamlit_testing.pages.dashboard.web_traffic.utils import apply_locale_string, set_metrics

import ds_utils.database_operations as dbo

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
with open("streamlit_testing/sql/dashboard/web_traffic/summary.sql", "r") as file:
    script = file.read()


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


df = load_data(script, connection)

# DRAW PAGE HEADER
st.title("Summary")

# DRAW INPUT WIDGETS
# Controls
start_date, end_date = elements.draw_date_range_inputs(
    min_date=df["date"].min(),
    max_date=df["date"].max(),
)

breakdowns = st.pills(
    label="Breakdowns",
    options=[
        "type",
        "research_area",
        "tag",
        "author",
        "published_year",
        "published_month",
        "published_day",
        "updated_year",
        "updated_month",
        "updated_day",
    ],
    selection_mode="multi",
    default="type",
    key="breakdowns",
)

# EDIT DATA
df = df[
    (df["date"] >= start_date) &
    (df["date"] <= end_date)
]

df_grouped_by_day = df[["date"] + METRICS].\
    groupby("date").sum().reset_index()

if breakdowns != []:
    df_grouped = df[breakdowns + ["partial"] + METRICS].groupby(breakdowns).agg(
        pages=("partial", "nunique"),
        **METRIC_AGGREGATIONS
    ).reset_index()
else:
    df.insert(0, "category", "All pages")
    df_grouped = df[["category", "partial"] + METRICS].groupby("category").agg(
        pages=("partial", "nunique"),
        **METRIC_AGGREGATIONS
    ).reset_index()

# DRAW OUTPUT WIDGETS
# Chart
elements.draw_line_chart_section(
    df=df_grouped_by_day,
    x="date",
    metrics=METRICS,
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

column_defs["pages"]["valueFormatter"] = apply_locale_string

for metric in METRICS:
    column_defs[metric]["valueFormatter"] = apply_locale_string

AgGrid(
    df_grouped,
    key="ag",
    update_on=[],
    gridOptions=grid_options,
    allow_unsafe_jscode=True,
)
