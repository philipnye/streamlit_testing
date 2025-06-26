from datetime import date, timedelta
import os
from typing import List

import pandas as pd
import plotly.express as px
from sqlalchemy import engine, exc
from st_aggrid import GridOptionsBuilder, JsCode
import streamlit as st

from streamlit_testing.config.colours import COLOURS
import streamlit_testing.pages.dashboard.web_metrics.config as config
from streamlit_testing.pages.dashboard.web_metrics.utils import (
    compare_dates, format_date,
)

import ds_utils.database_operations as dbo


@st.cache_data()
def calculate_derived_metrics(
    df: pd.DataFrame,
    calculations: dict
) -> pd.DataFrame:
    """Calculate derived metrics"""

    def _divide(x, y):
        if pd.isna(x) or pd.isna(y):
            return 0
        else:
            return x / y if y != 0 else 0

    if not calculations:
        return df

    for metric, (metric_1, metric_2, calculation) in calculations.items():
        if calculation == "divide":
            calculation = _divide
        df[metric] = df[metric_1].combine(
            df[metric_2], calculation
        )

    return df


def create_external_link(
    column_defs: dict,
    column: str,
) -> dict:
    """Create external link column"""

    column_defs[column]["cellRenderer"] = JsCode(f"""
        class UrlCellRenderer {{
            init(params) {{
                this.eGui = document.createElement("a");
                this.eGui.innerText = "View output ⮺";
                this.eGui.setAttribute(
                    "href", "https://www.instituteforgovernment.org.uk" + params.value
                );
                this.eGui.setAttribute("style", "text-decoration: none; color:{COLOURS['pink']};");
                this.eGui.setAttribute("target", "_blank");
            }}
            getGui() {{
                return this.eGui;
            }}
        }}
    """)
    return column_defs


def create_internal_link(
    column_defs: dict,
    column: str,
) -> dict:
    """Create internal link column"""

    column_defs[column]["cellRenderer"] = JsCode(f"""
        class UrlCellRenderer {{
            init(params) {{
                this.eGui = document.createElement("a");
                this.eGui.innerText = params.value;
                this.eGui.setAttribute(
                    "href", "/web_metrics_page_detail?url=" + params.data.URL
                );
                this.eGui.setAttribute("style", "text-decoration:none; color:{COLOURS['pink']};");
                this.eGui.setAttribute("target", "_blank");
            }}
            getGui() {{
                return this.eGui;
            }}
        }}
    """)
    return column_defs


def group_df(
    df: pd.DataFrame,
    group_by: list[str],
    dropna: bool = False
) -> pd.DataFrame:
    """Group dataframe by column"""

    df_grouped = df.groupby(group_by, dropna=dropna).sum().reset_index()

    return df_grouped


def set_table_defaults(
    df: pd.DataFrame,
    metrics: dict,
    sort_columns: str | List[str] | None = None,
    sort_order: str = "asc",
    pin_columns: str | List[str] | None = None
) -> tuple[dict, dict]:
    """Configure default table options"""

    grid_builder = GridOptionsBuilder.from_dataframe(df)
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

    if sort_columns:
        if isinstance(sort_columns, str):
            sort_columns = [sort_columns]
        for column in sort_columns:
            if column in column_defs:
                column_defs[column]["sort"] = sort_order

    if pin_columns:
        if isinstance(pin_columns, str):
            pin_columns = [pin_columns]
            for column in pin_columns:
                if column in column_defs:
                    column_defs[column]["pinned"] = "left"

    for metric, formatter in metrics.items():
        column_defs[metric]["valueFormatter"] = formatter

    return column_defs, grid_options


@st.cache_resource
def connect_database() -> engine.base.Engine:
    """Connect to SQL database"""

    return dbo.connect_sql_db(
        driver="pyodbc",
        driver_version=os.environ["ODBC_DRIVER"],
        dialect="mssql",
        server=os.environ["ODBC_SERVER"],
        database=os.environ["ODBC_DATABASE"],
        authentication=os.environ["ODBC_AUTHENTICATION"],
        username=os.environ["AZURE_CLIENT_ID"],
        password=os.environ["AZURE_CLIENT_SECRET"],
    )


def disable_sidebar():
    """Disable sidebar"""

    st.markdown(
        """
            <style>
                div[data-testid="stSidebarCollapsedControl"]{
                    display: none;
                }
                section[data-testid="stSidebar"][aria-expanded="true"]{
                    display: none;
                }
            </style>
        """,
        unsafe_allow_html=True
    )

    return


