select
    pv.date Date,
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
    year(c.published_date) as [Published date: year],
    month(c.published_date) as [Published date: month],
    day(c.published_date) as [Published date: day],
    c.updated_date_alternative [Updated date],
    year(c.updated_date_alternative) as [Updated date: year],
    month(c.updated_date_alternative) as [Updated date: month],
    day(c.updated_date_alternative) as [Updated date: day],
    a.author Author,
    ra.research_area [Research area],
    t.tag Tag,
    pv.screenPageViews [Page views],
    pv.activeUsers [Active users],
    pv.sessions Sessions,
    pv.engagedSessions [Engaged sessions],
    pv.userEngagementDuration [User engagement duration],
    d.eventCount Downloads
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
where
    pv.date between ? and ?;
