import os
from pyspark.sql.functions import col, regexp_replace
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("SilverLayerProcessing").getOrCreate()
silver_path = "medallion/silver/"
bronze_path = "/Users/adhithya/datascrape/medallion/bronze"
df_raw = spark.read.parquet(bronze_path)

df_silver = df_raw.withColumn("Price", regexp_replace(col("Price"), "[₹,\/Piece]", "").cast("double")) \
                  .withColumn("Rating", col("Rating").cast("double"))

# Deduplicate
df_silver = df_silver.dropDuplicates(["Product Name", "Supplier", "Category"])
categories = [row['Category'] for row in df_silver.select("Category").distinct().collect()]

for cat in categories:
    cat_name = cat.lower().replace("-", "_").replace(" ", "_")
    df_cat = df_silver.filter(col("Category") == cat)
    df_cat.write.mode("append").parquet(os.path.join(silver_path, cat_name))

print("Silver layer processed and saved by category.")
