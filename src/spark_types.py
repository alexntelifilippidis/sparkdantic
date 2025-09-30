from typing import Any
from pydantic_core import core_schema


class long(int):
    """
    Spark LongType: 64-bit signed integer for Spark DataFrames.

    Convert a number to a long integer for Spark operations.
    Represents Spark's LongType and provides type safety to distinguish
    from regular Python integers in DataFrame operations.
    """

    def __new__(cls, value=0):
        return super().__new__(cls, value)

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler) -> core_schema.CoreSchema:
        return core_schema.int_schema()


__all__ = ['long']
