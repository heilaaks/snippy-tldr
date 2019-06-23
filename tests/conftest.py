# -*- coding: utf-8 -*-
#
#  Snippy-tldr - A plugin to import tldr man pages for Snippy.
#  Copyright 2019 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
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

"""conftest: Fixtures for pytest."""

import pytest


@pytest.fixture(scope="function", name="mock-snippy")
def mock_snippy(mocker):
    """Mock Snippy."""

    mocker.patch.object(Parser, "format_data", return_value=())
    mocker.patch.object(Parser, "format_brief", return_value="")
    mocker.patch.object(Parser, "format_description", return_value="")
    mocker.patch.object(Parser, "format_name", return_value="")
    mocker.patch.object(Parser, "format_groups", return_value=())
    mocker.patch.object(Parser, "format_tags", return_value=())


class Const(object):  # pylint: disable=too-few-public-methods
    """Dummy mock class."""

    SNIPPET = "snippet"


class Parser(object):  # pylint: disable=too-few-public-methods
    """Dummy mock class."""

    @classmethod
    def format_data(cls, category, value):
        """Dummy method for mock."""

    @classmethod
    def format_brief(cls, category, value):
        """Dummy method for mock."""

    @classmethod
    def format_description(cls, category, value):
        """Dummy method for mock."""

    @classmethod
    def format_name(cls, category, value):
        """Dummy method for mock."""

    @classmethod
    def format_groups(cls, category, value):
        """Dummy method for mock."""

    @classmethod
    def format_tags(cls, category, value):
        """Dummy method for mock."""


class Schema(object):  # pylint: disable=too-few-public-methods
    """Dummy mock class."""

    @classmethod
    def validate(cls, document):
        """Dummy method for mock."""
