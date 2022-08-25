import re
from urllib.parse import urlparse
from lxml import etree
from os import listdir, environ
from os.path import isfile, isdir, join
from searx.plugins import logger
from flask_babel import gettext
from searx import searx_dir
from flask_babel import gettext

name = 'Example plugin'
default_on = True
preference_section = 'ui'
description = gettext('Perform search immediately if a category selected. '
                      'Disable to select multiple categories. (JavaScript required)')
js_dependencies = ('../static/plugins/js/search_on_category_select.js',)
