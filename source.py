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
    'eclipse': {}
    }


class Names():
    name_key = 'name'
    version_key = 'string'

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
        lateset = Element()
        print('ERROR: this should not we printed! :: ecli_elem: ' + str(ecli_elem) +
              ' :: lateset: ' + str(lateset))
    ecli_elem = ET.SubElement(apps, Tag.app)
    ecli_elem.set(Names.name_key, Names.Eclipse.name)

    lateset = ET.SubElement(ecli_elem, Tag.latest)
    lateset.text = '2019-12'

    versions = ET.SubElement(ecli_elem, Tag.versions)
    set_version(versions,
                version='2019-09',
                url='https://ftp.acc.umu.se/mirror/eclipse.org/technology/epp/downloads/release/2019-09/R/eclipse-javascript-2019-09-R-win32-x86_64.zip',
                md5url='https://ftp.acc.umu.se/mirror/eclipse.org/technology/epp/downloads/release/2019-09/R/eclipse-javascript-2019-09-R-win32-x86_64.zip.md5',
                md5sum='7b97b5c42cb30f36f14b8c90342a9e55',
                file='eclipse-javascript-2019-09-R-win32-x86_64.zip')

    set_version(versions,
                version='2019-12',
                url='https://ftp.acc.umu.se/mirror/eclipse.org/technology/epp/downloads/release/2019-12/R/eclipse-javascript-2019-12-R-win32-x86_64.zip',
                md5url='https://ftp.acc.umu.se/mirror/eclipse.org/technology/epp/downloads/release/2019-12/R/eclipse-javascript-2019-12-R-win32-x86_64.zip.md5',
                #md5sum='7b97b5c42cb30f36f14b8c90342a9e55',
                file='eclipse-javascript-2019-12-R-win32-x86_64.zip')

    append_plugins(ecli_elem)

def append_plugins(ecli_elem: Element):
    plugins = ET.SubElement(ecli_elem, Tag.plugins)
    plugin = ET.SubElement(plugins, Tag.plugin)
    plugin.set(Names.name_key, Names.Eclipse.Plugin.pydev)

    lateset = ET.SubElement(plugin, Tag.latest)
    lateset.text = '7.4.0'

    versions = ET.SubElement(plugin, Tag.versions)
    set_version(versions,
                version='7.4.0',
                url='https://sourceforge.net/projects/pydev/files/pydev/PyDev%207.4.0/PyDev 7.4.0.zip/download',
                # md5url='https://...',  # TODO: does sourceforge provide the sm5 file?
                md5sum='722dfe4a9bf1f50a2766c4d58eb6dd4d',
                file='PyDev 7.4.0.zip')

def set_version(versions: Element, version: str=None, url: str=None, md5url: str=None,
                md5sum: str=None, file: str=None):
    #versions = ET.SubElement(elem, Tag.versions)
    if not version:
        return  # noting to do
    version_elem = ET.SubElement(versions, Tag.version)
    #version_elem.text = '2019-09'
    version_elem.set(Names.version_key, version)
    set_url(version_elem, url)
    set_md5url(version_elem, md5url)
    set_md5sum(version_elem, md5sum)
    set_file(version_elem, file)

def set_url(elem: Element, url: str=None):
    if url:
        url_elem = ET.SubElement(elem, Tag.url)
        url_elem.text = url

def set_md5url(elem: Element, md5url: str=None):
    if md5url:
        md5url_elem = ET.SubElement(elem, Tag.md5url)
        md5url_elem.text = md5url

def set_md5sum(elem: Element, md5sum: str=None):
    if md5sum:
        md5sum_elem = ET.SubElement(elem, Tag.md5sum)
        md5sum_elem.text = md5sum

def set_file(elem: Element, file: str=None):
    if file:
        file_elem = ET.SubElement(elem, Tag.file)
        file_elem.text = file

