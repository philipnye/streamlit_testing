-- Content metadata
select
    c.page_title [Page title],
    c.partial URL,
    case
        when c.type in (
            'Analysis paper',
            'Case study',
            'Insight paper',
            'Report'
        ) then 'Publication'
        when c.type in (
            'Interview'
        ) then 'Special output'
        else c.type
    end [Content type],
    case
        when c.type in (
            'Analysis paper',
            'Case study',
            'Insight paper',
            'Report'
        ) then c.type
        else null
    end [Publication type],
    c.published_date [Published date],
    c.updated_date_alternative [Updated date],
    a.authors Authors,
    ra.research_areas [Research areas],
    t.tags Tags
from corporate.ifg_content c
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
    c.partial = '';


-- Web traffic
select
    pv.date Date,
    pv.screenPageViews [Page views],
    pv.activeUsers [Active users],
    pv.sessions Sessions,
    pv.engagedSessions [Engaged sessions],
    d.eventCount Downloads,
    pv.userEngagementDuration [User engagement duration]
from corporate.ga_page_views_by_date pv
    left join corporate.ga_downloads_by_date d on
        pv.pagePath = d.pagePath and
        pv.date = d.date
where
    pv.pagePath = ''
order by
    pv.date;
