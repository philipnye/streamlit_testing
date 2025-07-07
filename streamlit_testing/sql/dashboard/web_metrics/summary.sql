select
    pv.date Date,
    pt.page_title [Page title],
    pv.url URL,
    bm.content_type [Content type],
    bm.publication_type [Publication type],
    bm.published_date [Published date],
    year(bm.published_date) [Published date: year],
    month(bm.published_date) [Published date: month],
    day(bm.published_date) [Published date: day],
    bm.updated_date [Updated date],
    year(bm.updated_date) [Updated date: year],
    month(bm.updated_date) [Updated date: month],
    day(bm.updated_date) [Updated date: day],
    t.team Team,
    a.author Author,
    p.topic Topic,
    pv.page_views [Page views],
    pv.active_users [Active users],
    pv.sessions Sessions,
    pv.user_engagement_duration [User engagement duration],
    d.event_count Downloads
from corporate.page_views_canonical pv
    left join corporate.downloads_canonical d on
        pv.url = d.url and
        pv.date = d.date
    left join corporate.content_basic_metadata_canonical bm on
        pv.url = bm.url
    left join corporate.content_page_titles_canonical pt on
        bm.url = pt.url
    left join corporate.content_teams_canonical t on
        bm.url = t.url
    left join corporate.content_topics_canonical p on
        bm.url = p.url
    left join corporate.content_authors_canonical a on
        bm.url = a.url
where
    pv.date between ? and ?;
