web_traffic_metrics = [
    "Page views",
    "Active users",
    "Sessions",
    "Engaged sessions",
    "User engagement duration",
    "Downloads",
]
web_traffic_metric_aggregations = {
    "Page views": ("Page views", "sum"),
    "Active users": ("Active users", "sum"),
    "Sessions": ("Sessions", "sum"),
    "Engaged sessions": ("Engaged sessions", "sum"),
    "User engagement duration": ("User engagement duration", "sum"),
    "Downloads": ("Downloads", "sum"),
}
default_web_traffic_metric = "Page views"
download_metrics = [
    "Downloads",
]
download_metric_aggregations = {
    "Downloads": ("Downloads", "sum"),
}
default_download_metric = "Downloads"
date_ranges = {
    "Last 7 days": 7,
    "Last 30 days": 30,
    "Last 90 days": 90,
    "Last 12 months": 365,
    "Year to date": None,
    "Custom": None,
}
default_date_range = "Last 30 days"
