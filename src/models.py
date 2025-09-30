from pydantic import BaseModel
from typing import Any, List, Dict, Union, Type, ClassVar
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    FloatType,
    BooleanType,
    DataType,
    LongType,
)

from src.logger import SparkModelLogger
from src.spark_types import long


class SparkModel(BaseModel):
    """
    Base model for converting Pydantic models to Spark schemas.

    This class extends Pydantic's BaseModel to provide functionality for
    converting Pydantic model definitions to Apache Spark schemas and
    creating Spark DataFrames with proper type mapping.

    :cvar _logger: Class-specific logger instance
    :vartype _logger: logging.Logger
    """

    _logger: ClassVar[Any]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """
        Initialize subclass with dedicated logger.

        :param kwargs: Additional keyword arguments passed to parent class
        :type kwargs: Any
        """
        super().__init_subclass__(**kwargs)
        cls._logger = SparkModelLogger.get_logger(name="SparkDantic")

    @classmethod
    def create_spark_schema(cls) -> StructType:
        """
        Convert Pydantic model to Spark StructType schema.

        :return: Spark StructType schema representing the model
        :rtype: StructType
        """
        logger: Any = getattr(cls, "_logger", SparkModelLogger.get_logger())
        logger.info(f"🔄 Converting {cls.__name__} to Spark schema...")

        fields: list[StructField] = []
        for field_name, field_info in cls.model_fields.items():
            spark_type: DataType = cls._pydantic_to_spark_type(field_info.annotation)
            annotation_name: str = getattr(
                field_info.annotation, "__name__", str(field_info.annotation)
            )
            fields.append(StructField(field_name, spark_type, True))
            logger.debug(
                f"Mapped field '{field_name}': {annotation_name} -> {type(spark_type).__name__}"
            )

        schema: StructType = StructType(fields)
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
        """
        Create Spark DataFrame from data using the model's schema.

        :param spark: Active Spark session for DataFrame creation
        :type spark: SparkSession
        :param data: Input data in various supported formats
        :type data: Union[List[Union[Dict[str, Any], tuple, List[Any]]], Dict[str, Any], tuple, List[Any]]
        :return: Spark DataFrame with the model's schema and provided data
        :rtype: DataFrame
        """
        logger: Any = getattr(cls, "_logger", SparkModelLogger.get_logger())

        if not isinstance(data, list):
            data = [data]
            logger.debug("Wrapped single item in list")

        if not data:
            logger.warning("⚠️ No data provided. Returning an empty DataFrame.")
            empty_schema: StructType = cls.create_spark_schema()
            return spark.createDataFrame([], empty_schema)

        logger.info(
            f"📊 Creating DataFrame for {cls.__name__} with {len(data)} rows..."
        )

        schema: StructType = cls.create_spark_schema()

        if data and isinstance(data[0], dict):
            field_names: list[str] = [field.name for field in schema.fields]
            data = [
                tuple(row.get(field_name) for field_name in field_names)  # type: ignore
                for row in data
                if isinstance(row, dict)
            ]
            logger.debug(f"Converted {len(data)} dictionary rows to tuples")

        processed_data: list[tuple[Any, ...]] = []
        for row in data:
            if isinstance(row, (list, tuple)):
                processed_row: list[Any] = []
                for item in row:
                    if isinstance(item, (tuple, dict, list)):
                        processed_row.append(str(item))
                    else:
                        processed_row.append(item)
                processed_data.append(tuple(processed_row))
            elif isinstance(row, dict):
                continue
            else:
                continue

        df: DataFrame = spark.createDataFrame(processed_data, schema)
        logger.info(f"✅ Successfully created DataFrame with schema: {cls.__name__}")

        return df

    @staticmethod
    def _pydantic_to_spark_type(pydantic_type: Type[Any] | None) -> DataType:
        """
        Map Pydantic types to Spark types.

        :param pydantic_type: Python type annotation from Pydantic field
        :type pydantic_type: Type[Any] | None
        :return: Corresponding Spark SQL data type
        :rtype: DataType
        """
        logger: Any = SparkModelLogger.get_logger()

        if (
            pydantic_type is not None
            and hasattr(pydantic_type, "__mro__")
            and BaseModel in pydantic_type.__mro__
        ):
            logger.debug(f"Detected nested Pydantic model: {pydantic_type}")
            return StringType()

        type_mapping: dict[Type[Any], DataType] = {
            str: StringType(),
            int: IntegerType(),
            float: FloatType(),
            bool: BooleanType(),
            long: LongType(),
        }

        spark_type: DataType = type_mapping.get(
            pydantic_type if pydantic_type is not None else str, StringType()
        )

        if pydantic_type not in type_mapping:
            logger.warning(f"Unknown type {pydantic_type}, defaulting to StringType")

        return spark_type

    @classmethod
    def log_schema_info(cls, schema: StructType) -> None:
        """
        Log detailed schema information.

        :param schema: Spark schema to log information about
        :type schema: StructType
        :return: None
        :rtype: None
        """
        logger: Any = getattr(cls, "_logger", SparkModelLogger.get_logger())

        logger.info("📋 Schema Details:")
        for field in schema.fields:
            logger.info(
                f"  🔹 {field.name}: {type(field.dataType).__name__} (nullable: {field.nullable})"
            )
