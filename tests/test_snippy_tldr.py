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

"""test_snippy_tldr: Test tldr man page import plugin."""

import mock
import pytest
import responses

from snippy_tldr.plugin import SnippyTldr
from tests.lib.helper import GitHubApi
from tests.lib.helper import Snippet
from tests.lib.helper import TldrPage


# pylint: disable=unsupported-assignment-operation, unsubscriptable-object
class TestSnippyTldr(object):
    """Test snippy-tldr plugin."""

    @staticmethod
    @responses.activate
    def test_github_tldr_page_001():
        """Test reading one tldr ``page`` from the GitHib.

        Read one tldr page directly from the GitHub. The given URI is the URL
        copied from a web browser navigation link. This is the GitHub URL with
        a 'blob' data.
        """

        expect = [
            {
                "request": {
                    "url": "https://raw.githubusercontent.com/tldr-pages/tldr/master/pages/linux/pushd.md",
                    "headers": {},
                },
                "response": {"status": 200, "content": {"text": TldrPage.pushd}},
            },
            {
                "request": {
                    "url": "https://raw.githubusercontent.com/tldr-pages/tldr/master/pages/linux/adduser.md",
                    "headers": {},
                },
                "response": {"status": 200, "content": {"text": TldrPage.adduser}},
            },
        ]
        actual = GitHubApi.mock(expect)
        infile = "https://github.com/tldr-pages/tldr/blob/master/pages/linux/pushd.md"
        contents = SnippyTldr(Logger(), infile)
        assert len(contents) == 1
        assert next(contents) == Snippet.pushd

        infile = "https://github.com/tldr-pages/tldr/blob/master/pages/linux/adduser.md"
        contents = SnippyTldr(Logger(), infile)
        assert len(contents) == 1
        assert next(contents) == Snippet.adduser

        assert len(responses.calls) == 2
        assert GitHubApi.validate(expect, actual)

    @staticmethod
    @responses.activate
    def test_github_tldr_page_002():
        """Test reading one tldr ``page`` from the GitHib.

        Read one tldr page directly from the GitHub. The given URI is the raw
        URL of the tldr page.
        """

        expect = [
            {
                "request": {
                    "url": "https://raw.githubusercontent.com/tldr-pages/tldr/master/pages/linux/pushd.md",
                    "headers": {},
                },
                "response": {"status": 200, "content": {"text": TldrPage.pushd}},
            }
        ]
        actual = GitHubApi.mock(expect)
        infile = "https://raw.githubusercontent.com/tldr-pages/tldr/master/pages/linux/pushd.md"
        contents = SnippyTldr(Logger(), infile)
        assert len(contents) == 1
        assert next(contents) == Snippet.pushd
        assert len(responses.calls) == 1
        assert GitHubApi.validate(expect, actual)

    @staticmethod
    @responses.activate
    def test_github_tldr_page_003():
        """Test reading one tldr ``page`` from the GitHib.

        Read one tldr page directly from the GitHub. The given URI is a 'tree'
        URL that redirects in GitHub to the 'blob' URL. Using a 'tree' URL is
        not exactly correct but it must still work. For example GitHub raw HTML
        page uses 'tree' URL to point to files for some reason.
        """

        expect = [
            {
                "request": {
                    "url": "https://raw.githubusercontent.com/tldr-pages/tldr/master/pages/linux/pushd.md",
                    "headers": {},
                },
                "response": {"status": 200, "content": {"text": TldrPage.pushd}},
            }
        ]
        actual = GitHubApi.mock(expect)
        infile = "https://github.com/tldr-pages/tldr/tree/master/pages/linux/pushd.md"
        contents = SnippyTldr(Logger(), infile)
        assert len(contents) == 1
        assert next(contents) == Snippet.pushd
        assert len(responses.calls) == 1
        assert GitHubApi.validate(expect, actual)

    @staticmethod
    @responses.activate
    def test_github_tldr_platform_001():
        """Test reading tldr pages from GitHib under one ``platform``.

        Read default tldr man pages from English translated Linux platform
        when the tldr URI is not provided to the plugin.
        """

        expect = GitHubApi.default
        actual = GitHubApi.mock(expect)
        contents = SnippyTldr(Logger(), "")
        assert len(contents) == 2
        assert next(contents) == Snippet.add_apt_repository
        assert next(contents) == Snippet.adduser
        assert len(responses.calls) == 6
        assert GitHubApi.validate(expect, actual)

    @staticmethod
    @responses.activate
    def test_github_tldr_platform_002():
        """Test reading tldr pages from GitHib under one ``platform``.

        Read all English translated tldr pages from linux platform in GitHub
        master branch. The URL has a trailing slash.
        """

        expect = GitHubApi.default
        actual = GitHubApi.mock(expect)
        infile = "https://github.com/tldr-pages/tldr/tree/master/pages/linux/"
        contents = SnippyTldr(Logger(), infile)
        assert len(contents) == 2
        assert next(contents) == Snippet.add_apt_repository
        assert next(contents) == Snippet.adduser
        assert len(responses.calls) == 6
        assert GitHubApi.validate(expect, actual)

    @staticmethod
    @responses.activate
    def test_github_tldr_platform_003():
        """Test reading tldr pages from GitHib under one ``platform``.

        Read all Italian translated tldr pages from common platform in GitHub
        italian branch.
        """

        expect = GitHubApi.default
        expect[0]["request"][
            "url"
        ] = "https://api.github.com/repos/tldr-pages/tldr/branches/italian"
        expect[1]["response"]["content"]["json"]["tree"][2]["path"] = "pages.it"
        expect[3]["request"][
            "url"
        ] = "https://api.github.com/repos/tldr-pages/tldr/git/trees/63f4c272b4bc0a80c0f9f805766de29bac0bc055"
        expect[4]["request"][
            "url"
        ] = "https://raw.githubusercontent.com/tldr-pages/tldr/italian/pages.it/common/add-apt-repository.md"
        expect[5]["request"][
            "url"
        ] = "https://raw.githubusercontent.com/tldr-pages/tldr/italian/pages.it/common/adduser.md"
        snippets = [Snippet.add_apt_repository, Snippet.adduser]
        snippets[0]["groups"] = ["common"]
        snippets[0]["tags"] = ["common"]
        snippets[0]["links"] = [
            "https://raw.githubusercontent.com/tldr-pages/tldr/italian/pages.it/common/add-apt-repository.md"
        ]
        snippets[0][
            "source"
        ] = "https://raw.githubusercontent.com/tldr-pages/tldr/italian/pages.it/common/add-apt-repository.md"
        snippets[1]["groups"] = ["common"]
        snippets[1]["tags"] = ["common"]
        snippets[1]["links"] = [
            "https://raw.githubusercontent.com/tldr-pages/tldr/italian/pages.it/common/adduser.md"
        ]
        snippets[1][
            "source"
        ] = "https://raw.githubusercontent.com/tldr-pages/tldr/italian/pages.it/common/adduser.md"

        actual = GitHubApi.mock(expect)
        infile = "https://github.com/tldr-pages/tldr/tree/italian/pages.it/common"
        contents = SnippyTldr(Logger(), infile)
        assert len(contents) == 2
        assert next(contents) == snippets[0]
        assert next(contents) == snippets[1]
        assert len(responses.calls) == 6
        assert GitHubApi.validate(expect, actual)

    @staticmethod
    @responses.activate
    def test_github_tldr_platform_004():
        """Test reading tldr pages from GitHib under one ``platform``.

        Read all Brazilian Portuguese translated translated tldr pages from
        linux platform in GitHub master branch.
        """

        expect = GitHubApi.default
        expect[2]["request"][
            "url"
        ] = "https://api.github.com/repos/tldr-pages/tldr/git/trees/6b55cdc79c194f1951f3cd75f8908732d8a6e451"
        expect[4]["request"][
            "url"
        ] = "https://raw.githubusercontent.com/tldr-pages/tldr/master/pages.pt-BR/linux/add-apt-repository.md"
        expect[5]["request"][
            "url"
        ] = "https://raw.githubusercontent.com/tldr-pages/tldr/master/pages.pt-BR/linux/adduser.md"
        snippets = [Snippet.add_apt_repository, Snippet.adduser]
        snippets[0]["links"] = [
            "https://raw.githubusercontent.com/tldr-pages/tldr/master/pages.pt-BR/linux/add-apt-repository.md"
        ]
        snippets[0][
            "source"
        ] = "https://raw.githubusercontent.com/tldr-pages/tldr/master/pages.pt-BR/linux/add-apt-repository.md"
        snippets[1]["links"] = [
            "https://raw.githubusercontent.com/tldr-pages/tldr/master/pages.pt-BR/linux/adduser.md"
        ]
        snippets[1][
            "source"
        ] = "https://raw.githubusercontent.com/tldr-pages/tldr/master/pages.pt-BR/linux/adduser.md"

        actual = GitHubApi.mock(expect)
        infile = "https://github.com/tldr-pages/tldr/tree/master/pages.pt-BR/linux"
        contents = SnippyTldr(Logger(), infile)
        assert len(contents) == 2
        assert next(contents) == snippets[0]
        assert next(contents) == snippets[1]
        assert len(responses.calls) == 6
        assert GitHubApi.validate(expect, actual)

    @staticmethod
    @responses.activate
    def test_github_tldr_platform_005():
        """Test reading tldr pages from GitHib under one ``platform``.

        Read all English translated tldr pages from linux platform in GitHub
        waldyrious/alt-syntax branch.
        """

        expect = GitHubApi.default
        expect[0]["request"][
            "url"
        ] = "https://api.github.com/repos/tldr-pages/tldr/branches/waldyrious/alt-syntax"
        expect[4]["request"][
            "url"
        ] = "https://raw.githubusercontent.com/tldr-pages/tldr/waldyrious/alt-syntax/pages/linux/add-apt-repository.md"
        expect[5]["request"][
            "url"
        ] = "https://raw.githubusercontent.com/tldr-pages/tldr/waldyrious/alt-syntax/pages/linux/adduser.md"
        snippets = [Snippet.add_apt_repository, Snippet.adduser]
        snippets[0]["links"] = [
            "https://raw.githubusercontent.com/tldr-pages/tldr/waldyrious/alt-syntax/pages/linux/add-apt-repository.md"
        ]
        snippets[0][
            "source"
        ] = "https://raw.githubusercontent.com/tldr-pages/tldr/waldyrious/alt-syntax/pages/linux/add-apt-repository.md"
        snippets[1]["links"] = [
            "https://raw.githubusercontent.com/tldr-pages/tldr/waldyrious/alt-syntax/pages/linux/adduser.md"
        ]
        snippets[1][
            "source"
        ] = "https://raw.githubusercontent.com/tldr-pages/tldr/waldyrious/alt-syntax/pages/linux/adduser.md"

        actual = GitHubApi.mock(expect)
        infile = (
            "https://github.com/tldr-pages/tldr/tree/waldyrious/alt-syntax/pages/linux"
        )
        contents = SnippyTldr(Logger(), infile)
        assert len(contents) == 2
        assert next(contents) == snippets[0]
        assert next(contents) == snippets[1]
        assert len(responses.calls) == 6
        assert GitHubApi.validate(expect, actual)

    @staticmethod
    @pytest.mark.usefixtures("isfile_true")
    def test_local_tldr_page_001():
        """Test reading one tldr ``page`` from local directory.

        Read one tldr page directly from local file. In this case the file is
        defined with different variations leading to one tldr page.

        Because the filepath does not contain the tldr platform, the ``groups``
        and ``tags`` attributes cannot be set. The ``links`` and ``source``
        attributes cannot be set because the local filepath is not used as a
        link.
        """

        snippet = Snippet.pushd
        snippet["groups"] = ["default"]
        snippet["tags"] = []
        snippet["links"] = []
        snippet["source"] = ""

        files = [
            "pushd.md",
            "./pushd.md",
            "../pushd.md",
            "../../pushd.md",
            "../folder/pushd.md",
            "/root/folder/pushd.md",
        ]

        file_content = mock.mock_open(read_data=TldrPage.pushd)
        with mock.patch("snippy_tldr.plugin.open", file_content) as mock_file:
            for infile in files:
                contents = SnippyTldr(Logger(), infile)
                assert len(contents) == 1
                assert next(contents) == snippet
                mock_file.assert_called_once_with(infile, "r")
                mock_file.reset_mock()

    @staticmethod
    @pytest.mark.usefixtures("isfile_true")
    def test_local_tldr_page_002():
        """Test reading one tldr ``page`` from local directory.

        Read one tldr page directly from local file. In this case the file is
        defined with different variations leading to one tldr page and the file
        has the tldr platform.

        The ``links`` and ``source`` attributes cannot be set because the local
        filepath is not used as a link.
        """

        snippet = Snippet.adduser
        snippet["links"] = []
        snippet["source"] = ""

        files = [
            "./tldr/pages/linux/adduser.md",
            "/linux/adduser.md",
            "linux/adduser.md",
            # "/root/path/linux/adduser.md" # This does not work.
        ]

        file_content = mock.mock_open(read_data=TldrPage.adduser)
        with mock.patch("snippy_tldr.plugin.open", file_content) as mock_file:
            for infile in files:
                contents = SnippyTldr(Logger(), infile)
                assert len(contents) == 1
                assert next(contents) == snippet
                mock_file.assert_called_once_with(infile, "r")
                mock_file.reset_mock()

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
        # uri = "https://github.com/tldr-pages/tldr/tree/master/pages.zh/linux/"
        # uri = "https://github.com/tldr-pages/tldr/tree/waldyrious/alt-syntax/pages/osx"
        # uri = "https://github.com/tldr-pages/tldr/tree/master/pages"
        # uri = "https://github.com/tldr-pages/tldr/tree/master/pages/linux"
        # uri = "https://github.com/tldr-pages/tldr/tree/master/pages/osx"
        # uri = "https://raw.githubusercontent.com/tldr-pages/tldr/master/pages/linux/alpine.md"
        # uri = "https://github.com/tldr-pages/tldr/tree/master/pages/linux/alpine.md"
        # uri = "https://github.com/tldr-pages/tldr/blob/master/pages/linux/alpine.md"
        # uri = "https://github.com/tldr-pages/tldr/tree/italian/pages.it"
        # uri = "https://github.com/tldr-pages/tldr/tree/waldyrious/alt-syntax/pages"
        # uri = '../tldr/pages/linux/'
        # uri = '../tldr/pages/'
        uri = "../tldr/pages/linux/"
        # uri = 'file:../tldr/pages'
        uri = "../tldr/pages/linux/alpine.md"
        uri = "alpine.md"
        # uri = 'file:../tld'
        SnippyTldr(Logger(), uri)


class Logger(object):  # pylint: disable=too-few-public-methods
    """Logger mock."""

    def debug(self, *args, **kwargs):
        """Dummy debug method."""
