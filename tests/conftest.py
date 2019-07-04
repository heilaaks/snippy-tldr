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


@pytest.fixture(scope="function", name="isfile_true")
def mock_isfile_true(mocker):
    """Mock os.path.isfile."""

    mocker.patch("snippy_tldr.plugin.os.path.isfile", return_value=True)
    mocker.patch("snippy_tldr.plugin.os.access", return_value=True)
