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

"""test_snippy_tldr: Test tldr man page import plugin."""

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


class TestSnippyTldr(object):
    """Test snippy-tldr."""

    @staticmethod
    @responses.activate
    @pytest.mark.skip(reason="refactor")
    @pytest.mark.usefixtures("mock-snippy")
    def test_read_github_uri_001():
        """Test reading one ``page`` from GitHub.

        Read the default tldr man page when URI is not provided.
        """

        requests = [
            "https://api.github.com/repos/tldr-pages/tldr/branches/master",
            "https://github.com/tldr-pages/tldr/tree/master/pages/linux",
        ]
        responses.add(responses.GET, requests.pop(0), json={}, status=200)
        SnippyTldr(Logger(), "")
        assert len(responses.calls) == 1

    @staticmethod
    @responses.activate
    @pytest.mark.skip(reason="refactor")
    @pytest.mark.usefixtures("mock-snippy")
    def test_read_github_uri_002():
        """Test reading all ``pages`` under one ``translation``.

        Read all English translated tldr pages from GitHub master branch. The
        URI does not have trailing slash.
        """

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
        _ = SnippyTldr(Logger(), uri)
        assert len(responses.calls) == 5

    @staticmethod
    @responses.activate
    @pytest.mark.skip(reason="refactor")
    @pytest.mark.usefixtures("mock-snippy")
    def test_read_github_uri_003():
        """Test reading all ``pages`` under one ``translation``.

        Read all English translated tldr pages from GitHub master branch. The
        URI has a trailing slash.
        """

        uri = "https://github.com/tldr-pages/tldr/tree/master/pages/"
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
        _ = SnippyTldr(Logger(), uri)
        assert len(responses.calls) == 5

    @staticmethod
    @responses.activate
    @pytest.mark.skip(reason="refactor")
    @pytest.mark.usefixtures("mock-snippy")
    def test_read_github_uri_004():
        """Test reading all ``pages`` under one ``translation``.

        Read all Brazilian Portuguese translated tldr pages from GitHub master
        branch.
        """

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
        _ = SnippyTldr(Logger(), uri)
        assert len(responses.calls) == 5

    @staticmethod
    @responses.activate
    @pytest.mark.skip(reason="refactor")
    @pytest.mark.usefixtures("mock-snippy")
    def test_read_github_uri_005():
        """Test reading all ``pages`` from one ``translation``.

        Read all Chinese translated tldr pages from GitHub master branch.
        """

        uri = "https://github.com/tldr-pages/tldr/tree/master/pages.zh"
        body = (
            '<span class="css-truncate-target"><a class="js-navigation-open" title="common" id="cf2aa06853ba7" href="/tldr-pages/tldr/tree/master/pages.zh/common">common</a></span>'  # noqa pylint: disable=line-too-long
            '<span class="css-truncate-target"><a class="js-navigation-open" title="linux" id="e206a54e9f826" href="/tldr-pages/tldr/tree/master/pages.zh/linux">linux</a></span>'  # noqa pylint: disable=line-too-long
            '<span class="css-truncate-target"><a class="js-navigation-open" title="osx" id="8e4f88e9d55c6" href="/tldr-pages/tldr/tree/master/pages.zh/osx">osx</a></span>'  # noqa pylint: disable=line-too-long
            '<span class="css-truncate-target"><a class="js-navigation-open" title="windows" id="0f413351f633" href="/tldr-pages/tldr/tree/master/pages.zh/windows">windows</a></span>'  # noqa pylint: disable=line-too-long
        )
        requests = [
            "https://github.com/tldr-pages/tldr/tree/master/pages.zh",
            "https://github.com/tldr-pages/tldr/tree/master/pages.zh/common",
            "https://github.com/tldr-pages/tldr/tree/master/pages.zh/linux",
            "https://github.com/tldr-pages/tldr/tree/master/pages.zh/osx",
            "https://github.com/tldr-pages/tldr/tree/master/pages.zh/windows",
        ]
        responses.add(responses.GET, requests.pop(0), body=body, status=200)
        for _ in range(len(requests)):
            responses.add(responses.GET, requests.pop(0), body=body, status=200)
        _ = SnippyTldr(Logger(), uri)
        assert len(responses.calls) == 5

    @staticmethod
    @responses.activate
    @pytest.mark.skip(reason="refactor")
    @pytest.mark.usefixtures("mock-snippy")
    def test_read_github_uri_006():
        """Test reading all ``pages`` from a GitHub branch.

        Read all Italian translated tldr pages from the italian branch.
        """

        uri = "https://github.com/tldr-pages/tldr/tree/italian/pages.it"
        body = '<span class="css-truncate-target"><a class="js-navigation-open" title="common" id="9efab2399c7c560b" href="/tldr-pages/tldr/tree/italian/pages.it/common">common</a></span>'  # noqa pylint: disable=line-too-long
        requests = [
            "https://github.com/tldr-pages/tldr/tree/italian/pages.it",
            "https://github.com/tldr-pages/tldr/tree/italian/pages.it/common",
        ]
        responses.add(responses.GET, requests.pop(0), body=body, status=200)
        for _ in range(len(requests)):
            responses.add(responses.GET, requests.pop(0), body=body, status=200)
        _ = SnippyTldr(Logger(), uri)
        assert len(responses.calls) == 2

    @staticmethod
    @responses.activate
    @pytest.mark.skip(reason="refactor")
    @pytest.mark.usefixtures("mock-snippy")
    def test_read_github_uri_007():
        """Test reading ``tldr files`` from one ``page``.

        Read all tldr files from one tldr page in GitHub master branch.
        """

        uri = "https://github.com/tldr-pages/tldr/tree/master/pages/osx"
        files = (
            '<span class="css-truncate css-truncate-target"><a class="js-navigation-open" title="units.md" id="0c1af7a5ee4b57a644643230ed526db2-5d01b9086ff0bf4874b2757dbbde5233dd6ff3f7" href="/tldr-pages/tldr/blob/master/pages/osx/units.md">units.md</a></span>\n'  # noqa pylint: disable=line-too-long
            '<span class="css-truncate css-truncate-target"><a class="js-navigation-open" title="w.md" id="0dd87f8dc5cbfa861c16c5ad3c332ab4-1cf83af6e84ea532e6c09a1cead470b6922c6a91" href="/tldr-pages/tldr/blob/master/pages/osx/w.md">w.md</a></span>\n'  # noqa pylint: disable=line-too-long
            '<span class="css-truncate css-truncate-target"><a class="js-navigation-open" title="wacaw.md" id="6737e3eb2cef3810832f9b5adc372ea4-132b0b691c4c40bd79047f7b70afadd49dc43cd5" href="/tldr-pages/tldr/blob/master/pages/osx/wacaw.md">wacaw.md</a></span>\n'  # noqa pylint: disable=line-too-long
        )
        requests = [
            "https://github.com/tldr-pages/tldr/tree/master/pages/osx",
            "https://raw.githubusercontent.com/tldr-pages/tldr/master/pages/osx/units.md",
            "https://raw.githubusercontent.com/tldr-pages/tldr/master/pages/osx/w.md",
            "https://raw.githubusercontent.com/tldr-pages/tldr/master/pages/osx/wacaw.md",
        ]
        responses.add(responses.GET, requests.pop(0), body=files, status=200)
        responses.add(responses.GET, requests.pop(0), body="", status=200)
        responses.add(responses.GET, requests.pop(0), body="", status=200)
        responses.add(responses.GET, requests.pop(0), body="", status=200)
        _ = SnippyTldr(Logger(), uri)
        assert len(responses.calls) == 4

    @staticmethod
    @responses.activate
    @pytest.mark.skip(reason="refactor")
    @pytest.mark.usefixtures("mock-snippy")
    def test_read_github_file_001():
        """Test reading one ``tldr file`` from the GitHub.

        Read one tldr file directly from GitHub. The given URI is the URI
        copied from a web browser navigation link. This is the 'blob' URI.
        """

        uri_cli = (
            "https://github.com/tldr-pages/tldr/blob/master/pages.pt-BR/linux/alpine.md"
        )
        uri_req = "https://raw.githubusercontent.com/tldr-pages/tldr/master/pages.pt-BR/linux/alpine.md"
        body = ""
        responses.add(responses.GET, uri_req, body=body, status=200)
        _ = SnippyTldr(Logger(), uri_cli)

        uri_cli = "https://github.com/tldr-pages/tldr/blob/master/pages/osx/alpine.md"
        uri_req = "https://raw.githubusercontent.com/tldr-pages/tldr/master/pages/osx/alpine.md"
        responses.add(responses.GET, uri_req, body=body, status=200)
        _ = SnippyTldr(Logger(), uri_cli)

    @staticmethod
    @responses.activate
    @pytest.mark.skip(reason="refactor")
    @pytest.mark.usefixtures("mock-snippy")
    def test_read_github_file_002():
        """Test reading one ``tldr file`` from the GitHub.

        Read one tldr file directly from GitHub. The given URI is the URI
        copied from HTML page. This is the 'tree' URI that is redirected by
        GitHun to 'blob' URI.
        """

        uri_cli = (
            "https://github.com/tldr-pages/tldr/tree/master/pages.pt-BR/linux/alpine.md"
        )
        uri_req = "https://raw.githubusercontent.com/tldr-pages/tldr/master/pages.pt-BR/linux/alpine.md"
        body = ""
        responses.add(responses.GET, uri_req, body=body, status=200)
        _ = SnippyTldr(Logger(), uri_cli)

        uri_cli = "https://github.com/tldr-pages/tldr/tree/master/pages/osx/alpine.md"
        uri_req = "https://raw.githubusercontent.com/tldr-pages/tldr/master/pages/osx/alpine.md"
        responses.add(responses.GET, uri_req, body=body, status=200)
        _ = SnippyTldr(Logger(), uri_cli)

    @staticmethod
    @responses.activate
    @pytest.mark.skip(reason="refactor")
    @pytest.mark.usefixtures("mock-snippy")
    def test_read_github_file_003():
        """Test reading one ``tldr file`` from the GitHub.

        Read one tldr file directly from GitHub. The given URI is the raw
        formatted file, not the HTML URI.
        """

        uri_cli = "https://raw.githubusercontent.com/tldr-pages/tldr/master/pages.pt-BR/linux/alpine.md"
        uri_req = "https://raw.githubusercontent.com/tldr-pages/tldr/master/pages.pt-BR/linux/alpine.md"
        body = ""
        responses.add(responses.GET, uri_req, body=body, status=200)
        _ = SnippyTldr(Logger(), uri_cli)

        uri_cli = "https://raw.githubusercontent.com/tldr-pages/tldr/master/pages/osx/alpine.md"
        uri_req = "https://raw.githubusercontent.com/tldr-pages/tldr/master/pages/osx/alpine.md"
        responses.add(responses.GET, uri_req, body=body, status=200)
        _ = SnippyTldr(Logger(), uri_cli)

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

        uri = "https://github.com/tldr-pages/tldr/tree/master/pages/linux/"
        # uri = "https://github.com/tldr-pages/tldr/tree/master/pages.zh/"
        uri = "https://github.com/tldr-pages/tldr/tree/master/pages.zh/linux/"
        # uri = "https://github.com/tldr-pages/tldr/tree/waldyrious/alt-syntax/pages/osx"
        # uri = "https://github.com/tldr-pages/tldr/tree/master/pages"
        # uri = "https://github.com/tldr-pages/tldr/tree/master/pages/linux"
        # uri = "https://github.com/tldr-pages/tldr/tree/master/pages/osx"
        # uri = "https://raw.githubusercontent.com/tldr-pages/tldr/master/pages/linux/alpine.md"
        # uri = "https://github.com/tldr-pages/tldr/tree/master/pages/linux/alpine.md"
        # uri = "https://github.com/tldr-pages/tldr/blob/master/pages/linux/alpine.md"
        uri = "https://github.com/tldr-pages/tldr/tree/italian/pages.it"
        uri = "https://github.com/tldr-pages/tldr/tree/waldyrious/alt-syntax/pages"
        # uri = '../tldr/pages/linux/'
        # uri = '../tldr/pages/'
        # uri = 'file:../tldr/pages/linux/'
        # uri = 'file:../tldr/pages'
        # uri = 'file:../tldr/pages/linux/alpine.md'
        # uri = 'file:../tld'
        SnippyTldr(Logger(), uri)


class Logger(object):  # pylint: disable=too-few-public-methods
    """Logger mock."""

    def debug(self, *args, **kwargs):
        """Dummy debug method."""


class Const(object):  # pylint: disable=too-few-public-methods
    """Constants mock."""

    SNIPPET_COMMENT = "  #  "
    SNIPPET = "snippet"
