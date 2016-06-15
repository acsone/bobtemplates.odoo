#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2016 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from setuptools import setup

setup(
    name='bobtemplates.odoo',
    version='1.0.0a1',
    description='Templates for Odoo projects',
    long_description='\n'.join((
        open('README.rst').read(),
        open('CHANGES.rst').read(),
    )),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: '
        'GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    license='LGPLv3',
    author='ACSONE SA/NV',
    author_email='info@acsone.eu',
    url='http://github.com/acsone/bobtemplates.odoo',
    install_requires=[
        'mr.bob',
    ],
    include_package_data=True,
    setup_requires=['setuptools-git'],
)
