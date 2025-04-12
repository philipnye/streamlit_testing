from streamlit_testing.pages.dashboard.web_metrics.utils import (
    format_integer, format_decimal, format_percentage, format_time
)

breakdowns = [
    "Content type",
    "Publication type",
    "Research area",
    "Tag",
    "Author",
    "Published date: year",
    "Published date: month",
    "Published date: day",
    "Updated date: year",
    "Updated date: month",
    "Updated date: day",
]
date_ranges = {
    "Last 7 days": 7,
    "Last 30 days": 30,
    "Last 90 days": 90,
    "Last 12 months": 365,
    "Year to date": None,
    "Custom": None,
}
default_breakdowns = "Content type"
default_date_range = "Last 30 days"
default_download_metric = "Downloads"
default_web_traffic_metric = "Page views"
download_metric_aggregations = {
    "Downloads": ("Downloads", "sum"),
}
download_metric_calculations = None
download_metrics_display = {
    "Downloads": format_integer,
}
download_metrics_raw = [
    "Downloads",
]
metrics_by_output = [
    "Output title",
    "File name",
    "File extension",
    "Content type",
    "Published date",
    "Updated date",
    "Authors",
    "Research areas",
    "Tags",
]
metrics_by_page = [
    "Page title",
    "URL",
    "Content type",
    "Published date",
    "Updated date",
    "Authors",
    "Research areas",
    "Tags",
]
web_traffic_metric_aggregations = {
    "Page views": ("Page views", "sum"),
    "Active users": ("Active users", "sum"),
    "Sessions": ("Sessions", "sum"),
    "Engaged sessions": ("Engaged sessions", "sum"),
    "User engagement duration": ("User engagement duration", "sum"),
    "Downloads": ("Downloads", "sum"),
}
web_traffic_metric_calculations = {
    "Page views per active user": (
        "Page views",
        "Active users",
        "divide"
    ),
    "Engagement rate": (
        "Engaged sessions",
        "Sessions",
        "divide"
    ),
    "Average engagement time per active user": (
        "User engagement duration",
        "Active users",
        "divide"
    ),
    "Download rate": (
        "Downloads",
        "Page views",
        "divide"
    ),
}
web_traffic_metrics_display = {
    "Page views": format_integer,
    "Active users": format_integer,
    "Page views per active user": format_decimal,
    "Engagement rate": format_percentage,
    "Average engagement time per active user": format_time,
    "Downloads": format_integer,
    "Download rate": format_percentage,
}
web_traffic_metrics_raw = [
    "Page views",
    "Active users",
    "Sessions",
    "Engaged sessions",
    "User engagement duration",
    "Downloads",
]
