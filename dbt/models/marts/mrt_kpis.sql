with services as (

    select * from {{ ref('stg_services_weekly') }}

),

weekly_kpis as (

    select
        'week' as period_type,
        cast(week as int64) as period_value,
        service,
        sum(available_beds) as total_available_beds,
        sum(patients_admitted) as total_admissions,
        sum(patients_refused) as total_refusals,
        avg(occupancy_rate) as avg_occupancy_rate,
        avg(refusal_rate) as avg_refusal_rate,
        avg(patient_satisfaction) as avg_patient_satisfaction,
        avg(staff_morale) as avg_staff_morale
    from services
    group by period_type, period_value, service

),

monthly_kpis as (

    select
        'month' as period_type,
        month as period_value,
        service,
        sum(available_beds) as total_available_beds,
        sum(patients_admitted) as total_admissions,
        sum(patients_refused) as total_refusals,
        avg(occupancy_rate) as avg_occupancy_rate,
        avg(refusal_rate) as avg_refusal_rate,
        avg(patient_satisfaction) as avg_patient_satisfaction,
        avg(staff_morale) as avg_staff_morale
    from services
    group by period_type, period_value, service

)

select * from weekly_kpis
union all
select * from monthly_kpis
