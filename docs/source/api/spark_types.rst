Spark Types Module
==================

.. automodule:: src.spark_types
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:

Custom Type Definitions
-----------------------

Long Type
~~~~~~~~~

The ``Long`` class provides a Pydantic-compatible wrapper for Spark's 64-bit integer type.

**Usage:**

.. code-block:: python

   from sparkdantic import SparkModel
   from sparkdantic.spark_types import long

   class BigDataModel(SparkModel):
       id: long  # Maps to Spark LongType
       timestamp: long
       value: float

**Features:**

- Inherits from Python's ``int`` type
- Provides Pydantic core schema for validation
- Automatically maps to Spark's ``LongType()``
- Available as both ``Long`` (class) and ``long`` (alias)

**Type Conversion:**

When using ``long`` in your Pydantic model fields, SparkDantic automatically:

1. Validates the input as an integer
2. Maps to Spark's ``LongType`` in the schema
3. Handles serialization/deserialization correctly
