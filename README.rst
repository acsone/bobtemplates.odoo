bobtemplates.odoo
=================

.. image:: https://img.shields.io/badge/license-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl.html
   :alt: License: AGPL 3.0 or Later
.. image:: https://badge.fury.io/py/bobtemplates.odoo.svg
    :target: http://badge.fury.io/py/bobtemplates.odoo

``bobtemplates.odoo`` is a set of `mr.bob 
<https://http://mrbob.readthedocs.io/en/latest/>`_ 
templates to use when developing Odoo addons.

It provides the following templates

  * ``model``: an Odoo model with accompanying form, tree, action, menu and 
    basic ACL.

The following are candidates:

  * ``addon``: create an addon skeletton
  * ``report``
  * ``controller``

Install
~~~~~~~

  .. code:: shell

    pip install bobtemplates.odoo

Quickstart
~~~~~~~~~~

Add a new model in your current addon directory:

  .. code:: shell

    mrbob bobtemplates.odoo:model

Credits
~~~~~~~

Author:

  * Stéphane Bidoul (`ACSONE <http://acsone.eu/>`_)

Inspired by https://github.com/plone/bobtemplates.plone.

Maintainer
----------

.. image:: https://www.acsone.eu/logo.png
   :alt: ACSONE SA/NV
   :target: http://www.acsone.eu

This module is maintained by ACSONE SA/NV.
