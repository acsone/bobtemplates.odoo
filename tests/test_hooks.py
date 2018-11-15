# -*- coding: utf-8 -*-
# Copyright © 2016 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import unittest

from bobtemplates.odoo import hooks


class TestHooks(unittest.TestCase):
    def test_name_converters(self):
        self.assertEqual("ModelName", hooks._dotted_to_camelcased("model.name"))
        self.assertEqual("model_name", hooks._dotted_to_underscored("model.name"))
        self.assertEqual("Model Name", hooks._dotted_to_camelwords("model.name"))
        self.assertEqual("ModelName", hooks._underscored_to_camelcased("model_name"))
        self.assertEqual("Model Name", hooks._underscored_to_camelwords("model_name"))
