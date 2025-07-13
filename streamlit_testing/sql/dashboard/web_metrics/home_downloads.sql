select top 10
    pt.page_title [Output title],
    d.file_name_clean [File name],
    d.file_path_dedupe [Link],
    sum(d.event_count) Downloads
from corporate.downloads_canonical d
    left join corporate.content_basic_metadata_canonical bm on
        d.url = bm.url
    left join corporate.content_page_titles_canonical pt on
        d.url = pt.url
where
    pt.page_title is not null and
    d.date between ? and ? and
    bm.content_type = ? and
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
    d.file_name_clean,
    d.file_path_dedupe
order by
    sum(d.event_count) desc;
