from datetime import date, timedelta
import math
import os
from typing import List

import pandas as pd
import plotly.graph_objects as go
from sqlalchemy import engine, exc
from st_aggrid import GridOptionsBuilder, JsCode
import streamlit as st

from streamlit_testing.config.ag_grid_theme import (
    AG_GRID_ROW_HEIGHT, AG_GRID_HEADER_HEIGHT,
    AG_GRID_MIN_HEIGHT, AG_GRID_MAX_HEIGHT
)
from streamlit_testing.config.colours import COLOURS
import streamlit_testing.pages.dashboard.web_metrics.config as config
from streamlit_testing.pages.dashboard.web_metrics.chart_annotations import CHART_ANNOTATIONS
from streamlit_testing.pages.dashboard.web_metrics.definitions import DEFINITIONS
from streamlit_testing.pages.dashboard.web_metrics.notes import NOTES
from streamlit_testing.pages.dashboard.web_metrics.utils import (
    filter_dates, format_date, sort_dates
)

import ds_utils.database_operations as dbo


def draw_redact_data_warning():
    """Draw a flashing warning when in redact data mode"""
    st.html("""
        <style>
        @keyframes slow-flash {
            0%, 50% { opacity: 1; }
            25%, 75% { opacity: 0.3; }
        }
        .flashing-warning {
            animation: slow-flash 6s infinite;
        }
        </style>
        <h1 class='flashing-warning' style='color: #d0006f; font-size: 24px; font-family: Aller, sans-serif; font-weight: 700; text-align: right;'>[Data values obscured]</h1>
    """)


