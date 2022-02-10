from airflow import DAG
from datetime import datetime
from airflow.contrib.operators.bigquery_operator import BigQueryOperator

default_args = {
    'start_date' : datetime(2021,1,1)
}

with DAG(dag_id='adapting_query_to_bigquery',
         schedule_interval=None,
         default_args=default_args,
         tags=['cicd_test_alex'],
         catchup=False
         ) as dag :
    pass
