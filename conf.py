#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is execfile()d with the current directory set to its
# containing dir.
#

# -- General configuration ------------------------------------------------

# General information about the project.
project = 'Sarcasm tips'
copyright = '2016-2021, Guillaume Papin'
author = 'Guillaume Papin'

exclude_patterns = ['.build']

extensions = [
    'sphinx.ext.mathjax',
    'sphinx.ext.todo',
]

# try to find internal dead links.
# For external dead links use:
#     make linkcheck OR sphinx-build -b linkcheck
nitpicky = True

templates_path = [] # '.templates'

pygments_style = 'sphinx'

# If true, keep warnings as "system message" paragraphs in the built documents.
keep_warnings = True

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True


# -- Options for HTML output ----------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'haiku'
html_static_path = [] # '.static'
