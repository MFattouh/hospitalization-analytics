with services as (

    select * from {{ ref('stg_services_weekly') }}

)

select
    service,
    sum(patients_admitted) as total_admissions,
    sum(patients_refused) as total_refusals,
    avg(occupancy_rate) as avg_occupancy_rate,
    avg(patient_satisfaction) as avg_satisfaction,
    avg(staff_morale) as avg_staff_morale
from services
group by service
