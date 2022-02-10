import os
import codecs
from datetime import datetime
from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryCheckOperator,
    BigQueryCreateEmptyDatasetOperator,
    BigQueryCreateEmptyTableOperator,
    BigQueryDeleteDatasetOperator,
    BigQueryGetDataOperator,
    BigQueryInsertJobOperator,
    BigQueryIntervalCheckOperator,
    BigQueryValueCheckOperator,
)
from airflow.operators.dummy import DummyOperator
from google.cloud import storage

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/airflow/gcs/data/key/cj-olive-young-poc-7d67896f3d5c.json"

default_args = {
    'owner': 'airflow',
    'start_date' : datetime(2021,1,1),
    'email_on_failure': False,
    'email_on_retry': False,
}


def _extracting_sql() :
    client = storage.Client()
    bucket = client.get_bucket('asia-northeast3-cicd-airflo-b991dc6b-bucket')
    blob = bucket.get_blob('data/test.sql')
    sqlquery = blob.download_as_string()
    str_sqlquery = codecs.decode(sqlquery, 'UTF-8')

    return str_sqlquery

with DAG(dag_id='adapting_query_to_bigquery',
         schedule_interval=None,
         default_args=default_args,
         tags=['cicd_test_alex_update'],
         catchup=False
         ) as dag :
    t1= DummyOperator(task_id='start',
                          dag=dag)   
    t2= BigQueryInsertJobOperator(task_id='executing_sql_on_bigquery',
                                  gcp_conn_id='cicd_bigquery_conn',
                                  configuration={
                                                "query": {
                                                    "query": _extracting_sql(),
                                                    "useLegacySql": False
                                                }
                                            }
                                 )

    t3= DummyOperator(task_id='end',
                      dag=dag)

    t1 >> t2 >> t3
