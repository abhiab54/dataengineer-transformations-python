from pyspark.sql import DataFrame, SparkSession
from typing import List

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType

METERS_PER_FOOT = 0.3048
FEET_PER_MILE = 5280
EARTH_RADIUS_IN_METERS = 6371e3
METERS_PER_MILE = METERS_PER_FOOT * FEET_PER_MILE
EARTH_RADIUS_MILES = EARTH_RADIUS_IN_METERS / METERS_PER_MILE


def compute_distance(_spark: SparkSession, dataframe: DataFrame) -> DataFrame:
    """
    Add a 'distance_miles' column to the dataframe using the Haversine formula.
    Uses Spark SQL functions (no Python UDF) for performance.
    Raises ValueError if required columns are missing.
    """
    required = [
        "start_station_latitude",
        "start_station_longitude",
        "end_station_latitude",
        "end_station_longitude",
    ]
    missing = [c for c in required if c not in dataframe.columns]
    if missing:
        raise ValueError(f"Missing required columns for distance computation: {missing}")

    # Ensure numeric types
    df = dataframe
    for col in required:
        df = df.withColumn(col, F.col(col).cast(DoubleType()))

    # Convert degrees to radians
    lat1 = F.radians(F.col("start_station_latitude"))
    lon1 = F.radians(F.col("start_station_longitude"))
    lat2 = F.radians(F.col("end_station_latitude"))
    lon2 = F.radians(F.col("end_station_longitude"))

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = F.sin(dlat / 2) * F.sin(dlat / 2) + F.cos(lat1) * F.cos(lat2) * F.sin(dlon / 2) * F.sin(dlon / 2)
    c = 2 * F.atan2(F.sqrt(a), F.sqrt(1 - a))

    distance_miles = F.lit(EARTH_RADIUS_MILES) * c

    # Round to 2 decimals and handle null inputs by leaving distance null
    return df.withColumn("distance", F.round(distance_miles, 2))


def run(
    spark: SparkSession, input_dataset_path: str, transformed_dataset_path: str
) -> None:
    input_dataset = spark.read.parquet(input_dataset_path)
    # input_dataset.show()

    dataset_with_distances = compute_distance(spark, input_dataset)
    # dataset_with_distances.show()

    dataset_with_distances.write.parquet(transformed_dataset_path, mode="append")
