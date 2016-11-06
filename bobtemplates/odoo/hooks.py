# -*- coding: utf-8 -*-
# Copyright © 2016 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import ast
import os
import re

from mrbob.bobexceptions import ValidationError
from mrbob.hooks import show_message
from pkg_resources import parse_version

ODOO_FIELDS = [
        'char',
        'int', 'integer',
        'date',
        'datetime',
        'text',
        'selection',
        'm2o', 'many2one',
        'm2m', 'many2many',
        'o2m', 'one2many',
        'bool', 'boolean',
        'bin', 'binary',
        'float',
]

def _fields_to_dict(fields):
    _fields = fields and fields.split(' ') or []
    res = {}
    for f in _fields:
        if f:
            attrs = f.split(':')
            field_name = attrs[0]
            field_string = _dotted_to_camelwords(field_name)
            for string in attrs :
                if string.strip() :
                    string = string.strip()
                    if string[0].isalpha()  and string[0] == string.capitalize()[0]:
                        field_string = string
            related_field = [x for x in attrs[1:] if '_' in x]
            related_field = related_field and related_field[0] or ''
            model = default = False
            groups = ''
            selection = []
            field_type = list(set(ODOO_FIELDS).intersection(set(attrs)))
            field_type = field_type and field_type[0] or False
            if field_type:
                attrs.remove(field_type)
            if field_type == 'o2m' : field_type = 'one2many'
            if field_type == 'm2m' : field_type = 'many2many'
            if field_type == 'm2o' : field_type = 'many2one'
            if field_type == 'bool' : field_type = 'boolean'
            if field_type == 'bin' : field_type = 'binary'
            if field_type == 'int' : field_type = 'integer'
            if not field_type:
                if field_name == 'sequence' :
                    field_type = 'integer'
                elif field_name == 'company_id' :
                    field_type = 'many2one'
                    model='res.company'
                elif field_name == 'currency_id' :
                    field_type = 'many2one'
                    model='res.currency'
                elif field_name == 'journal_id' :
                    field_type = 'many2one'
                    model='account.journal'
                elif field_name == 'account_id' :
                    field_type = 'many2one'
                    model='account.account'
                elif field_name == 'product_id' :
                    field_type = 'many2one'
                    model='product.product'
                elif field_name == 'company_id' :
                    field_type = 'many2one'
                    model='res.company'
                elif field_name == 'partner_id' :
                    field_type = 'many2one'
                    model='res.partner'
                elif field_name == 'user_id' :
                    field_type = 'many2one'
                    model='res.users'
                elif field_name == 'state' :
                    field_type = 'selection'
                    attrs.append('readonly')
                elif field_name.endswith('s_id'):
                    field_type = 'many2many'
                elif field_name.endswith('_id'):
                    field_type = 'many2one'
                elif field_name.endswith('_ids'):
                    field_type = 'one2many'
                elif 'amount' in field_name:
                    field_type = 'float'
                elif 'date' in field_name:
                    field_type = 'date'
                elif 'count' in field_name:
                    field_type = 'integer'
                elif 'active' in field_name:
                    field_type = 'integer'
                    default = True
            args = []
            extras = []
            if 'readonly' in attrs or 'ro' in attrs:
                args.append(('readonly' , True),)
            if 'required' in attrs :
                args.append(('required' ,True),)
            if 'store' in attrs :
                args.append(('store' ,True),)
            if 'nocopy' in attrs :
                args.append(('copy' ,False),)
            if 'translate' in attrs :
                args.append(('translate' ,True),)
            if 'nolist' in attrs or 'notree' in attrs:
                extras.append('notree')
            if 'noform' in attrs:
                extras.append('noform')
            if 'search' in attrs:
                extras.append('search')
            if 'compute' in attrs:
                extras.append('compute')
            if 'inverse' in attrs:
                extras.append('inverse')
                extras.append('compute')
                store_exists = False
                for i, arg in enumerate(args):
                    if arg[0] == 'store':
                        args[i] = ('store' ,False)
                        store_exists = True
                        break
                if not store_exists :
                    args.append(('store' ,False),)
            for attr in attrs:
                if ',' in attr :
                    selection = attr.split(',')
                    if selection:
                        default = selection[0]
                if '.' in attr :
                    model = attr
            if not field_type:
                if model and '.' in model:
                    field_type = 'many2one'
                else:
                    field_type = 'char'
            if model == 'res.company' and 'many' in field_type:
                groups='base.group_multi_company'
            if model == 'res.currency' and 'many' in field_type:
                groups='base.group_multi_currency'
            if default:
                if unicode(default) in ['now','today']:
                    if field_type == 'date':
                        default='lambda self: fields.Date.today()'
                    if field_type == 'datetime':
                        default='lambda self: fields.Datetime.now()'
                if unicode(default) in ['me','user']:
                    if field_type == 'many2one' or field_type == 'many2many':
                        default='lambda self: self.env.user'
                if unicode(default) in ['company']:
                    if field_type == 'many2one':
                        default='lambda self: self.env.user.company_id'
                if field_type == 'selection':
                    default = "'%s'" % default
            res[field_name] = (field_string, field_type, args, extras, model, [(x, x.capitalize()) for x in selection], default, related_field, groups)
    return res

