from airflow import DAG
from datetime import datetime, timedelta

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

    @task()
    def greet():
        print("👋 Hello from my first task!")

    greet_task = greet()

    date_task = BashOperator(
        task_id="show_date",
        bash_command="date",
    )

    greet_task >> date_task