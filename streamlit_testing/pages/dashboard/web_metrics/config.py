web_traffic_metrics = [
    "activeUsers",
    "engagedSessions",
    "screenPageViews",
    "sessions",
    "userEngagementDuration",
    "eventCount",
]
web_traffic_metric_aggregations = {
    "activeUsers": ("activeUsers", "sum"),
    "engagedSessions": ("engagedSessions", "sum"),
    "screenPageViews": ("screenPageViews", "sum"),
    "sessions": ("sessions", "sum"),
    "userEngagementDuration": ("userEngagementDuration", "sum"),
    "eventCount": ("eventCount", "sum"),
}
default_web_traffic_metric = "screenPageViews"
download_metrics = [
    "eventCount",
]
download_metric_aggregations = {
    "eventCount": ("eventCount", "sum"),
}
default_download_metric = "eventCount"
date_ranges = {
    "Last 7 days": 7,
    "Last 30 days": 30,
    "Last 90 days": 90,
    "Last 12 months": 365,
    "Year to date": None,
    "Custom": None,
}
default_date_range = "Last 30 days"
