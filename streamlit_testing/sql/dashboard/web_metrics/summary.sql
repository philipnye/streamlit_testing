select
    pv.date Date,
    pt.pageTitle [Page title],
    bm.pagePath URL,
    case
        when bm.content_label in (
            'Analysis paper',
            'Case study',
            'Insight paper',
            'Report'
        ) then 'Publication'
        when bm.content_label in (
            'Interview'
        ) then 'Special output'
        else bm.content_label
    end [Content type],
    case
        when bm.content_label in (
            'Analysis paper',
            'Case study',
            'Insight paper',
            'Report'
        ) then bm.content_label
        else null
    end [Publication type],
    bm.publication_date [Published date],
    year(bm.publication_date) as [Published date: year],
    month(bm.publication_date) as [Published date: month],
    day(bm.publication_date) as [Published date: day],
    bm.update_date [Updated date],
    year(bm.update_date) as [Updated date: year],
    month(bm.update_date) as [Updated date: month],
    day(bm.update_date) as [Updated date: day],
    a.author Author,
    t.team [Team],
    p.topic Topic,
    pv.screenPageViews [Page views],
    pv.activeUsers [Active users],
    pv.sessions Sessions,
    pv.engagedSessions [Engaged sessions],
    pv.userEngagementDuration [User engagement duration],
    d.eventCount Downloads
from corporate.page_views_by_date pv
    left join corporate.downloads_by_date d on
        pv.pagePath = d.pagePath and
        pv.date = d.date
    left join corporate.content_basic_metadata_latest bm on
        pv.pagePath = bm.pagePath
    left join corporate.content_page_titles_latest pt on
        bm.pagePath = pt.pagePath
    left join corporate.content_teams_latest t on
        bm.pagePath = t.pagePath
    left join corporate.content_topics_latest p on
        bm.pagePath = p.pagePath
    left join corporate.content_authors_latest a on
        bm.pagePath = a.pagePath
where
    pv.date between ? and ?;
