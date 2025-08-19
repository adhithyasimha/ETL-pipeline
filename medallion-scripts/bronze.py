from pyspark.sql import SparkSession
from datetime import date
import os

spark = SparkSession.builder.appName("IndiaMartMedallion").getOrCreate()

bronze_path = "/Users/adhithya/datascrape/medallion/bronze/"
json_file = "/Users/adhithya/datascrape/scraped_content/indiamart_products.json"
df_bronze = spark.read.option("multiline", "true").json(json_file)

print(f"Records loaded: {df_bronze.count()}")
print("Schema:")
df_bronze.printSchema()
print("Sample data:")
df_bronze.show(3, truncate=False)

today = date.today().isoformat()
output_path = os.path.join(bronze_path, f"date={today}")
os.makedirs(bronze_path, exist_ok=True)
df_bronze.write.mode("append").parquet(output_path)

print(f"Bronze layer saved at {output_path}")


spark.stop()