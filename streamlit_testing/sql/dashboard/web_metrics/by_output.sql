-- NB: By using an outer apply to corporate.content_basic_metadata_canonical this picks up
-- details of the page from which an output is most commonly downloaded
select
    d.date Date,
    pt.page_title [Output title],
    d.file_name_clean [File name],
    d.file_path_dedupe Link,
    d.file_extension [File type],
    bm.content_type [Content type],
    bm.publication_type [Publication type],
    bm.published_date [Published date],
    bm.updated_date [Updated date],
    t.team Team,
    a.author Author,
    p.topic Topic,
    d.event_count Downloads
from corporate.downloads_canonical d
    outer apply (
        select top 1 *
        from corporate.content_basic_metadata_canonical bm
        where
            d.url = bm.url
    ) bm
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
where
    pt.page_title is not null and
    d.date between ? and ?;
