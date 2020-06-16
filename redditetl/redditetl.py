import os
import sys

import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

sys.path.insert(0,os.path.abspath(os.path.dirname('/home/airflow/.local/lib/python3.8/site-packages/airflow/example_dags/etl/reddit/redcollect.py')))
from redcollect import download_data 
from scraping import scrape_data 
from textanalysis import analyze_files
from s3upload import upload_to_s3


default_args = {
    'owner' : 'Airflow',
    'start_date' : datetime.datetime(2020, 6, 15)
}

with DAG(dag_id='reddit_dag', schedule_interval='@once', default_args=default_args) as dag:

    dummy_opr = DummyOperator(
        task_id = 'dummy_init'
        )

    py_reddit_opr = PythonOperator(
        task_id = 'reddit_pull',
        python_callable=download_data
        )

    py_scraping_opr = PythonOperator(
        task_id = 'scrape_website',
        python_callable=scrape_data
        )

    py_analyze_opr = PythonOperator(
        task_id = 'analyze_files',
        python_callable=analyze_files
        )

    py_s3_upload_opr = PythonOperator(
        task_id='s3_upload',
        python_callable=upload_to_s3
        )
    
    dummy_opr >> py_reddit_opr >> py_scraping_opr >> py_analyze_opr >> py_s3_upload_opr