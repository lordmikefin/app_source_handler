# -*- coding: UTF-8 -*-
"""
    util.py
    ~~~~~~~

    Usefull tools.

    License of this script file:
       MIT License

    License is available online:
      https://github.com/lordmikefin/app_source_handler/blob/master/LICENSE

    Latest version of this script file:
      https://github.com/lordmikefin/app_source_handler/blob/master/util.py


    :copyright: (c) 2020, Mikko Niemelä a.k.a. Lord Mike (lordmike@iki.fi)
    :license: MIT License
"""
import logging

def create_logger():
    # https://www.toptal.com/python/in-depth-python-logging
    log = logging.getLogger('app_source_handler')
    # Do not propagate the log up to parent
    log.propagate = False
    return log

logger = create_logger()
