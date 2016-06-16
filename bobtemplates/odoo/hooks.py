# -*- coding: utf-8 -*-
# Copyright © 2016 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import ast
import os

from mrbob.bobexceptions import ValidationError
from mrbob.hooks import show_message


def _dotted_to_camelcased(dotted):
    return ''.join([s.capitalize() for s in dotted.split('.')])


def _dotted_to_underscored(dotted):
    return dotted.replace('.', '_')


def _dotted_to_camelwords(dotted):
    return ' '.join([s.capitalize() for s in dotted.split('.')])


def _underscored_to_camelcased(underscored):
    return ''.join([s.capitalize() for s in underscored.split('_')])


def _underscored_to_camelwords(underscored):
    return ' '.join([s.capitalize() for s in underscored.split('_')])


def _delete_file(configurator, *args):
    """ remove file and remove it's directories if empty """
    path = os.path.join(configurator.target_directory, *args)
    os.remove(path)
    for i in range(1, len(args)):
        path = os.path.join(configurator.target_directory, *args[:-i])
        try:
            os.rmdir(path)
        except OSError:
            pass


def _load_manifest(configurator):
    manifest_path = os.path.join(configurator.target_directory,
                                 '__openerp__.py')
    if not os.path.exists(manifest_path):
        raise ValidationError("{} not found".format(manifest_path))
    with open(manifest_path) as manifest_file:
        return ast.literal_eval(manifest_file.read())


def _add_local_import(configurator, package, module):
    init_path = os.path.join(configurator.target_directory,
                             package, '__init__.py')
    import_string = 'from . import {}'.format(module)
    if os.path.exists(init_path):
        init = open(init_path).read()
    else:
        init = ''
    if import_string not in init:
        open(init_path, 'a').write(import_string + '\n')


def _rm_suffix(suffix, configurator, *args):
    path = os.path.join(configurator.target_directory, *args)
    assert path.endswith(suffix)
    os.rename(path, path[:-len(suffix)])


#
# model hooks
#

def pre_render_model(configurator):
    _load_manifest(configurator)  # check manifest is present
    variables = configurator.variables
    variables['model.name_underscored'] = \
        _dotted_to_underscored(variables['model.name_dotted'])
    variables['model.name_camelcased'] = \
        _dotted_to_camelcased(variables['model.name_dotted'])
    variables['model.name_camelwords'] = \
        _dotted_to_camelwords(variables['model.name_dotted'])
    variables['addon.name'] = \
        os.path.basename(os.path.normpath(configurator.target_directory))


def post_render_model(configurator):
    # make sure the models package is imported from the addon root
    _add_local_import(configurator, '',
                      'models')
    # add new model import in __init__.py
    _add_local_import(configurator, 'models',
                      configurator.variables['model.name_underscored'])
    # remove ACL
    if not configurator.variables['model.acl']:
        _delete_file(configurator, 'security',
                     configurator.variables['model.name_underscored'] + '.xml')
    # remove demo data
    if not configurator.variables['model.demo_data']:
        _delete_file(configurator, 'demo',
                     configurator.variables['model.name_underscored'] + '.xml')

    show_message(configurator)


#
# addon hooks
#


def pre_render_addon(configurator):
    variables = configurator.variables
    variables['addon.name_camelwords'] = \
        _underscored_to_camelwords(variables['addon.name'])


def post_render_addon(configurator):
    variables = configurator.variables
    if variables['addon.oca']:
        _rm_suffix('.oca', configurator, variables['addon.name'],
                   'README.rst.oca')
        _rm_suffix('.oca', configurator, variables['addon.name'],
                   'static', 'description', 'icon.svg.oca')
    else:
        _delete_file(configurator, variables['addon.name'],
                     'README.rst.oca')
        _delete_file(configurator, variables['addon.name'],
                     'static', 'description', 'icon.svg.oca')


#
# test hooks
#


def pre_render_test(configurator):
    _load_manifest(configurator)  # check manifest is present
    variables = configurator.variables
    variables['test.name_camelcased'] = \
        _underscored_to_camelcased(variables['test.name_underscored'])


def post_render_test(configurator):
    # add new test import in __init__.py
    _add_local_import(configurator, 'tests',
                      configurator.variables['test.name_underscored'])
