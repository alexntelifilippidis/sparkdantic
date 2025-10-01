"""
SparkDantic: Bridge Pydantic models with Apache Spark DataFrames.

This library provides seamless integration between Pydantic's data validation
and Apache Spark's distributed computing capabilities.
"""

from .models import SparkModel
from .spark_types import long

__version__ = "0.1.0"
__all__ = ["SparkModel", "long"]
