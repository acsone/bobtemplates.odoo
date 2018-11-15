# -*- coding: utf-8 -*-
# Copyright © 2016 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import os
import shutil
import tempfile
import unittest

from scripttest import TestFileEnvironment


class BaseTemplateTest(unittest.TestCase):

    # credit bobtemplates.plone

    def setUp(self):
        self.maxDiff = None
        self.tempdir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tempdir)

        # docs http://pythonpaste.org/scripttest/
        self.env = TestFileEnvironment(
            os.path.join(self.tempdir, "test-output"), ignore_hidden=False
        )

    def create_template(self):
        """Run mr.bob to create your template."""
        options = {
            "dir": os.path.join(os.path.dirname(__file__)),
            "template": self.template,
            "addon": self.addon,
            "answers_file": self.answers_file,
            "target_dir": self.target_dir,
        }
        return self.env.run(
            "mrbob -O %(target_dir)s --config "
            "%(dir)s/%(answers_file)s bobtemplates.odoo:%(template)s" % options
        )


class OdooTemplatesTest(BaseTemplateTest):
    template = ""
    addon = "addon_foo"
    answers_file = ""
    target_dir = ""

    def _create_addon(self):
        self.template = "addon"
        self.answers_file = "test_odoo_addon_answers.ini"
        self.target_dir = "."
        return self.create_template()

    def test_odoo_addon(self):
        result = self._create_addon()
        self.assertEqual(
            set(result.files_created.keys()),
            {
                self.addon,
                self.addon + "/__init__.py",
                self.addon + "/__manifest__.py",
                self.addon + "/README.rst",
                self.addon + "/static",
                self.addon + "/static/description",
                self.addon + "/static/description/icon.png",
            },
        )

    def test_odoo_model(self):
        self._create_addon()
        self.template = "model"
        self.answers_file = "test_odoo_model_answers.ini"
        self.target_dir = "addon_foo"
        result = self.create_template()
        self.assertEqual(
            set(result.files_created.keys()),
            {
                self.addon + "/models",
                self.addon + "/models/foo_model.py",
                self.addon + "/models/__init__.py",
                self.addon + "/views",
                self.addon + "/views/foo_model.xml",
                self.addon + "/demo",
                self.addon + "/demo/foo_model.xml",
                self.addon + "/security",
                self.addon + "/security/foo_model.xml",
            },
        )

    def test_odoo_test(self):
        self._create_addon()
        self.template = "test"
        self.answers_file = "test_odoo_test_answers.ini"
        self.target_dir = "addon_foo"
        result = self.create_template()
        self.assertEqual(
            set(result.files_created.keys()),
            {
                self.addon + "/tests",
                self.addon + "/tests/test_foo.py",
                self.addon + "/tests/__init__.py",
            },
        )

    def test_odoo_wizard(self):
        self._create_addon()
        self.template = "wizard"
        self.answers_file = "test_odoo_wizard_answers.ini"
        self.target_dir = "addon_foo"
        result = self.create_template()
        self.assertEqual(
            set(result.files_created.keys()),
            {
                self.addon + "/wizards",
                self.addon + "/wizards/foo_wizard.py",
                self.addon + "/wizards/__init__.py",
                self.addon + "/wizards/foo_wizard.xml",
            },
        )
