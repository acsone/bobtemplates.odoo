#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright © 2016 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from setuptools import find_packages, setup

setup(
    name="bobtemplates.odoo",
    use_scm_version=True,
    description="mr.bob templates for Odoo projects",
    long_description="\n".join((open("README.rst").read(), open("CHANGES.rst").read())),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: "
        "GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Odoo",
    ],
    license="LGPLv3",
    author="ACSONE SA/NV",
    author_email="info@acsone.eu",
    url="http://github.com/acsone/bobtemplates.odoo",
    install_requires=["mr.bob"],
    packages=find_packages(exclude=["tests"]),
    # TODO: bobtemplates.odoo should be a ns package too but that breaks mr.bob
    namespace_packages=["bobtemplates"],
    include_package_data=True,
    setup_requires=["setuptools_scm"],
)
