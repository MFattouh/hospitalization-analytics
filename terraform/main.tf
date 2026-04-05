# GCS Datalake Bucket
resource "google_storage_bucket" "datalake" {
  name          = var.bucket_name
  location      = var.location
  force_destroy = true

  uniform_bucket_level_access = true
}

# BigQuery Datasets
resource "google_bigquery_dataset" "raw" {
  dataset_id    = var.bq_dataset_raw
  location      = var.location
  friendly_name = "Raw data layer"
  description   = "External tables and raw ingested data"
}

resource "google_bigquery_dataset" "staging" {
  dataset_id    = var.bq_dataset_staging
  location      = var.location
  friendly_name = "Staging data layer"
  description   = "Cleaned and typed staging models"
}

resource "google_bigquery_dataset" "marts" {
  dataset_id    = var.bq_dataset_marts
  location      = var.location
  friendly_name = "Marts data layer"
  description   = "Business-ready analytics tables"
}

# IAM: Service Account access to GCS bucket
# Note: The service account email should be passed in or referenced.
# For simplicity, we grant access to the project's default compute SA
# or a specific SA email provided via variable.
# Uncomment and customize based on your SA setup:
#
# resource "google_storage_bucket_iam_member" "sa_gcs_access" {
#   bucket = google_storage_bucket.datalake.name
#   role   = "roles/storage.objectAdmin"
#   member = "serviceAccount:${var.service_account_email}"
# }
#
# resource "google_bigquery_dataset_iam_member" "sa_bq_raw" {
#   dataset_id = google_bigquery_dataset.raw.dataset_id
#   role       = "roles/bigquery.dataEditor"
#   member     = "serviceAccount:${var.service_account_email}"
# }
#
# Repeat for staging and marts datasets...
