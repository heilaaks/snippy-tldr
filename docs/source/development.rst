Development
===========

Installation
------------

To install, run:

.. code:: bash

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

The documentation includes manual and automated documentation. Automated
documentation is extracted from source code docstrings.

.. code:: bash

    # Create documents.
    make docs

    # Open the document in a web brower.
    file:///<home>/devel/snippy-tldr/docs/build/html/development.html

Relasing
--------

  .. code-block:: bash

      # Test PyPI installation before official release into PyPI.
      make clean-all
      python setup.py sdist bdist_wheel
      twine check dist/*
      twine upload --repository-url https://test.pypi.org/legacy/ dist/*

      # Create a tag where the version follows semating versioning 2.0.0.
      git tag -a 0.1.0 -m "Add new release 0.1.0"
      git push -u origin 0.1.0

      # Releast into PyPi.
      make clean-all
      python setup.py sdist bdist_wheel
      twine upload dist/*

Modules
-------

snippy_tldr.plugin
~~~~~~~~~~~~~~~~~~

Description
```````````

Design
``````

.. automodule:: snippy_tldr.plugin
   :members:
   :member-order: bysource
