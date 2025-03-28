from st_aggrid import JsCode

import streamlit_testing.pages.dashboard.web_traffic.config as config

apply_locale_string = JsCode("""
    function stringFormatter(params) {
        if (!params.value) {
            return params.value;
        } else {
            return params.value.toLocaleString();
        }
    }
""")
format_date = JsCode("""
    function stringFormatter(params) {
        const date = new Date(params.value);
        const formattedDate = date.toLocaleString('default', {
            day: 'numeric',
            month: 'long',
            year: 'numeric',
        });
        return formattedDate;
    }
""")
format_date_comparator = JsCode("""
    function(comparatorDate, cellValue) {
        const formattedDate = cellValue.toLocaleString('default');
        if (formattedDate < comparatorDate) {
        return 1;
        } else if (formattedDate > comparatorDate) {
        return -1;
        } else {
        return 0;
        }
    }
""")


def set_metrics(
    metric_type: str
) -> tuple[list, dict, str]:
    """Set metrics based on metric type"""

    if metric_type == "web_traffic":
        metrics = config.web_traffic_metrics
        metric_aggregations = config.web_traffic_metric_aggregations
        default_metric = config.default_web_traffic_metric
    elif metric_type == "download":
        metrics = config.download_metrics
        metric_aggregations = config.download_metric_aggregations
        default_metric = config.default_download_metric

    return metrics, metric_aggregations, default_metric
