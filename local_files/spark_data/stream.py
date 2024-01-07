from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, from_unixtime, col, year, month, dayofmonth
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, LongType, BooleanType, MapType
import logging

# Adicione esta linha no início do seu script
import os

checkpoint_location = "/data/spark-logs/checkpoint"
if not os.path.exists(checkpoint_location):
    os.makedirs(checkpoint_location)


# Define the Kafka topic and bootstrap servers
kafka_topic = "postgres.usuario.usuario"
kafka_bootstrap_servers = "172.18.0.3:9092"

# Define MinIO parameters
minio_endpoint = "http://172.18.0.8:9000"  # Use the MinIO container's IP and port
minio_access_key = "5T4gRXIIeRDm0sf6tyel"
minio_secret_key = "6FKOQXb45ft5XwCAtdKUfhE53BxUCw1Cf2CaZCg6"
minio_bucket = "usuario-database"
minio_path = "usuario"

hudi_version = "0.14.0"
spark_master = "local[*]"  # Change this to your Spark cluster URL if not running in local mode
spark_version = '3.1.2'

print('Starting Spark')
# Create a Spark session
spark = SparkSession.builder \
    .appName("HudiKafkaConsumer") \
    .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1')\
    .getOrCreate()


# Define the schema for the incoming Kafka messages
print("Spark Sartted")
# Define the schema for the message
schema = StructType([
    StructField("schema", StructType([
        StructField("before", StructType([
            StructField("id", StringType(), False),
            StructField("nome", StringType(), True),
            StructField("sobrenome", StringType(), True),
            StructField("idade", IntegerType(), True),
            StructField("telefone", StringType(), True),
            StructField("email", StringType(), True),
            StructField("created_at", LongType(), True),
            StructField("updated_at", LongType(), True)
        ]), True),
        StructField("after", StructType([
            StructField("id", StringType(), False),
            StructField("nome", StringType(), True),
            StructField("sobrenome", StringType(), True),
            StructField("idade", IntegerType(), True),
            StructField("telefone", StringType(), True),
            StructField("email", StringType(), True),
            StructField("created_at", LongType(), True),
            StructField("updated_at", LongType(), True)
        ]), True),
        StructField("source", StructType([
            StructField("version", StringType(), False),
            StructField("connector", StringType(), False),
            StructField("name", StringType(), False),
            StructField("ts_ms", LongType(), False),
            StructField("snapshot", StringType(), True),
            StructField("db", StringType(), False),
            StructField("sequence", StringType(), True),
            StructField("schema", StringType(), False),
            StructField("table", StringType(), False),
            StructField("txId", LongType(), True),
            StructField("lsn", LongType(), True),
            StructField("xmin", LongType(), True)
        ]), False),
        StructField("op", StringType(), False),
        StructField("ts_ms", LongType(), True),
        StructField("transaction", StructType([
            StructField("id", StringType(), False),
            StructField("total_order", LongType(), False),
            StructField("data_collection_order", LongType(), False)
        ]), True)
    ]), False),
    StructField("payload", StructType([
        StructField("before", StructType([
            StructField("id", StringType(), True),
            StructField("nome", StringType(), True),
            StructField("sobrenome", StringType(), True),
            StructField("idade", IntegerType(), True),
            StructField("telefone", StringType(), True),
            StructField("email", StringType(), True),
            StructField("created_at", LongType(), True),
            StructField("updated_at", LongType(), True)
        ]), True),
        StructField("after", StructType([
            StructField("id", StringType(), True),
            StructField("nome", StringType(), True),
            StructField("sobrenome", StringType(), True),
            StructField("idade", IntegerType(), True),
            StructField("telefone", StringType(), True),
            StructField("email", StringType(), True),
            StructField("created_at", LongType(), True),
            StructField("updated_at", LongType(), True)
        ]), True),
        StructField("source", StructType([
            StructField("version", StringType(), False),
            StructField("connector", StringType(), False),
            StructField("name", StringType(), False),
            StructField("ts_ms", LongType(), False),
            StructField("snapshot", StringType(), True),
            StructField("db", StringType(), False),
            StructField("sequence", StringType(), True),
            StructField("schema", StringType(), False),
            StructField("table", StringType(), False),
            StructField("txId", LongType(), True),
            StructField("lsn", LongType(), True),
            StructField("xmin", LongType(), True)
        ]), False),
        StructField("op", StringType(), False),
        StructField("ts_ms", LongType(), True),
        StructField("transaction", StructType([
            StructField("id", StringType(), False),
            StructField("total_order", LongType(), False),
            StructField("data_collection_order", LongType(), False)
        ]), True)
    ]), False)
])


