from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from datetime import datetime

with DAG(
    dag_id='kubernetes_pod_example',
    start_date=datetime(2025, 9, 24),
    schedule_interval="@daily",
    catchup=False,
    tags=['kubernetes', 'example'],
) as dag:

# A simple task running a command in an Alpine image
    run_simple_command = KubernetesPodOperator(
        task_id='run_simple_command',
        namespace='default',  # Or your specific namespace like 'composer-user-workloads'
        name='simple-command-pod',
        image='alpine:latest',
        cmds=['sh', '-c'],
        arguments=['echo "Hello from a Kubernetes Pod!"'],
        do_xcom_push=False,  # Set to True if you need to push XComs
        is_delete_operator_pod=True,  # Delete the pod after completion
        get_logs=True,  # Stream logs to Airflow task logs
        cluster_context="docker-desktop"
    )

    run_simple_command
