# -*- coding: UTF-8 -*-
"""
    source.py
    ~~~~~~~~~

    XML source file handler.

    License of this script file:
       MIT License

    License is available online:
      https://github.com/lordmikefin/app_source_handler/blob/master/LICENSE

    Latest version of this script file:
      https://github.com/lordmikefin/app_source_handler/blob/master/source.py


    :copyright: (c) 2020, Mikko Niemelä a.k.a. Lord Mike (lordmike@iki.fi)
    :license: MIT License
"""

import xml.etree.ElementTree as ET
#from . import source_file
from .tag import Tag
from . import __version__
from xml.etree.ElementTree import Element
from .util import logger
import LMToyBoxPython
from pathlib import Path


# TODO: should this be a class ?
APPS = {
    'eclipse': {},
    'java': {},
    'npp': {},
    }


class Names():
    name_key = 'name'
    version_key = 'string'

    class Java():
        name = 'java'

    class Eclipse():
        name = 'eclipse'

        class Plugin():
            pydev = 'pydev'

    class Npp():
        name = 'npp'


def create_sample(file: str):
    logger.info('create the sample config XML file: ' + str(file))
    root = ET.Element(Tag.source)
    tree = ET.ElementTree(root)
    #tree._setroot(root)

    root.append(ET.Comment(' Supported version of "app_source" '))

    version = ET.SubElement(root, Tag.version)
    version.text = __version__

    apps = ET.SubElement(root, Tag.apps)
    append_eclipse(apps)
    append_java(apps)
    append_npp(apps)

    indent(root)
    # NOTE: ElementTree.write() will use new line cgar CRLF but git repo has line ending LF
    #tree.write(file, encoding="UTF-8", xml_declaration=True)
    '''
    # NOTE: copied from ElementTree module _get_writer(...) -function
    #       This does not work -> byte writer is expected by ElementTree._get_writer()
    file_objects = open(file, "w", encoding="UTF-8", newline='\n',
                        errors="xmlcharrefreplace")
    '''
    file_objects = open(file, "wb")
    # TODO: ElementTree.write() -function should have parameter 'newline' and it should be passed to _get_writer() -function
    # TODO: Send request to ElementTree toolkit project. Python core project?
    #   https://docs.python.org/3/library/xml.etree.elementtree.html
    tree.write(file_objects, encoding="UTF-8", xml_declaration=True)


def create_sum_file(sum_file: str, source_file: str):
    logger.info('Creating hash sum file: ' + str(sum_file))
    sha256sum = LMToyBoxPython.sha256(source_file, show_progress=True)
    logger.debug('sha256sum: ' + str(sha256sum))

    lines = []
    file = Path(source_file)
    file_name = file.name
    # NOTE: sha256 file format is mimicked from npp.7.7.1.checksums.sha256
    line = sha256sum + '  ' + file_name + '\n'
    lines.append(line)
    LMToyBoxPython.write_lines_to_file(sum_file, lines)


def append_app_element(parent: Element, elem_name: str) -> Element:
    elem = ET.SubElement(parent, Tag.app)
    elem.set(Names.name_key, elem_name)
    return elem


def append_plugin_element(parent: Element, elem_name: str) -> Element:
    elem = ET.SubElement(parent, Tag.plugin)
    elem.set(Names.name_key, elem_name)
    return elem


def append_lateset_element(elem: Element, text: str):
    lateset = ET.SubElement(elem, Tag.latest)
    lateset.text = text


def append_npp(apps: Element):
    npp_elem = append_app_element(apps, Names.Npp.name)
    append_lateset_element(npp_elem, '7.7.1')
    versions = ET.SubElement(npp_elem, Tag.versions)
    set_version(versions,
                version='7.7.1',
                url='http://download.notepad-plus-plus.org/repository/7.x/7.7.1/npp.7.7.1.Installer.x64.exe',
                sha256url='http://download.notepad-plus-plus.org/repository/7.x/7.7.1/npp.7.7.1.checksums.sha256',
                sha256file='npp.7.7.1.checksums.sha256',
                file='npp.7.7.1.Installer.x64.exe')


