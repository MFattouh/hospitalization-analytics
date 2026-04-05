"""DAG 3: Run dbt deps, run, and test for hospital data transformations."""

import os
import subprocess
from pathlib import Path

from prefect import flow, task

DBT_PROJECT_DIR = os.getenv("DBT_PROJECT_DIR", "dbt")


@task
def run_dbt_command(command: str, project_dir: str) -> str:
    """Run a dbt command in the project directory."""
    result = subprocess.run(
        ["dbt", command],
        cwd=project_dir,
        capture_output=True,
        text=True,
        timeout=600,
    )

    if result.returncode != 0:
        raise RuntimeError(f"dbt {command} failed:\n{result.stderr}")

    print(f"dbt {command} completed successfully")
    return result.stdout


@flow(name="dbt-transform", log_prints=True)
def dbt_transform(
    project_dir: str = DBT_PROJECT_DIR,
) -> dict[str, str]:
    """Run dbt deps, run, and test."""
    project_path = Path(project_dir).resolve()
    print(f"Running dbt in: {project_path}")

    print("Running dbt deps...")
    run_dbt_command("deps", str(project_path))

    print("Running dbt run...")
    run_dbt_command("run", str(project_path))

    print("Running dbt test...")
    run_dbt_command("test", str(project_path))

    return {"status": "completed", "project_dir": str(project_path)}


if __name__ == "__main__":
    dbt_transform()
