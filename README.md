# Hospital Bed Operations Dashboard - Complete

## What Was Built

An end-to-end data engineering pipeline and executive dashboard for hospital bed occupancy KPIs, built on GCP with the following components:

### Infrastructure (Terraform)

- GCS bucket for datalake storage
- Three BigQuery datasets:
  - `hospital_ingest` (external tables + CTAS raw data)
  - `hospital_staging` (dbt staging views)
  - `hospital_marts` (dbt marts tables)
- IAM configuration for service account access

### Data Pipeline (Prefect)

Three modular DAGs:

1. **ingest_gcs.py** — Downloads hospital dataset from Kaggle → uploads to GCS
2. **ingest_bigquery.py** — Creates external tables → CTAS into ingest layer
3. **dbt_transform.py** — Runs dbt deps/run/test for transformations
4. **master_pipeline.py** — Orchestrates all three stages

### Data Transformation (dbt)

- **Staging Layer**: Cleaned patients & services data with derived fields
  - `stg_patients`: Adds length_of_stay, arrival_month/quarter, satisfaction_category
  - `stg_services_weekly`: Adds occupancy_rate, refusal_rate, capacity_category
- **Marts Layer**: Business-ready analytics tables
  - `fct_bed_occupancy`: Weekly service-level occupancy metrics
  - `fct_patient_satisfaction`: Patient-level satisfaction with service correlation
  - `dim_services`: Service dimension with aggregate statistics
  - `mrt_kpis`: Executive KPI summary at weekly/monthly grain

### Executive Dashboard (Looker Studio)

Connect to `hospital_marts` dataset to build:

**4 KPI Scorecards:**

- Avg Occupancy Rate (%)
- Total Admissions (count)
- Total Refusals (count)
- Avg Patient Satisfaction (0-100)

**4 Charts:**

1. Weekly Occupancy Rate by Service (line chart)
2. Bed Demand vs Capacity by Service (grouped bar chart)
3. Satisfaction vs Occupancy Correlation (scatter plot with trend line)
4. Refusal Rate & Staff Morale Impact (dual-axis chart)

**3 Filters:**

- Service (dropdown)
- Month (dropdown)
- Event Type (dropdown)

## How to Use

### 1. Set Up Environment

```bash
# Set environment variables
export GCS_BUCKET="your-hospital-datalake-bucket-name"
export BQ_DATASET_INGEST="hospital_ingest" 
export DBT_PROJECT_DIR="dbt"
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account.json"
export GCP_PROJECT_ID="your-gcp-project-id"

# Set Kaggle credentials for dataset download
# Option A: Place kaggle.json in ~/.config/kaggle/kaggle.json (chmod 600)
# Option B: Export env vars
export KAGGLE_USERNAME="your-kaggle-username"
export KAGGLE_KEY="your-kaggle-api-key"
```

### 2. Deploy Infrastructure

```bash
cd terraform
terraform init
terraform apply  # Review and confirm
```

### 3. Run the Data Pipeline

```bash
# Full pipeline (ingest → BigQuery → dbt)
python -m pipelines.master_pipeline

# Or run stages individually:
python -m pipelines.ingest_gcs     # CSVs → GCS
python -m pipelines.ingest_bigquery  # GCS → BigQuery ingest layer
python -m pipelines.dbt_transform    # dbt transformations
```

### 4. Validate the Data

```bash
python validate_pipeline.py
# Checks all datasets, tables, row counts, and data integrity
```

### 5. Build the Looker Studio Dashboard

1. Open [Looker Studio](https://lookerstudio.google.com/)
2. Create → New Report
3. Add Data Source → BigQuery → Select your project
4. Select dataset: `hospital_marts`
5. Add components as specified in `dashboard/looker_studio_spec.md`
6. Apply filters, style, and share
