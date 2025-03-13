-- Web traffic
--- By page
select
    pv.date,
    sum(pv.activeUsers) activeUsers,
    sum(pv.engagedSessions) engagedSessions,
    sum(pv.screenPageViews) screenPageViews,
    sum(pv.sessions) sessions,
    sum(pv.userEngagementDuration) userEngagementDuration
from corporate.ga_page_views_by_date pv
    left join corporate.ifg_content c on
        pv.pagePath = c.[partial]
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
    c.page_title is not null
group by
    pv.date
order by
    pv.date