select
    pv.date,
    c.page_title,
    c.partial,
    c.type,
    c.published_date,
    year(c.published_date) as published_year,
    month(c.published_date) as published_month,
    day(c.published_date) as published_day,
    c.updated_date_alternative,
    year(c.updated_date_alternative) as updated_year,
    month(c.updated_date_alternative) as updated_month,
    day(c.updated_date_alternative) as updated_day,
    a.author,
    ra.research_area,
    t.tag,
    pv.activeUsers,
    pv.engagedSessions,
    pv.screenPageViews,
    pv.sessions,
    pv.userEngagementDuration,
    d.eventCount
from corporate.ifg_content c
    inner join corporate.ga_page_views_by_date pv on
        c.partial = pv.pagePath
    left join corporate.ga_downloads_by_date d on
        c.partial = d.pagePath and
        pv.date = d.date
    left join corporate.ifg_research_areas ra on
        c.partial = ra.partial
    left join corporate.ifg_tags t on
        c.partial = t.partial
    left join corporate.ifg_authors a on
        c.partial = a.partial
