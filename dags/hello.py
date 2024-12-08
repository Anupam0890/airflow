from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator


def print_a():
    print("Hello Anupam")


with DAG("my_dag", start_date=datetime(2024, 12, 8), schedule='@daily', catchup=False,
         tags=['data_science'], description='A Sample DAG'):
    task_a = PythonOperator(task_id='task_a', python_callable=print_a)