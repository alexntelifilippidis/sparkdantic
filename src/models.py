from pydantic import BaseModel
from typing import Any, List, Dict, Union, Type
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    FloatType,
    BooleanType,
    DataType,
)

from src.logger import SparkModelLogger


class SparkModel(BaseModel):
    """Base model for converting Pydantic models to Spark schemas.

    This class extends Pydantic's BaseModel to provide functionality for
    converting Pydantic model definitions to Apache Spark schemas and
    creating Spark DataFrames with proper type mapping.

    :cvar _logger: Class-specific logger instance
    :vartype _logger: logging.Logger

    . note::
       Each subclass automatically gets its own logger instance named "SparkDantic".

    . code-block:: python

       class UserModel(SparkModel):
           name: str
           age: int

       schema = UserModel.create_spark_schema()
       df = UserModel.create_spark_dataframe(spark, [{"name": "John", "age": 30}])
    """

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Initialize subclass with dedicated logger.

        :param kwargs: Additional keyword arguments passed to parent class
        :type kwargs: Any
        :return: None
        :rtype: None
        """
        super().__init_subclass__(**kwargs)
        # Create a logger for each subclass
        cls._logger = SparkModelLogger.get_logger(name="SparkDantic")

    @classmethod
    def create_spark_schema(cls) -> StructType:
        """Convert Pydantic model to Spark StructType schema.

        Analyzes the Pydantic model fields and their type annotations
        to create a corresponding Spark schema with proper data types.

        :return: Spark StructType schema representing the model
        :rtype: StructType

        . note::
           All fields are created as nullable (True) by default.

        . code-block:: python

           class Person(SparkModel):
               name: str
               age: int

           schema = Person.create_spark_schema()
           print(schema)
        """
        logger = getattr(cls, "_logger", SparkModelLogger.get_logger())

        logger.info(f"🔄 Converting {cls.__name__} to Spark schema...")

        fields = []
        for field_name, field_info in cls.model_fields.items():
            spark_type = cls._pydantic_to_spark_type(field_info.annotation)
            fields.append(StructField(field_name, spark_type, True))
            logger.debug(
                f"Mapped field '{field_name}': {field_info.annotation.__name__} -> {type(spark_type).__name__}"
            )

        schema = StructType(fields)
        logger.info(f"✅ Successfully created schema with {len(fields)} fields")

        return schema

    @classmethod
    def create_spark_dataframe(
        cls,
        spark: SparkSession,
        data: Union[
            List[Union[Dict[str, Any], tuple, List[Any]]],
            Dict[str, Any],
            tuple,
            List[Any],
        ],
    ) -> DataFrame:
        """Create Spark DataFrame from data using the model's schema.

        Converts input data to a Spark DataFrame using the schema derived
        from the Pydantic model. Handles various input formats including
        dictionaries, tuples, and lists.

        :param spark: Active Spark session for DataFrame creation
        :type spark: SparkSession
        :param data: Input data in various supported formats
        :type data: Union[List[Union[Dict[str, Any], tuple, List[Any]]], Dict[str, Any], tuple, List[Any]]
        :return: Spark DataFrame with the model's schema and provided data
        :rtype: DataFrame

        . note::
           Single items are automatically wrapped in a list.
           Empty data returns an empty DataFrame with the correct schema.

        . warning::
           Complex nested structures are converted to string representations
           for compatibility with Spark.

        . code-block:: python

           class User(SparkModel):
               name: str
               age: int

           data = [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}]
           df = User.create_spark_dataframe(spark, data)
        """
        logger = getattr(cls, "_logger", SparkModelLogger.get_logger())

        # Handle single item data by wrapping in list
        if not isinstance(data, list):
            data = [data]
            logger.debug("Wrapped single item in list")

        if not data:
            logger.warning("⚠️ No data provided. Returning an empty DataFrame.")
            schema = cls.create_spark_schema()
            return spark.createDataFrame([], schema)

        logger.info(
            f"📊 Creating DataFrame for {cls.__name__} with {len(data)} rows..."
        )

        # Get the schema
        schema = cls.create_spark_schema()

        # Convert data if needed
        if isinstance(data[0], dict):
            # Convert dict data to tuples in field order
            field_names = [field.name for field in schema.fields]
            data = [
                tuple(row.get(field_name) for field_name in field_names) for row in data
            ]
            logger.debug(f"Converted {len(data)} dictionary rows to tuples")

        # Process complex nested structures
        processed_data = []
        for row in data:
            if isinstance(row, (list, tuple)):
                processed_row = []
                for item in row:
                    if isinstance(item, (tuple, dict, list)):
                        # Convert complex structures to string representation
                        processed_row.append(str(item))
                    else:
                        # Keep simple types as-is
                        processed_row.append(item)
                processed_data.append(tuple(processed_row))
            else:
                processed_data.append(row)

        # Create DataFrame
        df = spark.createDataFrame(processed_data, schema)
        logger.info(f"✅ Successfully created DataFrame with schema: {cls.__name__}")

        return df

    @staticmethod
    def _pydantic_to_spark_type(pydantic_type: Type[Any]) -> DataType:
        """Map Pydantic types to Spark types.

        Converts Python/Pydantic type annotations to corresponding
        Spark SQL data types with fallback to StringType for unknown types.

        :param pydantic_type: Python type annotation from Pydantic field
        :type pydantic_type: Type[Any]
        :return: Corresponding Spark SQL data type
        :rtype: DataType

        . note::
           Unknown types default to StringType with a warning logged.

        . code-block:: python

           spark_type = SparkModel._pydantic_to_spark_type(int)
           print(type(spark_type).__name__)  # IntegerType
        """
        logger = SparkModelLogger.get_logger()

        type_mapping: Dict[Type[Any], DataType] = {
            str: StringType(),
            int: IntegerType(),
            float: FloatType(),
            bool: BooleanType(),
        }

        spark_type = type_mapping.get(pydantic_type, StringType())

        if pydantic_type not in type_mapping:
            logger.warning(f"Unknown type {pydantic_type}, defaulting to StringType")

        return spark_type

    @classmethod
    def log_schema_info(cls, schema: StructType) -> None:
        """Log detailed schema information.

        Provides comprehensive logging of schema structure including
        field names, data types, and nullability information.

        :param schema: Spark schema to log information about
        :type schema: StructType
        :return: None
        :rtype: None

        . code-block:: python

           schema = UserModel.create_spark_schema()
           UserModel.log_schema_info(schema)
        """
        logger = getattr(cls, "_logger", SparkModelLogger.get_logger())

        logger.info("📋 Schema Details:")
        for field in schema.fields:
            logger.info(
                f"  🔹 {field.name}: {type(field.dataType).__name__} (nullable: {field.nullable})"
            )
