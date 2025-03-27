metrics = [
    "activeUsers",
    "engagedSessions",
    "screenPageViews",
    "sessions",
    "userEngagementDuration",
    "eventCount",
]
metric_aggregations = {
    "activeUsers": ("activeUsers", "sum"),
    "engagedSessions": ("engagedSessions", "sum"),
    "screenPageViews": ("screenPageViews", "sum"),
    "sessions": ("sessions", "sum"),
    "userEngagementDuration": ("userEngagementDuration", "sum"),
    "eventCount": ("eventCount", "sum"),
}
default_metric = "screenPageViews"
date_ranges = {
    "Last 7 days": 7,
    "Last 30 days": 30,
    "Last 90 days": 90,
    "Last 12 months": 365,
    "Year to date": None,
    "Custom": None,
}
default_date_range = "Last 30 days"
