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
copyright = '2015, Igor Kalnitsky'
release = dooku_version
version = re.sub('[^0-9.]', '', release)

# sphinx settings
extensions = ['sphinx.ext.autodoc', 'alabaster']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
exclude_patterns = ['_build']
pygments_style = 'sphinx'

# html output settings
import alabaster

html_theme = 'alabaster'
html_theme_path = [alabaster.get_path()]
html_theme_options = {
    'logo': 'dooku.png',
    'description': 'a set of libraries for everyday!',
    'gratipay_user': 'ikalnitsky',
    'github_user': 'ikalnitsky',
    'github_repo': 'dooku',
    'github_button': True,
    'github_banner': True,
    'travis_button': True,
    'extra_nav_links': {
        'Issue Tracker': 'https://github.com/ikalnitsky/dooku/issues',
    },
}
html_sidebars = {
    '**': [
        'about.html', 'navigation.html', 'searchbox.html', 'donate.html',
    ]
}
html_static_path = ['_static']
