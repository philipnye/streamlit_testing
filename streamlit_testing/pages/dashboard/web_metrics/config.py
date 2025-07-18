from streamlit_testing.pages.dashboard.web_metrics.utils import (
    format_integer, format_decimal, format_percentage, format_time
)

BREAKDOWNS = [
    "Content type",
    "Publication type",
    "Team",
    "Author",
    "Topic",
    "Published date: year",
    "Published date: month",
    "Published date: day",
    "Updated date: year",
    "Updated date: month",
    "Updated date: day",
]
DATE_RANGES = {
    "Last 7 days": 7,
    "Last 30 days": 30,
    "Last 90 days": 90,
    "Last 12 months": 365,
    "Year to date": None,
    "Custom": None,
}
DEFAULT_BREAKDOWNS = "Content type"
DEFAULT_DATE_RANGE = "Last 30 days"
DEFAULT_DOWNLOAD_METRIC = "Downloads"
DEFAULT_WEB_TRAFFIC_METRIC = "Page views"
DOWNLOAD_METRIC_AGGREGATIONS = {
    "Page views (pages downloadable from)": ("Page views (pages downloadable from)", "sum"),
    "Downloads": ("Downloads", "sum"),
}
DOWNLOAD_METRIC_CALCULATIONS = {
    "Download rate (pages downloadable from)": (
        "Downloads",
        "Page views (pages downloadable from)",
        "divide"
    ),
}
DOWNLOAD_METRICS_DISPLAY = {
    "Page views (pages downloadable from)": format_integer,
    "Downloads": format_integer,
    "Download rate (pages downloadable from)": format_percentage,
}
DOWNLOAD_METRICS_RAW = [
    "Page views (pages downloadable from)",
    "Downloads",
]
METRICS_PUBLICATIONS = [
    "Publication title",
    "File name",
    "Link",
    "File type",
    "Content type",
    "Publication type",
    "Published date",
    "Updated date",
    "Team",
    "Author",
    "Topic",
]
METRICS_PAGES = [
    "Page title",
    "Link",
    "Content type",
    "Publication type",
    "Published date",
    "Updated date",
    "Team",
    "Author",
    "Topic",
]
SQL_EARLIEST_DATE = "1900-01-01"
SQL_LATEST_DATE = "9999-12-31"
WEB_TRAFFIC_METRIC_AGGREGATIONS = {
    "Page views": ("Page views", "sum"),
    "Active users": ("Active users", "sum"),
    "User engagement duration": ("User engagement duration", "sum"),
    "Downloads": ("Downloads", "sum"),
}
WEB_TRAFFIC_METRIC_CALCULATIONS = {
    "Page views per active user": (
        "Page views",
        "Active users",
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
WEB_TRAFFIC_METRICS_DISPLAY = {
    "Page views": format_integer,
    "Active users": format_integer,
    "Page views per active user": format_decimal,
    "Average engagement time per active user": format_time,
    "Downloads": format_integer,
    "Download rate": format_percentage,
}
WEB_TRAFFIC_METRICS_RAW = [
    "Page views",
    "Active users",
    "User engagement duration",
    "Downloads",
]
YAXIS_TICKFORMAT = {
    "Page views": ",d",
    "Page views (pages downloadable from)": ",d",
    "Active users": ",d",
    "Page views per active user": ".1f",
    "Average engagement time per active user": "hh:mm:ss",
    "Downloads": ",d",
    "Download rate": ".0%",
    "Download rate (pages downloadable from)": ".0%",
}
