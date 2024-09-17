Changes
~~~~~~~

.. Future (?)
.. ----------
.. -

3.2.0 (2024-09-17)
------------------

- Odoo 18 support

3.1.0 (2023-06-13)
------------------

- [IMP] Remove view name for Odoo >= 12

3.0.0 (2022-12-14)
------------------

- Support python 3.11. Remove support of python 3.6.
- [IMP] wizard: no api.multi decorator in Odoo >= 13


2.1.0 (2022-10-20)
------------------

- [IMP] addon: add a question to generate the README file or not

2.0.0 (2022-09-26)
------------------

- Support python 3.10. Remove support of python < 3.6.

1.5.2 (2022-09-29)
------------------

- [FIX] Fix readme template

1.5.1 (2022-09-29)
------------------

- [CHG] Update readme

1.5.0 (2022-09-29)
------------------

- [ADD] Add readme template
- [CHG] Download fragments from https://github.com/OCA/maintainer-tools
  for OCA module (for usage of oca-gen-addon-readme)

1.4.1 (2022-02-18)
------------------
- [IMP] GNU: Change url to https

1.4.0 (2021-08-13)
------------------
- [ADD] Odoo 13 and 14 support
- [IMP] use python3 super()
- [IMP] better pep8 compatibility

1.3.0 (2018-11-23)
------------------
- [IMP] Some Odoo 11/12 support (default to 12)
- [IMP] Do not add utf-8 headers to python 3 files
- [IMP] Support python 3.6

1.2.1 (2018-09-18)
------------------
- [FIX] indentation in the wizard view
- [IMP] Test Template: allow to choose test class
- [FIX] prevent repeated imports in __init__.py

1.2.0 (2017-09-11)
------------------
- [CHG] The data tag in XML file is no longer required in version 9 and following
- [FIX] issue when adding imports to __init__.py
- [IMP] better button template in form views

1.1.2 (2017-04-07)
------------------
- updated pypi trove classifiers, no functional changer

1.1.1 (2017-01-14)
------------------
- [FIX] wizard: Return correct action type
- [IMP] do not add items (eg views) that already exists in manifest

1.1.0 (2016-10-28)
------------------
- [IMP] Odoo 10.0 support

1.0.1 (2016-09-09)
------------------
- [FIX] packaging error in 1.0.0 (removed icon.svg.oca)

1.0.0 (2016-09-01)
------------------
- [IMP] wizard: improve form view template
- [IMP] wizard: use 'new' target in wizard action
- [ADD] wizard: add action in More/Action menu
- [FIX] wizard: remove parenthesis in multi decorator that caused crash in Odoo 8.0
- [FIX] addon: for OCA addons, generate icon.png instead of icon.svg
- [IMP] wizard, model: use <odoo> instead of <openerp> for Odoo >= 9.0

1.0.0b3 (2016-06-25)
--------------------
- [ADD] wizard template
- [IMP] model: auto-add view, demo data and acl in addon manifest
- [IMP] addon: put summary in description field if there is no README.rst
- [IMP] model: do not generate action view_type (which is mostly obsolete)
- [IMP] model: add domain and context in action
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
