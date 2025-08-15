select top 10
    pt.page_title [Page title],
    pv.url Link,
    sum(pv.page_views) [Page views]
from corporate.page_views_canonical pv
    left join corporate.content_basic_metadata_canonical bm on
        pv.url = bm.url
    left join corporate.content_page_titles_canonical pt on
        bm.url = pt.url
where
    pv.date between ? and ? and
    bm.content_type = ? and
    (
        (
            isnull(bm.published_date, '1900-01-01') >= ? and
            isnull(bm.published_date, '9999-12-31') <= ?
        ) or
        (
            isnull(bm.updated_date, '1900-01-01') >= ? and
            isnull(bm.updated_date, '9999-12-31') <= ?
        )
    )
group by
    pt.page_title,
    pv.url
order by
    sum(pv.page_views) desc;
