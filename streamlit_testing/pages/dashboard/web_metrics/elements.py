from datetime import date, timedelta

import pandas as pd
import streamlit as st

import streamlit_testing.pages.dashboard.web_metrics.config as config


def draw_date_range_inputs(
    min_date: str,
    max_date: str,
) -> tuple[pd.Timestamp, pd.Timestamp]:
    """Draw date range option inputs"""

    col1, col2 = st.columns([1, 5])

    with col1:
        date_range_option = st.selectbox(
            label="Choose date range",
            options=config.date_ranges.keys(),
            index=list(config.date_ranges.keys()).index(config.default_date_range),
            key="date_range_option",
        )

    if config.date_ranges[date_range_option]:
        start_date = (
            date.today() - timedelta(days=config.date_ranges[date_range_option])
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

    return start_date, end_date


def draw_line_chart_section(
    df: pd.DataFrame,
    x: str,
    metrics: list[str],
    default_metric: str,
) -> None:
    """Draw line chart section"""

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

        st.line_chart(
            data=df,
            x=x,
            y=selected_metric,
            use_container_width=True,
            x_label="",
            y_label="",
        )

    return
