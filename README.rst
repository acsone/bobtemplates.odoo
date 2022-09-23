bobtemplates.odoo
=================

.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: https://www.gnu.org/licenses/agpl.html
   :alt: License: AGPL 3.0 or Later
.. image:: https://badge.fury.io/py/bobtemplates.odoo.svg
   :target: http://badge.fury.io/py/bobtemplates.odoo
.. image:: https://travis-ci.org/acsone/bobtemplates.odoo.svg?branch=master
   :target: https://travis-ci.org/acsone/bobtemplates.odoo

``bobtemplates.odoo`` is a set of `mr.bob
<https://mrbob.readthedocs.io/en/latest/>`_
templates to use when developing Odoo addons.

It provides the following templates:

  * ``addon``: an addon skeletton, with readme file and fragments/icon for OCA addon
  * ``model``: an Odoo model with accompanying form, tree, action, menu,
    demo data and ACL
  * ``test``: a test class
  * ``wizard``: a wizard with transient model, view and action
  * ``readme``: Add readme file or fragments for OCA addon

The following are candidates (pull requests welcome):

  * ``report``
  * ``controller``
  * ``widget``

Install
~~~~~~~

  .. code:: shell

    pip install bobtemplates.odoo

Quickstart
~~~~~~~~~~

CAUTION: it is recommanded to backup or vcs commit your current
directory before running these commands, so you can easily see
what has been generated and/or changed.

Create a new addon in the current directory:

  .. code:: shell

    mrbob bobtemplates.odoo:addon

Now go to the newly created addon directory and run this to
add a new model, with associated views, demo data, and acl:

  .. code:: shell

    mrbob bobtemplates.odoo:model

Add a test class:

  .. code:: shell

    mrbob bobtemplates.odoo:test

Tip: read the `mr.bob user guide
<http://mrbob.readthedocs.io/en/latest/userguide.html>`_.
In particular it explains how to set default values to avoid
retyping the same answers at each run (such as the copyright
author).

Useful links
~~~~~~~~~~~~

* pypi page: https://pypi.python.org/pypi/bobtemplates.odoo
* code repository: https://github.com/acsone/bobtemplates.odoo
* report issues at: https://github.com/acsone/bobtemplates.odoo/issues

Credits
~~~~~~~

Author:

  * Stéphane Bidoul (`ACSONE <http://acsone.eu/>`_)

Inspired by https://github.com/plone/bobtemplates.plone.

Contributors:

  * Adrien Peiffer (`ACSONE <http://acsone.eu/>`_)
  * Olivier Laurent (`ACSONE <http://acsone.eu/>`_)
  * Mohamed Cherkaoui
  * Thomas Binsfeld (`ACSONE <http://acsone.eu/>`_)

Maintainer
----------

.. image:: https://www.acsone.eu/logo.png
   :alt: ACSONE SA/NV
   :target: http://www.acsone.eu

This module is maintained by ACSONE SA/NV.
