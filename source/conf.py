# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'SphinxDiary'
copyright = '2023, 李仲亮'
author = '李仲亮'
release = 'v1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['myst_parser', 'sphinx_copybutton', 'sphinx_wagtail_theme']
source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}

myst_enable_extensions = [
    "dollarmath",
    "deflist",
    "fieldlist",
    "linkify",
    "html_image",
    "replacements",
    "smartquotes",
    "tasklist",
]

# extensions = ['recommonmark', 'sphinx_markdown_tables', 'sphinx_copybutton', 'sphinx.ext.mathjax']
templates_path = ['_templates']
exclude_patterns = []

language = 'zh_CN'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = ''
html_theme = "sphinx_wagtail_theme"
# html_logo = "logo.png"
html_static_path = ['_static']

