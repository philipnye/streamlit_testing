select
    min(pv.date) min_date,
    max(pv.date) max_date
from corporate.page_views_canonical pv
