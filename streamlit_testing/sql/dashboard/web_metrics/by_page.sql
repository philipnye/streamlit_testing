select
    pv.date Date,
    pt.pageTitle [Page title],
    pv.pagePath URL,
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
    bm.update_date [Updated date],
    a.authors Authors,
    t.teams [Teams],
    p.topics Topics,
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
        bm.pagePath = pv.pagePath
    left join corporate.content_page_titles_latest pt on
        bm.pagePath = pt.pagePath
    outer apply (
        select
            string_agg(t.team, ', ') as teams
        from corporate.content_teams_latest t
        where
            bm.pagePath = t.pagePath
        group by
            t.pagePath
    ) t
    outer apply (
        select
            string_agg(p.topic, ', ') as topics
        from corporate.content_topics_latest p
        where
            bm.pagePath = p.pagePath
        group by
            p.pagePath
    ) p
    outer apply (
        select
            string_agg(a.author, ', ') as authors
        from corporate.content_authors_latest a
        where
            bm.pagePath = a.pagePath
        group by
            a.pagePath
    ) a
where
    pt.pageTitle is not null and
    pv.date between ? and ?;
