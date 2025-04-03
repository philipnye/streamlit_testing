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

with open("streamlit_testing/js/compare_dates.js", "r") as f:
    script = f.read()
    compare_dates = JsCode(script)


def set_metrics(
    metric_type: str
) -> tuple[list, dict, str]:
    """Set metrics based on metric type"""

    if metric_type == "web_traffic":
        metrics_raw = config.web_traffic_metrics_raw
        metrics_display = config.web_traffic_metrics_display
        metric_aggregations = config.web_traffic_metric_aggregations
        metric_calculations = config.web_traffic_metric_calculations
        default_metric = config.default_web_traffic_metric
    elif metric_type == "download":
        metrics_raw = config.download_metrics_raw
        metrics_display = config.download_metrics_display
        metric_aggregations = config.download_metric_aggregations
        metric_calculations = config.download_metric_calculations
        default_metric = config.default_download_metric

    return (
        metrics_raw,
        metrics_display,
        metric_aggregations,
        metric_calculations,
        default_metric
    )
