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

import pytest
import responses

from snippy_tldr.plugin import SnippyTldr


class TestSnippyTldr(object):  # pylint: disable=too-few-public-methods
    """Test snippy-tldr."""

    @staticmethod
    @responses.activate
    @pytest.mark.usefixtures("mock-snippy")
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

    @staticmethod
    def test_002():
        """First test."""

        # Test with
        #
        #  Fetch pages from URI
        #       https://github.com/tldr-pages/tldr/tree/master/pages/    # Trailing slash
        #       https://github.com/tldr-pages/tldr/tree/0.0.1/pages
        #       https://github.com/tldr-pages/tldr/tree/italian/pages
        #
        # Fetch pages localhost uri
        #       '../tldr/pages/'
        #       './tldr/pages/'
        #       './tldr/pages'
        #       '.'
        #
        # Fetch pages localhost uri
        #       uri = 'file:../tldr/pages/linux/'
        #       uri = 'file:../tldr/pages'
        #       uri = 'file:../tldr/pages/linux/alpine.md'
        #       uri = 'file:../tld'

        uri = "https://github.com/tldr-pages/tldr/tree/master/pages/linux"
        uri = "https://github.com/tldr-pages/tldr/tree/master/pages"
        # uri = '../tldr/pages/linux/'
        # uri = '../tldr/pages/'
        # uri = 'file:../tldr/pages/linux/'
        # uri = 'file:../tldr/pages'
        # uri = 'file:../tldr/pages/linux/alpine.md'
        # uri = 'file:../tld'
        SnippyTldr(Logger(), uri, "test", "test")


class Logger(object):  # pylint: disable=too-few-public-methods
    """Logger mock."""

    def debug(self, *args, **kwargs):
        """Dummy debug method."""


class Const(object):  # pylint: disable=too-few-public-methods
    """Constants mock."""

    SNIPPET_COMMENT = "  #  "
