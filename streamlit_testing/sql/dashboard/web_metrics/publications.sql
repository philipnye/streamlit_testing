select
    d.date Date,
    pt.page_title [Output title],
    d.file_name_clean [File name],
    d.file_path_latest Link,
    d.file_extension [File type],
    bm.content_type [Content type],
    bm.publication_type [Publication type],
    bm.published_date [Published date],
    bm.updated_date [Updated date],
    t.team Team,
    a.author Author,
    p.topic Topic,
    d.event_count Downloads
from corporate.downloads_aggregated d
    left join corporate.content_basic_metadata_canonical bm on
        d.url_most_common = bm.url
    left join corporate.content_page_titles_canonical pt on
        d.url_most_common = pt.url
    outer apply (
        select
            string_agg(t.team, ', ') team
        from corporate.content_teams_canonical t
        where
            d.url_most_common = t.url
        group by
            t.url
    ) t
    outer apply (
        select
            string_agg(p.topic, ', ') topic
        from corporate.content_topics_canonical p
        where
            d.url_most_common = p.url
        group by
            p.url
    ) p
    outer apply (
        select
            string_agg(a.author, ', ') author
        from corporate.content_authors_canonical a
        where
            d.url_most_common = a.url
        group by
            a.url
    ) a
where
    pt.page_title is not null and
    d.date between ? and ?;
