with source as (

    select * from {{ source('raw', 'patients') }}

),

renamed as (

    select
        patient_id,
        name,
        age,
        arrival_date,
        departure_date,
        service,
        satisfaction,
        date_diff(departure_date, arrival_date, day) as length_of_stay,
        extract(month from arrival_date) as arrival_month,
        extract(quarter from arrival_date) as arrival_quarter,
        case
            when satisfaction <= 50 then 'Low'
            when satisfaction <= 75 then 'Medium'
            else 'High'
        end as satisfaction_category
    from source

)

select * from renamed
