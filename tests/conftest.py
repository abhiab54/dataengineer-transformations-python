import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark() -> SparkSession:
    """Session-scoped Spark fixture for unit tests."""
    return SparkSession.builder.appName("UnitTests").getOrCreate()
