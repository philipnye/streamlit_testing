import os

import streamlit as st
from st_aggrid import AgGrid, StAggridTheme

from streamlit_testing.config.ag_grid_theme import AG_GRID_THEME_BASE, AG_GRID_THEME_DEFAULTS
import streamlit_testing.pages.dashboard.web_metrics.config as config
import streamlit_testing.pages.dashboard.web_metrics.elements as elements
from streamlit_testing.pages.dashboard.web_metrics.notes import NOTES
from streamlit_testing.pages.dashboard.web_metrics.utils import format_integer, format_percentage

# SET CONSTANTS
TAB_CONFIG = {
    "Publications, comments, explainers": [
        {
            "display_name": "Publication page views and downloads",
            "content_type": "Publication",
            "sql_script": "streamlit_testing/sql/dashboard/web_metrics/home_publications.sql",
            "metrics": {
                "Page views (pages downloadable from)": format_integer,
                "Downloads": format_integer,
                "Download rate (pages downloadable from)": format_percentage,
            },
            "title_column": "Publication title",
            "file_name_column": "File name",
            "internal_link_type": "publication",
            "external_link_column": "Link",
            "external_link_text": "View publication ⮺",
            "sort_columns": "Downloads",
            "notes": [NOTES["downloads_note"]],
            "width": "full",
        },
        {
            "display_name": "Comment page views",
            "content_type": "Comment",
            "sql_script": "streamlit_testing/sql/dashboard/web_metrics/home_comments_explainers_events.sql",
            "metrics": {"Page views": format_integer},
            "title_column": "Page title",
            "internal_link_type": "page",
            "external_link_column": "Link",
            "external_link_text": "View page ⮺",
            "sort_columns": "Page views",
            "width": "half",
        },
        {
            "display_name": "Explainer page views",
            "content_type": "Explainer",
            "sql_script": "streamlit_testing/sql/dashboard/web_metrics/home_comments_explainers_events.sql",
            "metrics": {"Page views": format_integer},
            "title_column": "Page title",
            "internal_link_type": "page",
            "external_link_column": "Link",
            "external_link_text": "View page ⮺",
            "sort_columns": "Page views",
            "width": "half",
        }
    ],
    "Events": [
        {
            "display_name": "Event page views",
            "content_type": "Event",
            "sql_script": "streamlit_testing/sql/dashboard/web_metrics/home_comments_explainers_events.sql",
            "metrics": {"Page views": format_integer},
            "title_column": "Page title",
            "internal_link_type": "page",
            "external_link_column": "Link",
            "external_link_text": "View page ⮺",
            "sort_columns": "Page views",
            "notes": [NOTES["event_page_views_note"]],
            "width": "full",
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
        label="Choose scope",
        options=["All content", "New/updated content"],
        index=0,
        help="Select whether to include all content or only that published or updated during the selected date range.",
        key="page_filter",
    )

# CREATE TABS
tab_names = list(TAB_CONFIG.keys())
tabs = st.tabs(tab_names)


def create_table(table_config, tab_index, page_filter, start_date, end_date, connection, sort_column=None):
    """Create a single table with all the necessary data loading and configuration."""

    # LOAD PAGE DATA
    with open(f"{table_config['sql_script']}", "r") as file:
        script = file.read()

    # Determine parameters based on page filter
    if page_filter == "All content":
        published_start_date = config.SQL_EARLIEST_DATE
        published_end_date = config.SQL_LATEST_DATE
    elif page_filter == "New/updated content":
        published_start_date = start_date
        published_end_date = end_date

    if table_config["content_type"] == "Publication":
        df = elements.load_data(
            script,
            connection,
            (start_date, end_date, start_date, end_date, table_config["content_type"], published_start_date, published_end_date, published_start_date, published_end_date)
        )
    else:
        df = elements.load_data(
            script,
            connection,
            (start_date, end_date, table_config["content_type"], published_start_date, published_end_date, published_start_date, published_end_date)
        )

    # EDIT DATA
    if table_config["content_type"] == "Publication":
        METRIC_CALCULATIONS = config.DOWNLOAD_METRIC_CALCULATIONS
        df = elements.calculate_derived_metrics(df, METRIC_CALCULATIONS)

        # Apply sorting and filtering for publications table
        if sort_column:
            if sort_column == "Download rate (pages downloadable from)*":
                df_filtered = df[df["Downloads"] >= 25].copy()
                if not df_filtered.empty:
                    df = df_filtered.sort_values("Download rate (pages downloadable from)", ascending=False).head(10)
                else:
                    df = df.iloc[0:0]
            else:
                df = df.sort_values(sort_column, ascending=False).head(10)

    # DRAW TABLE
    column_defs, grid_options, df_for_grid = elements.set_table_defaults(
        df=df,
        metrics=table_config["metrics"],
        sortable=False,
        sort_columns="index",
        sort_order="asc",
        filter=False,
        lockPinned=True,
    )

    column_defs = elements.create_internal_link(
        column_defs,
        table_config["title_column"],
        page_type=table_config["internal_link_type"],
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
    grid_options["pagination"] = True
    grid_options["paginationPageSize"] = 10
    grid_options["suppressPaginationPanel"] = True

    # Prevent column reordering
    grid_options["suppressMovableColumns"] = True

    # Enable auto-sizing on second+ tabs
    # NB: This is to get around an issue with streamlit-aggrid, with autosizing not working for tabs bar the first (https://github.com/PablocFonseca/streamlit-aggrid/issues/249)
    if tab_index > 0:
        grid_options["autoSizeStrategy"] = "SizeColumnsToFitProvidedWidthStrategy"

    # Add row numbers to show index
    grid_options["rowClassRules"] = {
        "row-index": "true"
    }

    # Add index column that updates after sorting
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

    if table_config["content_type"] == "Publication":
        METRICS_DISPLAY = config.DOWNLOAD_METRICS_DISPLAY

        for metric, formatter in METRICS_DISPLAY.items():
            column_defs[metric]["valueFormatter"] = formatter

    # Create the AgGrid table
    AgGrid(
        df_for_grid,
        key=f"ag_{table_config['content_type'].lower()}_{table_config['sql_script'].replace('.sql', '')}_{tab_index}",
        license_key=os.environ["AG_GRID_LICENCE_KEY"],
        enable_enterprise_modules="enterpriseOnly",
        gridOptions=grid_options,
        allow_unsafe_jscode=True,
        theme=StAggridTheme(base=AG_GRID_THEME_BASE).withParams(**theme_params),
        height=500,
    )

    if sort_column == "Download rate (pages downloadable from)*":
        st.warning(NOTES["download_rate_note"]["text"])

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


for tab_index, (tab_name, tables) in enumerate(TAB_CONFIG.items()):
    with tabs[tab_index]:

        # Group tables by their width to handle layout
        full_width_tables = [table for table in tables if table.get("width") == "full"]
        half_width_tables = [table for table in tables if table.get("width") == "half"]

        # Process full-width tables first
        for table_config in full_width_tables:
            st.subheader(table_config["display_name"])
            st.write("_Download figures for publications, plus page view figures for the pages from which they are downloadable_")

            # Add order by selectbox for publications table
            if table_config["content_type"] == "Publication":
                order_by_options = [
                    "Page views (pages downloadable from)",
                    "Downloads",
                    "Download rate (pages downloadable from)*"
                ]
                col1, col2 = st.columns([1, 3])

                with col1:
                    sort_column = st.selectbox(
                        label="Top 10 by",
                        options=order_by_options,
                        index=1,
                        key=f"order_by_{table_config['content_type']}_{tab_index}"
                    )
                create_table(table_config, tab_index, page_filter, start_date, end_date, connection, sort_column)
            else:
                create_table(table_config, tab_index, page_filter, start_date, end_date, connection)

        # Process half-width tables in pairs
        for i in range(0, len(half_width_tables), 2):
            columns = st.columns(2)

            # Process up to 2 tables in this row
            for col_idx in range(2):
                table_idx = i + col_idx
                if table_idx < len(half_width_tables):
                    table_config = half_width_tables[table_idx]

                    with columns[col_idx]:
                        st.subheader(table_config["display_name"])
                        create_table(table_config, tab_index, page_filter, start_date, end_date, connection)
