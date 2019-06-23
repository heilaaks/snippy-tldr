# SPDX-License-Identifier: Apache-2.0

# Disable default suffixes and rules to reduce spam with make --debug
# option. This is a Python project and these builtins are not needed.
MAKEFLAGS += --no-builtin-rules
MAKEFLAGS += --no-builtin-variables

DEV_VERSION    ?= 0.2a0
TAG_VERSION    ?= 0.1.0

PIP            ?= pip
PYTHON         ?= python
PYTHON_VERSION ?= $(shell python -c 'import sys; print(sys.version_info[0])')
INSTALL_USER   ?=
COVERAGE       ?= --cov snippy_tldr --cov-branch
QUIET          ?= -qq
V              ?=

# Enable verbose print with 'make [target] V=1'.
$(V).SILENT:

# The new pyproject.toml from PEP517 does not support --editable install.
# It is not possible to run --user install inside a virtual environment.
install:
	$(PIP) install $(QUIET) $(INSTALL_USER) .

upgrade:
	$(PIP) install --upgrade $(QUIET) $(INSTALL_USER) .

uninstall:
	$(PIP) uninstall $(QUIET) --yes snippy-tldr

upgrade-wheel:
	test -x "$(shell which pip)" || $(PYTHON) -m ensurepip $(INSTALL_USER)
	$(PYTHON) -m pip install pip setuptools wheel twine --upgrade $(QUIET) $(INSTALL_USER)

install-devel:
	$(PYTHON) -m pip install $(QUIET) $(INSTALL_USER) .[devel]

install-tests:
	$(PYTHON) -m pip install $(QUIET) $(INSTALL_USER) .[tests]

install-coverage:
	$(PYTHON) -m pip install $(QUIET) $(INSTALL_USER) codecov coveralls

outdated:
	$(PYTHON) -m pip list --outdated

.PHONY: docs
docs:
	make -C docs html

.PHONY: tests
tests:
	$(PYTHON) -m pytest -x ${COVERAGE}

tests-tox:
	tox

coverage:
	$(PYTHON) -m pytest ${COVERAGE} --cov-report html

lint:
	$(PYTHON) -m pylint --jobs=0 snippy_tldr/
	$(PYTHON) -m pylint --jobs=0 tests/

format:
	black snippy_tldr
	black tests
	black setup.py

clean: clean-build clean-pyc clean-tests

clean-all: clean

clean-build:
	rm -drf .cache
	rm -drf build
	rm -drf dist
	rm -drf docs/build/*
	rm -drf pip-wheel-metadata
	rm -drf snippy.egg-info
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-tests:
	rm -drf .cache
	rm -drf .coverage
	rm -drf .pytest_cache
	rm -drf .tox
	rm -drf htmlcov
	rm -f .coverage.*
	rm -f coverage.xml
	rm -f pytestdebug.log
	rm -f snippy.bash-completion

help:
	@echo 'Cleaning targets:'
	@echo '  clean                 - Clean all targets.'
	@echo ''
	@echo 'Testing targets:'
	@echo '  tests                 - Run tests.'
	@echo ''
	@echo 'Debugging examples:'
	@echo '  make [target] --debug - Enable Makefile debugging.'
	@echo '  make [target] V=1     - Enable Makefile verbose targets.'
	@echo '  make [target] QUIET=  - Enable pip verbose build.'
	@echo ''
	@echo 'Variable usage precedence:'
	@echo '  1. Makefile variable defined from command line.'
	@echo '  2. Makefile variable defined from environment variable.'
	@echo '  3. Makefile variable default.'
	@echo ''
	@echo 'For further information see the 'development.rst' file'