def append_java(apps: Element):
    java_elem = append_app_element(apps, Names.Java.name)
    append_lateset_element(java_elem, 'jdk-8.0.242.08-hotspot')

    # https://adoptopenjdk.net/installation.html#windows-msi
    # https://github.com/AdoptOpenJDK/openjdk8-binaries/releases/tag/jdk8u242-b08
    versions = ET.SubElement(java_elem, Tag.versions)
    set_version(versions,
                version='jdk-8.0.242.08-hotspot',
                url='https://github.com/AdoptOpenJDK/openjdk8-binaries/releases/download/jdk8u242-b08/OpenJDK8U-jdk_x64_windows_hotspot_8u242b08.msi',
                sha256url='https://github.com/AdoptOpenJDK/openjdk8-binaries/releases/download/jdk8u242-b08/OpenJDK8U-jdk_x64_windows_hotspot_8u242b08.msi.sha256.txt',
                sha256file='OpenJDK8U-jdk_x64_windows_hotspot_8u242b08.msi.sha256.txt',
                #md5sum='7b97b5c42cb30f36f14b8c90342a9e55',
                file='OpenJDK8U-jdk_x64_windows_hotspot_8u242b08.msi')


def append_eclipse(apps: Element):
    ecli_elem = append_app_element(apps, Names.Eclipse.name)
    append_lateset_element(ecli_elem, '2019-12')

    versions = ET.SubElement(ecli_elem, Tag.versions)
    set_version(versions,
                version='2019-09',
                url='https://ftp.acc.umu.se/mirror/eclipse.org/technology/epp/downloads/release/2019-09/R/eclipse-javascript-2019-09-R-win32-x86_64.zip',
                md5url='https://ftp.acc.umu.se/mirror/eclipse.org/technology/epp/downloads/release/2019-09/R/eclipse-javascript-2019-09-R-win32-x86_64.zip.md5',
                md5file='eclipse-javascript-2019-09-R-win32-x86_64.zip.md5',
                #md5sum='7b97b5c42cb30f36f14b8c90342a9e55',
                file='eclipse-javascript-2019-09-R-win32-x86_64.zip')

    set_version(versions,
                version='2019-12',
                url='https://ftp.acc.umu.se/mirror/eclipse.org/technology/epp/downloads/release/2019-12/R/eclipse-javascript-2019-12-R-win32-x86_64.zip',
                md5url='https://ftp.acc.umu.se/mirror/eclipse.org/technology/epp/downloads/release/2019-12/R/eclipse-javascript-2019-12-R-win32-x86_64.zip.md5',
                md5file='eclipse-javascript-2019-12-R-win32-x86_64.zip.md5',
                #md5sum='7b97b5c42cb30f36f14b8c90342a9e55',
                file='eclipse-javascript-2019-12-R-win32-x86_64.zip')

    append_plugins(ecli_elem)

def append_plugins(ecli_elem: Element):
    plugins = ET.SubElement(ecli_elem, Tag.plugins)
    plugin = append_plugin_element(plugins, Names.Eclipse.Plugin.pydev)
    append_lateset_element(plugin, '7.5.0')

    versions = ET.SubElement(plugin, Tag.versions)
    set_version(versions,
                version='7.4.0',
                url='https://sourceforge.net/projects/pydev/files/pydev/PyDev%207.4.0/PyDev 7.4.0.zip/download',
                # md5url='https://...',  # TODO: does sourceforge provide the md5 file?
                md5sum='722dfe4a9bf1f50a2766c4d58eb6dd4d',
                file='PyDev 7.4.0.zip')

    set_version(versions,
                version='7.5.0',
                url='https://sourceforge.net/projects/pydev/files/pydev/PyDev%207.5.0/PyDev 7.5.0.zip/download',
                # md5url='https://...',  # TODO: does sourceforge provide the md5 file?
                md5sum='ca391869d7d9358cab4e2e162a03b57f',
                file='PyDev 7.5.0.zip')

def set_version(versions: Element, version: str=None, url: str=None,
                md5sum: str=None, file: str=None,
                md5url: str=None, md5file: str=None,
                sha256url: str=None, sha256file: str=None):
    #versions = ET.SubElement(elem, Tag.versions)
    if not version:
        return  # noting to do
    version_elem = ET.SubElement(versions, Tag.version)
    #version_elem.text = '2019-09'
    version_elem.set(Names.version_key, version)
    set_url(version_elem, url)
    set_md5url(version_elem, md5url, md5file)
    set_md5sum(version_elem, md5sum)
    set_file(version_elem, file)
    set_sha256url(version_elem, sha256url, sha256file)

def set_url(elem: Element, url: str=None):
    create_elem(elem, Tag.url, url)

