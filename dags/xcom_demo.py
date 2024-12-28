from airflow.decorators import task, dag
from datetime import datetime


@dag(
    'xcom_demo',
    tags=["dp"],
    start_date=datetime(2024, 12, 28),
    schedule="@daily",
    catchup=False,
)
def xcom_demo1():
    @task
    def task_a(ti=None):
        ti.xcom_push(key="mobile", value="Motorola")

    @task
    def task_b(ti=None):
        phone_detail = ti.xcom_pull(task_ids="task_a", key="mobile")
        print(phone_detail)

    task_a() >> task_b()


xcom_demo1()
