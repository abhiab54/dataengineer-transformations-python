import logging

from pyspark.sql import DataFrame
from pyspark.sql.functions import split, explode, lower, regexp_replace, col
from pyspark.sql import SparkSession


def run(spark: SparkSession, input_path: str, output_path: str) -> None:
    logging.info("Reading text file from: %s", input_path)
    input_df = spark.read.text(input_path)
    logging.info("Calculating word counts")

    words_df = (
        input_df
        # split into array of words
        .withColumn("word", explode(split(col("value"), "\\s+")))
        # clean punctuation + lowercase
        .withColumn("word", lower(regexp_replace(col("word"), r"(^\W+|\W+$)", "")))
        .withColumn("word", explode(split(col("word"), "--")))
        .filter(col("word") != "")
    )

    word_count_df = words_df.groupBy("word").count().orderBy("word")

    logging.info("Writing csv to directory: %s", output_path)

    word_count_df.coalesce(1).write.csv(output_path, header=True)
