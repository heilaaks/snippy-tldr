# -*- coding: utf-8 -*-
#
#  Snippy-tldr - A plugin to import tldr man pages for Snippy.
#  Copyright 2019-2020 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#  SPDX-License-Identifier: Apache-2.0

"""setup: Install Snippy tool."""

import io
from setuptools import setup


with io.open("README.rst", mode="r", encoding="utf-8") as infile:
    README = infile.read()

REQUIRES = (
    "requests",
    "jsonschema==3.2.0",  # For the snippy.plugins module.
    "snippy>=0.11.0",
)

EXTRAS_DEVEL = (
    'black ; python_version>"3.5"',
    'sphinx==1.8.5 ; python_version<="3.4"',
    'sphinx==2.4.4 ; python_version>="3.5"',
    "sphinx_rtd_theme==0.4.3",
    "sphinx-autobuild==0.7.1",
)

EXTRAS_TESTS = (
    "flake8==3.7.9",
    'importlib_metadata ; python_version!="3.4"',  # To get tox to install in Python 3.4.
    'importlib_metadata==0.23 ; python_version=="3.4"',  # To get tox to install in Python 3.4.
    'mock==3.0.5 ; python_version<="3.5"',
    'mock==4.0.1 ; python_version>="3.6"',
    "pluggy==0.13.1",
    'pylint==1.9.5 ; python_version=="2.7.*"',
    'pylint==2.3.1 ; python_version=="3.4.*"',
    'pylint==2.4.4 ; python_version>="3.5"',
    'pytest==4.6.9 ; python_version<="3.4"',
    'pytest==5.3.5 ; python_version>="3.5"',
    "pytest-cov==2.8.1",
    "pytest-mock==2.0.0",
    "pytest-xdist==1.31.0",
    "responses==0.10.12",
    'tox==3.14.5 ; python_version=="2.7.*" or python_version>="3.5"',
    'tox==3.14.0 ; python_version=="3.4.*"',
)

setup(
    name="snippy-tldr",
    version="0.2.0",
    author="Heikki J. Laaksonen",
    author_email="laaksonen.heikki.j@gmail.com",
    license="Apache Software License 2.0",
    url="https://github.com/heilaaks/snippy-tldr",
    description="Snippy plugin to import tldr man pages.",
    long_description=README,
    long_description_content_type="text/x-rst",
    packages=["snippy_tldr"],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    install_requires=REQUIRES,
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Software Development :: Documentation",
        "Topic :: Utilities",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License",
    ],
    extras_require={"devel": EXTRAS_DEVEL + EXTRAS_TESTS, "tests": EXTRAS_TESTS},
    tests_require=EXTRAS_TESTS,
    test_suite="tests",
    entry_points={"snippyplugin": ["snippy = snippy_tldr.plugin"]},
)
