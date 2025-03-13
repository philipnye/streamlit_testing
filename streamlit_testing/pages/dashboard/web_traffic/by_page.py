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

# RUN QUERY
with open("streamlit_testing/sql/dashboard/by_page.sql", "r") as file:
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

# EDIT DATA
df["pagePath"] = df["pagePath"].apply(
    lambda x: f"https://www.instituteforgovernment.org.uk{x}"
)

# DISPLAY RESULTS
# Streamlit dataframe
st.dataframe(
    df,
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
grid_builder = GridOptionsBuilder.from_dataframe(df)
grid_options = grid_builder.build()

columnDefs = {columnDef["field"]: columnDef for columnDef in grid_options["columnDefs"]}

columnDefs["page_title"]["pinned"] = "left"

AgGrid(
    df,
    key="ag",
    update_on=[],
    gridOptions=grid_options,
)
