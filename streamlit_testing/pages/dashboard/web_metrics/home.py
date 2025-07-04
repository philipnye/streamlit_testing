import os

import streamlit as st
from st_aggrid import AgGrid, StAggridTheme

from streamlit_testing.config.ag_grid_theme import AG_GRID_THEME_BASE, AG_GRID_THEME_DEFAULTS
import streamlit_testing.pages.dashboard.web_metrics.config as config
import streamlit_testing.pages.dashboard.web_metrics.elements as elements
from streamlit_testing.pages.dashboard.web_metrics.utils import format_integer

# SET CONSTANTS
TAB_CONFIG = {
    "Publications, comments, explainers": [
        {
            "display_name": "Publication downloads",
            "content_type": "Publication",
            "sql_script": "streamlit_testing/sql/dashboard/web_metrics/home_downloads.sql",
            "metrics": {"Downloads": format_integer},
            "title_column": "Output title",
            "external_link_column": "File name",
            "background_color": "#e2f8ff"       # Blue lighter 90%
        },
        {
            "display_name": "Publication page views",
            "content_type": "Publication",
            "sql_script": "streamlit_testing/sql/dashboard/web_metrics/home_page_views.sql",
            "metrics": {"Page views": format_integer},
            "title_column": "Page title",
            "external_link_column": "URL"
        },
        {
            "display_name": "Comment page views",
            "content_type": "Comment",
            "sql_script": "streamlit_testing/sql/dashboard/web_metrics/home_page_views.sql",
            "metrics": {"Page views": format_integer},
            "title_column": "Page title",
            "external_link_column": "URL"
        },
        {
            "display_name": "Explainer page views",
            "content_type": "Explainer",
            "sql_script": "streamlit_testing/sql/dashboard/web_metrics/home_page_views.sql",
            "metrics": {"Page views": format_integer},
            "title_column": "Page title",
            "external_link_column": "URL"
        }
    ],
    "Events": [
        {
            "display_name": "Events",
            "content_type": "Event",
            "sql_script": "streamlit_testing/sql/dashboard/web_metrics/home_page_views.sql",
            "metrics": {"Page views": format_integer},
            "title_column": "Page title",
            "external_link_column": "URL"
        }
    ]
}

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
# # DRAW PAGE FILTER INPUT
col1, col2 = st.columns([1, 5])

with col1:
    page_filter = st.selectbox(
        label="Choose pages of interest",
        options=["All pages", "New/updated pages"],
        index=0,
        help="Select whether to include all pages or only those that were published or updated during the selected date range.",
        key="page_filter",
    )

# CREATE TABS
tab_names = list(TAB_CONFIG.keys())
tabs = st.tabs(tab_names)

for tab_index, (tab_name, tables) in enumerate(TAB_CONFIG.items()):
    with tabs[tab_index]:

        # CREATE TWO COLUMNS TO HOLD CONTENT
        num_tables = len(tables)
        rows = []
        for idx in range(0, num_tables, 2):
            row = list(range(idx, min(idx + 2, num_tables)))
            rows.append(row)

        # LOAD DATA AND CREATE TABLES FOR EACH CONTENT TYPE
        for row_indices in rows:
            columns = st.columns(2)

            for col_idx, content_type_idx in enumerate(row_indices):
                table_config = tables[content_type_idx]
                with columns[col_idx]:
                    st.subheader(table_config["display_name"])

                    # LOAD DATA
                    with open(f"{table_config['sql_script']}", "r") as file:
                        script = file.read()

                    # Determine parameters based on page filter
                    if page_filter == "All pages":
                        df = elements.load_data(
                            script,
                            connection,
                            (start_date, end_date, table_config["content_type"], config.SQL_EARLIEST_DATE, config.SQL_LATEST_DATE, config.SQL_EARLIEST_DATE, config.SQL_LATEST_DATE)
                        )
                    elif page_filter == "New/updated pages":
                        df = elements.load_data(
                            script,
                            connection,
                            (start_date, end_date, table_config["content_type"], start_date, end_date, start_date, end_date)
                        )

                    # DRAW TABLE
                    column_defs, grid_options = elements.set_table_defaults(
                        df=df,
                        metrics=table_config["metrics"],
                        sort_columns="index",
                        sort_order="asc",
                    )

                    column_defs = elements.create_external_link(
                        column_defs,
                        table_config["external_link_column"],
                    )

                    # Apply formatting to metric columns
                    for metric_column in table_config["metrics"]:
                        column_defs[metric_column]["valueFormatter"] = format_integer

                    # Set explicit column widths
                    column_defs[table_config["title_column"]]["width"] = 300
                    column_defs[table_config["external_link_column"]]["width"] = 200

                    # Set width for metric columns
                    for metric_column in table_config["metrics"]:
                        column_defs[metric_column]["width"] = 100

                    # Disable pagination
                    grid_options["pagination"] = False

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

                    # Create theme with background color if specified
                    theme_params = AG_GRID_THEME_DEFAULTS.copy()
                    if "background_color" in table_config:
                        theme_params["backgroundColor"] = table_config["background_color"]

                    AgGrid(
                        df,
                        key=f"ag_{table_config['content_type'].lower()}_{table_config['sql_script'].replace('.sql', '')}_{tab_index}",
                        license_key=os.environ["AG_GRID_LICENCE_KEY"],
                        update_on=[],
                        gridOptions=grid_options,
                        allow_unsafe_jscode=True,
                        theme=StAggridTheme(base=AG_GRID_THEME_BASE).withParams(**theme_params),
                        height=500,
                    )
