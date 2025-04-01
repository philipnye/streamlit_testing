import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

import streamlit_testing.pages.dashboard.web_metrics.elements as elements
from streamlit_testing.pages.dashboard.web_metrics.utils import (
    apply_locale_string, format_date, format_date_comparator,
    set_metrics
)

# SET METRIC TYPE
METRIC_TYPE = "web_traffic"
(
    METRICS_RAW, METRICS_DISPLAY, METRIC_AGGREGATIONS, METRIC_CALCULATIONS, DEFAULT_METRIC
) = set_metrics(METRIC_TYPE)

# CONNECT TO DATABASE
connection = elements.connect_database()

# LOAD DATA
with open("streamlit_testing/sql/dashboard/web_metrics/by_page.sql", "r") as file:
    script = file.read()

df = elements.load_data(script, connection)

# DRAW PAGE HEADER
st.title("By page")

# DRAW INPUT WIDGETS
# Controls
start_date, end_date = elements.draw_date_range_inputs(
    min_date=df["Date"].min(),
    max_date=df["Date"].max(),
)

# EDIT DATA
df = df[
    (df["Date"] >= start_date) &
    (df["Date"] <= end_date)
]

df_by_day = df[["Date"] + METRICS_RAW].groupby("Date").sum().reset_index()

df_by_page = df[
    [
        "Page title",
        "URL",
        "Content type",
        "Published date",
        "Updated date",
        "Authors",
        "Research areas",
        "Tags",
    ] + METRICS_RAW
].groupby([
    "Page title",
    "URL",
    "Content type",
    "Published date",
    "Updated date",
    "Authors",
    "Research areas",
    "Tags",
]).sum().reset_index()

df_by_day = elements.calculate_derived_metrics(df_by_day, METRIC_CALCULATIONS)
df_by_page = elements.calculate_derived_metrics(df_by_page, METRIC_CALCULATIONS)

df_by_page = df_by_page[
    [
        "Page title",
        "URL",
        "Content type",
        "Published date",
        "Updated date",
        "Authors",
        "Research areas",
        "Tags",
    ] + METRICS_DISPLAY
]

df_by_page["Published date"] = pd.to_datetime(
    df_by_page["Published date"]
).dt.strftime("%Y-%m-%d")
df_by_page["Updated date"] = pd.to_datetime(
    df_by_page["Updated date"]
).dt.strftime("%Y-%m-%d")

# DRAW OUTPUT WIDGETS
# Chart
elements.draw_line_chart_section(
    df=df_by_day,
    x="Date",
    metrics=METRICS_DISPLAY,
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
column_defs["Page title"]["pinned"] = "left"
column_defs["Page title"]["cellRenderer"] = JsCode("""
    class UrlCellRenderer {
        init(params) {
            this.eGui = document.createElement("a");
            this.eGui.innerText = params.value;
            this.eGui.setAttribute(
                "href", "/web_metrics_page_detail?url=" + params.data.URL
            );
            this.eGui.setAttribute("style", "text-decoration:none");
            this.eGui.setAttribute("target", "_blank");
        }
        getGui() {
            return this.eGui;
        }
    }
""")
column_defs["URL"]["cellRenderer"] = JsCode("""
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
column_defs["Published date"]["Content type"] = "Date"
column_defs["Published date"]["cellClass"] = "ag-right-aligned-cell"
column_defs["Published date"]["headerClass"] = "ag-right-aligned-header"
column_defs["Published date"]["valueFormatter"] = format_date
column_defs["Published date"]["comparator"] = format_date_comparator
column_defs["Updated date"]["Content type"] = "Date"
column_defs["Updated date"]["cellClass"] = "ag-right-aligned-cell"
column_defs["Updated date"]["headerClass"] = "ag-right-aligned-header"
column_defs["Updated date"]["valueFormatter"] = format_date
column_defs["Updated date"]["comparator"] = format_date_comparator

column_defs[DEFAULT_METRIC]["sort"] = "desc"
for metric in METRICS_DISPLAY:
    column_defs[metric]["valueFormatter"] = apply_locale_string

AgGrid(
    df_by_page,
    key="ag",
    update_on=[],
    gridOptions=grid_options,
    allow_unsafe_jscode=True,
)
