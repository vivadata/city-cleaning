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
    dag_id="dag_colonne_verre",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["city-cleaning"],
) as dag_colonne_verre:

    download_datasets_clvr = BashOperator(
        task_id="download_datasets_clvr",
        bash_command="""
            curl -X 'GET' 'https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/dechets-menagers-points-dapport-volontaire-colonnes-a-verre/exports/csv?delimiter=%3B&list_separator=%2C&quote_all=false&with_bom=true&limit=20' -H 'accept: */*' > /tmp/colonnes-a-verre.csv
        """,
    )
    
    upload_to_gcs_clvr = LocalFilesystemToGCSOperator(
        task_id="upload_to_gcs_clvr",
        src="/tmp/colonnes-a-verre.csv",
        dst="colonnes-a-verre.csv",
        bucket=BUCKET_NAME,
    )
    
    transform_to_bq_clvr = GCSToBigQueryOperator(
        task_id="transform_to_bq_clvr",
        destination_project_dataset_table=f"{DESTINATION_PROJECT_DATASET}.colonne_verre",
        bucket=BUCKET_NAME,
        source_objects="colonnes-a-verre.csv",
        write_disposition='WRITE_TRUNCATE',
        field_delimiter=";"
    )

    dbt_task_clvr = BashOperator(
        task_id="dbt_task_clvr",
        bash_command="dbt build --select stg_colonne_verre",
    )

   # [transform_to_bq_dmr, transform_to_bq_clvr, transform_to_bq_cpst, transform_to_bq_txtl, transform_to_bq_rclr, transform_to_bq_trlb] >> dbt_task
    download_datasets_clvr >> upload_to_gcs_clvr >> transform_to_bq_clvr >> dbt_task_clvr
    # transform_to_bq_dmr >> transform_to_bq_clvr >> transform_to_bq_cpst >> transform_to_bq_txtl >> transform_to_bq_rclr >> transform_to_bq_trlb >> dbt_task