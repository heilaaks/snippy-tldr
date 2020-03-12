# SPDX-License-Identifier: Apache-2.0

# Disable default suffixes and rules to reduce spam with make --debug
# option. This is a Python project and these built-ins are not needed.
MAKEFLAGS += --no-builtin-rules
MAKEFLAGS += --no-builtin-variables

DEV_VERSION    ?= 0.2a0
TAG_VERSION    ?= 0.1.0

PIP            ?= pip
PIP_CACHE      ?=
PIP_PROXY      ?= ""
PIP_UPGRADE    ?= --upgrade --upgrade-strategy eager
PYTHON         ?= python
PYTHON_VERSION ?= $(shell python -V 2>&1 | grep -Po '(?<=Python )(.+)')
INSTALL_USER   ?=
COVERAGE       ?= --cov snippy_tldr --cov-branch
QUIET          ?= -qq
V              ?=

# Enable verbose print with 'make [target] V=1'.
$(V).SILENT:

# Python 3.4 seems to fail a local installation for unknown reason.
# This is a workaround to force the '--no-cache-dir' that seems to
# fix the problem: 'BadZipfile: File is not a zip file'.
ifneq (,$(findstring 3.4,$(PYTHON_VERSION)))
PIP_CACHE = --no-cache-dir
endif

# The new pyproject.toml from PEP517 does not support --editable install.
# It is not possible to run --user install inside a virtual environment.
install:
	$(PIP) install $(PIP_CACHE) $(INSTALL_USER) $(QUIET) --proxy $(PIP_PROXY) .

upgrade:
	$(PIP) install $(PIP_UPGRADE) $(PIP_CACHE) $(INSTALL_USER) $(QUIET) --proxy $(PIP_PROXY) .

uninstall:
	$(PIP) uninstall $(QUIET) --yes snippy-tldr

upgrade-wheel:
	test -x "$(shell which pip)" || $(PYTHON) -m ensurepip $(INSTALL_USER)
	$(PYTHON) -m pip install $(PIP_UPGRADE) $(PIP_CACHE) $(INSTALL_USER) $(QUIET) pip setuptools wheel twine

install-devel:
	$(PYTHON) -m pip install $(PIP_UPGRADE) $(PIP_CACHE) $(INSTALL_USER) $(QUIET) --proxy $(PIP_PROXY) .[devel]

install-tests:
	$(PYTHON) -m pip install $(PIP_UPGRADE) $(PIP_CACHE) $(INSTALL_USER) $(QUIET) --proxy $(PIP_PROXY) .[tests]

install-coverage:
	$(PYTHON) -m pip install $(PIP_UPGRADE) $(PIP_CACHE) $(INSTALL_USER) $(QUIET) --proxy $(PIP_PROXY) codecov coveralls

outdated:
	$(PYTHON) -m pip list --outdated

.PHONY: docs
docs:
	make -C docs html

.PHONY: tests
tests:
	$(PYTHON) -m pytest -x ${COVERAGE} tests/

tests-tox:
	tox

coverage:
	$(PYTHON) -m pytest ${COVERAGE} --cov-report html tests/

lint:
	$(PYTHON) -m pylint --jobs=0 snippy_tldr/
	$(PYTHON) -m pylint --jobs=0 tests/

format:
	black snippy_tldr/
	black tests/
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