@st.cache_data(ttl="5h")
def calculate_derived_metrics(
    df: pd.DataFrame,
    calculations: dict | None
) -> pd.DataFrame:
    """Calculate derived metrics"""

    def _divide(x, y):
        if pd.isna(x) or pd.isna(y):
            return pd.NA
        else:
            return x / y if y != 0 else pd.NA

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
    link_text: str
) -> dict:
    """Create external link column"""

    column_defs[column]["cellRenderer"] = JsCode(f"""
        class UrlCellRenderer {{
            init(params) {{
                // Check if the cell value is empty or null
                if (!params.value || params.value === '') {{
                    this.eGui = document.createElement("span");
                    this.eGui.innerText = "";
                }} else {{
                    this.eGui = document.createElement("a");
                    this.eGui.innerText = "{link_text}";
                    this.eGui.setAttribute(
                        "href", "https://www.instituteforgovernment.org.uk" + params.value
                    );
                    this.eGui.setAttribute("style", "text-decoration: none; color:{COLOURS['pink']};");
                    this.eGui.setAttribute("target", "_blank");
                }}
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
    page_type: str,
) -> dict:
    """Create internal link column"""

    # Determine URL path based on page type
    if page_type == "page":
        url_path = "/web_metrics_page_detail"
    elif page_type == "publication":
        url_path = "/web_metrics_publication_detail"

    column_defs[column]["cellRenderer"] = JsCode(f"""
        class UrlCellRenderer {{
            init(params) {{
                // Check if the cell value is empty or null, or if it's a totals row
                if (!params.value || params.value === '' || params.value === 'Total') {{
                    this.eGui = document.createElement("span");
                    this.eGui.innerText = params.value || "";
                }} else {{
                    this.eGui = document.createElement("a");
                    this.eGui.innerText = params.value;
                    this.eGui.setAttribute(
                        "href", "{url_path}?url=" + params.data.Link
                    );
                    this.eGui.setAttribute("style", "text-decoration:none; color:{COLOURS['pink']};");
                    this.eGui.setAttribute("target", "_blank");
                }}
            }}
            getGui() {{
                return this.eGui;
            }}
        }}
    """)
    return column_defs


def add_column_header_tooltips(
    column_defs: dict,
    definitions: dict = DEFINITIONS
) -> dict:
    """Add tooltips to column headers using definitions"""

    for column_name, column_def in column_defs.items():
        if column_name in definitions:
            column_def["headerTooltip"] = definitions[column_name]

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
    sortable: bool = True,
    sort_columns: str | List[str] | None = None,
    sort_order: str | dict[str, str] = "asc",
    filter: bool = True,
    lockPinned: bool = False,
    pin_columns: str | List[str] | None = None,
) -> tuple[dict, dict, pd.DataFrame]:
    """
    Configure default table options

    Notes:
    - Care needs to be taken if more than one column is pinned, as on small screen AG Grid can unpin columns left-to-right, which can result in unexpected behaviour (https://github.com/ag-grid/ag-grid/issues/8335)
    """

    grid_builder = GridOptionsBuilder.from_dataframe(df)
    grid_options = grid_builder.build()

    grid_options["pagination"] = True
    grid_options["paginationPageSize"] = 20
    grid_options["defaultColDef"] = {
        "filter": filter,
        "filterParams": {
            "excelMode": "windows",
        },
        "sortable": sortable,
        "lockPinned": lockPinned,
    }

    column_defs = {column_def["field"]: column_def for column_def in grid_options["columnDefs"]}

    if sort_columns:
        if isinstance(sort_columns, str):
            sort_columns = [sort_columns]
        for column in sort_columns:
            if column in column_defs:
                column_defs[column]["sort"] = sort_order if isinstance(sort_order, str) else sort_order.get(column, "asc")

    if isinstance(sort_order, dict):
        for column, first_sort in sort_order.items():
            if column in column_defs:
                if first_sort == "desc":
                    column_defs[column]["sortingOrder"] = ["desc", "asc", None]
                else:
                    column_defs[column]["sortingOrder"] = ["asc", "desc", None]

    if pin_columns:
        if isinstance(pin_columns, str):
            pin_columns = [pin_columns]
        for column in pin_columns:
            if column in column_defs:
                column_defs[column]["pinned"] = "left"

    for metric in metrics:
        column_defs[metric]["sortingOrder"] = ["desc", "asc", None]

    # Add tooltips to column headers
    column_defs = add_column_header_tooltips(column_defs)

    return column_defs, grid_options


@st.cache_resource(ttl="5h")
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


def disable_sidebar() -> None:
    """Disable sidebar"""

    st.markdown(
        """
            <style>
                div[data-testid="stSidebarCollapsedControl"] {
                    display: none;
                }
                section[data-testid="stSidebar"][aria-expanded="true"] {
                    display: none;
                }
                button[data-testid="stExpandSidebarButton"] {
                    display: none;
                }
            </style>
        """,
        unsafe_allow_html=True
    )

    return


def save_session_state_value(key):
    st.session_state[key] = st.session_state["_"+key]


def load_session_state_value(key):
    st.session_state["_"+key] = st.session_state[key]


def draw_date_range_inputs(
    min_date: date,
    max_date: date,
) -> tuple[str, date, date]:
    """Draw date range option inputs"""

    # Initialise session state keys if they don't exist
    if "date_range_option" not in st.session_state:
        st.session_state["date_range_option"] = config.DEFAULT_DATE_RANGE
    if "start_date" not in st.session_state:
        st.session_state["start_date"] = min_date
    if "end_date" not in st.session_state:
        st.session_state["end_date"] = max_date

    col1, col2 = st.columns([1, 5])

    with col1:
        load_session_state_value("date_range_option")
        date_range_option = st.selectbox(
            label="Choose date range",
            options=config.DATE_RANGES.keys(),
            key="_date_range_option",
            on_change=save_session_state_value,
            args=["date_range_option"],
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
            load_session_state_value("start_date")
            start_date = st.date_input(
                label="Start date",
                min_value=min_date,
                max_value=max_date,
                format="DD/MM/YYYY",
                help=f"{min_date.strftime('%d %B %Y')} is the earliest date for which data is available",
                key="_start_date",
                on_change=save_session_state_value,
                args=["start_date"],
            )
        with col2:
            load_session_state_value("end_date")
            end_date = st.date_input(
                label="End date",
                min_value=min_date,
                max_value=max_date,
                format="DD/MM/YYYY",
                key="_end_date",
                on_change=save_session_state_value,
                args=["end_date"],
            )

    start_date = pd.to_datetime(start_date).date()
    end_date = pd.to_datetime(end_date).date()

    return date_range_option, start_date, end_date


def draw_badge_with_date(
    display_date: str | date,
    text: str,
    color: str = "primary"
) -> None:
    """Draw badge with date"""

    if isinstance(display_date, date):
        display_date = "{dt.day} {dt:%B} {dt.year}".format(dt=display_date)
    elif isinstance(display_date, str):
        display_date = "{dt.day} {dt:%B} {dt.year}".format(dt=pd.to_datetime(display_date))

    st.badge(text + display_date, color=color)

    return


def draw_latest_data_badge(display_date: str | date) -> None:
    """Draw latest data badge"""

    draw_badge_with_date(
        display_date=display_date,
        text="Includes data up to: ",
    )

    return


def draw_last_updated_badge(display_date: str | date) -> None:
    """Draw last updated badge"""

    draw_badge_with_date(
        display_date=display_date,
        text="Last updated: ",
    )

    return


def draw_line_chart_section(
    df: pd.DataFrame,
    x: str,
    start_date: date,
    end_date: date,
    metrics: list[str],
    default_metric: str,
    content_type: str = "pages",
    show_all_content_warning: bool = True,
    redact_data: bool = False,
) -> str:
    """
    Draw line chart section

    Notes:
    - fixedrange=True is required to disable zooming
    - y-axis range is extended slightly beyond the highest value to force plotly to draw a gridline - it won't draw a gridline at the edge of the chart
    - Final 48 hours are marked as being provisional
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

        # Handle case where start_date is earlier than first date in data
        df_chart = df.copy()

        # Calculate sensible y-axis max
        y_data = df_chart[selected_metric].dropna()
        if not y_data.empty:
            y_max = y_data.max()

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

        # Split data into final and provisional, with different styling
        # NB: In Plotly GO, styling applies to the line segment that follows a point
        # This would therefore mean Final styling would be applied to the line segment
        # between the last final point and the first provisional point. In order to
        # get around this, a third segment - labelled "Final", but applying provisional
        # styling - is added
        # NB: Data segments need to contain two or more points in order for a line to be
        # drawn
        df_chart_sorted = df_chart.sort_values(x)
        end_date_minus_1_day = pd.to_datetime(end_date) - pd.Timedelta(days=1)
        end_date_minus_2_days = pd.to_datetime(end_date) - pd.Timedelta(days=2)

        df_final = df_chart_sorted[df_chart_sorted[x] <= end_date_minus_2_days]
        df_finalprovisional = df_chart_sorted[
            df_chart_sorted[x].isin([end_date_minus_2_days, end_date_minus_1_day])
        ]
        df_provisional = df_chart_sorted[df_chart_sorted[x] >= end_date_minus_1_day]

        # Create figure with go.Figure for more control
        fig = go.Figure()

        # Function to identify isolated points (not connected to other points)
        def get_isolated_points(df_segment):
            """Identify points that are isolated (surrounded by NA values)"""
            if df_segment.empty or len(df_segment) < 3:
                return pd.DataFrame()

            df_sorted = df_segment.sort_values(x).reset_index(drop=True)
            isolated_points = []

            for i in range(len(df_sorted)):
                current_value = df_sorted.iloc[i][selected_metric]

                # Skip if current value is NA
                if pd.isna(current_value):
                    continue

                # Check previous value
                prev_na = True
                if i > 0:
                    prev_value = df_sorted.iloc[i-1][selected_metric]
                    prev_na = pd.isna(prev_value)

                # Check next value
                next_na = True
                if i < len(df_sorted) - 1:
                    next_value = df_sorted.iloc[i+1][selected_metric]
                    next_na = pd.isna(next_value)

                # If both previous and next are NA, this is an isolated point
                if prev_na and next_na:
                    isolated_points.append(df_sorted.iloc[i])

            return pd.DataFrame(isolated_points) if isolated_points else pd.DataFrame()

        # Add final data line
        if not df_final.empty:
            hovertemplate = "%{x|%a %e %b}: xxxxx <span style='color:#d0006f'>(final)</span><extra></extra>" if redact_data else "%{x|%a %e %b}: %{y} <span style='color:#d0006f'>(final)</span><extra></extra>"
            fig.add_trace(go.Scatter(
                x=df_final[x],
                y=df_final[selected_metric],
                mode="lines",
                line=dict(color=COLOURS["pink"], width=2),
                name="Final",
                showlegend=True,
                hovertemplate=hovertemplate
            ))

        # Add final/provisional data line
        if not df_finalprovisional.empty:
            hovertemplate = "%{x|%a %e %b}: xxxxx <span style='color:#d0006f'>(final)</span><extra></extra>" if redact_data else "%{x|%a %e %b}: %{y} <span style='color:#d0006f'>(final)</span><extra></extra>"
            fig.add_trace(go.Scatter(
                x=df_finalprovisional[x],
                y=df_finalprovisional[selected_metric],
                mode="lines",
                line=dict(color=COLOURS["pink"], width=2, dash="dot"),
                name="Final",
                showlegend=True,
                hovertemplate=hovertemplate
            ))

        # Add provisional data line
        if not df_provisional.empty:
            hovertemplate = "%{x|%a %e %b}: xxxxx <span style='color:#d0006f'>(provisional)</span><extra></extra>" if redact_data else "%{x|%a %e %b}: %{y} <span style='color:#d0006f'>(provisional)</span><extra></extra>"
            fig.add_trace(go.Scatter(
                x=df_provisional[x],
                y=df_provisional[selected_metric],
                mode="lines",
                line=dict(color=COLOURS["pink"], width=2, dash="dot"),
                name="Provisional",
                showlegend=True,
                hovertemplate=hovertemplate
            ))

        # Add isolated points for all segments
        for df_segment, color, name in [
            (df_final, COLOURS["pink"], "Final"),
            (df_finalprovisional, COLOURS["pink"], "Final"),
            (df_provisional, COLOURS["pink"], "Provisional")
        ]:
            isolated_points = get_isolated_points(df_segment)
            if not isolated_points.empty:
                # Set tooltip based on data type and redact data mode
                if redact_data:
                    if name == "Final":
                        hovertemplate = "%{x|%a %e %b}: xxxxx <span style='color:#d0006f'>(final)</span><extra></extra>"
                    else:
                        hovertemplate = "%{x|%a %e %b}: xxxxx <span style='color:#d0006f'>(provisional)</span><extra></extra>"
                else:
                    if name == "Final":
                        hovertemplate = "%{x|%a %e %b}: %{y} <span style='color:#d0006f'>(final)</span><extra></extra>"
                    else:
                        hovertemplate = "%{x|%a %e %b}: %{y} <span style='color:#d0006f'>(provisional)</span><extra></extra>"

                fig.add_trace(go.Scatter(
                    x=isolated_points[x],
                    y=isolated_points[selected_metric],
                    mode="markers",
                    marker=dict(
                        color=color,
                        size=6,
                        symbol="circle"
                    ),
                    name=name,
                    showlegend=False,
                    hovertemplate=hovertemplate
                ))

        # Handle special formatting for time-based metrics
        yaxis_config = dict(
            zeroline=True,
            zerolinecolor=COLOURS["dark_grey"],
            tickfont=dict(
                color=COLOURS["dark_grey"],
                family="Aller Light, sans-serif",
                size=12,
            ),
            gridcolor=COLOURS["grey_lighter_80pct"],
            fixedrange=True,
        )

        # Special handling for time metrics
        if config.YAXIS_TICKFORMAT.get(selected_metric) == "hh:mm:ss":

            def format_seconds_to_hms(seconds):
                """Convert seconds to hh:mm:ss format"""
                if pd.isna(seconds) or seconds < 0:
                    return "00:00:00"
                hours = int(seconds // 3600)
                minutes = int((seconds % 3600) // 60)
                secs = int(seconds % 60)
                return f"{hours:02d}:{minutes:02d}:{secs:02d}"

            # Generate appropriate tick values based on the data range
            if y_axis_max <= 60:
                tick_interval = 10
            elif y_axis_max <= 300:
                tick_interval = 30
            elif y_axis_max <= 600:
                tick_interval = 60
            elif y_axis_max <= 1800:
                tick_interval = 300
            elif y_axis_max <= 3600:
                tick_interval = 600
            else:
                tick_interval = 900

            # Round y_axis_max up to the next tick interval to ensure regular spacing
            adjusted_y_axis_max = math.ceil(y_axis_max / tick_interval) * tick_interval

            # Generate tick values at regular intervals
            tick_vals = list(range(0, adjusted_y_axis_max + 1, tick_interval))
            tick_text = [format_seconds_to_hms(val) for val in tick_vals]

            # Update the y-axis range to match the adjusted maximum
            yaxis_config["range"] = [0, adjusted_y_axis_max * 1.01]

            yaxis_config.update({
                "tickvals": tick_vals,
                "ticktext": tick_text,
            })

        # Use standard tick formatting for other metrics
        else:
            yaxis_config["range"] = [0, y_axis_max * 1.01]
            yaxis_config["tickformat"] = config.YAXIS_TICKFORMAT.get(selected_metric)

        # Override tick labels with 'xxxxx' if using redact data
        if redact_data:
            if "tickvals" in yaxis_config:
                tick_vals = yaxis_config["tickvals"]
            else:
                tick_vals = list(range(0, int(y_axis_max * 1.01) + 1, max(1, int(y_axis_max / 5))))
                yaxis_config["tickvals"] = tick_vals

            # Replace all tick labels with 'xxxxx'
            yaxis_config["ticktext"] = ["xxxxx"] * len(tick_vals)

        # Add chart annotations for ranges within the chart date range
        range_highlights = []
        annotations = []

        for annotation in CHART_ANNOTATIONS:
            annotation_start = pd.to_datetime(annotation["start_date"]).date()
            annotation_end = pd.to_datetime(annotation["end_date"]).date()

            # Check if annotation range overlaps with chart date range
            if annotation_start <= end_date and annotation_end >= start_date:

                # Clip annotation range to chart range
                clipped_start = max(annotation_start, start_date)
                clipped_end = min(annotation_end, end_date)

                # Add range highlight as a shape
                range_highlights.append(
                    dict(
                        type="rect",
                        xref="x",
                        yref="y",
                        x0=clipped_start,
                        y0=0,
                        x1=clipped_end,
                        y1=y_axis_max * 1.01,
                        fillcolor=COLOURS["grey_darker_25pct"],
                        opacity=0.3,
                        line=dict(width=0),
                        layer="below"
                    )
                )

                # Add text annotation
                # Position based on annotation position setting
                if annotation.get("position") == "end":
                    x_pos = clipped_end + pd.Timedelta(days=2)
                    xanchor = "left"
                else:
                    x_pos = clipped_start
                    xanchor = "right"

                # Add line breaks to description for better readability
                description = annotation["text"]
                if len(description) > 40:
                    words = description.split()
                    lines = []
                    current_line = ""

                    for word in words:
                        if len(current_line + " " + word) > 40 and current_line:
                            lines.append(current_line)
                            current_line = word
                        else:
                            current_line = current_line + " " + word if current_line else word

                    # Add the last line
                    if current_line:
                        lines.append(current_line)

                    description = "<br>".join(lines)

                annotations.append(
                    dict(
                        x=x_pos,
                        y=y_axis_max * 0.9,
                        text=description,
                        showarrow=False,
                        font=dict(
                            color=COLOURS["dark_grey"],
                            size=12,
                            family="Aller Light, sans-serif"
                        ),
                        xanchor=xanchor,
                        yanchor="top",
                        align="left"
                    )
                )

        fig.update_layout(
            title=dict(
                text=selected_metric + (f", all {content_type}" if show_all_content_warning else ""),
                font=dict(
                    color=COLOURS["dark_grey"],
                    family="Aller, sans-serif",
                    size=16,
                ),
                x=0.01,
                y=0.9,
            ),
            xaxis_title="",
            yaxis_title="",
            showlegend=False,
            hoverlabel=dict(
                bgcolor="white",
                bordercolor=COLOURS["grey"],
                font=dict(
                    family="Aller Light, sans-serif",
                    size=12,
                    color=COLOURS["dark_grey"]
                )
            ),
            xaxis=dict(
                zeroline=False,
                tickfont=dict(
                    color=COLOURS["dark_grey"],
                    family="Aller Light, sans-serif",
                    size=12,
                ),
                gridcolor=COLOURS["grey_lighter_80pct"],
                fixedrange=True,
                tickformat="%a %e %b",
            ),
            yaxis=yaxis_config,
            plot_bgcolor="white",
            shapes=range_highlights,
            annotations=annotations,
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

        # Add general line chart caveat
        if show_all_content_warning:
            st.warning(NOTES["line_chart_all_content_note"]["text"].format(content_type=content_type))

        # Check if the selected metric contains any NA values and show warning
        if df_chart[selected_metric].isna().any():
            st.warning(NOTES["chart_blanks_note"]["text"])

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
        column_defs[metric]["comparator"] = sort_dates
        column_defs[metric]["filter"] = "agDateColumnFilter"
        column_defs[metric]["filterParams"] = {
            "comparator": filter_dates,
            "includeTime": False,
            "maxNumConditions": 1,
        }

    return column_defs


@st.cache_data(ttl="5h", show_spinner="Loading data...")
def load_data(
    script: str,
    _connection: engine.base.Engine,
    params: tuple | None = None,
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
def raise_page_not_found_message() -> None:
    """Raise page not found message"""
    st.write(
        "The page that you have requested doesn't seem to exist."
    )

    return


@st.cache_data(ttl="5h")
def calculate_ag_grid_height(
    num_rows: int,
    row_height: int = None,
    header_height: int = None,
    min_height: int = None,
    max_height: int = None
) -> int:
    """Calculate dynamic height for AgGrid based on number of rows"""

    row_height = row_height or AG_GRID_ROW_HEIGHT
    header_height = header_height or AG_GRID_HEADER_HEIGHT
    min_height = min_height or AG_GRID_MIN_HEIGHT
    max_height = max_height or AG_GRID_MAX_HEIGHT

    calculated_height = num_rows * row_height + header_height
    return min(max(calculated_height, min_height), max_height)


def fill_missing_dates(
    df: pd.DataFrame,
    start_date: date,
    end_date: date,
    date_column: str,
    fill_columns: list[str],
) -> pd.DataFrame:
    """
    Fill missing dates between start_date and end_date with zeros for specified columns

    Args:
        df: DataFrame with date column and metrics to fill
        start_date: Start date for the range
        end_date: End date for the range
        date_column: Name of the date column (default "Date")
        fill_columns: List of columns to fill with zeros (if None, fills all numeric columns)

    Returns:
        DataFrame with missing dates filled with zeros
    """
    if df.empty:
        return df

    # Convert date column to datetime if it's not already
    df = df.copy()
    df[date_column] = pd.to_datetime(df[date_column])

    # Create complete date range
    date_range = pd.date_range(start=start_date, end=end_date, freq="D")
    complete_dates_df = pd.DataFrame({date_column: date_range})

    # Merge with original data
    result_df = complete_dates_df.merge(df, on=date_column, how="left")

    # Fill missing values with zeros for specified columns
    for col in fill_columns:
        if col in result_df.columns:
            result_df[col] = result_df[col].fillna(0)

    return result_df
