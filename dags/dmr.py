from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator

#BUCKET_NAME = "cc-datasets-storage-dev"
BUCKET_NAME = "cc-datasets-storage-dev"
PROJECT_ID = "rue-de-paris-472314"
DESTINATION_PROJECT_DATASET = "city_cleaning_dev"

#
# Run on Cloud Run Jobs.
#
with DAG(
    dag_id="dag_dmr",
    start_date=datetime(2025, 1, 1),
    schedule="0 1 * * *",
    catchup=False,
    tags=["city-cleaning"],
) as dag_dmr:

    download_datasets_dmr = BashOperator(
        task_id="download_datasets_dmr",
        bash_command="""
            curl -X 'GET' 'https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/dans-ma-rue/exports/csv?delimiter=%3B&list_separator=%2C&quote_all=false&with_bom=true' -H 'accept: */*' > /tmp/dans-ma-rue.csv
        """,
    )
    
    upload_to_gcs_dmr = LocalFilesystemToGCSOperator(
        task_id="upload_to_gcs_dmr",
        src="/tmp/dans-ma-rue.csv",
        dst="dans-ma-rue.csv",
        bucket=BUCKET_NAME,
    )

    transform_to_bq_dmr = GCSToBigQueryOperator(
        task_id="transform_to_bq_dmr",
        destination_project_dataset_table=f"{DESTINATION_PROJECT_DATASET}.dmr",
        bucket=BUCKET_NAME,
        source_objects="dans-ma-rue.csv",
        write_disposition='WRITE_TRUNCATE',
        field_delimiter=";"
    )

    dbt_task_dmr = BashOperator(
        task_id="dbt_task_dmr",
        bash_command="""
            dbt build --select stg_anomalie &&
            dbt build --select activite &&
            dbt build --select arbre &&
            dbt build --select auto &&
            dbt build --select degradation &&
            dbt build --select eau &&
            dbt build --select eclairage &&
            dbt build --select graffiti &&
            dbt build --select mobilier_urbain &&
            dbt build --select objet_abandonne &&
            dbt build --select proprete &&
            dbt build --select voirie
        """,
    )

    download_datasets_dmr >> upload_to_gcs_dmr >> transform_to_bq_dmr >> dbt_task_dmr