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


def post_render_model(configurator):
    init_path = os.path.join(configurator.target_directory,
                             'models', '__init__.py')
    with open(init_path, 'a') as init_file:
        init_file.write('from . import {}\n'.format(
            configurator.variables['model.name_underscored']))
    show_message(configurator)
