# -*- coding: UTF-8 -*-
"""
    app_source_handler
    ~~~~~~~~~~~~~~~~~~

    Read/write 'app_source' xml file content.

    License of this script file:
       MIT License

    License is available online:
      https://github.com/lordmikefin/app_source_handler/blob/master/LICENSE

    Latest version of this script file:
      https://github.com/lordmikefin/app_source_handler/blob/master/__init__.py


    :copyright: (c) 2020, Mikko Niemelä a.k.a. Lord Mike (lordmike@iki.fi)
    :license: MIT License
"""

__license__ = "MIT License"
__version__ = "0.0.13"
__revision__ = "app_source_handler (module)  v" + __version__ + " (2020-07-10)"

import sys

# NOTE: This code is tested only with Python version 3.7
assert sys.version_info >= (3, 7)

from . import source
from .util import logger
