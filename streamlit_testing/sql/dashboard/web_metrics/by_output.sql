-- NB: By using an outer apply to corporate.content_basic_metadata_latest this picks up
-- details of the page from which an output is most commonly downloaded
select
    d.date Date,
    pt.pageTitle [Output title],
    d.fileName [File name],
    d.fileExtension [File extension],
    bm.content_label [Content type],
    bm.publication_date [Published date],
    bm.update_date [Updated date],
    a.authors Authors,
    t.teams [Teams],
    p.topics Topics,
    d.eventCount Downloads
from corporate.downloads_by_date d
    outer apply (
        select top 1 *
        from corporate.content_basic_metadata_latest bm
        where
            d.pagePath = bm.pagePath
    ) bm
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
    d.date between ? and ?
order by
    d.eventCount;
