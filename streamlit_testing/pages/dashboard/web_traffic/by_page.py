import os

import pandas as pd
from sqlalchemy import exc
import streamlit as st

import ds_utils.database_operations as dbo

# CONNECT TO DATABASE
connection = dbo.connect_sql_db(
    driver='pyodbc',
    driver_version=os.environ['ODBC_DRIVER'],
    dialect='mssql',
    server=os.environ['ODBC_SERVER'],
    database=os.environ['ODBC_DATABASE'],
    authentication=os.environ['ODBC_AUTHENTICATION'],
    username=os.environ['AZURE_CLIENT_ID'],
    password=os.environ['AZURE_CLIENT_SECRET'],
)

# RUN QUERY
with open('streamlit_testing/sql/dashboard/by_page.sql', 'r') as file:
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

# DISPLAY RESULTS
st.dataframe(df)
