select
    pv.date,
    c.page_title,
    c.partial,
    c.type,
    c.published_date,
    c.updated_date_alternative,
    a.author,
    ra.research_area,
    t.tag,
    pv.activeUsers,
    pv.engagedSessions,
    pv.screenPageViews,
    pv.sessions,
    pv.userEngagementDuration
from corporate.ga_page_views_by_date pv
    left join corporate.ifg_content c on
        pv.pagePath = c.partial
    left join corporate.ifg_research_areas ra on
        c.partial = ra.partial
    left join corporate.ifg_tags t on
        c.partial = t.partial
    left join corporate.ifg_authors a on
        c.partial = a.partial
