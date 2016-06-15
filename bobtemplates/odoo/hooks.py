# -*- coding: utf-8 -*-
# Copyright © 2016 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from mrbob.bobexceptions import ValidationError


def _camelcase(dotted):
    return ''.join([s.capitalize() for s in dotted.split('.')])


def _underscore(dotted):
    return dotted.replace('.', '_')


def post_model_name_dotted(configurator, question, answer):
    if '.' not in answer:
        raise ValidationError('Name must contain a dot')
    configurator.variables['model.name_underscored'] = _underscore(answer)
    configurator.variables['model.name_camelcased'] = _camelcase(answer)
    return answer
