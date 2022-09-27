from airflow import DAG
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator


dag = DAG('hello_world_pod_operator', description='Hello World DAG',
          schedule_interval='0 12 * * *',
          start_date=datetime(2017, 3, 20), catchup=False)

k = KubernetesPodOperator(
    name="hello-dry-run",
    image="debian",
    cmds=["bash", "-cx"],
    arguments=["echo", "10"],
    labels={"foo": "bar"},
    task_id="dry_run_demo",
    dag=dag
)
