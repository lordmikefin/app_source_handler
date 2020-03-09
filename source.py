# -*- coding: UTF-8 -*-
"""
    source.py
    ~~~~~~~~~

    XML source file handler.

    License of this script file:
       MIT License

    License is available online:
      https://github.com/lordmikefin/update_app_source/blob/master/LICENSE

    Latest version of this script file:
      https://github.com/lordmikefin/update_app_source/blob/master/update_app_source/source.py


    :copyright: (c) 2020, Mikko Niemelä a.k.a. Lord Mike (lordmike@iki.fi)
    :license: MIT License
"""

import xml.etree.ElementTree as ET
#from . import source_file
from .tag import Tag
from . import __version__


def create_sample(source_file: str):
    file = source_file
    print('create the sample config XML file: ' + str(file))
    root = ET.Element(Tag.source)
    tree = ET.ElementTree(root)
    #tree._setroot(root)

    root.append(ET.Comment(' Supported version of "app_source" '))

    version = ET.SubElement(root, Tag.version)
    version.text = __version__

    apps = ET.SubElement(root, Tag.apps)

    #indent(root)
    tree.write(file, encoding="UTF-8", xml_declaration=True)

def parse(source_file: str):
    print('parse the source XML file')
    file = source_file
    tree = ET.parse(file)
    root = tree.getroot()
    for elem in root:
        if elem.tag == Tag.version:
            version = elem.text
            print('source XML file version: ' + str(version))
            # TODO: do real version comparsion
            if version != __version__:
                # TODO: log warnings.
                print('WARNING: version different.')
        else:
            print('Unhandled tag: ' + str(elem.tag))