def parse(source_file: str):
    # TODO: is there better way to fix Eclipse auto complete ?
    if False:  # for Eclipse auto complete only :)
        elem = Element()
        print('ERROR: this should not we printed! :: elem: ' + str(elem))
    #global APPS
    print('parse the source XML file')
    file = source_file
    tree = ET.parse(file)
    root = tree.getroot()
    is_version = False
    for elem in root:
        if elem.tag == Tag.version:
            is_version = True
            version = elem.text
            print('source XML file version: ' + str(version))
            # TODO: do real version comparsion
            if version != __version__:
                # TODO: log warnings.
                print('WARNING: version different.')
        elif elem.tag == Tag.apps:
            #eclipse_list = list(APPS.get('eclipse', []))
            parse_apps(elem)
            #APPS['eclipse'] = eclipse_list
        else:
            print('Unhandled tag: ' + str(elem.tag))

    if not is_version:
        print('ERROR: source XML file version must be defined.')

def parse_apps(elem: Element):
    global APPS
    for elem_app in elem:
        if elem_app.tag == Tag.app:
            #eclipse_list = list(APPS.get('eclipse', []))
            #ecli_elem.set(Names.name_key, Names.Eclipse.name)
            name = elem_app.get(Names.name_key, None)
            if not name:
                print('ERROR: Name is not defined. Skip element.')
            print('name: ' + str(name))
            if name == Names.Eclipse.name:
                parse_eclipse(elem_app, name)
        else:
            print('Unhandled tag: ' + str(elem_app.tag))

def parse_eclipse(elem: Element, name: str):
    global APPS
    eclipse_dict = dict(APPS.get(name, {}))
    for tags_app in elem:
        if tags_app.tag == Tag.latest:
            eclipse_dict['latest'] = tags_app.text
        elif tags_app.tag == Tag.versions:
            #eclipse_dict['version'] = tags_app.text
            versions_dict = dict(APPS.get('versions', {}))
            parse_versions(tags_app, versions_dict)
            eclipse_dict['versions'] = versions_dict
        elif tags_app.tag == Tag.plugins:
            #plugins = tags_app.text
            plugins_dict = dict(eclipse_dict.get('plugins', {}))
            parse_plugins(tags_app, plugins_dict)
            eclipse_dict['plugins'] = plugins_dict
        else:
            print('Unhandled tag: ' + str(tags_app.tag))

    if eclipse_dict:
        APPS[name] = eclipse_dict

def parse_versions(elem: Element, versions_dict: dict):
    for elem_ver in elem:
        if elem_ver.tag == Tag.version:
            version = elem_ver.get(Names.version_key, None)
            if not version:
                print('ERROR: version is not defined. Skip element.')
            print('version: ' + str(version))
            data = {}
            versions_dict[str(version)] = data
            for ver_tag in elem_ver:
                if ver_tag.tag == Tag.url:
                    data['url'] = ver_tag.text
                elif ver_tag.tag == Tag.md5url:
                    data['md5url'] = ver_tag.text
                elif ver_tag.tag == Tag.md5sum:
                    data['md5sum'] = ver_tag.text
                elif ver_tag.tag == Tag.file:
                    data['file'] = ver_tag.text
                else:
                    print('Unhandled tag: ' + str(ver_tag.tag))
        else:
            print('Unhandled tag: ' + str(elem_ver.tag))

def parse_plugins(elem: Element, plugins_dict: dict):
    for elem_plug in elem:
        if elem_plug.tag == Tag.plugin:
            #plugin.set(Names.name_key, Names.Eclipse.Plugin.pydev)
            name = elem_plug.get(Names.name_key, None)
            if not name:
                print('ERROR: Name is not defined. Skip element.')
            print('name: ' + str(name))
            if name == Names.Eclipse.Plugin.pydev:
                pydev_dict = dict(plugins_dict.get(name, {}))
                for tags_plug in elem_plug:
                    if tags_plug.tag == Tag.latest:
                        pydev_dict['latest'] = tags_plug.text
                    elif tags_plug.tag == Tag.versions:
                        #versions = tags_plug.text
                        versions_dict = dict(pydev_dict.get('versions', {}))
                        parse_versions(tags_plug, versions_dict)
                        pydev_dict['versions'] = versions_dict
                    else:
                        print('Unhandled tag: ' + str(tags_plug.tag))
    
                if pydev_dict:
                    plugins_dict[name] = pydev_dict
        else:
            print('Unhandled tag: ' + str(elem_plug.tag))

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
