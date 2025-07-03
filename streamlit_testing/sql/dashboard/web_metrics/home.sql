select top 10
    pt.page_title [Page title],
    pv.url URL,
    sum(pv.page_views) [Page views]
from corporate.page_views_canonical pv
    left join corporate.content_basic_metadata_canonical bm on
        pv.url = bm.url
    left join corporate.content_page_titles_canonical pt on
        bm.url = pt.url
where
    pv.date between ? and ? and
    bm.content_type = ?
group by
    pt.page_title,
    pv.url
order by
    sum(pv.page_views) desc;
