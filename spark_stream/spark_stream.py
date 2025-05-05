from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, IntegerType, DoubleType, LongType
import psycopg2

spark = SparkSession.builder.appName("KafkaToTimescaleDB").getOrCreate()

schema = StructType() \
    .add("sensor_id", IntegerType()) \
    .add("temperature", DoubleType()) \
    .add("timestamp", LongType())

df_raw = spark.read.format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "sensors") \
    .load()

df_parsed = df_raw.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

def write_to_pg(df, epoch_id):
    rows = df.collect()
    conn = psycopg2.connect(
        dbname="mydb", user="myuser", password="mypassword", host="timescaledb", port=5432
    )
    cur = conn.cursor()
    for r in rows:
        cur.execute(
            "INSERT INTO sensor_data (sensor_id, temperature, timestamp) VALUES (%s, %s, to_timestamp(%s))",
            (r.sensor_id, r.temperature, r.timestamp)
        )
    conn.commit()
    cur.close()
    conn.close()

df_parsed.writeStream.foreachBatch(write_to_pg).start().awaitTermination()
