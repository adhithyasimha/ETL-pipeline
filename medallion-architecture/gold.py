import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

driver_folder = "/Users/adhithya/datascrape/redshiftjdbcdriver/"
jar_files = [
    os.path.join(driver_folder, f)
    for f in os.listdir(driver_folder)
    if f.endswith(".jar")
]
jars_string = ",".join(jar_files)
spark = SparkSession.builder \
    .appName("GoldLayerRedshift") \
    .config("spark.jars", jars_string) \
    .getOrCreate()
silver_base_path = "/Users/adhithya/datascrape/medallion/silver/"
df_silver = spark.read.option("recursiveFileLookup", "true").parquet(silver_base_path)

print(f"Total records in Silver layer: {df_silver.count()}")
df_silver.show(3, truncate=False)
redshift_jdbc_url = "jdbc:redshift://indiamart.587403180581.eu-north-1.redshift-serverless.amazonaws.com:5439/dev"
redshift_properties = {
    "user": "admin",
    "password": "password",
    "driver": "com.amazon.redshift.jdbc.Driver"
}
categories = [row['Category'] for row in df_silver.select("Category").distinct().collect()]

for cat in categories:
    cat_table = cat.lower().replace("-", "_").replace(" ", "_")
    df_cat = df_silver.filter(col("Category") == cat)
    df_cat.write.jdbc(
        url=redshift_jdbc_url,
        table=cat_table,
        mode="append", 
        properties=redshift_properties
    )
    print(f"Category '{cat}' written to Redshift table: {cat_table}")

spark.stop()
print("All categories successfully written to Redshift.")
