# -*- coding: utf-8 -*-
# Copyright © 2016 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import unittest
import os
import tempfile
import shutil

from scripttest import TestFileEnvironment


class BaseTemplateTest(unittest.TestCase):

    # credit bobtemplates.plone

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tempdir)

        # docs http://pythonpaste.org/scripttest/
        self.env = TestFileEnvironment(
            os.path.join(self.tempdir, 'test-output'),
            ignore_hidden=False,
        )

    def create_template(self):
        """Run mr.bob to create your template."""
        options = {
            'dir': os.path.join(os.path.dirname(__file__)),
            'template': self.template,
            'addon': self.addon,
            'answers_file': self.answers_file,
            'target_dir': self.target_dir,
        }
        return self.env.run(
            'mrbob -O %(target_dir)s --config '
            '%(dir)s/%(answers_file)s bobtemplates.odoo:%(template)s'
            % options)


class PloneTemplateTest(BaseTemplateTest):
    """Tests for the `plone_addon` template."""
    template = ''
    addon = ''
    answers_file = ''
    target_dir = '.'

    def test_odoo_addon(self):
        self.template = 'addon'
        self.addon = 'addon_foo'
        self.answers_file = 'test_odoo_addon_answers.ini'
        self.target_dir = '.'
        self.maxDiff = None
        result = self.create_template()
        self.assertItemsEqual(
            result.files_created.keys(),
            [
                self.addon,
                self.addon + '/__init__.py',
                self.addon + '/__openerp__.py',
            ]
        )
