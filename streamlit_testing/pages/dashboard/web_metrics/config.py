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
    "Downloads": ("Downloads", "sum"),
}
DOWNLOAD_METRIC_CALCULATIONS = None
DOWNLOAD_METRICS_DISPLAY = {
    "Downloads": format_integer,
}
DOWNLOAD_METRICS_RAW = [
    "Downloads",
]
METRICS_BY_OUTPUT = [
    "Output title",
    "File name",
    "File extension",
    "Content type",
    "Published date",
    "Updated date",
    "Teams",
    "Authors",
    "Topics",
]
METRICS_BY_PAGE = [
    "Page title",
    "URL",
    "Content type",
    "Published date",
    "Updated date",
    "Teams",
    "Authors",
    "Topics",
]
SQL_EARLIEST_DATE = "1900-01-01"
SQL_LATEST_DATE = "9999-12-31"
WEB_TRAFFIC_METRIC_AGGREGATIONS = {
    "Page views": ("Page views", "sum"),
    "Active users": ("Active users", "sum"),
    "Sessions": ("Sessions", "sum"),
    "Engaged sessions": ("Engaged sessions", "sum"),
    "User engagement duration": ("User engagement duration", "sum"),
    "Downloads": ("Downloads", "sum"),
}
WEB_TRAFFIC_METRIC_CALCULATIONS = {
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
WEB_TRAFFIC_METRICS_DISPLAY = {
    "Page views": format_integer,
    "Active users": format_integer,
    "Page views per active user": format_decimal,
    "Engagement rate": format_percentage,
    "Average engagement time per active user": format_time,
    "Downloads": format_integer,
    "Download rate": format_percentage,
}
WEB_TRAFFIC_METRICS_RAW = [
    "Page views",
    "Active users",
    "Sessions",
    "Engaged sessions",
    "User engagement duration",
    "Downloads",
]
YAXIS_TICKFORMAT = {
    "Page views": ",d",
    "Active users": ",d",
    "Page views per active user": ".1f",
    "Engagement rate": ".0%",
    "Average engagement time per active user": ",d",
    "Downloads": ",d",
    "Download rate": ".0%",
}
