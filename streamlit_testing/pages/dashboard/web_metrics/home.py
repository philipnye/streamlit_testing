import os

import streamlit as st
from st_aggrid import AgGrid

from streamlit_testing.config.ag_grid_theme import ag_grid_theme
import streamlit_testing.pages.dashboard.web_metrics.config as config
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

# CREATE TABS
tab_config = {
    "Publications, comments, explainers": ["Publication", "Comment", "Explainer"],
    "Events": ["Event"]
}
tab_names = list(tab_config.keys())
tabs = st.tabs(tab_names)

for tab_index, (tab_name, content_types) in enumerate(tab_config.items()):
    with tabs[tab_index]:
        # DRAW PAGE FILTER INPUT
        col1, col2 = st.columns([1, 5])
        with col1:
            page_filter = st.selectbox(
                label="Page filter",
                options=["All pages", "New/updated pages"],
                index=0,
                help="Select whether to include all pages or only those that were published or updated during the selected date range.",
                key=f"page_filter_{tab_index}",
            )

        # CREATE COLUMNS DYNAMICALLY
        columns = st.columns(len(content_types))

        # LOAD DATA AND CREATE TABLES FOR EACH CONTENT TYPE
        for i, content_type in enumerate(content_types):
            with columns[i]:
                st.subheader(f"{content_type}s")

                # LOAD DATA
                with open("streamlit_testing/sql/dashboard/web_metrics/home.sql", "r") as file:
                    script = file.read()

                if page_filter == "All pages":
                    df = elements.load_data(
                        script,
                        connection,
                        (start_date, end_date, content_type, config.SQL_EARLIEST_DATE, config.SQL_LATEST_DATE, config.SQL_EARLIEST_DATE, config.SQL_LATEST_DATE)
                    )
                elif page_filter == "New/updated pages":
                    df = elements.load_data(
                        script,
                        connection,
                        (start_date, end_date, content_type, start_date, end_date, start_date, end_date)
                    )

                # DRAW TABLE
                column_defs, grid_options = elements.set_table_defaults(
                    df=df,
                    metrics={"Page views": format_integer},
                    sort_columns="Page views",
                    sort_order="desc",
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
                    key=f"ag_{content_type.lower()}_{tab_index}",
                    license_key=os.environ["AG_GRID_LICENCE_KEY"],
                    update_on=[],
                    gridOptions=grid_options,
                    allow_unsafe_jscode=True,
                    theme=ag_grid_theme,
                )
