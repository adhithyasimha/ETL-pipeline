from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime

default_args = {
    "owner": "adhithya",
    "start_date": datetime(2025, 8, 19),
    "retries": 1,
}

with DAG(
    dag_id="indiamart_category_dag",
    default_args=default_args,
    schedule='@daily',  
    catchup=False,
) as dag:

    scrape_categories = BashOperator(
        task_id="scrape_categories",
        bash_command="""
        cd /Users/adhithya/datascrape/ && \                  
            python3.11 product_scraper.py
        """
    )
