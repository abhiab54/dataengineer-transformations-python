import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark_session() -> SparkSession:
    print(">>> [TEST STARTUP] Creating SparkSession")   # startup message
    spark = (
        SparkSession.builder
        .master("local[2]")
        .appName("pytest")
        .config("spark.ui.enabled", "false")
        .getOrCreate()
    )
    yield spark
    # teardown
    print(">>> [TEST TEARDOWN] Stopping SparkSession")
    spark.stop()
