|badge-pypiv| |badge-pys| |badge-pyv| |badge-cov| |badge-docs| |badge-build| |badge-black|

Snippy-tldr
===========

Snippy_ plugin to import tldr_ man pages.

Installation
============

To install, run:

.. code:: text

    pip install snippy-tldr --user

Usage
=====

To import all English translated tldr Linux man pages from GitHub, run:

.. code:: text

    snippy import --plugin tldr

To import one man page from GitHub, run:

.. code:: text

    snippy import --plugin tldr --file https://github.com/tldr-pages/tldr/blob/master/pages/linux/alpine.md

To import all operating system man pages from GitHub, run:

.. code:: text

    snippy import --plugin tldr --file https://github.com/tldr-pages/tldr/tree/master/pages/osx

To import one tldr man page translation from GitHub, run:

.. code:: text

    snippy import --plugin tldr --file https://github.com/tldr-pages/tldr/tree/master/pages.zh

To import tldr man pages locally, run:

.. code:: text

    snippy import --plugin tldr --file ./tldr/pages/linux

To import one tldr man page locally, run:

.. code:: text

    snippy import --plugin tldr --file ./tldr/pages/linux/apk.md

.. _Snippy: https://github.com/heilaaks/snippy

.. _tldr: https://github.com/tldr-pages/tldr

.. |badge-pypiv| image:: https://img.shields.io/pypi/v/snippy-tldr.svg
   :target: https://pypi.python.org/pypi/snippy-tldr

.. |badge-pys| image:: https://img.shields.io/pypi/status/snippy-tldr.svg
   :target: https://pypi.python.org/pypi/snippy-tldr

.. |badge-pyv| image:: https://img.shields.io/pypi/pyversions/snippy-tldr.svg
   :target: https://pypi.python.org/pypi/snippy-tldr

.. |badge-cov| image:: https://codecov.io/gh/heilaaks/snippy-tldr/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/heilaaks/snippy-tldr

.. |badge-docs| image:: https://readthedocs.org/projects/snippy-tldr/badge/?version=latest
   :target: http://snippy-tldr.readthedocs.io/en/latest/?badge=latest

.. |badge-build| image:: https://travis-ci.org/heilaaks/snippy-tldr.svg?branch=master
   :target: https://travis-ci.org/heilaaks/snippy-tldr

.. |badge-black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/python/black
