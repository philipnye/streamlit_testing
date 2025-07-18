-- Builds a base table of unique files for which content metadata is pulled, before identifying all URLs associated with that file, and finally retrieving all page views and downloads for those URLs
-- This is done so that page metadata can be attached via most common URL without dropping anything
-- NB: It matters that the date condition is on pv, not dc2, otherwise we lose page views on days where there are no downloads
select
    pt.page_title [Publication title],
    da.file_name_clean [File name],
    da.file_path_latest [Link],
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
    left join corporate.content_basic_metadata_canonical bm on
        da.url_most_common = bm.url
    left join corporate.content_page_titles_canonical pt on
        da.url_most_common = pt.url
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
    pt.page_title is not null and
    pv.date between ? and ? and
    bm.content_type = ? and
    da.file_name_clean not like '%briefing%' and
    (
        (
            bm.published_date >= ? and
            bm.published_date <= ?
        ) or
        (
            bm.updated_date >= ? and
            bm.updated_date <= ?
        )
    )
group by
    pt.page_title,
    da.file_name_clean,
    da.url_most_common,
    da.file_path_latest
order by
    sum(dc2.event_count) desc;
