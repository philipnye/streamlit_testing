metrics = [
    "activeUsers",
    "engagedSessions",
    "screenPageViews",
    "sessions",
    "userEngagementDuration",
]
metric_aggregations = {
    "activeUsers": ("activeUsers", "sum"),
    "engagedSessions": ("engagedSessions", "sum"),
    "screenPageViews": ("screenPageViews", "sum"),
    "sessions": ("sessions", "sum"),
    "userEngagementDuration": ("userEngagementDuration", "sum"),
}
default_metric = "screenPageViews"
