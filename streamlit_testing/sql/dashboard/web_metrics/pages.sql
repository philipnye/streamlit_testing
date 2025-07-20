-- NB: Uses an aggregation on dc as there can be multiple files downloadable from a single URL. Using a left join without an aggregation results in page views being duplicated
select
    pv.date Date,
    pt.page_title [Page title],
    pv.url Link,
    bm.content_type [Content type],
    bm.publication_type [Publication type],
    bm.published_date [Published date],
    bm.updated_date [Updated date],
    t.team Team,
    a.author Author,
    p.topic Topic,
    pv.page_views [Page views],
    pv.active_users [Active users],
    pv.user_engagement_duration [User engagement duration],
    dc.event_count Downloads
from corporate.page_views_canonical pv
    left join corporate.content_basic_metadata_canonical bm on
        bm.url = pv.url
    left join corporate.content_page_titles_canonical pt on
        bm.url = pt.url
    outer apply (
        select
            string_agg(t.team, ', ') team
        from corporate.content_teams_canonical t
        where
            bm.url = t.url
        group by
            t.url
    ) t
    outer apply (
        select
            string_agg(p.topic, ', ') topic
        from corporate.content_topics_canonical p
        where
            bm.url = p.url
        group by
            p.url
    ) p
    outer apply (
        select
            string_agg(a.author, ', ') author
        from corporate.content_authors_canonical a
        where
            bm.url = a.url
        group by
            a.url
    ) a
    outer apply (
        select
            dc.date,
            sum(dc.event_count) event_count
        from corporate.downloads_canonical dc
        where
            pv.url = dc.url and
            pv.date = dc.date
        group by
            dc.date
    ) dc
where
    pt.page_title is not null and
    pv.date between ? and ?;
