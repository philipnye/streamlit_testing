import os

import streamlit as st
from st_aggrid import AgGrid, StAggridTheme

from streamlit_testing.config.ag_grid_theme import AG_GRID_THEME_BASE, AG_GRID_THEME_DEFAULTS
import streamlit_testing.pages.dashboard.web_metrics.config as config
import streamlit_testing.pages.dashboard.web_metrics.elements as elements
from streamlit_testing.pages.dashboard.web_metrics.notes import NOTES
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
            "file_name_column": "File name",
            "external_link_column": "Link",
            "external_link_text": "View output ⮺",
            "background_color": "#e2f8ff",       # Blue lighter 90%
            "notes": [NOTES["downloads_note"]],
        },
        {
            "display_name": "Publication page views",
            "content_type": "Publication",
            "sql_script": "streamlit_testing/sql/dashboard/web_metrics/home_page_views.sql",
            "metrics": {"Page views": format_integer},
            "title_column": "Page title",
            "external_link_column": "Link",
            "external_link_text": "View page ⮺",
        },
        {
            "display_name": "Comment page views",
            "content_type": "Comment",
            "sql_script": "streamlit_testing/sql/dashboard/web_metrics/home_page_views.sql",
            "metrics": {"Page views": format_integer},
            "title_column": "Page title",
            "external_link_column": "Link",
            "external_link_text": "View page ⮺",
        },
        {
            "display_name": "Explainer page views",
            "content_type": "Explainer",
            "sql_script": "streamlit_testing/sql/dashboard/web_metrics/home_page_views.sql",
            "metrics": {"Page views": format_integer},
            "title_column": "Page title",
            "external_link_column": "Link",
            "external_link_text": "View page ⮺",
        }
    ],
    "Events": [
        {
            "display_name": "Event page views",
            "content_type": "Event",
            "sql_script": "streamlit_testing/sql/dashboard/web_metrics/home_page_views.sql",
            "metrics": {"Page views": format_integer},
            "title_column": "Page title",
            "external_link_column": "Link",
            "external_link_text": "View page ⮺",
            "notes": [NOTES["event_page_views_note"]],
        }
    ]
}

# CONNECT TO DATABASE
connection = elements.connect_database()

# LOAD DATE RANGE DATA
with open("streamlit_testing/sql/dashboard/web_metrics/date_range.sql", "r") as file:
    script_date_range = file.read()

df_date_range = elements.load_data(
    script_date_range,
    connection,
)

# DRAW PAGE HEADER
st.title("Home")
elements.draw_latest_data_badge(df_date_range["max_date"][0])
st.markdown("\n\n")
st.markdown("\n\n")

# DRAW DATE RANGE INPUTS
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

                    # LOAD PAGE DATA
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
                        sortable=False,
                        sort_columns="index",
                        sort_order="asc",
                        filter=False,
                        lockPinned=True,
                    )

                    column_defs = elements.create_external_link(
                        column_defs,
                        table_config["external_link_column"],
                        table_config["external_link_text"]
                    )

                    # Apply formatting to metric columns
                    for metric_column in table_config["metrics"]:
                        column_defs[metric_column]["valueFormatter"] = format_integer

                    # Set explicit column widths
                    column_defs[table_config["title_column"]]["width"] = 300
                    if "file_name_column" in table_config:
                        column_defs[table_config["file_name_column"]]["width"] = 300
                    column_defs[table_config["external_link_column"]]["width"] = 200

                    # Set width for metric columns
                    for metric_column in table_config["metrics"]:
                        column_defs[metric_column]["width"] = 100

                    # Disable pagination
                    grid_options["pagination"] = False

                    # Enable auto-sizing on second+ tabs
                    # NB: This is to get around an issue with streamlit-aggrid, with autosizing not working for tabs bar the first (https://github.com/PablocFonseca/streamlit-aggrid/issues/249)
                    if tab_index > 0:
                        grid_options["autoSizeStrategy"] = "SizeColumnsToFitProvidedWidthStrategy"

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

                    # Prevent column reordering
                    grid_options["suppressMovableColumns"] = True

                    # Create theme with background color if specified
                    theme_params = AG_GRID_THEME_DEFAULTS.copy()
                    if "background_color" in table_config:
                        theme_params["backgroundColor"] = table_config["background_color"]

                    AgGrid(
                        df,
                        key=f"ag_{table_config['content_type'].lower()}_{table_config['sql_script'].replace('.sql', '')}_{tab_index}",
                        license_key=os.environ["AG_GRID_LICENCE_KEY"],
                        enable_enterprise_modules="enterpriseOnly",
                        update_on=[],
                        gridOptions=grid_options,
                        allow_unsafe_jscode=True,
                        theme=StAggridTheme(base=AG_GRID_THEME_BASE).withParams(**theme_params),
                        height=500,
                    )

                    if "notes" in table_config:
                        for note in table_config["notes"]:
                            if note["type"] == "warning":
                                st.warning(note["text"])
                            elif note["type"] == "info":
                                st.info(note["text"])
                            elif note["type"] == "error":
                                st.error(note["text"])
                            elif note["type"] == "success":
                                st.success(note["text"])
