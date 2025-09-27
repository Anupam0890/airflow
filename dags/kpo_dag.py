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
        namespace='airflow-cluster',  # Or your specific namespace like 'composer-user-workloads'
        name='simple-command-pod',
        image='alpine:latest',
        cmds=['sh', '-c'],
        arguments=['echo "Hello from a Kubernetes Pod!"'],
        do_xcom_push=False,  # Set to True if you need to push XComs
        is_delete_operator_pod=True,  # Delete the pod after completion
        get_logs=True
    )

    run_python_script = KubernetesPodOperator(
        task_id="run_python_script_in_pod",
        namespace="default",  # Ensure this namespace exists in your Minikube
        image="python:3.12.11-alpine3.21",  # A suitable Python image
        cmds=["python", "-c"],
        arguments=["print('Hello from a Kubernetes Pod in Minikube!')"],
        name="python-pod-task",
        get_logs=True,  # Stream logs from the pod to Airflow task logs
        do_xcom_push=False  # Set to True if you need to push XComs from the pod
    )

    run_simple_command >> run_python_script
