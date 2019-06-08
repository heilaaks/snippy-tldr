Development
===========

Installation
------------

To install, run:

.. code:: text

    pip install snippy-tldr --user

Workflows
---------

Testing
~~~~~~~

For the snippy-tldr development, prefer a virtual environment with the
latest Python release and Python 2.7. The continuous integration will
run all the tests against all supported Python version but the most
problems can be captured by testing with the latest Python 3 version
and Python 2.7.

.. code:: bash

    # Work in a Python virtual environment.
    workon snippy-tldr-python3.7

The snippy-tldr continuous integration will run all tests the same
make test target.

.. code:: bash

    # Run the development tests.
    make test

Documentation
~~~~~~~~~~~~~

TODO

Relasing
--------

  .. code-block:: text

      # Test PyPI installation before official release into PyPI.
      > https://testpypi.python.org/pypi
      make clean-all
      python setup.py sdist bdist_wheel
      twine check dist/*
      twine upload --repository-url https://test.pypi.org/legacy/ dist/*
