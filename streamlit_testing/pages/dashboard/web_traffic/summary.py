import os

import pandas as pd
from sqlalchemy import exc
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder

import ds_utils.database_operations as dbo

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
with open("streamlit_testing/sql/dashboard/summary.sql", "r") as file:
    script = file.read()

try:
    df = pd.read_sql_query(
        sql=script,
        con=connection,
    )
except exc.DBAPIError:
    df = pd.read_sql_query(
        sql=script,
        con=connection,
    )

# DRAW INPUT WIDGETS
# Controls
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
    value=df["date"].min(),
    min_value=df["date"].min(),
    max_value=df["date"].max(),
    key="start_date",
)
end_date = st.date_input(
    label="End date",
    value=df["date"].max(),
    min_value=df["date"].min(),
    max_value=df["date"].max(),
    key="end_date",
)

breakdowns = st.pills(
    label="Breakdowns",
    options=[
        "type",
        # "published_date",
        # "updated_date_alternative",
        "author",
        "research_area",
        "tag",
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

df_grouped_by_day = df[[
    "date",
    "activeUsers",
    "engagedSessions",
    "screenPageViews",
    "sessions",
    "userEngagementDuration",
]].groupby("date").sum().reset_index().sort_values("date")

if breakdowns != []:
    df_grouped = df[breakdowns + [
        "activeUsers",
        "engagedSessions",
        "screenPageViews",
        "sessions",
        "userEngagementDuration",
    ]].groupby(breakdowns).sum().reset_index().sort_values(breakdowns)
else:
    df_grouped = df[[
        "activeUsers",
        "engagedSessions",
        "screenPageViews",
        "sessions",
        "userEngagementDuration",
    ]].sum().reset_index()

# DRAW OUTPUT WIDGETS
# Chart
st.line_chart(
    data=df_grouped_by_day,
    x="date",
    y=metric,
    use_container_width=True,
)

# Table
grid_builder = GridOptionsBuilder.from_dataframe(df_grouped)
grid_options = grid_builder.build()

grid_options["pagination"] = True
grid_options["paginationPageSize"] = 25

grid_options["defaultColDef"] = {
    "filter": True,
}

column_defs = {column_def["field"]: column_def for column_def in grid_options["columnDefs"]}

AgGrid(
    df_grouped,
    key="ag",
    update_on=[],
    gridOptions=grid_options,
    allow_unsafe_jscode=True,
)
