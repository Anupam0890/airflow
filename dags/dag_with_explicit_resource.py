from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import time
from kubernetes.client import models as k8s

k8s_exec_config_resource_requirements = {
    "pod_override": k8s.V1Pod(
        spec=k8s.V1PodSpec(
            containers=[
                k8s.V1Container(
                    name="base",
                    resources=k8s.V1ResourceRequirements(
                        requests={"cpu": "500m", "memory": "1024Mi"},
                        limits={"cpu": 1, "memory": "2048Mi"}
                    )
                )
            ]
        )
    )
}

@dag(
    'dag_with_explicit_resource',
    start_date=datetime.today() - timedelta(days=1),
    # Airflow 3 compatible schedule
    schedule='@daily',
    description='A Simple Dag Explicit ',
    tags=['data_platform'],
    catchup=False
)
def dag_with_explicit_resource():
    bash_resource_overrise = BashOperator(
      task_id="bash_resource_requirements_override_example",
      bash_command="echo hi",
      executor_config=k8s_exec_config_resource_requirements
    )
    @task(executor_config=k8s_exec_config_resource_requirements)
    def resource_requirements_override_example():
        print("Started waiting ...")
        time.sleep(600)

    bash_resource_overrise >> resource_requirements_override_example()


dag_with_explicit_resource()
