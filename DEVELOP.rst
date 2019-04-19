How to set up dev environment
=============================

* run ``tox -e dev`` (if not installed ``apt-get install tox``)
* run ``. ./.tox/dev/bin/activate``

How to run tests
================

* run ``deactivate`` - if you are currently in a dev pyenvironment
* run ``tox``

How to release
==============

* update changelog in CHANGES.rst, referring to the next version
* python setup.py check --restructuredtext
* commit everything
* make sure tests pass!
* git tag <version>, where <version> is pep 440 compliant
* git push --tags

Uploading of tagged versions to pypi will be taken care of by travis.
