from unittest.mock import MagicMock

from src.models import SparkModel


def test_dataframe_creation_with_mock_spark():
    """Ensure DataFrame creation works with mocked Spark session."""

    class MockModel(SparkModel):
        name: str
        age: int

    mock_spark = MagicMock()
    mock_df = MagicMock()
    mock_spark.createDataFrame.return_value = mock_df

    data = [{"name": "Alice", "age": 25}]
    result = MockModel.create_spark_dataframe(mock_spark, data)

    mock_spark.createDataFrame.assert_called_once()
    call_args = mock_spark.createDataFrame.call_args
    actual_data = call_args[0][0]
    actual_schema = call_args[0][1]

    assert len(actual_data) == 1
    assert actual_data[0][0] == "Alice"
    assert actual_data[0][1] == 25
    assert actual_schema is not None
    assert result == mock_df


def test_handles_mixed_data_types_in_tuple():
    """Ensure tuples with mixed data types are processed correctly."""

    class MixedTypesModel(SparkModel):
        name: str
        score: float
        active: bool

    mock_spark = MagicMock()
    mock_df = MagicMock()
    mock_spark.createDataFrame.return_value = mock_df

    data = [("Alice", 95.5, True), ("Bob", 87.2, False)]
    MixedTypesModel.create_spark_dataframe(mock_spark, data)

    mock_spark.createDataFrame.assert_called_once()
    call_args = mock_spark.createDataFrame.call_args
    actual_data = call_args[0][0]

    assert len(actual_data) == 2
    assert actual_data[0][0] == "Alice"
    assert actual_data[0][1] == 95.5
    assert actual_data[0][2] is True
    assert actual_data[1][0] == "Bob"
    assert actual_data[1][1] == 87.2
    assert actual_data[1][2] is False


def test_handles_none_values_in_data():
    """Ensure None values are handled correctly in DataFrame creation."""

    class NullableModel(SparkModel):
        name: str
        age: int

    mock_spark = MagicMock()
    mock_df = MagicMock()
    mock_spark.createDataFrame.return_value = mock_df

    data = [{"name": "Alice", "age": None}, {"name": None, "age": 30}]
    NullableModel.create_spark_dataframe(mock_spark, data)

    mock_spark.createDataFrame.assert_called_once()
    call_args = mock_spark.createDataFrame.call_args
    actual_data = call_args[0][0]

    assert len(actual_data) == 2
    assert actual_data[0][0] == "Alice"
    assert actual_data[0][1] is None
    assert actual_data[1][0] is None
    assert actual_data[1][1] == 30


def test_handles_complex_nested_data_structures():
    """Ensure complex nested structures are converted to strings."""

    class ComplexModel(SparkModel):
        name: str
        metadata: str

    mock_spark = MagicMock()
    mock_df = MagicMock()
    mock_spark.createDataFrame.return_value = mock_df

    complex_data = {"nested": {"key": "value"}, "list": [1, 2, 3]}
    data = [("Alice", complex_data)]

    ComplexModel.create_spark_dataframe(mock_spark, data)

    mock_spark.createDataFrame.assert_called_once()
    call_args = mock_spark.createDataFrame.call_args
    actual_data = call_args[0][0]

    assert len(actual_data) == 1
    assert actual_data[0][0] == "Alice"
    assert "nested" in actual_data[0][1]
    assert "key" in actual_data[0][1]["nested"]
    assert "value" in actual_data[0][1]["nested"]["key"]
    assert "list" in actual_data[0][1]
