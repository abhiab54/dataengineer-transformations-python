import pytest
from pyspark.sql import SparkSession

import logging
logger = logging.getLogger(__name__)

@pytest.fixture(scope="session")
def spark_session() -> SparkSession:
    logger.info(">>> [TEST STARTUP] Creating SparkSession")   # startup message
    spark = (
        SparkSession.builder
        .master("local[2]")
        .appName("pytest")
        .config("spark.ui.enabled", "false")
        .getOrCreate()
    )
    yield spark
    # teardown
    logger.info(">>> [TEST TEARDOWN] Stopping SparkSession")
    spark.stop()
