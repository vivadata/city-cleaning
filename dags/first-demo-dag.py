from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator


default_args = {
    "owner": "Aloys",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="first_demo_dag",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    default_args=default_args,
    tags=["bootcamp-de"],
) as dag_basics:

    def legacy_fn():
        print("hello from legacy")

    legacy = PythonOperator(
        task_id="legacy",
        python_callable=legacy_fn,
    )

    date_task = BashOperator(
        task_id="show_date",
        bash_command="date",
    )

    legacy >> date_task