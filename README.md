# SparkDantic ✨

🧩 **Seamlessly morph Pydantic models ➡️ PySpark StructType schemas & conjure magical DataFrames from model lists**

A playful bridge from Pydantic models to PySpark DataFrames full of sparkly goodness!

## 🚀 Features

- **Automatic Schema Generation**: Convert Pydantic models to PySpark StructType schemas
- **DataFrame Creation**: Generate PySpark DataFrames from Python data using model schemas
- **Nested Model Support**: Handle complex nested Pydantic models
- **Tuple Processing**: Smart handling of tuple data with recursive conversion
- **Colorful Logging**: Beautiful colored console output with emojis
- **Type Safety**: Leverages Pydantic's type validation

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/sparkdantic.git
cd sparkdantic

# Install dependencies with uv
uv pip install -e .
```

## 🎯 Quick Start

```python
from pyspark.sql import SparkSession
from src.models import SparkModel
from pydantic import Field

# Create Spark session
spark = SparkSession.builder.master("local[1]").appName("SparkDantic").getOrCreate()

# Define your models
class Street(SparkModel):
    name: str
    number: int

class Address(SparkModel):
    street: Street
    city: str
    zip_code: str

class User(SparkModel):
    name: str
    age: int
    height: float
    is_active: bool
    email: str = Field(default="")
    address: Address

# Generate Spark schema
schema = User.create_spark_schema()
print(schema)

# Create sample data
data = [
    {
        "name": "Alice",
        "age": 25,
        "height": 5.6,
        "is_active": True,
        "email": "alice@example.com",
        "address": {
            "street": {"name": "123 Main St", "number": 0},
            "city": "Springfield",
            "zip_code": "12345"
        }
    }
]

# Create DataFrame
df = User.create_spark_dataframe(spark=spark, data=data)
df.show(truncate=False)
```

## 🔧 Core Components

### SparkModel
Base class that extends Pydantic's `BaseModel` with Spark functionality:

- `create_spark_schema()`: Converts model to PySpark StructType
- `create_spark_dataframe()`: Creates DataFrame from data using model schema
- Automatic type mapping from Python types to Spark types
- Built-in logging with colorful output

### Supported Types
- `str` → `StringType()`
- `int` → `IntegerType()`
- `float` → `FloatType()`
- `bool` → `BooleanType()`
- Nested models → `StringType()` (converted to string representation)

### Tuple Handling
SparkDantic includes smart tuple processing:
- Recursive conversion of nested tuples
- Automatic dictionary conversion for structured data
- Preserves other data types as-is

## 📂 Project Structure

```
sparkdantic/
├── src/
│   ├── models.py          # Main SparkModel class
│   └── logger.py          # Colored logging utilities
├── main.py                # Example usage
├── pyproject.toml         # Project configuration
├── README.md              # This file
└── LICENSE                # MIT License
```

## 🎨 Logging Features

SparkDantic includes beautiful colored logging with:
- 🔍 Debug messages in cyan
- ✨ Info messages in green
- ⚠️ Warnings in yellow
- ❌ Errors in red
- 🚨 Critical messages in magenta

## 🧪 Example Output

```
2025-01-17 10:30:15 - SparkDantic - ✨ INFO - 🔄 Converting User to Spark schema...
2025-01-17 10:30:15 - SparkDantic - ✨ INFO - ✅ Successfully created schema with 6 fields
2025-01-17 10:30:15 - SparkDantic - ✨ INFO - 📊 Creating DataFrame for User with 3 rows...
2025-01-17 10:30:15 - SparkDantic - ✨ INFO - ✅ Successfully created DataFrame with schema: User
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Pydantic](https://pydantic-docs.helpmanual.io/) for data validation
- Powered by [PySpark](https://spark.apache.org/docs/latest/api/python/) for big data processing
- Colorful logging with [Colorama](https://pypi.org/project/colorama/)

---

Made with ❤️ and ✨ for the Python + Spark community
```
