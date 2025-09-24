from datetime import datetime, timedelta

from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator


#
# Run on Cloud Run Jobs.
#
with DAG(
    dag_id="first_demo_dag",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["bootcamp-de-dbt"],
) as dag_basics:

    @task()
    def greet():
        print("👋 Hello from my first task!")

    greet_task = greet()

    dbt_task = BashOperator(
        task_id="test_dbt",
        bash_command="dbt -h",
    )

    greet_task >> dbt_task