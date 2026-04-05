with services as (

    select * from {{ ref('stg_services_weekly') }}

)

select
    week,
    month,
    service,
    available_beds,
    patients_request,
    patients_admitted,
    patients_refused,
    occupancy_rate,
    refusal_rate,
    patient_satisfaction,
    staff_morale,
    event,
    capacity_category
from services
