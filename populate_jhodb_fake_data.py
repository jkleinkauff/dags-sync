from datetime import datetime
from airflow import DAG
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator


dag = DAG('jhodb_fake_date', description='Hello World DAG',
          schedule_interval='0 30 * * *',
          start_date=datetime(2017, 3, 20), catchup=False)

k = KubernetesPodOperator(
    namespace="jhodb",
    name="jhodb-fake-data",
    image="kleinkauff/jho-pg-datagen",
    cmds=["/bin/bash"],
    arguments=["./generator.py"],
    labels={"foo": "bar"},
    task_id="fake_data",
    dag=dag
)
