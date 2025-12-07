from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

spark = SparkSession.builder.appName("NewsStreamingConsumer") \
    .config("spark.sql.shuffle.partitions", "2") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")


raw_df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "DonaldTrump") \
    .option("startingOffsets", "latest") \
    .load()


string_df = raw_df.selectExpr("CAST(value AS STRING) as value")


split_df = string_df.select(
    split(col("value"), "\|").getItem(0).alias("source"),
    split(col("value"), "\|").getItem(1).alias("author"),
    split(col("value"), "\|").getItem(2).alias("description"),
    split(col("value"), "\|").getItem(3).alias("urlToImage"),
    split(col("value"), "\|").getItem(4).alias("content"),
    current_timestamp().alias("timestamp")
)


aggregated_df = split_df \
    .withWatermark("timestamp", "1 minute") \
    .groupBy(window(col("timestamp"), "1 minute"),col("source")).count()


query = aggregated_df.select(col("window").start.alias("window_start"),
        col("window").end.alias("window_end"),
        col("source"),
        col("count")) \
    .writeStream \
    .outputMode("append") \
    .format("csv") \
    .option("path", "/BigData/news_data/") \
    .option("checkpointLocation", "/BigData/news_checkpoint") \
    .start()

query.awaitTermination()

