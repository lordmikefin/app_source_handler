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
from xml.etree.ElementTree import Element

# TODO: should this be a class ?
APPS = {
    'eclipse': []
    }


class Names():
    name_key = 'name'

    class Eclipse():
        name = 'eclipse'

        class Plugin():
            pydev = 'pydev'


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
    append_eclipse(apps)

    indent(root)
    tree.write(file, encoding="UTF-8", xml_declaration=True)
    # TODO: create md5 file

def append_eclipse(apps: Element):
    # TODO: is there better way to fix Eclipse auto complete ?
    if False:  # for Eclipse auto complete only :)
        ecli_elem = Element()
        print('ERROR: this should not we printed! :: ecli_elem: ' + str(ecli_elem))
    ecli_elem = ET.SubElement(apps, Tag.app)
    ecli_elem.set(Names.name_key, Names.Eclipse.name)

def parse(source_file: str):
    global APPS
    print('parse the source XML file')
    file = source_file
    tree = ET.parse(file)
    root = tree.getroot()
    for elem in root:
        # TODO: parse into global var
        '''
        eclipse_list = list(APPS.get('eclipse', []))
        eclipse_list['latest'] = '2019-09'
        eclipse_list['versions'] = [
            'version': '2019-09'
            'url': 'https://...'
            'url_md5': 'https://...'
            'md5sum': 'A1B2C3FF'
        ]

        eclipse_plugins = list(eclipse_list.get('plugins', []))
        eclipse_pydev = list(eclipse_plugins.get('pydev', []))
        eclipse_pydev['latest'] = '2019-09'
        eclipse_pydev['versions'] = [
            'version': '2019-09'
            'url': 'https://...'
            'url_md5': 'https://...'
            'md5sum': 'A1B2C3FF'
        ]

        eclipse_plugins['pydev'] = eclipse_pydev
        eclipse_list['plugins'] = eclipse_plugins

        APPS['eclipse'] = eclipse_list
        '''
        if elem.tag == Tag.version:
            version = elem.text
            print('source XML file version: ' + str(version))
            # TODO: do real version comparsion
            if version != __version__:
                # TODO: log warnings.
                print('WARNING: version different.')
        else:
            print('Unhandled tag: ' + str(elem.tag))

def indent(elem, level=0):
    ''' Indent the xml tree '''
    # TODO: this should be part of 'xml.etree.ElementTree'
    # NOTE: Copied from 'setup_apps'  :)
    # TODO: Create common code base! And move this there.

    # NOTE: code copied from stackoverflow
    # https://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
