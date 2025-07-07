-- Content metadata
select
    pt.page_title [Page title],
    bm.url URL,
    bm.content_type [Content type],
    bm.publication_type [Publication type],
    bm.published_date [Published date],
    bm.updated_date [Updated date],
    t.teams Teams,
    a.authors Authors,
    p.topics Topics
from corporate.content_basic_metadata_canonical bm
    left join corporate.content_page_titles_canonical pt on
        bm.url = pt.url
    outer apply (
        select
            string_agg(t.team, ', ') as teams
        from corporate.content_teams_canonical t
        where
            bm.url = t.url
        group by
            t.url
    ) t
    outer apply (
        select
            string_agg(p.topic, ', ') as topics
        from corporate.content_topics_canonical p
        where
            bm.url = p.url
        group by
            p.url
    ) p
    outer apply (
        select
            string_agg(a.author, ', ') as authors
        from corporate.content_authors_canonical a
        where
            bm.url = a.url
        group by
            a.url
    ) a
where
    bm.url = ?;


-- Metrics
select
    pv.date Date,
    pv.page_views [Page views],
    pv.active_users [Active users],
    pv.sessions Sessions,
    pv.user_engagement_duration [User engagement duration],
    d.event_count Downloads
from corporate.page_views_canonical pv
    left join corporate.downloads_canonical d on
        pv.url = d.url and
        pv.date = d.date
where
    pv.url = ? and
    pv.date between ? and ?
order by
    pv.date;
