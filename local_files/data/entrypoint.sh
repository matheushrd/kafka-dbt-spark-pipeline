#!/bin/bash


cd ../../../ && ls && chmod 777 data/*

sleep 5

spark-submit --master spark://spark-master:7077 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2,org.apache.hudi:hudi-spark3.3-bundle_2.12:0.12.0,org.apache.hadoop:hadoop-aws:3.2.0,com.amazonaws:aws-java-sdk:1.12.426  --class org.apache.hudi.utilities.streamer.HoodieStreamer --conf "spark.serializer=org.apache.spark.serializer.KryoSerializer" --conf 'spark.sql.catalog.spark_catalog=org.apache.spark.sql.hudi.catalog.HoodieCatalog' --conf 'spark.sql.extensions=org.apache.spark.sql.hudi.HoodieSparkSessionExtension' --conf "spark.sql.hive.convertMetastoreParquet=false" --conf spark.driver.extraJavaOptions="-Divy.cache.dir=/tmp -Divy.home=/tmp" --conf "spark.executor.extraJavaOptions='-Dlog4j.configuration=log4j.properties'" --conf 'spark.hadoop.fs.s3a.access.key=5T4gRXIIeRDm0sf6tyel' --conf 'spark.hadoop.fs.s3a.secret.key=6FKOQXb45ft5XwCAtdKUfhE53BxUCw1Cf2CaZCg6' --conf 'spark.hadoop.fs.s3a.endpoint=http://172.18.0.8:9000' --conf 'spark.hadoop.fs.s3a.path.style.access=true' --conf 'fs.s3a.signing-algorithm=S3SignerType' --conf "fs.s3a.multipart.size=104857600" --driver-memory 1G --executor-memory 2G /data/stream.py
