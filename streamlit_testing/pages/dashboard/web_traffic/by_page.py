import os

import pandas as pd
from sqlalchemy import engine, exc
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

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
with open("streamlit_testing/sql/dashboard/by_page.sql", "r") as file:
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
st.title("By page")

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

# EDIT DATA
df = df[
    (df["date"] >= start_date) &
    (df["date"] <= end_date)
]

df_by_day = df[[
    "date",
    "activeUsers",
    "engagedSessions",
    "screenPageViews",
    "sessions",
    "userEngagementDuration",
]].groupby("date").sum().reset_index().sort_values("date")

df_by_page = df[[
    "page_title",
    "pagePath",
    "type",
    "published_date",
    "updated_date_alternative",
    "authors",
    "research_areas",
    "tags",
    "activeUsers",
    "engagedSessions",
    "screenPageViews",
    "sessions",
    "userEngagementDuration",
]].groupby([
    "page_title",
    "pagePath",
    "type",
    "published_date",
    "updated_date_alternative",
    "authors",
    "research_areas",
    "tags",
]).sum().reset_index().sort_values(metric, ascending=False)

# DRAW OUTPUT WIDGETS
# Chart
st.line_chart(
    data=df_by_day,
    x="date",
    y=metric,
    use_container_width=True,
)

# Table
grid_builder = GridOptionsBuilder.from_dataframe(df_by_page)
grid_options = grid_builder.build()

grid_options["pagination"] = True
grid_options["paginationPageSize"] = 25

grid_options["defaultColDef"] = {
    "filter": True,
}

column_defs = {column_def["field"]: column_def for column_def in grid_options["columnDefs"]}
column_defs["page_title"]["pinned"] = "left"
column_defs["page_title"]["cellRenderer"] = JsCode("""
    class UrlCellRenderer {
        init(params) {
            this.eGui = document.createElement("a");
            this.eGui.innerText = params.value;
            this.eGui.setAttribute(
                "href", "/web_traffic_page_detail?url=" + params.data.pagePath
            );
            this.eGui.setAttribute("style", "text-decoration:none");
            this.eGui.setAttribute("target", "_blank");
        }
        getGui() {
            return this.eGui;
        }
    }
""")
column_defs["pagePath"]["cellRenderer"] = JsCode("""
    class UrlCellRenderer {
        init(params) {
            this.eGui = document.createElement("a");
            this.eGui.innerText = "View page ⮺";
            this.eGui.setAttribute(
                "href", "https://www.instituteforgovernment.org.uk" + params.value
            );
            this.eGui.setAttribute("style", "text-decoration:none");
            this.eGui.setAttribute("target", "_blank");
        }
        getGui() {
            return this.eGui;
        }
    }
""")

AgGrid(
    df_by_page,
    key="ag",
    update_on=[],
    gridOptions=grid_options,
    allow_unsafe_jscode=True,
)
