# -*- coding: utf-8 -*-
"""
    Sphinx configuration file for building dooku's documentation.
"""
from __future__ import unicode_literals

import re
import os
import sys


# add parent dir to PYTHONPATH for allowing import em's version
sys.path.append(os.path.abspath(os.pardir))
from dooku import __version__ as dooku_version


# project settings
project = 'dooku'
copyright = '2014, Igor Kalnitsky'
release = dooku_version
version = re.sub('[^0-9.]', '', release)

# sphinx settings
extensions = ['sphinx.ext.autodoc']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
exclude_patterns = ['_build']
pygments_style = 'sphinx'

# html output settings
html_theme = 'default'
html_static_path = ['_static']
