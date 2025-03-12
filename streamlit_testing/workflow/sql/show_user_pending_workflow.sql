-- Show pending workflows for current user
-- Criteria are:
    -- Latest status is 'created' in workflow.task_allocation
    -- Current reviewer has role of 'reviewer' in workflow.task_allocation
select
    t.id,
    t.workflow,
    t.[description],
    ts.[datetime] created
from workflow.task t
outer apply (
    select top 1 *
    from workflow.task_status ts
    where
        t.id = ts.task_id
    order by
        [datetime] desc
) ts
where
    ts.status = 'created' and
    exists (
        select *
        from workflow.task_allocation ta
        where
            t.id = ta.task_id and
            ta.[user] = ?
    )
order by
    ts.[datetime]