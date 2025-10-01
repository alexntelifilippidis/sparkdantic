Welcome to SparkDantic Documentation
=====================================

**SparkDantic** is a Python library that bridges Pydantic models with Apache Spark DataFrames, providing seamless data validation and type conversion for big data applications.

✨ **Key Features**
-------------------

- 🔄 **Automatic Schema Conversion**: Convert Pydantic models to Spark schemas effortlessly
- 📊 **DataFrame Creation**: Create typed Spark DataFrames from your data
- 🎨 **Colored Logging**: Beautiful, emoji-rich logging for better debugging
- 🔍 **Type Safety**: Leverage Pydantic's validation with Spark's distributed computing
- 🚀 **Easy Integration**: Drop-in replacement for manual schema definitions

📚 **Quick Start**
------------------

Installation:

.. code-block:: bash

   pip install sparkdantic

Basic usage:

.. code-block:: python

   from pydantic import BaseModel
   from sparkdantic import SparkModel
   from pyspark.sql import SparkSession

   class UserModel(SparkModel):
       name: str
       age: int
       is_active: bool

   # Create Spark session
   spark = SparkSession.builder.appName("SparkDantic").getOrCreate()

   # Create DataFrame with automatic schema
   data = [
       {"name": "Alice", "age": 30, "is_active": True},
       {"name": "Bob", "age": 25, "is_active": False}
   ]

   df = UserModel.create_spark_dataframe(spark, data)
   df.show()

📖 **Documentation Sections**
-----------------------------

.. toctree::
   :maxdepth: 2
   :caption: Library Reference:

   api/models
   api/logger
   api/spark_types

.. toctree::
   :maxdepth: 1
   :caption: Examples:

   examples/basic_usage
   examples/advanced_features

🔗 **External Links**
---------------------

- `GitHub Repository <https://github.com/alexntelifilippidis/sparkdantic>`_
- `Issue Tracker <https://github.com/alexntelifilippidis/sparkdantic/issues>`_

📇 **Indices and Tables**
=========================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
