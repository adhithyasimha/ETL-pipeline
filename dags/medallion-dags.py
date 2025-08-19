from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime,timedelta

default_args={
    "owner":"airflow",
    "start_date":datetime(2025,8,19),
    "retries":2
}

medallion_dag=DAG(
    dag_id='medallion_dags',
    default_args=default_args,
    schedule='10 0 * * *'
)

bronze_task=BashOperator(
    task_id='bronze',
    dag=medallion_dag,
    bash_command="python3.11 /Users/adhithya/datascrape/medallion-scripts/bronze.py"


)
silver_task=BashOperator(
    task_id='silver',
    dag=medallion_dag,
    bash_command="python3.11 /Users/adhithya/datascrape/medallion-scripts/silver.py"
)

gold_task=BashOperator(
    task_id='gold',
    dag=medallion_dag,
    bash_command="python3.11 /Users/adhithya/datascrape/medallion-scripts/gold.py"
)


bronze_task >> silver_task>>gold_task