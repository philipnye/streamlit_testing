select top 10
    pt.page_title [Page title],
    pv.url URL,
    sum(d.event_count) [Downloads]
from corporate.page_views_canonical pv
    left join corporate.content_basic_metadata_canonical bm on
        pv.url = bm.url
    left join corporate.content_page_titles_canonical pt on
        bm.url = pt.url
    left join corporate.downloads_canonical d on
        pv.url = d.url and
        pv.date = d.date
where
    pv.date between ? and ? and
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
    pv.url
order by
    sum(d.event_count) desc;
