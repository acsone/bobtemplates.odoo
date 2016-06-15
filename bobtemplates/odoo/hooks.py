# -*- coding: utf-8 -*-
# Copyright © 2016 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from mrbob.bobexceptions import ValidationError


def to_boolean(configurator, question, answer):
    """
    If you want to convert an answer to Python boolean, you can
    use this function as :ref:`post-question-hook`:
    .. code-block:: ini
        [questions]
        idiot.question = Are you young?
        idiot.post_ask_question = mrbob.hooks:to_boolean
    Following variables can be converted to a boolean:
    **y, n, yes, no, true, false, 1, 0**
    """
    if isinstance(answer, bool):
        return answer
    value = answer.lower()
    if value in ['y', 'yes', 'true', '1']:
        return True
    elif value in ['n', 'no', 'false', '0']:
        return False
    else:
        raise ValidationError('Value must be a boolean (y/n)')


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
