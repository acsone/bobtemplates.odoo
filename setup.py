#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2016 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from setuptools import setup, find_packages

setup(
    name='bobtemplates.odoo',
    version='1.1.0',
    description='mr.bob templates for Odoo projects',
    long_description='\n'.join((
        open('README.rst').read(),
        open('CHANGES.rst').read(),
    )),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: '
        'GNU Affero General Public License v3 or later (AGPLv3+)',
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
    packages=find_packages(exclude=['tests']),
    # TODO: bobtemplates.odoo should be a ns package too but that breaks mr.bob
    namespace_packages=['bobtemplates'],
    include_package_data=True,
    setup_requires=['setuptools-git'],
)
