import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, LongType, BooleanType

spark = SparkSession.builder.appName("HudiKafkaConsumer").getOrCreate()

spark.stop()