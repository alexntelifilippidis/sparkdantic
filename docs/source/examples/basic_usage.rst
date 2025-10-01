Basic Usage Examples
====================

This section demonstrates the fundamental usage patterns of SparkDantic.

Simple Model Definition
-----------------------

.. code-block:: python

   from sparkdantic import SparkModel

   class User(SparkModel):
       name: str
       age: int
       email: str
       is_active: bool

Creating DataFrames
-------------------

.. code-block:: python

   from pyspark.sql import SparkSession

   # Initialize Spark
   spark = SparkSession.builder.appName("SparkDantic Example").getOrCreate()

   # Sample data
   users_data = [
       {"name": "Alice", "age": 30, "email": "alice@example.com", "is_active": True},
       {"name": "Bob", "age": 25, "email": "bob@example.com", "is_active": False},
       {"name": "Charlie", "age": 35, "email": "charlie@example.com", "is_active": True}
   ]

   # Create DataFrame with automatic schema
   df = User.create_spark_dataframe(spark, users_data)

   # Show the DataFrame
   df.show()

   # Print the schema
   df.printSchema()

Schema Generation
-----------------

.. code-block:: python

   # Generate just the schema
   schema = User.create_spark_schema()
   print(schema)

   # Log detailed schema information
   User.log_schema_info(schema)
