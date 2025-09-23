
import pytest
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark():
    """Create Spark session for testing."""
    spark = (
        SparkSession.builder.appName("SparkModelTests")
        .master("local[*]")
        .config("spark.sql.adaptive.enabled", "false")
        .getOrCreate()
    )
    yield spark
    spark.stop()
