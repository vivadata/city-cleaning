from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator

#BUCKET_NAME = "cc-datasets-storage-dev"
BUCKET_NAME = "dans-ma-rue"
PROJECT_ID = "rue-de-paris-472314"
DESTINATION_PROJECT_DATASET = "city_cleaning_dev"

#
# Run on Cloud Run Jobs.
#
with DAG(
    dag_id="test_dbt",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["bootcamp-de-dbt"],
) as dag_basics:

    transform_to_bq_dmr = GCSToBigQueryOperator(
        task_id="transform_to_bq_dmr",
        destination_project_dataset_table=f"{DESTINATION_PROJECT_DATASET}.dmr",
        bucket=BUCKET_NAME,
        source_objects="dans-ma-rue.csv",
        write_disposition='WRITE_TRUNCATE'
    )
    
    transform_to_bq_clvr = GCSToBigQueryOperator(
        task_id="transform_to_bq_clvr",
        destination_project_dataset_table=f"{DESTINATION_PROJECT_DATASET}.colonne_verre",
        bucket=BUCKET_NAME,
        source_objects="dechets-menagers-points-dapport-volontaire-colonnes-a-verre.csv",
        write_disposition='WRITE_TRUNCATE'
    )
    
    transform_to_bq_cpst = GCSToBigQueryOperator(
        task_id="transform_to_bq_cpst",
        destination_project_dataset_table=f"{DESTINATION_PROJECT_DATASET}.composteur",
        bucket=BUCKET_NAME,
        source_objects="dechets-menagers-points-dapport-volontaire-composteurs.csv",
        write_disposition='WRITE_TRUNCATE'
    )
    
    transform_to_bq_txtl = GCSToBigQueryOperator(
        task_id="transform_to_bq_txtl",
        destination_project_dataset_table=f"{DESTINATION_PROJECT_DATASET}.textile",
        bucket=BUCKET_NAME,
        source_objects="dechets-menagers-points-dapport-volontaire-conteneur-textile.csv",
        write_disposition='WRITE_TRUNCATE'
    )
    
    transform_to_bq_rclr = GCSToBigQueryOperator(
        task_id="transform_to_bq_rclr",
        destination_project_dataset_table=f"{DESTINATION_PROJECT_DATASET}.recyclerie",
        bucket=BUCKET_NAME,
        source_objects="dechets-menagers-points-dapport-volontaire-recycleries-et-ressourceries.csv",
        write_disposition='WRITE_TRUNCATE'
    )
    
    transform_to_bq_trlb = GCSToBigQueryOperator(
        task_id="transform_to_bq_trlb",
        destination_project_dataset_table=f"{DESTINATION_PROJECT_DATASET}.trilib",
        bucket=BUCKET_NAME,
        source_objects="dechets-menagers-points-dapport-volontaire-stations-trilib.csv",
        write_disposition='WRITE_TRUNCATE'
    )

    dbt_task = BashOperator(
        task_id="test_dbt",
        bash_command="dbt run",
    )

    [transform_to_bq_dmr, transform_to_bq_clvr, transform_to_bq_cpst, transform_to_bq_txtl, transform_to_bq_rclr, transform_to_bq_trlb] >> dbt_task