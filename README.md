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

## 📦 Distribution & Docs

- **Wheel Support**: Build and distribute as a Python wheel.
- **Documentation**: [GitHub Pages 🌐](https://alexntelifilippidis.github.io/sparkdantic/)

## 📂 Project Structure

```
sparkdantic/
├── src/
│   ├── sparkdantic/          # Main package
│       ├── __init__.py       # Package initialization
│       ├── spark_types.py    # Type conversion utilities
│       ├── models.py         # Main SparkModel class
│       └── logger.py         # Colored logging utilities
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
