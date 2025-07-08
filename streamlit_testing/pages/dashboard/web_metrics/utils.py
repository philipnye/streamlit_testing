from st_aggrid import JsCode

import streamlit_testing.pages.dashboard.web_metrics.config as config

with open("streamlit_testing/js/format_date.js", "r") as f:
    script = f.read()
    format_date = JsCode(script)
with open("streamlit_testing/js/format_decimal.js", "r") as f:
    script = f.read()
    format_decimal = JsCode(script)
with open("streamlit_testing/js/format_integer.js", "r") as f:
    script = f.read()
    format_integer = JsCode(script)
with open("streamlit_testing/js/format_percentage.js", "r") as f:
    script = f.read()
    format_percentage = JsCode(script)
with open("streamlit_testing/js/format_time.js", "r") as f:
    script = f.read()
    format_time = JsCode(script)
with open("streamlit_testing/js/sort_dates_comparator.js", "r") as f:
    script = f.read()
    sort_dates = JsCode(script)
with open("streamlit_testing/js/filter_dates_comparator.js", "r") as f:
    script = f.read()
    filter_dates = JsCode(script)


def set_metrics(
    metric_type: str
) -> tuple[list, dict, dict, dict | None, str]:
    """Set metrics based on metric type"""

    if metric_type == "web_traffic":
        metrics_raw = config.WEB_TRAFFIC_METRICS_RAW
        metrics_display = config.WEB_TRAFFIC_METRICS_DISPLAY
        metric_aggregations = config.WEB_TRAFFIC_METRIC_AGGREGATIONS
        metric_calculations = config.WEB_TRAFFIC_METRIC_CALCULATIONS
        default_metric = config.DEFAULT_WEB_TRAFFIC_METRIC
    elif metric_type == "download":
        metrics_raw = config.DOWNLOAD_METRICS_RAW
        metrics_display = config.DOWNLOAD_METRICS_DISPLAY
        metric_aggregations = config.DOWNLOAD_METRIC_AGGREGATIONS
        metric_calculations = config.DOWNLOAD_METRIC_CALCULATIONS
        default_metric = config.DEFAULT_DOWNLOAD_METRIC

    return (
        metrics_raw,
        metrics_display,
        metric_aggregations,
        metric_calculations,
        default_metric
    )
