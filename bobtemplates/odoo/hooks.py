# -*- coding: utf-8 -*-
# Copyright © 2016 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import os

from mrbob.bobexceptions import ValidationError
from mrbob.hooks import show_message


def _dotted_to_camelcased(dotted):
    return ''.join([s.capitalize() for s in dotted.split('.')])


def _dotted_to_underscored(dotted):
    return dotted.replace('.', '_')


def _dotted_to_camelwords(underscored):
    return ' '.join([s.capitalize() for s in underscored.split('.')])


def _underscored_to_camelwords(underscored):
    return ' '.join([s.capitalize() for s in underscored.split('_')])


def _open_file(mode, configurator, *args):
    path = os.path.join(configurator.target_directory, *args)
    return open(path, mode)


def _delete_file(configurator, *args):
    path = os.path.join(configurator.target_directory, *args)
    try:
        os.remove(path)
    except OSError:
        pass


def _delete_dir(configurator, *args):
    path = os.path.join(configurator.target_directory, *args)
    try:
        os.rmdir(path)
    except OSError:
        pass


def post_question_model_name_dotted(configurator, question, answer):
    if '.' not in answer:
        raise ValidationError('Name must contain a dot')
    configurator.variables['model.name_underscored'] = \
        _dotted_to_underscored(answer)
    configurator.variables['model.name_camelcased'] = \
        _dotted_to_camelcased(answer)
    configurator.variables['model.name_camelwords'] = \
        _dotted_to_camelwords(answer)
    return answer


def pre_render_model(configurator):
    configurator.variables['addon.name'] = \
        os.path.basename(os.path.normpath(configurator.target_directory))


def post_render_model(configurator):
    # add model import in __init__.py
    with _open_file('a', configurator, 'models', '__init__.py') as init_file:
        init_file.write('from . import {}\n'.format(
            configurator.variables['model.name_underscored']))
    # remove ACL
    if not configurator.variables['model.acl']:
        _delete_file(configurator, 'security',
                     configurator.variables['model.name_underscored'] + '.xml')
        _delete_dir(configurator, 'security')
    # remove demo data
    if not configurator.variables['model.demo_data']:
        _delete_file(configurator, 'demo',
                     configurator.variables['model.name_underscored'] + '.xml')
        _delete_dir(configurator, 'demo')

    show_message(configurator)
