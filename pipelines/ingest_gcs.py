"""DAG 1: Download CSVs from source URLs and upload to GCS datalake."""

import os
from pathlib import Path
from tempfile import TemporaryDirectory

import requests
from google.cloud import storage
from prefect import flow, task

PATIENTS_URL = "https://storage.googleapis.com/kagglesdsdata/datasets/8395374/13249373/patients.csv"
SERVICES_URL = "https://storage.googleapis.com/kagglesdsdata/datasets/8395374/13249373/services_weekly.csv"

GCS_BUCKET = os.getenv("GCS_BUCKET", "hospital-datalake")
GCS_PREFIX = "raw"


@task(retries=2, retry_delay_seconds=10)
def download_csv(url: str, dest_path: Path) -> Path:
    """Download a CSV file from a URL to a local path."""
    response = requests.get(url, timeout=120)
    response.raise_for_status()
    dest_path.write_bytes(response.content)
    return dest_path


@task
def upload_to_gcs(file_path: Path, bucket_name: str, blob_name: str) -> str:
    """Upload a file to a GCS bucket."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(str(file_path))
    return f"gs://{bucket_name}/{blob_name}"


@flow(name="ingest-gcs", log_prints=True)
def ingest_gcs(
    gcs_bucket: str = GCS_BUCKET,
) -> dict[str, str]:
    """Download hospital data CSVs and upload to GCS datalake."""
    with TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        patients_path = tmpdir / "patients.csv"
        services_path = tmpdir / "services_weekly.csv"

        print("Downloading patients.csv...")
        download_csv(PATIENTS_URL, patients_path)

        print("Downloading services_weekly.csv...")
        download_csv(SERVICES_URL, services_path)

        print(f"Uploading to gs://{gcs_bucket}/{GCS_PREFIX}/...")
        patients_uri = upload_to_gcs(
            patients_path, gcs_bucket, f"{GCS_PREFIX}/patients.csv"
        )
        services_uri = upload_to_gcs(
            services_path, gcs_bucket, f"{GCS_PREFIX}/services_weekly.csv"
        )

        print(f"patients.csv → {patients_uri}")
        print(f"services_weekly.csv → {services_uri}")

        return {
            "patients": patients_uri,
            "services_weekly": services_uri,
        }


if __name__ == "__main__":
    ingest_gcs()
