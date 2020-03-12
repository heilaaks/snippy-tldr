Development
===========

Installation
------------

The instructions are tested with Fedora 30 and Bash shell.

.. note::

   The instructions install virtual environments with ``python3`` and add
   the Python 3 virtual environment modules to Python user script directory.
   This allows for example creating own Linux user for Snippy-tldr development
   which has an isolated virtual environment setup from global Python modules.

   In case you want different virtual environment setup, you have to modify
   the examples.

   The virtual environments are installed under ``${HOME}/.cache/snippy-tldr``.

.. note::

   The installation instructions add new software packages. Execute at your
   own risk.

Fedora
~~~~~~

Follow the instructions to install the project on a Fedora Linux.

.. code:: bash

    # Clone the project from the GitHub.
    mkdir -p ${HOME}/.cache/snippy-tldr
    mkdir -p ${HOME}/.local/share/snippy-tldr
    mkdir -p ${HOME}/devel/snippy-tldr && cd $_
    git clone https://github.com/heilaaks/snippy-tldr.git .

    # Install CPython versions.
    sudo dnf install -y \
        python27 \
        python34 \
        python35 \
        python36 \
        python37 \
        python38 \
        python3-devel \
        python2-devel

    # Upgrade CPython versions.
    sudo dnf upgrade -y \
        python27 \
        python34 \
        python35 \
        python36 \
        python37 \
        python38 \
        python3-devel \
        python2-devel

    # Install PyPy versions.
    sudo dnf install -y \
        pypy2 \
        pypy3 \
        pypy2-devel \
        pypy3-devel \
        postgresql-devel

    # Upgrade PyPy versions.
    sudo dnf upgrade -y \
        pypy2 \
        pypy3 \
        pypy2-devel \
        pypy3-devel \
        postgresql-devel

    # Below are 'generic instructions' that can be used also with other
    # Linux distributions.

    # Upgrade pip.
    pip install --upgrade pip

    # Install Python virtual environments.
    pip3 install --user --upgrade \
        pipenv \
        virtualenv \
        virtualenvwrapper

    # Enable virtualenvwrapper and add the Python user script directory
    # to the path if needed.
    vi ~/.bashrc
        # Snippy-tldr development settings.
        [[ ":$PATH:" != *"${HOME}/.local/bin"* ]] && PATH="${PATH}:${HOME}/.local/bin"
        export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
        export VIRTUALENVWRAPPER_VIRTUALENV=${HOME}/.local/bin/virtualenv
        export WORKON_HOME=${HOME}/.cache/snippy-tldr/.virtualenvs
        source virtualenvwrapper.sh
        cd ${HOME}/devel/snippy-tldr
        workon snippy-tldr-python3.7
    source ~/.bashrc

    # Create virtual environments.
    for PYTHON in python2.7 \
                  python3.4 \
                  python3.5 \
                  python3.6 \
                  python3.7 \
                  python3.8 \
                  pypy \
                  pypy3
    do
        if which ${PYTHON} > /dev/null 2>&1; then
            printf "create snippy-tldr venv for ${PYTHON}\033[39G: "
            mkvirtualenv --python $(which ${PYTHON}) snippy-tldr-${PYTHON} > /dev/null 2>&1
            if [[ -n "${VIRTUAL_ENV}" ]]; then
                printf "\033[32mOK\033[0m\n"
            else
                printf "\e[31mNOK\033[0m\n"
            fi
            deactivate > /dev/null 2>&1
        fi
    done

    # Install virtual environments. Some versions are not pinned.
    for VENV in $(lsvirtualenv -b | grep snippy-tldr-py)
    do
        workon ${VENV}
        printf "deploy venv ${VENV}\033[39G: "
        if [[ ${VIRTUAL_ENV} == *${VENV}* ]]; then
            make upgrade-wheel PIP_CACHE=--no-cache-dir
            make install-devel PIP_CACHE=--no-cache-dir
            printf "\033[32mOK\033[0m\n"
        else
            printf "\e[31mNOK\033[0m\n"
        fi
        deactivate > /dev/null 2>&1
    done

    # Example how to delete Snippy-tldr virtual environments.
    deactivate > /dev/null 2>&1
    for VENV in $(lsvirtualenv -b | grep snippy-tldr-py)
    do
        printf "delete venv ${VENV}\033[39G: "
        rmvirtualenv ${VENV} > /dev/null 2>&1
        printf "\033[32mOK\033[0m\n"
    done

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
make tests target.

.. code:: bash

    # Run the development tests.
    make tests

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
   :private-members:
   :member-order: bysource
