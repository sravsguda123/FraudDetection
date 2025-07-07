from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StringType, IntegerType

# Start Spark Session
spark = SparkSession.builder \
    .appName("FraudDetectionConsumer") \
    .getOrCreate()

# Define schema for JSON parsing
schema = StructType() \
    .add("transaction_id", StringType()) \
    .add("amount", IntegerType()) \
    .add("status", StringType())

# Read from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "payments") \
    .option("startingOffsets", "latest") \
    .load()

# Convert Kafka value to String, parse JSON
json_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Filter only fraudulent
fraud_df = json_df.filter(col("status") == "fraudulent")

# Show output in console
query = fraud_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()