def draw_date_range_inputs(
    min_date: str,
    max_date: str,
) -> tuple[str, pd.Timestamp, pd.Timestamp]:
    """Draw date range option inputs"""

    col1, col2 = st.columns([1, 5])

    with col1:
        date_range_option = st.selectbox(
            label="Choose date range",
            options=config.DATE_RANGES.keys(),
            index=list(config.DATE_RANGES.keys()).index(config.DEFAULT_DATE_RANGE),
            key="date_range_option",
        )

    if config.DATE_RANGES[date_range_option]:
        start_date = (
            date.today() - timedelta(days=config.DATE_RANGES[date_range_option])
        ).strftime("%Y-%m-%d")
        end_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    elif date_range_option == "Year to date":
        start_date = date.today().strftime("%Y-01-01")
        end_date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    elif date_range_option == "Custom":
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            start_date = st.date_input(
                label="Start date",
                value=min_date,
                min_value=min_date,
                max_value=max_date,
                key="start_date",
            )
        with col2:
            end_date = st.date_input(
                label="End date",
                value=max_date,
                min_value=min_date,
                max_value=max_date,
                key="end_date",
            )

    start_date = pd.to_datetime(start_date).date()
    end_date = pd.to_datetime(end_date).date()

    return date_range_option, start_date, end_date


def draw_line_chart_section(
    df: pd.DataFrame,
    x: str,
    metrics: list[str],
    default_metric: str,
) -> str:
    """
    Draw line chart section

    Notes:
    - fixedrange=True is required to disable zooming
    - y-axis range is extended slightly beyond the highest value to force plotly to draw a gridline - it won't draw a gridline at the edge of the chart
    """

    with st.container(
        border=True,
    ):
        col1, col2 = st.columns([1, 5])

        with col1:
            selected_metric = st.selectbox(
                label="Metric",
                label_visibility="collapsed",
                options=metrics,
                index=metrics.index(default_metric),
                disabled=len(metrics) == 1,
                key="selected_metric",
            )

        # Calculate sensible y-axis max
        y_data = df[selected_metric].dropna()
        if not y_data.empty:
            y_max = y_data.max()

            import math
            if y_max == 0:
                y_axis_max = 1
            else:
                magnitude = 10 ** math.floor(math.log10(y_max))
                for factor in [1, 2, 5, 10, 100, 1000]:
                    if y_max <= factor * magnitude:
                        y_axis_max = factor * magnitude
                        break
                else:
                    y_axis_max = 10 * magnitude
        else:
            y_axis_max = 1

        fig = px.line(
            df,
            x=x,
            y=selected_metric,
            color_discrete_sequence=[COLOURS["pink"]],
        )
        fig.update_layout(
            xaxis_title="",
            yaxis_title="",
            xaxis=dict(
                zeroline=False,
                tickfont=dict(
                    color=COLOURS["dark_grey"],
                    family="Open Sans, sans-serif",
                    size=14,
                ),
                gridcolor=COLOURS["grey_lighter_80pct"],
                fixedrange=True,
                tickformat="%a %d %b",
            ),
            yaxis=dict(
                zeroline=True,
                zerolinecolor=COLOURS["dark_grey"],
                tickfont=dict(
                    color=COLOURS["dark_grey"],
                    family="Open Sans, sans-serif",
                    size=14,
                ),
                gridcolor=COLOURS["grey_lighter_80pct"],
                range=[0, y_axis_max * 1.01],
                tickformat=config.YAXIS_TICKFORMAT.get(selected_metric),
                fixedrange=True,
            ),
            plot_bgcolor="white",
        )
        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displayModeBar": False,
                "displaylogo": False,
                "scrollZoom": False,
                "doubleClick": False,
                "showAxisDragHandles": False,
                "showAxisRangeEntryBoxes": False,
                "editSelection": False,
            }
        )

    return selected_metric


def format_date_cols(
    column_defs: dict,
    metrics: list[str],
) -> dict:
    """Format date columns"""

    for metric in metrics:
        column_defs[metric]["type"] = "dateColumn"
        column_defs[metric]["cellClass"] = "ag-right-aligned-cell"
        column_defs[metric]["headerClass"] = "ag-right-aligned-header"
        column_defs[metric]["cellRenderer"] = format_date
        column_defs[metric]["comparator"] = compare_dates
        column_defs[metric]["filter"] = "agDateColumnFilter"
        column_defs[metric]["filterParams"] = {"comparator": compare_dates}

    return column_defs


@st.cache_data(show_spinner="Loading data...")
def load_data(
    script: str,
    _connection: engine.base.Engine,
    params: dict = None,
) -> pd.DataFrame:
    """Load data from database"""

    try:
        df = pd.read_sql_query(
            sql=script,
            con=_connection,
            params=params,
        )
    except exc.DBAPIError:
        df = pd.read_sql_query(
            sql=script,
            con=_connection,
            params=params,
        )

    return df


@st.dialog("Page not found")
def raise_page_not_found_message():
    """Raise page not found message"""
    st.write(
        "The page that you have requested does not seem to exist."
    )

    return
