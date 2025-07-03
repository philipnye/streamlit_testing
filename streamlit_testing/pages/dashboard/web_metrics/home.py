import os

import streamlit as st
from st_aggrid import AgGrid

from streamlit_testing.config.ag_grid_theme import ag_grid_theme
import streamlit_testing.pages.dashboard.web_metrics.elements as elements
from streamlit_testing.pages.dashboard.web_metrics.utils import format_integer

# CONNECT TO DATABASE
connection = elements.connect_database()

# DRAW PAGE HEADER
st.title("Home")

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

# CONTENT TYPES TO DISPLAY
content_types = ["Publication", "Comment", "Explainer", "Event"]

# CREATE FOUR COLUMNS FOR THE TABLES
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
columns = [col1, col2, col3, col4]

# LOAD DATA AND CREATE TABLES FOR EACH CONTENT TYPE
for i, content_type in enumerate(content_types):
    with columns[i]:
        st.subheader(f"{content_type}s")

        # LOAD DATA
        with open("streamlit_testing/sql/dashboard/web_metrics/home.sql", "r") as file:
            script = file.read()

        df = elements.load_data(
            script,
            connection,
            (start_date, end_date, content_type)
        )

        # DRAW TABLE
        column_defs, grid_options = elements.set_table_defaults(
            df=df,
            metrics={"Page views": format_integer},
            sort_columns="Page views",
            sort_order="desc",
            pin_columns=["Page title"]
        )

        column_defs = elements.create_external_link(
            column_defs,
            "URL",
        )

        column_defs["Page views"]["valueFormatter"] = format_integer

        # Make the grid smaller for the home page layout
        grid_options["pagination"] = False
        grid_options["domLayout"] = "autoHeight"

        # Add row numbers to show index
        grid_options["rowClassRules"] = {
            "row-index": "true"
        }

        # Add index column
        index_column = {
            "headerName": "#",
            "field": "index",
            "valueGetter": "node.rowIndex + 1",
            "width": 50,
            "pinned": "left",
            "suppressMenu": True,
            "sortable": False,
            "filter": False,
            "cellClass": "text-center"
        }
        grid_options["columnDefs"].insert(0, index_column)

        AgGrid(
            df,
            key=f"ag_{content_type.lower()}",
            license_key=os.environ["AG_GRID_LICENCE_KEY"],
            update_on=[],
            gridOptions=grid_options,
            allow_unsafe_jscode=True,
            theme=ag_grid_theme,
            # height=400,
        )