payload_schema = StructType(
    [
        StructField("after", StructType([
            StructField("id", StringType(), True),
            StructField("nome", StringType(), True),
            StructField("sobrenome", StringType(), True),
            StructField("idade", IntegerType(), True),
            StructField("telefone", StringType(), True),
            StructField("email", StringType(), True),
            StructField("created_at", LongType(), True),
            StructField("updated_at", LongType(), True)
        ]), True),
        StructField("source", StructType([
            StructField("version", StringType(), False),
            StructField("connector", StringType(), False),
            StructField("name", StringType(), False),
            StructField("ts_ms", LongType(), False),
            StructField("snapshot", StringType(), True),
            StructField("db", StringType(), False),
            StructField("sequence", StringType(), True),
            StructField("schema", StringType(), False),
            StructField("table", StringType(), False),
            StructField("txId", LongType(), True),
            StructField("lsn", LongType(), True),
            StructField("xmin", LongType(), True)
        ]), False),
        StructField("op", StringType(), False),
        StructField("ts_ms", LongType(), True)
    ]
)


###### QUERY PRINT CONSOLE

# kafka_stream_df = spark \
#   .readStream \
#   .format("kafka") \
#   .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
#   .option("subscribe",kafka_topic) \
#   .load() \
#   .selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
#   .writeStream \
#   .option("truncate", "false") \
#   .format("console") \
#   .trigger(continuous="1 second") \
#   .start() \
#   .awaitTermination()

#.select("after.id, after.nome, after.sobrenome, after.idade, after.telefone, after.email, after.created_at, after.updated_at , op, ts_ms") \


# kafka_stream_df = spark \
#   .readStream \
#   .format("kafka") \
#   .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
#   .option("subscribe",kafka_topic) \
#   .load() \
#   .selectExpr("CAST(value AS STRING) as value_string") \
#   .select(from_json("value_string", schema).alias("value_struct")) \
#   .select(
#       "value_struct.payload.after.id",
#        "value_struct.payload.after.nome",
#        "value_struct.payload.after.sobrenome",
#        "value_struct.payload.after.idade",
#        "value_struct.payload.after.telefone",
#        "value_struct.payload.after.email",
#        "value_struct.payload.after.created_at",
#        "value_struct.payload.after.updated_at",
#        "value_struct.payload.op",
#        "value_struct.payload.ts_ms"
#   ) \
#   .withColumn("ts_unix", col("ts_ms") / 1000) \
#   .withColumn("year", year(from_unixtime("ts_unix"))) \
#   .withColumn("month", month(from_unixtime("ts_unix"))) \
#   .withColumn("day", dayofmonth(from_unixtime("ts_unix"))) \
#   .writeStream \
#   .option("truncate", "false") \
#   .format("console") \
#   .trigger(continuous="2 seconds") \
#   .start() \
#   .awaitTermination()


delete_statement = f"""
    DELETE FROM usuarios
    WHERE op = 'd'
"""

# ##### QUERY WRITE MINIO
kafka_stream_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe",kafka_topic) \
    .option("failOnDataLoss", False) \
    .load() \
    .selectExpr("CAST(value AS STRING) as value_string") \
    .select(from_json("value_string", schema).alias("value_struct")) \
    .select(
      "value_struct.payload.after.id",
       "value_struct.payload.after.nome",
       "value_struct.payload.after.sobrenome",
       "value_struct.payload.after.idade",
       "value_struct.payload.after.telefone",
       "value_struct.payload.after.email",
       "value_struct.payload.after.created_at",
       "value_struct.payload.after.updated_at",
       "value_struct.payload.op",
       "value_struct.payload.ts_ms"
    ) \
    .withColumn("ts_unix", col("ts_ms") / 1000) \
    .withColumn("year", year(from_unixtime("ts_unix"))) \
    .withColumn("month", month(from_unixtime("ts_unix"))) \
    .withColumn("day", dayofmonth(from_unixtime("ts_unix"))) \
    .writeStream \
    .format("hudi") \
    .trigger(processingTime="2 seconds") \
    .option("checkpointLocation", checkpoint_location) \
    .option("hoodie.table.name", "usuarios") \
    .option("hoodie.datasource.write.recordkey.field", "id") \
    .option("hoodie.datasource.write.partitionpath.field", "year,month,day") \
    .option("hoodie.datasource.write.precombine.field", "ts_ms") \
    .option("hoodie.datasource.write.operation", "upsert") \
    .option("path", f's3a://{minio_bucket}/{minio_path}') \
    .outputMode("append") \
    .start() \
    .awaitTermination()

    