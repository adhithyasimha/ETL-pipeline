# ETL Data Pipeline 

This project implements a robust data engineering pipeline to scrape product data from IndiaMART, process it through a Medallion Architecture (Bronze → Silver → Gold), and load curated results into AWS Redshift Serverless for visualization in AWS QuickSight. 
The pipeline is orchestrated using **Apache Airflow** for seamless scheduling and execution.

## Setup Instructions

### 1. Install Python 3.11 using `pyenv`
```
pyenv install 3.11.9
pyenv virtualenv 3.11.9 datascrape-env
pyenv activate datascrape-env
```
### 2. Install Project Dependencies
```
pip install -r requirements.txt

```
## Running the Pipeline
### 1. Initialise Airflow
```
airflow db init
airflow standalone

```
### 2. Copy DAGs to Airflow Directory
```
cp dags/*.py ~/airflow/dags/

```
### 3. Trigger DAGs
The DAGs are scheduled to run automatically at the following times:
```
indiamart_category_dag: Daily at 00:00
product_scrapping_dag: Daily at 00:05
medallion_dags: Daily at 00:10

```

## DAG Details
### 1. indiamart_category_dag (Runs daily at 00:00)

Purpose: Scrapes category links from IndiaMART using Scrapy.
Output: Stores results in ```categories.json```

### 2. product_scrapping_dag (Runs daily at 00:05)

Purpose: Scrapes product details from each category link using Scrapy.
Output: Stores results in ```products.json```
### 3. medallion_dags (Runs daily at 00:10)

Purpose: Processes data through the Medallion Architecture using Apache Spark 3.4.3.

Tasks:

bronze_task: ```Ingests raw data.```

silver_task: ```Cleans and transforms data.```

gold_task: ```Aggregates and curates data for analytics.```


Flow: ```bronze_task >> silver_task >> gold_task```

## Architecture
<img width="1091" height="620" alt="Screenshot 2025-08-19 at 8 48 19 PM" src="https://github.com/user-attachments/assets/ba68519d-addc-4dff-956f-d95e300d55ab" />

### Analytics

Storage: Gold layer data is loaded into AWS ```Redshift Serverless``` for scalable querying.
Visualisation: Dashboards are built in AWS QuickSight to provide insights into:

<img width="1432" height="885" alt="Screenshot 2025-08-19 at 9 11 05 PM" src="https://github.com/user-attachments/assets/01520022-f501-4136-a25a-22f595158f33" />

