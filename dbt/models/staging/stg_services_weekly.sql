with source as (

    select * from {{ source('raw', 'services_weekly') }}

),

renamed as (

    select
        week,
        month,
        service,
        available_beds,
        patients_request,
        patients_admitted,
        patients_refused,
        patient_satisfaction,
        staff_morale,
        event,
        safe_divide(patients_admitted, available_beds) as occupancy_rate,
        safe_divide(patients_refused, patients_request) as refusal_rate,
        case
            when safe_divide(patients_admitted, available_beds) < 0.60 then 'Underutilized'
            when safe_divide(patients_admitted, available_beds) <= 0.85 then 'Optimal'
            else 'Overloaded'
        end as capacity_category
    from source

)

select * from renamed