def _dotted_to_camelcased(dotted):
    return ''.join([s.capitalize() for s in dotted.split('.')])


def _dotted_to_underscored(dotted):
    return dotted.replace('.', '_')

def _underscored_to_dotted(dotted):
    return dotted.replace('_', '.')


def _dotted_to_camelwords(dotted):
    return ' '.join([s.capitalize() for s in dotted.split('.')])


def _underscored_to_camelcased(underscored):
    return ''.join([s.capitalize() for s in underscored.split('_')])


def _underscored_to_camelwords(underscored):
    return ' '.join([s.capitalize() for s in underscored.split('_')])


def _delete_file(configurator, path):
    """ remove file and remove it's directories if empty """
    path = os.path.join(configurator.target_directory, path)
    os.remove(path)
    try:
        os.removedirs(os.path.dirname(path))
    except OSError:
        pass


def _open_manifest(configurator, mode='r'):
    manifest_path = os.path.join(configurator.target_directory,
                                 '__openerp__.py')
    if not os.path.exists(manifest_path):
        manifest_path = os.path.join(configurator.target_directory,
                                     '__manifest__.py')
        if not os.path.exists(manifest_path):
            raise ValidationError("{} not found".format(manifest_path))
    return open(manifest_path, mode)


def _load_manifest(configurator):
    with _open_manifest(configurator) as f:
        return ast.literal_eval(f.read())


def _insert_manifest_item(configurator, key, item):
    """ Insert an item in the list of an existing manifest key """
    with _open_manifest(configurator) as f:
        manifest = f.read()
    pattern = """(["']{}["']:\\s*\\[)""".format(key)
    repl = """\\1\n        '{}',""".format(item)
    manifest = re.sub(pattern, repl, manifest, re.MULTILINE)
    with _open_manifest(configurator, 'w') as f:
        f.write(manifest)


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


def _rm_suffix(suffix, configurator, path):
    path = os.path.join(configurator.target_directory, path)
    assert path.endswith(suffix)
    os.rename(path, path[:-len(suffix)])


#
# model hooks
#


def _model_has_view(variables):
    return (
        variables['model.view_form'] or
        variables['model.view_tree'] or
        variables['model.view_search'] or
        variables['model.view_menu']
    )


def pre_render_model(configurator):
    _load_manifest(configurator)  # check manifest is present
    variables = configurator.variables
    variables['odoo.version'] = \
        int(variables['odoo.version'])
    variables['model.name_underscored'] = \
        _dotted_to_underscored(variables['model.name_dotted'])
    variables['model.name_camelcased'] = \
        _dotted_to_camelcased(variables['model.name_dotted'])
    variables['model.fields_mapped'] = \
        _fields_to_dict(variables['model.fields'])
    variables['model.name_camelwords'] = \
        _dotted_to_camelwords(variables['model.name_dotted'])
    variables['addon.name'] = \
        os.path.basename(os.path.normpath(configurator.target_directory))


