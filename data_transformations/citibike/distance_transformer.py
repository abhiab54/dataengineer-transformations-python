from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import StructType, StructField, DoubleType, StringType
from pyspark.sql import functions as F
import math



METERS_PER_FOOT = 0.3048
FEET_PER_MILE = 5280
EARTH_RADIUS_IN_METERS = 6371e3  # 6,371,000 meters
METERS_PER_MILE = METERS_PER_FOOT * FEET_PER_MILE
EARTH_RADIUS_IN_KM =  EARTH_RADIUS_IN_METERS / 1000
EARTH_RADIUS_IN_MILES = EARTH_RADIUS_IN_METERS / METERS_PER_MILE

def haversine(lat1, lon1, lat2, lon2):
    
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    return EARTH_RADIUS_IN_MILES * c

haversine_udf = F.udf(haversine, DoubleType())

def compute_distance(_spark: SparkSession, dataframe: DataFrame) -> DataFrame:
    df = dataframe.withColumn(
    "distance",
    F.round(haversine_udf(
        F.col("start_station_latitude"),
        F.col("start_station_longitude"),
        F.col("end_station_latitude"),
        F.col("end_station_longitude")
    ), 2))


    return df


def run(
    spark: SparkSession, input_dataset_path: str, transformed_dataset_path: str
) -> None:
    input_dataset = spark.read.parquet(input_dataset_path)
    input_dataset.show()

    dataset_with_distances = compute_distance(spark, input_dataset)
    dataset_with_distances.show()

    dataset_with_distances.write.parquet(transformed_dataset_path, mode="append")
