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

"""test-snippy-tldr: Test snippy plugin to import tldr man pages."""

import responses

from snippy_tldr.plugin import SnippyTldr


class TestSnippyTldr(object):  # pylint: disable=too-few-public-methods
    """Test snippy-tldr."""

    @staticmethod
    @responses.activate
    def test_001():
        """First test."""

        responses.add(
            responses.GET,
            "https://github.com/tldr-pages/tldr/tree/master/pages/linux",
            json={},
            status=200,
        )
        _ = SnippyTldr(Logger(), "test", "test", "test")

        assert 1


class Logger(object):  # pylint: disable=too-few-public-methods
    """Logger mock."""

    def debug(self, *args, **kwargs):
        """Dummy debug method."""


class Const(object):  # pylint: disable=too-few-public-methods
    """Constants mock."""

    SNIPPET_COMMENT = "  #  "
