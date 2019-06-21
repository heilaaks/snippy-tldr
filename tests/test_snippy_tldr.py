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

# The responses module does not seem to work when responses are set
# in a for loop by iterating the value of a list. It seems that the
# module takes a reference to value (pointer to list) and that gets
# updated in the responses module in every loop.
#
# This causes the responses always to use the last value in a loop
# as a first and only response. The iteration must be made without
# actually iterating the values but the size of the list.


class TestSnippyTldr(object):  # pylint: disable=too-few-public-methods
    """Test snippy-tldr."""

    @staticmethod
    @responses.activate
    @pytest.mark.usefixtures("mock-snippy")
    def test_001():
        """Test reading remote tldr pages."""

        # Read default tldr man page when user did not use ``--file`` option.
        responses.add(
            responses.GET,
            "https://github.com/tldr-pages/tldr/tree/master/pages/linux",
            json={},
            status=200,
        )
        _ = SnippyTldr(Logger(), "", None, None)
        assert len(responses.calls) == 1
        responses.reset()

        # Read all tldr pages when the URI does not have trailing slash.
        uri = "https://github.com/tldr-pages/tldr/tree/master/pages"
        body = (
            '<span class="css-truncate-target"><a class="js-navigation-open" title="linux" id="e206a54e9f826" href="/tldr-pages/tldr/tree/master/pages/linux">linux</a></span>'  # noqa pylint: disable=line-too-long
            '<span class="css-truncate-target"><a class="js-navigation-open" title="osx" id="8e4f88e9d55c6" href="/tldr-pages/tldr/tree/master/pages/osx">osx</a></span>'  # noqa pylint: disable=line-too-long
            '<span class="css-truncate-target"><a class="js-navigation-open" title="sunos" id="cf2aa06853ba7" href="/tldr-pages/tldr/tree/master/pages/sunos">sunos</a></span>'  # noqa pylint: disable=line-too-long
            '<span class="css-truncate-target"><a class="js-navigation-open" title="windows" id="0f413351f633" href="/tldr-pages/tldr/tree/master/pages/windows">windows</a></span>'  # noqa pylint: disable=line-too-long
        )
        requests = [
            "https://github.com/tldr-pages/tldr/tree/master/pages",
            "https://github.com/tldr-pages/tldr/tree/master/pages/linux",
            "https://github.com/tldr-pages/tldr/tree/master/pages/osx",
            "https://github.com/tldr-pages/tldr/tree/master/pages/sunos",
            "https://github.com/tldr-pages/tldr/tree/master/pages/windows",
        ]
        responses.add(responses.GET, requests.pop(0), body=body, status=200)
        for _ in range(len(requests)):
            responses.add(responses.GET, requests.pop(0), body=body, status=200)
        _ = SnippyTldr(Logger(), uri, None, None)
        assert len(responses.calls) == 5
        responses.reset()

        # Test reading all tldr pages under 'pt-BR' translation.
        uri = "https://github.com/tldr-pages/tldr/tree/master/pages.pt-BR"
        body = (
            '<span class="css-truncate-target"><a class="js-navigation-open" title="linux" id="e206a54e9f826" href="/tldr-pages/tldr/tree/master/pages.pt-BR/linux">linux</a></span>'  # noqa pylint: disable=line-too-long
            '<span class="css-truncate-target"><a class="js-navigation-open" title="osx" id="8e4f88e9d55c6" href="/tldr-pages/tldr/tree/master/pages.pt-BR/osx">osx</a></span>'  # noqa pylint: disable=line-too-long
            '<span class="css-truncate-target"><a class="js-navigation-open" title="sunos" id="cf2aa06853ba7" href="/tldr-pages/tldr/tree/master/pages.pt-BR/sunos">sunos</a></span>'  # noqa pylint: disable=line-too-long
            '<span class="css-truncate-target"><a class="js-navigation-open" title="windows" id="0f413351f633" href="/tldr-pages/tldr/tree/master/pages.pt-BR/windows">windows</a></span>'  # noqa pylint: disable=line-too-long
        )
        requests = [
            "https://github.com/tldr-pages/tldr/tree/master/pages.pt-BR",
            "https://github.com/tldr-pages/tldr/tree/master/pages.pt-BR/linux",
            "https://github.com/tldr-pages/tldr/tree/master/pages.pt-BR/osx",
            "https://github.com/tldr-pages/tldr/tree/master/pages.pt-BR/sunos",
            "https://github.com/tldr-pages/tldr/tree/master/pages.pt-BR/windows",
        ]
        responses.add(responses.GET, requests.pop(0), body=body, status=200)
        for _ in range(len(requests)):
            responses.add(responses.GET, requests.pop(0), body=body, status=200)
        _ = SnippyTldr(Logger(), uri, None, None)
        assert len(responses.calls) == 5

        # Test reading one tldr snippet.
        uri = (
            "https://github.com/tldr-pages/tldr/tree/master/pages.pt-BR/linux/alpine.md"
        )
        responses.add(responses.GET, uri, body=body, status=200)
        _ = SnippyTldr(Logger(), uri, None, None)

        uri = "https://github.com/tldr-pages/tldr/tree/master/pages/osx/alpine.md"
        responses.add(responses.GET, uri, body=body, status=200)
        _ = SnippyTldr(Logger(), uri, None, None)

    @staticmethod
    @pytest.mark.skip(reason="no way of currently testing this")
    def test_999():
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

        # uri = "https://github.com/tldr-pages/tldr/tree/master/pages/linux/"
        # uri = "https://github.com/tldr-pages/tldr/tree/master/pages.zh/"
        # uri = "https://github.com/tldr-pages/tldr/tree/master/pages"
        uri = "https://github.com/tldr-pages/tldr/tree/master/pages/linux"
        uri = "https://github.com/tldr-pages/tldr/tree/master/pages/linux/alpine.md"
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
    SNIPPET = "snippet"
