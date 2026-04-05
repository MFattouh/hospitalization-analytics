with patients as (

    select * from {{ ref('stg_patients') }}

),

service_monthly_occupancy as (

    select
        service,
        month,
        avg(occupancy_rate) as service_avg_occupancy_month
    from {{ ref('stg_services_weekly') }}
    group by service, month

)

select
    p.patient_id,
    p.service,
    p.arrival_month,
    p.satisfaction,
    p.satisfaction_category,
    p.length_of_stay,
    coalesce(smo.service_avg_occupancy_month, 0) as service_avg_occupancy_month
from patients p
left join service_monthly_occupancy smo
    on p.service = smo.service
    and p.arrival_month = smo.month
