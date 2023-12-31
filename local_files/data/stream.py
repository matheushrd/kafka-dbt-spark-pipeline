from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
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
minio_endpoint = "http://172.18.0.7:9000"  # Use the MinIO container's IP and port
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
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .config("spark.sql.hive.convertMetastoreParquet", "false") \
    .config("spark.hadoop.fs.s3a.multipart.size", "104857600") \
    .config("spark.sql.streaming.checkpointLocation", checkpoint_location) \
    .getOrCreate()

# Define the schema for the incoming Kafka messages
print("Spark Sartted")
# Define the schema for the message
schema = StructType([
    StructField("schema", StructType([
        StructField("type", StringType(), False),
        StructField("fields", StructType([
            StructField("before", StructType([
                StructField("id", StringType(), False),
                StructField("nome", StringType(), True),
                StructField("sobrenome", StringType(), True),
                StructField("idade", IntegerType(), True),
                StructField("telefone", StringType(), True),
                StructField("email", StringType(), True),
                StructField("created_at", LongType(), True),
                StructField("updated_at", LongType(), True),
            ]), True),
            StructField("after", StructType([
                StructField("id", StringType(), False),
                StructField("nome", StringType(), True),
                StructField("sobrenome", StringType(), True),
                StructField("idade", IntegerType(), True),
                StructField("telefone", StringType(), True),
                StructField("email", StringType(), True),
                StructField("created_at", LongType(), True),
                StructField("updated_at", LongType(), True),
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
                StructField("xmin", LongType(), True),
            ]), False),
            StructField("op", StringType(), False),
            StructField("ts_ms", LongType(), True),
            StructField("transaction", StructType([
                StructField("id", StringType(), False),
                StructField("total_order", LongType(), False),
                StructField("data_collection_order", LongType(), False),
            ]), True),
        ]), False),
        StructField("optional", BooleanType(), False),
        StructField("name", StringType(), False),
    ]), False),
    StructField("payload", StructType([
        StructField("before", StructType([
            StructField("id", StringType(), False),
            StructField("nome", StringType(), True),
            StructField("sobrenome", StringType(), True),
            StructField("idade", IntegerType(), True),
            StructField("telefone", StringType(), True),
            StructField("email", StringType(), True),
            StructField("created_at", LongType(), True),
            StructField("updated_at", LongType(), True),
        ]), True),
        StructField("after", StructType([
            StructField("id", StringType(), False),
            StructField("nome", StringType(), True),
            StructField("sobrenome", StringType(), True),
            StructField("idade", IntegerType(), True),
            StructField("telefone", StringType(), True),
            StructField("email", StringType(), True),
            StructField("created_at", LongType(), True),
            StructField("updated_at", LongType(), True),
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
            StructField("xmin", LongType(), True),
        ]), False),
        StructField("op", StringType(), False),
        StructField("ts_ms", LongType(), True),
        StructField("transaction", StructType([
            StructField("id", StringType(), False),
            StructField("total_order", LongType(), False),
            StructField("data_collection_order", LongType(), False),
        ]), True),
    ]), False),
])
# Create a Kafka DataFrame

kafka_schema = StructType([
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
])

kafka_stream_df = spark\
      .readStream \
      .format("kafka") \
      .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
      .option("subscribe", kafka_topic) \
      .option("startingOffsets", "earliest") \
      .load()


# query = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
#     .writeStream \
#     .format("console") \
#     .option("checkpointLocation", checkpoint_location) \
#     .start()

# query.awaitTermination()
(kafka_stream_df.printSchema)

# Extract the JSON payload as a map
json_data = kafka_stream_df.select(from_json(col("value").cast("string"), generic_schema).alias("data")).select("data.json")



minio_write_query = (
    json_data 
    .writeStream
    .format("hudi")
    .outputMode("append")
    .option("hoodie.table.name", "usuarios")
    .option("hoodie.datasource.write.recordkey.field", "id")
    .option("hoodie.datasource.write.partitionpath.field", "ts")
    .option("hoodie.datasource.write.precombine.field", "timestamp")
    .option("hoodie.datasource.write.operation", "upsert")
    .option("checkpointLocation", checkpoint_location)
    .option("newRows", 10)
    .option("endpoint", minio_endpoint)
    .option("accessKey", minio_access_key)
    .option("secretKey", minio_secret_key)
    .option("bucket", minio_bucket)
    .option("path", minio_path)
    .start()
)

minio_write_query.awaitTermination()
