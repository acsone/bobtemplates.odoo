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


def _underscored_to_camelwords(underscored):
    return ' '.join([s.capitalize() for s in underscored.split('_')])


def post_question_model_name_dotted(configurator, question, answer):
    if '.' not in answer:
        raise ValidationError('Name must contain a dot')
    configurator.variables['model.name_underscored'] = \
        _dotted_to_underscored(answer)
    configurator.variables['model.name_camelcased'] = \
        _dotted_to_camelcased(answer)
    return answer


def pre_render_model(configurator):
    configurator.variables['addon.name'] = \
        os.path.basename(os.path.normpath(configurator.target_directory))


def post_render_model(configurator):
    # add model import in __init__.py
    init_path = os.path.join(configurator.target_directory,
                             'models', '__init__.py')
    with open(init_path, 'a') as init_file:
        init_file.write('from . import {}\n'.format(
            configurator.variables['model.name_underscored']))
    # acl file
    security_path = os.path.join(configurator.target_directory, 'security')
    security_csv_name = 'ir.model.access.' + \
        configurator.variables['model.name_underscored'] + '.csv'
    if not configurator.variables['model.acl']:
        os.remove(os.path.join(security_path, security_csv_name))
        try:
            os.rmdir(security_path)
        except OSError:
            # not empty, probably
            pass
    else:
        print("Do not forget to add {} "
              "in __openerp__.py data section.".format(
                  "security/" + security_csv_name))

    show_message(configurator)
