Models Module
=============

.. automodule:: sparkdantic.models
   :members:
   :undoc-members:
   :show-inheritance:
   :no-index:


Core Classes
------------

SparkModel
~~~~~~~~~~

The ``SparkModel`` class is the heart of SparkDantic, extending Pydantic's ``BaseModel`` to provide Spark integration capabilities.

**Key Methods:**

- ``create_spark_schema()``: Converts the Pydantic model to a Spark StructType
- ``create_spark_dataframe()``: Creates a Spark DataFrame with the model's schema
- ``log_schema_info()``: Logs detailed information about the generated schema

**Usage Example:**

.. code-block:: python

   from sparkdantic import SparkModel

   class Product(SparkModel):
       id: int
       name: str
       price: float
       in_stock: bool

   # Generate Spark schema
   schema = Product.create_spark_schema()

   # Create DataFrame
   data = [{"id": 1, "name": "Widget", "price": 19.99, "in_stock": True}]
   df = Product.create_spark_dataframe(spark, data)

**Type Mapping:**

The following Python types are automatically mapped to Spark types:

- ``str`` → ``StringType()``
- ``int`` → ``IntegerType()``
- ``float`` → ``FloatType()``
- ``bool`` → ``BooleanType()``
- ``long`` → ``LongType()``
- Nested Pydantic models → ``StringType()`` (serialized)