def set_md5url(elem: Element, md5url: str=None, md5file: str=None):
    create_elem(elem, Tag.md5url, md5url)
    create_elem(elem, Tag.md5file, md5file)

def set_md5sum(elem: Element, md5sum: str=None):
    create_elem(elem, Tag.md5sum, md5sum)

def set_file(elem: Element, file: str=None):
    create_elem(elem, Tag.file, file)

def set_sha256url(elem: Element, sha256url: str=None, sha256file: str=None):
    create_elem(elem, Tag.sha256url, sha256url)
    create_elem(elem, Tag.sha256file, sha256file)

def create_elem(elem: Element, tag_name: str=None, text: str=None):
    if not text:
        return  # do not create empty element
    elem = ET.SubElement(elem, tag_name)
    elem.text = text

def parse(source_file: str):
    # TODO: is there better way to fix Eclipse auto complete ?
    if False:  # for Eclipse auto complete only :)
        elem = Element()
        logger.error('This should not we printed! :: elem: ' + str(elem))

    logger.info('Parse the source XML file')
    file = source_file
    tree = ET.parse(file)
    root = tree.getroot()
    is_version = False
    for elem in root:
        if elem.tag == Tag.version:
            is_version = True
            version = elem.text
            logger.info('Source XML file version: ' + str(version))
            # TODO: do real version comparsion
            if version != __version__:
                logger.warning('Version different.')
        elif elem.tag == Tag.apps:
            parse_apps(elem)
        else:
            logger.error('Unhandled tag: ' + str(elem.tag))

    if not is_version:
        logger.error('Source XML file version must be defined.')

def parse_apps(elem: Element):
    global APPS
    for elem_app in elem:
        if elem_app.tag == Tag.app:
            #eclipse_list = list(APPS.get('eclipse', []))
            #ecli_elem.set(Names.name_key, Names.Eclipse.name)
            name = elem_app.get(Names.name_key, None)
            if not name:
                logger.error('Name is not defined. Skip element.')
            logger.info('name: ' + str(name))
            parse_app(elem_app, name)
            '''
            if name == Names.Eclipse.name:
                parse_app(elem_app, name)
            if name == Names.Java.name:
                parse_app(elem_app, name)
            if name == Names.Npp.name:
                parse_app(elem_app, name)
            else:
                print('Unhandled app: ' + str(name))
            '''
        else:
            logger.error('Unhandled tag: ' + str(elem_app.tag))

def parse_app(elem: Element, name: str):
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
            logger.error('Unhandled tag: ' + str(tags_app.tag))

    if eclipse_dict:
        APPS[name] = eclipse_dict

def parse_versions(elem: Element, versions_dict: dict):
    for elem_ver in elem:
        if elem_ver.tag == Tag.version:
            version = elem_ver.get(Names.version_key, None)
            if not version:
                logger.error('Version is not defined. Skip element.')
            logger.info('version: ' + str(version))
            data = {}
            versions_dict[str(version)] = data
            for ver_tag in elem_ver:
                if ver_tag.tag == Tag.url:
                    data['url'] = ver_tag.text
                elif ver_tag.tag == Tag.file:
                    data['file'] = ver_tag.text
                elif ver_tag.tag == Tag.md5url:
                    data['md5url'] = ver_tag.text
                elif ver_tag.tag == Tag.md5file:
                    data['md5file'] = ver_tag.text
                elif ver_tag.tag == Tag.md5sum:
                    data['md5sum'] = ver_tag.text
                elif ver_tag.tag == Tag.sha256url:
                    data['sha256url'] = ver_tag.text
                elif ver_tag.tag == Tag.sha256file:
                    data['sha256file'] = ver_tag.text
                else:
                    logger.error('Unhandled tag: ' + str(ver_tag.tag))
        else:
            logger.error('Unhandled tag: ' + str(elem_ver.tag))

def parse_plugins(elem: Element, plugins_dict: dict):
    for elem_plug in elem:
        if elem_plug.tag == Tag.plugin:
            #plugin.set(Names.name_key, Names.Eclipse.Plugin.pydev)
            name = elem_plug.get(Names.name_key, None)
            if not name:
                logger.error('Name is not defined. Skip element.')
            logger.info('Name: ' + str(name))
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
                        logger.error('Unhandled tag: ' + str(tags_plug.tag))
    
                if pydev_dict:
                    plugins_dict[name] = pydev_dict
        else:
            logger.error('Unhandled tag: ' + str(elem_plug.tag))

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
