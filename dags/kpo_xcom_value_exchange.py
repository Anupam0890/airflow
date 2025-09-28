from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from datetime import datetime
from airflow.decorators import task 

with DAG(
    dag_id='kubernetes_pod_xcom',
    start_date=datetime(2025, 9, 27),
    schedule_interval="@daily",
    catchup=False,
    tags=['kubernetes', 'xcom', 'example'],
) as dag:
    
    kpo_push_xcom = KubernetesPodOperator( 
            task_id="kpo_push_xcom", 
            namespace="airflow-cluster", 
            image="localhost:5000/simple_app", 
            name="airflow-test-pod",
            do_xcom_push=True,
            is_delete_operator_pod=True, 
            get_logs=True, 
            log_events_on_failure=False 
        )
    
    @task 
    def pull_data(ti=None): 
        print(ti.xcom_pull(task_ids='kpo_push_xcom')) 

    kpo_push_xcom >> pull_data()
    