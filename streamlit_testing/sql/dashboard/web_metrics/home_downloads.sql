-- NB: By using an outer apply to corporate.content_basic_metadata_canonical this picks up
-- details of the page from which an output is most commonly downloaded
select top 10
    pt.page_title [Output title],
    d.file_name [Link],
    sum(d.event_count) Downloads
from corporate.downloads_canonical d
    outer apply (
        select top 1 *
        from corporate.content_basic_metadata_canonical bm
        where
            d.url = bm.url
    ) bm
    left join corporate.content_page_titles_canonical pt on
        bm.url = pt.url
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
    d.file_name
order by
    sum(d.event_count) desc;
