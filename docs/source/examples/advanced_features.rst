Advanced Features
=================

Working with Custom Types
--------------------------

.. code-block:: python

   from sparkdantic import SparkModel
   from sparkdantic.spark_types import long

   class Transaction(SparkModel):
       transaction_id: long  # 64-bit integer
       user_id: int
       amount: float
       timestamp: long
       description: str

Nested Models
-------------

.. code-block:: python

   class Address(SparkModel):
       street: str
       city: str
       zipcode: str

   class UserWithAddress(SparkModel):
       name: str
       age: int
       address: Address  # Nested model (serialized as string in Spark)

Custom Logging
--------------

.. code-block:: python

   from sparkdantic.logger import SparkModelLogger

   # Create custom logger
   logger = SparkModelLogger.get_logger("DataProcessor")

   logger.info("Starting data processing...")
   logger.warning("Memory usage is high")
   logger.error("Failed to process batch")

Handling Large Datasets
------------------------

.. code-block:: python

   # For large datasets, consider partitioning
   large_data = [{"id": i, "value": f"item_{i}"} for i in range(1000000)]

   # Create DataFrame
   df = MyModel.create_spark_dataframe(spark, large_data)

   # Repartition for better performance
   df_partitioned = df.repartition(10)

   # Write to storage
   df_partitioned.write.parquet("output/large_dataset")
