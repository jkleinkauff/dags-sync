import boto3
from datetime import timedelta, datetime
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import (
    SparkKubernetesOperator,
)
from airflow.providers.cncf.kubernetes.sensors.spark_kubernetes import (
    SparkKubernetesSensor,
)
from airflow.utils.dates import days_ago
from airflow.models import Variable
from airflow.providers.amazon.aws.hooks.base_aws import AwsBaseHook

aws_access_key = Variable.get("AWS_ACCESS_KEY")


#Replacing env vars in config.yaml - This is FAR from recommended. 
# The ideal solution - for spark operator - is to enable a WebHook in k8s cluster
# If not enabled, you need to use the env vars like I'm doing here

aws_cred = AwsBaseHook("aws-spark", client_type="s3").get_credentials()
s3_client = boto3.client(
    "s3",
    aws_access_key_id=aws_cred.access_key,
    aws_secret_access_key=aws_cred.secret_key,
)

s3_client.download_file(f"data-lake-jho", "spark-jobs/config.yaml", "config.yaml")

with open('config.yaml', 'r') as file :
  yaml_data = file.read()

yaml_data = yaml_data.replace('@AWS_ACCESS_KEY', 'aws_access_key')

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(1),
    "email": ["airflow@example.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "max_active_runs": 1,
    "retries": 0,
}
# [END default_args]

# [START instantiate_dag]

dag = DAG(
    "spark_pi",
    default_args=default_args,
    schedule_interval=timedelta(days=1),
    tags=["example"],
)

# spark = open(
#     "example_spark_kubernetes_operator_pi.yaml").read()

submit = SparkKubernetesOperator(
    task_id="spark_pi_submit",
    namespace="airflow",
    # application_file="spark/config.yaml",
    application_file=yaml_data,
    kubernetes_conn_id="kubernetes_in_cluster",
    do_xcom_push=True,
    dag=dag,
    api_group="sparkoperator.k8s.io",
)

sensor = SparkKubernetesSensor(
    task_id="spark_pi_monitor",
    namespace="airflow",
    application_name="{{ task_instance.xcom_pull(task_ids='spark_pi_submit')['metadata']['name'] }}",
    kubernetes_conn_id="kubernetes_in_cluster",
    dag=dag,
    api_group="sparkoperator.k8s.io",
    attach_log=True,
)

submit >> sensor
