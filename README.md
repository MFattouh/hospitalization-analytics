# Hospital Bed Operations Dashboard

An end-to-end data engineering pipeline and executive dashboard for hospital bed occupancy KPIs, built on GCP.

## Architecture

```
CSV Sources → GCS (Datalake) → BigQuery External Tables → BigQuery Raw → dbt (Staging → Marts) → Looker Studio
                                    ↑
                              Prefect Orchestration
```

## Prerequisites

- GCP project with a service account (BigQuery Admin, Storage Admin, Compute Admin)
- Terraform >= 1.5.0
- Python >= 3.10
- dbt-core with dbt-bigquery
- Prefect >= 2.14.0

## Setup

### 1. Terraform

```bash
cd terraform

# Create a tfvars file
cat > terraform.tfvars <<EOF
gcp_project_id     = "your-project-id"
credentials_file   = "/path/to/service-account.json"
location           = "US"
bucket_name        = "your-hospital-datalake-bucket"
bq_dataset_raw     = "raw"
bq_dataset_staging = "staging"
bq_dataset_marts   = "marts"
EOF

terraform init
terraform plan
terraform apply
```

### 2. Python Environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. dbt Setup

```bash
cd dbt

# Copy and edit profiles.yml
cp profiles.yml.example profiles.yml

# Install dependencies
dbt deps
```

### 4. Prefect Server

```bash
# Start local Prefect server
prefect server start

# In another terminal, deploy flows
prefect deployment build pipelines/master_pipeline.py:hospital_data_pipeline --name main -a
prefect deployment apply master_pipeline-deployment.yaml
```

## Running the Pipeline

### Full Pipeline

```bash
export GCS_BUCKET="your-bucket-name"
export BQ_DATASET_RAW="raw"
export DBT_PROJECT_DIR="dbt"
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
export GCP_PROJECT_ID="your-project-id"

python -m pipelines.master_pipeline
```

### Individual Stages

```bash
# Stage 1 only: CSVs → GCS
python -m pipelines.ingest_gcs

# Stage 2 only: GCS → BigQuery raw
python -m pipelines.ingest_bigquery

# Stage 3 only: dbt transformations
python -m pipelines.dbt_transform
```

### dbt Commands

```bash
cd dbt

# Run all models
dbt run

# Run staging models only
dbt run --select staging

# Run tests
dbt test

# Generate documentation
dbt docs generate
dbt docs serve
```

## Project Structure

```
├── terraform/          # Infrastructure as Code
├── pipelines/          # Prefect orchestration flows
├── dbt/                # dbt transformations
│   ├── models/
│   │   ├── staging/    # Cleaned, typed models
│   │   └── marts/      # Business-ready tables
│   └── tests/          # Generic dbt tests
└── requirements.txt    # Python dependencies
```

## Dashboard

Connect Looker Studio to the `marts` dataset in BigQuery. Build the executive dashboard with:

- **4 KPI Scorecards:** Avg Occupancy Rate, Total Admissions, Total Refusals, Avg Satisfaction
- **4 Charts:** Weekly Occupancy Trend, Demand vs Capacity, Satisfaction Correlation, Refusal Rate & Staff Morale
- **3 Filters:** Service, Month, Event Type
