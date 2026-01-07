import logging

from pyspark.sql import SparkSession
from pyspark.sql.functions import split, explode, regexp_replace, trim, lower, col

def word_tokenizer(dataframe):
    return (dataframe
        .withColumn("word", explode(split(dataframe.columns[0], r"\s+")))
        .withColumn("word", lower(trim(regexp_replace("word", r"^[^\w']+|[^\w']+$", ""))))
        .withColumn("word", explode(split("word", "--")))
        .filter(col("word") != "")
        .select("word"))

def run(spark: SparkSession, input_path: str, output_path: str) -> None:
    logging.info("Reading text file from: %s", input_path)
    input_df = spark.read.text(input_path)

    logging.info("Tokenizing words")
    tokenized_df = word_tokenizer(input_df)
    logging.info("Counting words")
    tokenized_df = (tokenized_df
        .groupBy("word")
        .count()
        .orderBy("word"))

    logging.info("Writing csv to directory: %s", output_path)

    tokenized_df.coalesce(1).write.csv(output_path, header=True)
