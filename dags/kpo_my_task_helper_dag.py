from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from datetime import datetime

with DAG(
        dag_id='python_with_args_k8s_pod_operator',
        start_date=datetime(2025, 10, 11),
        schedule_interval=None,
        catchup=False,
        tags=['kubernetes', 'python'],
) as dag:
    run_python_script = KubernetesPodOperator(
        task_id='run_python_with_args',
        namespace='airflow',  # Or your specific Kubernetes namespace
        image='localhost:5000/kpo_task_helper', # Replace with your image
        image_pull_policy='Never', # Download local images
        cmds=['python'],
        arguments=['/app/my_task_helper.py', 'json_to_df', '{"name": "Anupam Pandit", "age": 303, "email": "anupam.p443@fpbizx.com"}'],
        name='python-script-pod',
        is_delete_operator_pod=True, # Delete the pod after completion
        get_logs=True, # Fetch logs from the pod
        )

    run_csv_string_to_json_func = KubernetesPodOperator(
        task_id='run_csv_string_to_json_func',
        namespace='airflow',  # Or your specific Kubernetes namespace
        image='localhost:5000/kpo_task_helper', # Replace with your image
        image_pull_policy='Never', # Download local images
        cmds=['python'],
        arguments=['/app/my_task_helper.py', 'csv_string_to_json', 'Name,Age,City\nJhon,28,New York\nAlice,24, Los Angeles\nBob,30,Chicago'],
        name='python-script-with-args',
        is_delete_operator_pod=True, # Delete the pod after completion
        get_logs=True, # Fetch logs from the pod
    )
    

    run_python_script >> run_csv_string_to_json_func
