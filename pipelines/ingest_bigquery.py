"""DAG 2: Create external tables in BigQuery and CTAS into raw layer."""

import os

from google.cloud import bigquery
from prefect import flow, task

GCS_BUCKET = os.getenv("GCS_BUCKET", "hospital-datalake")
BQ_DATASET_RAW = os.getenv("BQ_DATASET_RAW", "raw")


@task
def create_external_table(
    table_name: str,
    gcs_uri: str,
    dataset_id: str,
    schema: list[bigquery.SchemaField],
) -> str:
    """Create an external table in BigQuery pointing to a GCS CSV."""
    client = bigquery.Client()
    full_table_id = f"{client.project}.{dataset_id}.{table_name}"

    external_config = bigquery.ExternalConfig("CSV")
    external_config.source_uris = [gcs_uri]
    external_config.skip_leading_rows = 1
    external_config.autodetect = True

    table = bigquery.Table(full_table_id, schema=schema)
    table.external_data_configuration = external_config
    table = client.create_table(table, exists_ok=True)

    print(f"External table created: {table.full_table_id}")
    # full_table_id uses colon (project:dataset.table), but SQL needs dots
    return table.full_table_id.replace(":", ".")


@task
def ctas_raw_table(
    source_table: str,
    dest_table_name: str,
    dataset_id: str,
) -> str:
    """Create a permanent table from an external table using CTAS."""
    client = bigquery.Client()
    dest_table_id = f"{client.project}.{dataset_id}.{dest_table_name}"

    query = f"""
    CREATE OR REPLACE TABLE `{dest_table_id}` AS
    SELECT * FROM `{source_table}`
    """

    job = client.query(query)
    job.result()

    print(f"CTAS complete: {dest_table_id}")
    return dest_table_id


@flow(name="ingest-bigquery", log_prints=True)
def ingest_bigquery(
    gcs_bucket: str = GCS_BUCKET,
    bq_dataset_raw: str = BQ_DATASET_RAW,
) -> dict[str, str]:
    """Create external tables and CTAS into raw BigQuery layer."""
    project = bigquery.Client().project

    # Define schemas
    patients_schema = [
        bigquery.SchemaField("patient_id", "STRING"),
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("age", "INTEGER"),
        bigquery.SchemaField("arrival_date", "DATE"),
        bigquery.SchemaField("departure_date", "DATE"),
        bigquery.SchemaField("service", "STRING"),
        bigquery.SchemaField("satisfaction", "FLOAT"),
    ]

    services_schema = [
        bigquery.SchemaField("week", "INTEGER"),
        bigquery.SchemaField("month", "INTEGER"),
        bigquery.SchemaField("service", "STRING"),
        bigquery.SchemaField("available_beds", "INTEGER"),
        bigquery.SchemaField("patients_request", "INTEGER"),
        bigquery.SchemaField("patients_admitted", "INTEGER"),
        bigquery.SchemaField("patients_refused", "INTEGER"),
        bigquery.SchemaField("patient_satisfaction", "FLOAT"),
        bigquery.SchemaField("staff_morale", "FLOAT"),
        bigquery.SchemaField("event", "STRING"),
    ]

    # External table names
    ext_patients = "external_patients"
    ext_services = "external_services_weekly"

    # GCS URIs
    patients_uri = f"gs://{gcs_bucket}/raw/patients.csv"
    services_uri = f"gs://{gcs_bucket}/raw/services_weekly.csv"

    # Create external tables
    ext_patients_id = create_external_table(
        ext_patients, patients_uri, bq_dataset_raw, patients_schema
    )
    ext_services_id = create_external_table(
        ext_services, services_uri, bq_dataset_raw, services_schema
    )

    # CTAS into raw layer
    raw_patients = ctas_raw_table(ext_patients_id, "patients", bq_dataset_raw)
    raw_services = ctas_raw_table(ext_services_id, "services_weekly", bq_dataset_raw)

    return {
        "raw_patients": raw_patients,
        "raw_services_weekly": raw_services,
    }


if __name__ == "__main__":
    ingest_bigquery()
