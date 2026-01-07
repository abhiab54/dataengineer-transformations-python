from typing import List

from pyspark.sql import Column, DataFrame
from pyspark.sql import functions as F

# Reuse the same coordinate names used across the codebase
REQUIRED_COORDS: List[str] = [
    "start_station_latitude",
    "start_station_longitude",
    "end_station_latitude",
    "end_station_longitude",
]


def trip_is_valid_expr() -> Column:
    """
    Returns a Spark Column (boolean expression) that is True when:
      - All four coordinate columns are non-null
      - Latitudes are in [-90, 90]
      - Longitudes are in [-180, 180]
    The expression itself may evaluate to NULL for rows with NULL inputs; callers
    may want to coalesce to False if a strict boolean is required.
    """
    return (
        F.col("start_station_latitude").isNotNull()
        & F.col("start_station_longitude").isNotNull()
        & F.col("end_station_latitude").isNotNull()
        & F.col("end_station_longitude").isNotNull()
        & F.col("start_station_latitude").between(-90.0, 90.0)
        & F.col("end_station_latitude").between(-90.0, 90.0)
        & F.col("start_station_longitude").between(-180.0, 180.0)
        & F.col("end_station_longitude").between(-180.0, 180.0)
    )


def add_trip_validity_column(df: DataFrame, col_name: str = "trip_is_valid") -> DataFrame:
    """
    Returns a new DataFrame with a boolean column named `col_name` indicating validity.
    Uses coalesce(..., False) so the column is always boolean (no NULLs).
    """
    expr = trip_is_valid_expr()
    return df.withColumn(col_name, F.coalesce(expr, F.lit(False)))
