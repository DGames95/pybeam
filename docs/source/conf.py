# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import toml
import datetime

import os
import sys
sys.path.insert(0, os.path.abspath("../..")) 


pyproject = toml.load("../../pyproject.toml")

project = pyproject["project"]["name"]
copyright = str(datetime.datetime.now().year) + ", " + pyproject["project"]["authors"][0]["name"]
author = pyproject["project"]["authors"][0]["name"]
release = pyproject["project"]["version"]

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",  # Google/NumPy docstring support
    "sphinx_autodoc_typehints",  # for type hints in docs
]

html_theme = "sphinx_rtd_theme"

templates_path = ['_templates']
exclude_patterns = []
html_static_path = ['_static']