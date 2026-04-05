"""DAG 1: Download CSVs from Kaggle and upload to GCS datalake."""

import os
from pathlib import Path
from tempfile import TemporaryDirectory

import kagglehub
from google.cloud import storage
from prefect import flow, task

KAGGLE_DATASET = "jaderz/hospital-beds-management"

GCS_BUCKET = os.getenv("GCS_BUCKET", "hospital-datalake")
GCS_PREFIX = "raw"


@task(retries=2, retry_delay_seconds=10)
def download_from_kaggle(dataset_handle: str, output_dir: Path) -> Path:
    """Download a Kaggle dataset to a local directory."""
    download_path = kagglehub.dataset_download(
        dataset_handle,
        output_dir=str(output_dir),
        force_download=True,
    )
    return Path(download_path)


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
    """Download hospital data CSVs from Kaggle and upload to GCS datalake."""
    with TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        print(f"Downloading dataset '{KAGGLE_DATASET}' from Kaggle...")
        download_path = download_from_kaggle(KAGGLE_DATASET, tmpdir)

        patients_path = Path(download_path) / "patients.csv"
        services_path = Path(download_path) / "services_weekly.csv"

        if not patients_path.exists():
            raise FileNotFoundError(f"patients.csv not found in {download_path}")
        if not services_path.exists():
            raise FileNotFoundError(f"services_weekly.csv not found in {download_path}")

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
