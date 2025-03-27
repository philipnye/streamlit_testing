select
    pv.date,
    c.page_title,
    pv.pagePath,
    c.type,
    c.published_date,
    c.updated_date_alternative,
    a.authors,
    ra.research_areas,
    t.tags,
    pv.activeUsers,
    pv.engagedSessions,
    pv.screenPageViews,
    pv.sessions,
    pv.userEngagementDuration,
    d.eventCount
from corporate.ifg_content c
    inner join corporate.ga_page_views_by_date pv on
        pv.pagePath = c.partial
    left join corporate.ga_downloads_by_date d on
        c.partial = d.pagePath and
        pv.date = d.date
    outer apply (
        select
            string_agg(ra.research_area, ', ') as research_areas
        from corporate.ifg_research_areas ra
        where
            c.partial = ra.partial
        group by
            ra.partial
    ) ra
    outer apply (
        select
            string_agg(t.tag, ', ') as tags
        from corporate.ifg_tags t
        where
            c.partial = t.partial
        group by
            t.partial
    ) t
    outer apply (
        select
            string_agg(a.author, ', ') as authors
        from corporate.ifg_authors a
        where
            c.partial = a.partial
        group by
            a.partial
    ) a
where
    c.page_title is not null;
