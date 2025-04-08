select
    min(pv.date) min_date,
    max(pv.date) max_date
from corporate.ga_page_views_by_date pv
