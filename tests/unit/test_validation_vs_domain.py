import pytest
from pyspark.sql import Row
from pyspark.sql.types import DoubleType, StructField, StructType

from data_transformations.citibike.domain import Trip
from data_transformations.citibike.validation import add_trip_validity_column

# Define explicit schema for DataFrames to handle None values
TRIP_SCHEMA = StructType([
    StructField("start_station_latitude", DoubleType(), True),
    StructField("start_station_longitude", DoubleType(), True),
    StructField("end_station_latitude", DoubleType(), True),
    StructField("end_station_longitude", DoubleType(), True),
])


def build_trip_row(start_lat, start_lon, end_lat, end_lon):
    return Row(
        start_station_latitude=start_lat,
        start_station_longitude=start_lon,
        end_station_latitude=end_lat,
        end_station_longitude=end_lon,
    )


@pytest.mark.parametrize(
    "start_lat,start_lon,end_lat,end_lon",
    [
        (40.0, -73.0, 40.001, -73.001),  # valid, small distance
        (40.0, -73.0, 40.0, -73.0),      # same point -> valid, distance 0
        (None, -73.0, 40.0, -73.0),      # missing start lat -> invalid
        (95.0, -73.0, 40.0, -73.0),      # start lat out of range -> invalid
        (40.0, -200.0, 40.0, -73.0),     # start lon out of range -> invalid
        (40.0, -73.0, None, None),       # missing end coords -> invalid
    ],
)
def test_spark_validation_matches_domain(spark, start_lat, start_lon, end_lat, end_lon):
    """
    For each sample row, compare the boolean result from the Spark expression
    with the Trip.is_valid() domain implementation.
    """
    rows = [build_trip_row(start_lat, start_lon, end_lat, end_lon)]
    df = spark.createDataFrame(rows, schema=TRIP_SCHEMA)

    df_with_flag = add_trip_validity_column(df, col_name="trip_is_valid")
    collected = df_with_flag.collect()

    assert len(collected) == 1
    row = collected[0].asDict()

    # Domain-level validation using the Trip dataclass
    trip = Trip(
        start_station_latitude=row.get("start_station_latitude"),
        start_station_longitude=row.get("start_station_longitude"),
        end_station_latitude=row.get("end_station_latitude"),
        end_station_longitude=row.get("end_station_longitude"),
    )
    domain_valid = trip.is_valid()

    # Spark-side validation (coalesced to False by helper) should be boolean
    spark_valid = bool(row.get("trip_is_valid"))

    assert spark_valid == domain_valid, f"Mismatch for row {row}: spark={spark_valid}, domain={domain_valid}"
