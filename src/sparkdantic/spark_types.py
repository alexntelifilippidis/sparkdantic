from typing import Any
from pydantic_core import core_schema


class Long(int):
    """
    Spark LongType: 64-bit signed integer for Spark DataFrames.
    """

    def __new__(cls, value=0):
        return super().__new__(cls, value)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler
    ) -> core_schema.CoreSchema:
        return core_schema.int_schema()


# Create lowercase alias
long = Long

__all__ = ["long"]
