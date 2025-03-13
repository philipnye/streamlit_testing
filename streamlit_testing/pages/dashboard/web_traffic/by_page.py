import os

import pandas as pd
from sqlalchemy import exc
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

# RUN QUERY
with open("streamlit_testing/sql/dashboard/by_page.sql", "r") as file:
    by_page_script = file.read()
with open("streamlit_testing/sql/dashboard/by_day.sql", "r") as file:
    by_day_script = file.read()

try:
    df_by_page = pd.read_sql_query(
        sql=by_page_script,
        con=connection,
    )
except exc.DBAPIError:
    df_by_page = pd.read_sql_query(
        sql=by_page_script,
        con=connection,
    )

try:
    df_by_day = pd.read_sql_query(
        sql=by_day_script,
        con=connection,
    )
except exc.DBAPIError:
    df_by_day = pd.read_sql_query(
        sql=by_day_script,
        con=connection,
    )

# EDIT DATA
df_by_page["pagePath"] = df_by_page["pagePath"].apply(
    lambda x: f"https://www.instituteforgovernment.org.uk{x}"
)

# DISPLAY RESULTS
st.line_chart(
    data=df_by_day,
    x="date",
    y="screenPageViews",
    use_container_width=True,
)

# Streamlit dataframe
st.dataframe(
    df_by_page,
    hide_index=True,
    column_config={
        "page_title": st.column_config.Column(
            label="Page title",
            pinned=True,
        ),
        "pagePath": st.column_config.LinkColumn(
            display_text="https://www.instituteforgovernment.org.uk(.*)"
        )
    },
)

# AG Grid
# Ref (hyperlinks): https://github.com/PablocFonseca/streamlit-aggrid/issues/198
grid_builder = GridOptionsBuilder.from_dataframe(df_by_page)
grid_options = grid_builder.build()

grid_options["pagination"] = True
grid_options["paginationPageSize"] = 25

grid_options["defaultColDef"] = {
    "filter": True,
}

column_defs = {column_def["field"]: column_def for column_def in grid_options["columnDefs"]}
column_defs["page_title"]["pinned"] = "left"
column_defs["pagePath"]["cellRenderer"] = JsCode("""
    class UrlCellRenderer {
    init(params) {
        this.eGui = document.createElement("a");
        this.eGui.innerText = params.value;
        this.eGui.setAttribute("href", params.value);
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
