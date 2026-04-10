"""Master DAG: Chains ingest_gcs → ingest_bigquery → dbt_transform."""

import os

from prefect import flow

from pipelines.ingest_gcs import ingest_gcs
from pipelines.ingest_bigquery import ingest_bigquery
from pipelines.dbt_transform import dbt_transform

GCS_BUCKET = os.getenv("GCS_BUCKET", "hospital-datalake")
BQ_DATASET_RAW = os.getenv("BQ_DATASET_RAW", "hospital_raw")
DBT_PROJECT_DIR = os.getenv("DBT_PROJECT_DIR", "dbt")


@flow(name="hospital-data-pipeline", log_prints=True)
def hospital_data_pipeline(
    gcs_bucket: str = GCS_BUCKET,
    bq_dataset_raw: str = BQ_DATASET_RAW,
    dbt_project_dir: str = DBT_PROJECT_DIR,
) -> dict:
    """Run the full hospital data pipeline end-to-end."""
    print("=== Starting Hospital Data Pipeline ===")

    # Stage 1: Ingest CSVs to GCS
    print("\n--- Stage 1: Ingest to GCS ---")
    gcs_results = ingest_gcs(gcs_bucket=gcs_bucket)
    print(f"GCS ingestion complete: {gcs_results}")

    # Stage 2: Load GCS → BigQuery raw layer
    print("\n--- Stage 2: Ingest to BigQuery ---")
    bq_results = ingest_bigquery(
        gcs_bucket=gcs_bucket,
        bq_dataset_raw=bq_dataset_raw,
    )
    print(f"BigQuery ingestion complete: {bq_results}")

    # Stage 3: dbt transformations
    print("\n--- Stage 3: dbt Transformations ---")
    dbt_results = dbt_transform(project_dir=dbt_project_dir)
    print(f"dbt transformations complete: {dbt_results}")

    print("\n=== Hospital Data Pipeline Complete ===")

    return {
        "gcs": gcs_results,
        "bigquery": bq_results,
        "dbt": dbt_results,
    }


if __name__ == "__main__":
    hospital_data_pipeline()
