from airflow.decorators import dag, task
from datetime import datetime, timedelta
import time


@dag(
    'check_dag_test',
    start_date=datetime.today() - timedelta(days=1),
    schedule_interval='@daily',
    description='A Simple Check Dag',
    tags=['data_platform'],
    catchup=False
)
def check_dag():
    @task
    def check_task():
        t_end = time.time() + 60 * 15
        while time.time() < t_end:
            print(f"I am at time {time}")
            time.sleep(10)

    check_task()


check_dag()
