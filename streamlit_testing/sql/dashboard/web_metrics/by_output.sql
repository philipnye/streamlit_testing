-- NB: By using an outer apply to corporate.ifg_content this picks up
-- the page title of the page from which an output is most commonly downloaded
select
    d.date Date,
    c.page_title [Output title],
    d.fileName [File name],
    d.fileExtension [File extension],
    c.type [Content type],
    c.published_date [Published date],
    c.updated_date_alternative [Updated date],
    a.authors Authors,
    ra.research_areas [Research areas],
    t.tags Tags,
    d.eventCount Downloads
from corporate.ga_downloads_by_date d
    outer apply (
        select top 1 *
        from corporate.ifg_content c
        where
            d.pagePath = c.partial
    ) c
    outer apply (
        select
            string_agg(ra.research_area, ', ') as research_areas
        from corporate.ifg_research_areas ra
        where
            c.partial = ra.partial
        group by
            ra.partial
    ) ra
    outer apply (
        select
            string_agg(t.tag, ', ') as tags
        from corporate.ifg_tags t
        where
            c.partial = t.partial
        group by
            t.partial
    ) t
    outer apply (
        select
            string_agg(a.author, ', ') as authors
        from corporate.ifg_authors a
        where
            c.partial = a.partial
        group by
            a.partial
    ) a
where
    c.page_title is not null
order by
    d.eventCount;
