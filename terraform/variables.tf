variable "gcp_project_id" {
  description = "GCP project ID"
  type        = string
}

variable "credentials_file" {
  description = "Path to GCP service account JSON key file"
  type        = string
}

variable "location" {
  description = "GCP region for resources"
  type        = string
  default     = "US"
}

variable "bucket_name" {
  description = "GCS datalake bucket name"
  type        = string
}

variable "bq_dataset_raw" {
  description = "BigQuery raw dataset name"
  type        = string
  default     = "hospital_raw"
}

variable "bq_dataset_staging" {
  description = "BigQuery staging dataset name"
  type        = string
  default     = "hospital_staging"
}

variable "bq_dataset_marts" {
  description = "BigQuery marts dataset name"
  type        = string
  default     = "hospital_marts"
}
