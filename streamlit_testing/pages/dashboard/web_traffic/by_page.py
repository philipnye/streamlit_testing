import os

import pandas as pd
from sqlalchemy import engine, exc
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

import streamlit_testing.pages.dashboard.web_traffic.elements as elements
from streamlit_testing.pages.dashboard.web_traffic.utils import (
    apply_locale_string, format_date, format_date_comparator,
    set_metrics
)

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
with open("streamlit_testing/sql/dashboard/web_traffic/by_page.sql", "r") as file:
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
start_date, end_date = elements.draw_date_range_inputs(
    min_date=df["date"].min(),
    max_date=df["date"].max(),
)

# EDIT DATA
df = df[
    (df["date"] >= start_date) &
    (df["date"] <= end_date)
]

df_by_day = df[["date"] + METRICS].groupby("date").sum().reset_index()

df_by_page = df[
    [
        "page_title",
        "pagePath",
        "type",
        "published_date",
        "updated_date_alternative",
        "authors",
        "research_areas",
        "tags",
    ] + METRICS
].groupby([
    "page_title",
    "pagePath",
    "type",
    "published_date",
    "updated_date_alternative",
    "authors",
    "research_areas",
    "tags",
]).sum().reset_index()

df_by_page["published_date"] = pd.to_datetime(
    df_by_page["published_date"]
).dt.strftime("%Y-%m-%d")
df_by_page["updated_date_alternative"] = pd.to_datetime(
    df_by_page["updated_date_alternative"]
).dt.strftime("%Y-%m-%d")

# DRAW OUTPUT WIDGETS
# Chart
elements.draw_line_chart_section(
    df=df_by_day,
    x="date",
    metrics=METRICS,
    default_metric=DEFAULT_METRIC,
)

# Table
grid_builder = GridOptionsBuilder.from_dataframe(df_by_page)
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
column_defs["published_date"]["type"] = "date"
column_defs["published_date"]["cellClass"] = "ag-right-aligned-cell"
column_defs["published_date"]["headerClass"] = "ag-right-aligned-header"
column_defs["published_date"]["valueFormatter"] = format_date
column_defs["published_date"]["comparator"] = format_date_comparator
column_defs["updated_date_alternative"]["type"] = "date"
column_defs["updated_date_alternative"]["cellClass"] = "ag-right-aligned-cell"
column_defs["updated_date_alternative"]["headerClass"] = "ag-right-aligned-header"
column_defs["updated_date_alternative"]["valueFormatter"] = format_date
column_defs["updated_date_alternative"]["comparator"] = format_date_comparator

column_defs[DEFAULT_METRIC]["sort"] = "desc"
for metric in METRICS:
    column_defs[metric]["valueFormatter"] = apply_locale_string

AgGrid(
    df_by_page,
    key="ag",
    update_on=[],
    gridOptions=grid_options,
    allow_unsafe_jscode=True,
)