def post_render_model(configurator):
    variables = configurator.variables
    # make sure the models package is imported from the addon root
    _add_local_import(configurator, '',
                      'models')
    # add new model import in __init__.py
    _add_local_import(configurator, 'models',
                      variables['model.name_underscored'])
    # views
    view_path = 'views/{}.xml'.format(variables['model.name_underscored'])
    if _model_has_view(variables):
        _insert_manifest_item(configurator, 'data', view_path)
    else:
        _delete_file(configurator, view_path)
    # ACL
    acl_path = 'security/{}.xml'.format(variables['model.name_underscored'])
    if variables['model.acl']:
        _insert_manifest_item(configurator, 'data', acl_path)
    else:
        _delete_file(configurator, acl_path)
    # demo data
    demo_path = 'demo/{}.xml'.format(variables['model.name_underscored'])
    if variables['model.demo_data']:
        _insert_manifest_item(configurator, 'demo', demo_path)
    else:
        _delete_file(configurator, demo_path)
    # show message if any
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
        _rm_suffix('.oca', configurator, variables['addon.name'] +
                   '/README.rst.oca')
        _rm_suffix('.oca', configurator, variables['addon.name'] +
                   '/static/description/icon.png.oca')
    else:
        _delete_file(configurator, variables['addon.name'] +
                     '/README.rst.oca')
        _delete_file(configurator, variables['addon.name'] +
                     '/static/description/icon.png.oca')
    version = variables['addon.version']
    if parse_version(version) >= parse_version('10.0'):
        manifest_file = os.path.join(
            configurator.target_directory,
            variables['addon.name'] + '/__openerp__.py')
        manifest_new_file = os.path.join(
            configurator.target_directory,
            variables['addon.name'] + '/__manifest__.py')
        os.rename(manifest_file, manifest_new_file)
    # show message if any
    show_message(configurator)


#
# test hooks
#


def pre_render_test(configurator):
    _load_manifest(configurator)  # check manifest is present
    variables = configurator.variables
    variables['odoo.version'] = \
        int(variables['odoo.version'])
    variables['test.name_camelcased'] = \
        _underscored_to_camelcased(variables['test.name_underscored'])


def post_render_test(configurator):
    # add new test import in __init__.py
    _add_local_import(configurator, 'tests',
                      configurator.variables['test.name_underscored'])
    # show message if any
    show_message(configurator)


#
# wizard hooks
#


def _wizard_has_view(variables):
    return (
        variables['wizard.view_form'] or
        variables['wizard.view_action'] or
        variables['wizard.action_multi'] or
        variables['wizard.view_menu']
    )


def pre_render_wizard(configurator):
    _load_manifest(configurator)  # check manifest is present
    variables = configurator.variables
    variables['odoo.version'] = \
        int(variables['odoo.version'])
    variables['wizard.name_underscored'] = \
        _dotted_to_underscored(variables['wizard.name_dotted'])
    variables['wizard.name_camelcased'] = \
        _dotted_to_camelcased(variables['wizard.name_dotted'])
    variables['wizard.name_camelwords'] = \
        _dotted_to_camelwords(variables['wizard.name_dotted'])
    variables['addon.name'] = \
        os.path.basename(os.path.normpath(configurator.target_directory))


def post_render_wizard(configurator):
    variables = configurator.variables
    # make sure the wizards package is imported from the addon root
    _add_local_import(configurator, '',
                      'wizards')
    # add new wizard import in __init__.py
    _add_local_import(configurator, 'wizards',
                      variables['wizard.name_underscored'])
    # views
    view_path = 'wizards/{}.xml'.format(variables['wizard.name_underscored'])
    if _wizard_has_view(variables):
        _insert_manifest_item(configurator, 'data', view_path)
    else:
        _delete_file(configurator, view_path)
    # show message if any
    show_message(configurator)
