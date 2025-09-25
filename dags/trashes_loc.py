from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator

BUCKET_NAME = "cc-datasets-storage-dev"
PROJECT_ID = "rue-de-paris-472314"
DESTINATION_PROJECT_DATASET = "city_cleaning_dev"

#
# Run on Cloud Run Jobs.
#
with DAG(
    dag_id="dag_trashes_loc",
    start_date=datetime(2025, 1, 1),
    schedule="0 0 1 * *",
    catchup=False,
    tags=["city-cleaning"],
) as dag_trashes_loc:


    #
    # COLONNES A VERRE
    #

    download_datasets_clvr = BashOperator(
        task_id="download_datasets_clvr",
        bash_command="""
            curl -X 'GET' 'https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/dechets-menagers-points-dapport-volontaire-colonnes-a-verre/exports/csv?delimiter=%3B&list_separator=%2C&quote_all=false&with_bom=true' -H 'accept: */*' > /tmp/colonnes-a-verre.csv
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

    #
    # COMPOSTEUR
    #

    download_datasets_cpst = BashOperator(
        task_id="download_datasets_cpst",
        bash_command="""
            curl -X 'GET' 'https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/dechets-menagers-points-dapport-volontaire-composteurs/exports/csv?delimiter=%3B&list_separator=%2C&quote_all=false&with_bom=true' -H 'accept: */*' > /tmp/composteur.csv
        """,
    )
    
    upload_to_gcs_cpst = LocalFilesystemToGCSOperator(
        task_id="upload_to_gcs_cpst",
        src="/tmp/composteur.csv",
        dst="composteur.csv",
        bucket=BUCKET_NAME,
    )
    
    transform_to_bq_cpst = GCSToBigQueryOperator(
        task_id="transform_to_bq_cpst",
        destination_project_dataset_table=f"{DESTINATION_PROJECT_DATASET}.composteur",
        bucket=BUCKET_NAME,
        source_objects="composteur.csv",
        write_disposition='WRITE_TRUNCATE',
        field_delimiter=";"
    )

    dbt_task_cpst = BashOperator(
        task_id="dbt_task_cpst",
        bash_command="dbt build --select stg_composteur",
    )

    #
    # TEXTILE
    #
    download_datasets_txtl = BashOperator(
        task_id="download_datasets_txtl",
        bash_command="""
            curl -X 'GET' 'https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/dechets-menagers-points-dapport-volontaire-conteneur-textile/exports/csv?delimiter=%3B&list_separator=%2C&quote_all=false&with_bom=true' -H 'accept: */*' > /tmp/textile.csv
        """,
    )
    
    upload_to_gcs_txtl = LocalFilesystemToGCSOperator(
        task_id="upload_to_gcs_txtl",
        src="/tmp/textile.csv",
        dst="textile.csv",
        bucket=BUCKET_NAME,
    )

    transform_to_bq_txtl = GCSToBigQueryOperator(
        task_id="transform_to_bq_txtl",
        destination_project_dataset_table=f"{DESTINATION_PROJECT_DATASET}.textile",
        bucket=BUCKET_NAME,
        source_objects="textile.csv",
        write_disposition='WRITE_TRUNCATE',
        field_delimiter=";"
    )

    dbt_task_txtl = BashOperator(
        task_id="dbt_task_txtl",
        bash_command="dbt build --select stg_textile",
    )

    #
    # RECYCLERIE
    #
    download_datasets_rclr = BashOperator(
        task_id="download_datasets_rclr",
        bash_command="""
            curl -X 'GET' 'https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/dechets-menagers-points-dapport-volontaire-recycleries-et-ressourceries/exports/csv?delimiter=%3B&list_separator=%2C&quote_all=false&with_bom=true' -H 'accept: */*' > /tmp/recyclerie.csv
        """,
    )
    
    upload_to_gcs_rclr = LocalFilesystemToGCSOperator(
        task_id="upload_to_gcs_rclr",
        src="/tmp/recyclerie.csv",
        dst="recyclerie.csv",
        bucket=BUCKET_NAME,
    )
    
    transform_to_bq_rclr = GCSToBigQueryOperator(
        task_id="transform_to_bq_rclr",
        destination_project_dataset_table=f"{DESTINATION_PROJECT_DATASET}.recyclerie",
        bucket=BUCKET_NAME,
        source_objects="recyclerie.csv",
        write_disposition='WRITE_TRUNCATE',
        field_delimiter=";"
    )
    
    dbt_task_rclr = BashOperator(
        task_id="dbt_task_rclr",
        bash_command="dbt build --select stg_recyclerie",
    )
    
    #
    # TRILIB
    #
    download_datasets_trlb = BashOperator(
        task_id="download_datasets_trlb",
        bash_command="""
            curl -X 'GET' 'https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/dechets-menagers-points-dapport-volontaire-stations-trilib/exports/csv?delimiter=%3B&list_separator=%2C&quote_all=false&with_bom=true' -H 'accept: */*' > /tmp/trilib.csv
        """,
    )
    
    upload_to_gcs_trlb = LocalFilesystemToGCSOperator(
        task_id="upload_to_gcs_trlb",
        src="/tmp/trilib.csv",
        dst="trilib.csv",
        bucket=BUCKET_NAME,
    )
    
    transform_to_bq_trlb = GCSToBigQueryOperator(
        task_id="transform_to_bq_trlb",
        destination_project_dataset_table=f"{DESTINATION_PROJECT_DATASET}.trilib",
        bucket=BUCKET_NAME,
        source_objects="trilib.csv",
        write_disposition='WRITE_TRUNCATE',
        field_delimiter=";"
    )

    dbt_task_trlb = BashOperator(
        task_id="dbt_task_trlb",
        bash_command="dbt build --select stg_trilib",
    )
    
    dbt_task_build_mart = BashOperator(
        task_id="dbt_task_build_mart",
        bash_command="dbt build --select poubelle",
    )

    download_datasets_clvr >> upload_to_gcs_clvr >> transform_to_bq_clvr >> dbt_task_clvr >> download_datasets_cpst >> upload_to_gcs_cpst >> transform_to_bq_cpst >> dbt_task_cpst >> download_datasets_txtl >> upload_to_gcs_txtl >> transform_to_bq_txtl >> dbt_task_txtl >> download_datasets_rclr >> upload_to_gcs_rclr >> transform_to_bq_rclr >> dbt_task_rclr >> download_datasets_trlb >> upload_to_gcs_trlb >> transform_to_bq_trlb >> dbt_task_trlb >> dbt_task_build_mart