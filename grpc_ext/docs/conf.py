# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
import subprocess

sys.path.insert(0, os.path.abspath("../grpc_server"))

project = "async_grpc_ragflow"
copyright = "2025, Rohan R. Poojary"
author = "Rohan R. Poojary"
release = "v1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
subprocess.call("sphinx-apidoc -o . ../grpc_server", shell=True)


extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",  # for Numpy/Google docstrings
    "sphinx.ext.viewcode",  # optional, adds links to source code
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", ".ipynb_checkpoints"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
# html_static_path = ['_static']

# Add at the end of the conf.py

html_theme = "sphinx_rtd_theme"

# Optional: if you want custom CSS or static files
html_static_path = ["_static"]
