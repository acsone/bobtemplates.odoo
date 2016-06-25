Changes
~~~~~~~

.. Future (?)
.. ----------
.. -

1.0.0b3 (2016-06-25)
--------------------
- [ADD] wizard template
- [IMP] model: auto-add view, demo data and acl in addon manifest
- [IMP] addon: put summary in description field if there is no README.rst
- [IMP] model: do not generate action view_type (which is mostly obsolete)
- [IMP] model: add model and context in action
- [IMP] model: add example field when not inherited
- [IMP] model: add default group in form view
- [IMP] model: do not generate an empty view xml file
- [FIX] model: menu name is mandatory when creating menu with a record entry

1.0.0b2 (2016-06-17)
--------------------
- [ADD] addon: add optional OCA mode (author, README.rst and icon.svg)
- [IMP] model: improve order of import in the model file
- [FIX] model: avoid to set ir.model.access data as non updatable record

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
