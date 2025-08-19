from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime,timedelta


default_args={
    "owner":"airflow",
    "start_date":datetime(2025,8,19),
    "retries":2
}

product_dag=DAG(
    dag_id='product_scrapping_dag',
    default_args=default_args,
    schedule='5 0 * * *'
)

scraping_task=BashOperator(
    task_id='scraping_task',
    bash_command="""cd /Users/adhithya/datascrape/scraper_v1/spider && \
        python3.11 product_scraper.py
        """,
    dag=product_dag
    
    
)
scraping_task


