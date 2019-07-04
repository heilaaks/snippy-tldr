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

To import one tldr page from GitHub, run:

.. code:: text

    snippy import --plugin tldr --file https://github.com/tldr-pages/tldr/blob/master/pages/linux/alpine.md

To import all English translated tldr pages for Linux from GitHub, run:

.. code:: text

    snippy import --plugin tldr

To import all tldr pages from one platform from GitHub, run:

.. code:: text

    snippy import --plugin tldr --file https://github.com/tldr-pages/tldr/tree/master/pages/osx

To import all Chinese translated tldr pages from GitHub, run:

.. code:: text

    snippy import --plugin tldr --file https://github.com/tldr-pages/tldr/tree/master/pages.zh

To import one tldr page from local file system, run:

.. code:: text

    snippy import --plugin tldr --file ./tldr/pages/linux/apk.md

To import all Linux platform tldr pages from local file system, run:

.. code:: text

    snippy import --plugin tldr --file ./tldr/pages/linux

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
