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
    dag_id="test_dbt",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["city-cleaning"],
) as dag_basics:

    download_datasets = BashOperator(
        task_id="download_datasets",
        bash_command="""
            curl -X 'GET' 'https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/dans-ma-rue/exports/csv?delimiter=%3B&list_separator=%2C&quote_all=false&with_bom=true&limit=20' -H 'accept: */*' > /tmp/dans-ma-rue.csv
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
    
    # transform_to_bq_clvr = GCSToBigQueryOperator(
    #     task_id="transform_to_bq_clvr",
    #     destination_project_dataset_table=f"{DESTINATION_PROJECT_DATASET}.colonne_verre",
    #     bucket=BUCKET_NAME,
    #     source_objects="dechets-menagers-points-dapport-volontaire-colonnes-a-verre.csv",
    #     write_disposition='WRITE_TRUNCATE',
    #     field_delimiter=";"
    # )
    
    # transform_to_bq_cpst = GCSToBigQueryOperator(
    #     task_id="transform_to_bq_cpst",
    #     destination_project_dataset_table=f"{DESTINATION_PROJECT_DATASET}.composteur",
    #     bucket=BUCKET_NAME,
    #     source_objects="dechets-menagers-points-dapport-volontaire-composteurs.csv",
    #     write_disposition='WRITE_TRUNCATE',
    #     field_delimiter=";"
    # )
    
    # transform_to_bq_txtl = GCSToBigQueryOperator(
    #     task_id="transform_to_bq_txtl",
    #     destination_project_dataset_table=f"{DESTINATION_PROJECT_DATASET}.textile",
    #     bucket=BUCKET_NAME,
    #     source_objects="dechets-menagers-points-dapport-volontaire-conteneur-textile.csv",
    #     write_disposition='WRITE_TRUNCATE',
    #     field_delimiter=";"
    # )
    
    # transform_to_bq_rclr = GCSToBigQueryOperator(
    #     task_id="transform_to_bq_rclr",
    #     destination_project_dataset_table=f"{DESTINATION_PROJECT_DATASET}.recyclerie",
    #     bucket=BUCKET_NAME,
    #     source_objects="dechets-menagers-points-dapport-volontaire-recycleries-et-ressourceries.csv",
    #     write_disposition='WRITE_TRUNCATE',
    #     field_delimiter=";"
    # )
    
    # transform_to_bq_trlb = GCSToBigQueryOperator(
    #     task_id="transform_to_bq_trlb",
    #     destination_project_dataset_table=f"{DESTINATION_PROJECT_DATASET}.trilib",
    #     bucket=BUCKET_NAME,
    #     source_objects="dechets-menagers-points-dapport-volontaire-stations-trilib.csv",
    #     write_disposition='WRITE_TRUNCATE',
    #     field_delimiter=";"
    # )

    dbt_task = BashOperator(
        task_id="test_dbt",
        bash_command="dbt build --select stg_anomalie",
    )

   # [transform_to_bq_dmr, transform_to_bq_clvr, transform_to_bq_cpst, transform_to_bq_txtl, transform_to_bq_rclr, transform_to_bq_trlb] >> dbt_task
    download_datasets >> upload_to_gcs_dmr >> transform_to_bq_dmr >> dbt_task
    # transform_to_bq_dmr >> transform_to_bq_clvr >> transform_to_bq_cpst >> transform_to_bq_txtl >> transform_to_bq_rclr >> transform_to_bq_trlb >> dbt_task