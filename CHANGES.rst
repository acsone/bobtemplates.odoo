Changes
~~~~~~~

.. Future (?)
.. ----------
.. -

1.0.0b3 (unreleased)
--------------------
- model: auto-add view, demo data and acl in addon manifest
- addon: put summary in description field if there is no README.rst

1.0.0b2 (2016-06-17)
--------------------
- addon: add optional OCA mode (author, README.rst and icon.svg)
- model: improve order of import in the model file
- model: avoid to set ir.model.access data as non updatable record

1.0.0b1 (2016-06-16)
--------------------
- add post render message inviting the user to add the generated xml
  files in __openerp__.py data section
- auto add model import to models/__init__.py
- many improvements and fixes to the model template (views, security,
  demo data, and more)
- addon template
- test template
- tests (with tox and travis)

1.0.0a2 (2016-06-15)
--------------------
- fix broken namespace package distribution

1.0.0a1 (2016-06-15)
--------------------
- first version, very rough template for an Odoo model with view
