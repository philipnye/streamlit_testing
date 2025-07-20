-- Content metadata
select distinct
    pt.page_title [Publication title],
    da.file_name_clean [File name],
    da.file_path_latest Link,
    da.file_extension [File type],
    bm.content_type [Content type],
    bm.publication_type [Publication type],
    bm.published_date [Published date],
    bm.updated_date [Updated date],
    t.team Team,
    a.author Author,
    p.topic Topic
from
(
    select distinct
        da.url_most_common,
        da.file_path_latest,
        da.file_name_clean,
        da.file_extension
    from corporate.downloads_aggregated da
) da
    left join corporate.content_basic_metadata_canonical bm on
        da.url_most_common = bm.url
    left join corporate.content_page_titles_canonical pt on
        da.url_most_common = pt.url
    outer apply (
        select
            string_agg(t.team, ', ') team
        from corporate.content_teams_canonical t
        where
            da.url_most_common = t.url
        group by
            t.url
    ) t
    outer apply (
        select
            string_agg(p.topic, ', ') topic
        from corporate.content_topics_canonical p
        where
            da.url_most_common = p.url
        group by
            p.url
    ) p
    outer apply (
        select
            string_agg(a.author, ', ') author
        from corporate.content_authors_canonical a
        where
            da.url_most_common = a.url
        group by
            a.url
    ) a
where
    pt.page_title is not null and
    da.file_path_latest = ?;


-- Metrics
select
    pv.date Date,
    sum(pv.page_views) [Page views (pages downloadable from)],
    sum(dc2.event_count) Downloads
from
(
    select distinct
        da.url_most_common,
        da.file_path_latest,
        da.file_name_clean,
        da.file_extension
    from corporate.downloads_aggregated da
) da
    outer apply (
        select distinct
            dc1.url
        from corporate.downloads_canonical dc1
        where
            dc1.date between ? and ? and
            da.file_path_latest = dc1.file_path_latest
    ) dc1
    left join corporate.page_views_canonical pv on
        dc1.url = pv.url
    left join corporate.downloads_canonical dc2 on
        pv.url = dc2.url and
        pv.date = dc2.date and
        da.file_path_latest = dc2.file_path_latest
where
    da.file_path_latest = ? and
    pv.date between ? and ?
group by
    pv.date;


-- Pages downloadable from
select
    pt.page_title [Page title],
    dc1.url [Link],
    bm.content_type [Content type],
    sum(pv.page_views) [Page views],
    sum(dc2.event_count) [Downloads]
from
(
    select distinct
        da.url_most_common,
        da.file_path_latest,
        da.file_name_clean,
        da.file_extension
    from corporate.downloads_aggregated da
) da
    outer apply (
        select distinct
            dc1.url
        from corporate.downloads_canonical dc1
        where
            dc1.date between ? and ? and
            da.file_path_latest = dc1.file_path_latest
    ) dc1
    left join corporate.page_views_canonical pv on
        dc1.url = pv.url and
        pv.date between ? and ?
    left join corporate.downloads_canonical dc2 on
        pv.url = dc2.url and
        pv.date = dc2.date and
        da.file_path_latest = dc2.file_path_latest
    left join corporate.content_basic_metadata_canonical bm on
        dc1.url = bm.url
    left join corporate.content_page_titles_canonical pt on
        dc1.url = pt.url
where
    da.file_path_latest = ?
group by
    pt.page_title,
    dc1.url,
    bm.content_type,
    bm.publication_type,
    bm.published_date,
    bm.updated_date;
