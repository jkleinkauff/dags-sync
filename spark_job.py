from datetime import datetime
from airflow import DAG
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator


dag = DAG(
    "spark_job",
    description="Hello World Spark DAG",
    schedule_interval="0 */6 * * *",
    start_date=datetime(2017, 3, 20),
    catchup=False,
)

k = KubernetesPodOperator(
    task_id='spark-job-task-ex',
    name='spark-job-task',
    namespace='airflow',
    image='kleinkauff/spark-py',
    cmds=['./bin/spark-submit'],
    arguments=[
        '--master k8s://https://192.168.15.180:6443',
        #'--deploy-mode cluster',
        '--name spark-pi',
        ' --class org.apache.spark.examples.SparkPi',
        '--conf spark.executor.instances=3',
        '--conf spark.kubernetes.container.image=kleinkauff/spark-py',
        '$SPARK_HOME/examples/src/main/python/pi.py'
    ],
    dag=dag,
)