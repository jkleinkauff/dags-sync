from datetime import datetime
from airflow import DAG
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator


dag = DAG('jhodb_fake_date', description='Hello World DAG',
          schedule_interval='0 */3 * * *',
          start_date=datetime(2017, 3, 20), catchup=False)

k = KubernetesPodOperator(
    namespace="airflow",
    name="jhodb-fake-data",
    image="kleinkauff/jho-pg-datagen",
    cmds=["./generator.py"],
    arguments=["--dsn postgresql://user_jhodb:jhodb@192.168.15.191:32284/jhodb --batch-size 20 --rows 3 --target examples/simple/ecommerce.py"],
    labels={"foo": "bar"},
    task_id="fake_data",
    dag=dag
)
