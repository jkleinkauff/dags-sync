from datetime import datetime
from airflow import DAG
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator

dag = DAG(
    "spark_job_operator",
    description="Hello World Spark Operator DAG",
    schedule_interval="0 */6 * * *",
    start_date=datetime(2017, 3, 20),
    catchup=False,
)

transformation = SparkKubernetesOperator(
    task_id='spark_transform_frete_new',
    namespace='airflow',
    application_file='spark/config.yaml',
    kubernetes_conn_id='kubernetes_default',
    do_xcom_push=False,
)

transformation