## add this helm repository & pull updates from it
helm repo add airflow-stable https://airflow-helm.github.io/charts
helm repo update

## set the release-name & namespace
export AIRFLOW_NAME="airflow-cluster"
export AIRFLOW_NAMESPACE="airflow-cluster"

helm install \
  "$AIRFLOW_NAME" \
  airflow-stable/airflow \
  --namespace "$AIRFLOW_NAMESPACE" \
  --version "8.9.0" \
  --debug
  --values ./airflow-values.yaml


## Create PVC to store Airflow Logs
kubectl apply -f airflow-logs-pv.yaml
kubectl apply -f airflow-logs-pvc.yaml