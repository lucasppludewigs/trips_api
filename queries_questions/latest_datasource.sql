with main_result as (
    SELECT region, datasource, datetime
    FROM trips
    WHERE region IN (
        SELECT region
        FROM trips
        GROUP BY region
        ORDER BY COUNT(*) DESC
        LIMIT 2
    )
),
max_timestamps as (
    select region, max(datetime) as mdatetime from trips group by 1
)
select mr.region, mr.datasource
from main_result mr
inner join max_timestamps mt on mr.region = mt.region and mr.datetime = mt.mdatetime;