import datetime

from dag_utils.tools import DBTComposerJobOperator
from airflow.models import Param
from airflow.decorators import dag


#
# Run on Cloud Run Jobs.
#
@dag(
    schedule_interval=None,
    catchup=False,
    start_date=datetime.datetime(2022, 1, 1),
    params={
        'job_name': Param(
            default='example-dbt-run-job',
            type='string',
        ),
    },
)
def example_dbt_run_dag():

    # Launch the job, optionally parameterising it from different
    # job names.
    DBTComposerJobOperator(
        task_id='example_dbt_run_job',
        job_name='{{ params.job_name }}',
        capture_docs=True,
        cmds=[
            "/bin/bash",
            "-xc",
            "&&".join([
                "dbt -h"
            ]),
        ],
        dbt_vars={
            "reporting_day": "{{ ds }}",
        },
    )


example_dbt_run_dag()