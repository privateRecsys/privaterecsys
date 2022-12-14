'''
searx is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

searx is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with searx. If not, see < http://www.gnu.org/licenses/ >.

(C) 2015 by Adam Tauber, <asciimoo@gmail.com>
'''

from hashlib import sha256
from importlib import import_module
from os import listdir, makedirs, remove, stat, utime
from os.path import abspath, basename, dirname, exists, join
from shutil import copyfile

from searx import logger, settings, static_path


logger = logger.getChild('plugins')

from searx.plugins import (oa_doi_rewrite,
                           ahmia_filter,
                           hash_plugin,
                           https_rewrite,
                           infinite_scroll,
                           self_info,
                           hostname_replace,
                           search_on_category_select,
                           search_operators,
                           tracker_url_remover,
                           vim_hotkeys,
                           examply)

required_attrs = (('name', str),
                  ('description', str),
                  ('default_on', bool))

optional_attrs = (('js_dependencies', tuple),
                  ('css_dependencies', tuple))


class Plugin():
    default_on = False
    name = 'Default plugin'
    description = 'Default plugin description'


class PluginStore():

    def __init__(self):
        self.plugins = []

    def __iter__(self):
        for plugin in self.plugins:
            yield plugin

    def register(self, *plugins, external=False):
        if external:
            plugins = load_external_plugins(plugins)
        for plugin in plugins:
            for plugin_attr, plugin_attr_type in required_attrs:
                if not hasattr(plugin, plugin_attr) or not isinstance(getattr(plugin, plugin_attr), plugin_attr_type):
                    logger.critical('missing attribute "{0}", cannot load plugin: {1}'.format(plugin_attr, plugin))
                    exit(3)
            for plugin_attr, plugin_attr_type in optional_attrs:
                if not hasattr(plugin, plugin_attr) or not isinstance(getattr(plugin, plugin_attr), plugin_attr_type):
                    setattr(plugin, plugin_attr, plugin_attr_type())
            plugin.id = plugin.name.replace(' ', '_')
            self.plugins.append(plugin)

    def call(self, ordered_plugin_list, plugin_type, request, *args, **kwargs):
        ret = True
        for plugin in ordered_plugin_list:
            if hasattr(plugin, plugin_type):
                ret = getattr(plugin, plugin_type)(request, *args, **kwargs)
                if not ret:
                    break

        return ret


def load_external_plugins(plugin_names):
    plugins = []
    for name in plugin_names:
        logger.debug('loading plugin: {0}'.format(name))
        try:
            pkg = import_module(name)
        except Exception as e:
            logger.critical('failed to load plugin module {0}: {1}'.format(name, e))
            exit(3)

        pkg.__base_path = dirname(abspath(pkg.__file__))

        prepare_package_resources(pkg, name)

        plugins.append(pkg)
        logger.debug('plugin "{0}" loaded'.format(name))
    return plugins


def sync_resource(base_path, resource_path, name, target_dir, plugin_dir):
    dep_path = join(base_path, resource_path)
    file_name = basename(dep_path)
    resource_path = join(target_dir, file_name)
    if not exists(resource_path) or sha_sum(dep_path) != sha_sum(resource_path):
        try:
            copyfile(dep_path, resource_path)
            # copy atime_ns and mtime_ns, so the weak ETags (generated by
            # the HTTP server) do not change
            dep_stat = stat(dep_path)
            utime(resource_path, ns=(dep_stat.st_atime_ns, dep_stat.st_mtime_ns))
        except:
            logger.critical('failed to copy plugin resource {0} for plugin {1}'.format(file_name, name))
            exit(3)

    # returning with the web path of the resource
    return join('plugins/external_plugins', plugin_dir, file_name)


def prepare_package_resources(pkg, name):
    plugin_dir = 'plugin_' + name
    target_dir = join(static_path, 'plugins/external_plugins', plugin_dir)
    try:
        makedirs(target_dir, exist_ok=True)
    except:
        logger.critical('failed to create resource directory {0} for plugin {1}'.format(target_dir, name))
        exit(3)

    resources = []

    if hasattr(pkg, 'js_dependencies'):
        resources.extend(map(basename, pkg.js_dependencies))
        pkg.js_dependencies = tuple([
            sync_resource(pkg.__base_path, x, name, target_dir, plugin_dir)
            for x in pkg.js_dependencies
        ])
    if hasattr(pkg, 'css_dependencies'):
        resources.extend(map(basename, pkg.css_dependencies))
        pkg.css_dependencies = tuple([
            sync_resource(pkg.__base_path, x, name, target_dir, plugin_dir)
            for x in pkg.css_dependencies
        ])

    for f in listdir(target_dir):
        if basename(f) not in resources:
            resource_path = join(target_dir, basename(f))
            try:
                remove(resource_path)
            except:
                logger.critical('failed to remove unused resource file {0} for plugin {1}'.format(resource_path, name))
                exit(3)


def sha_sum(filename):
    with open(filename, "rb") as f:
        file_content_bytes = f.read()
        return sha256(file_content_bytes).hexdigest()


plugins = PluginStore()
plugins.register(oa_doi_rewrite)
plugins.register(hash_plugin)
plugins.register(https_rewrite)
plugins.register(infinite_scroll)
plugins.register(self_info)
plugins.register(hostname_replace)
plugins.register(search_on_category_select)
plugins.register(search_operators)
plugins.register(tracker_url_remover)
plugins.register(vim_hotkeys)
plugins.register(examply)

# load external plugins
if 'plugins' in settings:
    plugins.register(*settings['plugins'], external=True)

if 'enabled_plugins' in settings:
    for plugin in plugins:
        if plugin.name in settings['enabled_plugins']:
            plugin.default_on = True
        else:
            plugin.default_on = False

# load tor specific plugins
if settings['outgoing'].get('using_tor_proxy'):
    plugins.register(ahmia_filter)
