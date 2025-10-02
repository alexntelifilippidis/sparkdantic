# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

# Add the project root and src to the Python path
project_root = os.path.abspath("../..")
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, "src"))

# -- Project information -----------------------------------------------------
project = "SparkDantic"
copyright = "2025, Alex.D"
author = "Alex.D"
release = "0.1.0"
version = "0.1.0"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "myst_parser",
]

templates_path = ["_templates"]
# Exclude patterns to avoid duplicates
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "src.rst",  # Exclude auto-generated files
    "modules.rst",  # Exclude auto-generated files
]


# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_rtd_theme"
html_static_path: list = []  # Remove _static since it's created dynamically

# -- Autodoc configuration ---------------------------------------------------
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
}

# Mock imports for dependencies that might not be available during doc build
autodoc_mock_imports = ["pyspark", "pydantic", "pydantic_core"]


# -- Napoleon settings -------------------------------------------------------
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# -- Intersphinx mapping -----------------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "pydantic": ("https://docs.pydantic.dev/latest/", None),
    "pyspark": ("https://spark.apache.org/docs/latest/api/python/", None),
}

# -- HTML theme options ------------------------------------------------------
html_theme_options = {
    "canonical_url": "",
    "logo_only": False,
    "prev_next_buttons_location": "bottom",
    "style_external_links": False,
    "collapse_navigation": True,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
}

# Todo extension
todo_include_todos = True

# Source file suffixes
source_suffix = {
    ".rst": None,
    ".md": "myst_parser.parsers.myst",
}

# The master toctree document
master_doc = "index"
