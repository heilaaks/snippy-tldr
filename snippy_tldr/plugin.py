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

"""Snippy-tldr is a plugin to import tldr man pages for Snippy."""

import os.path
import re

from glob import glob

try:
    from urllib.parse import urljoin
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urljoin, urlparse

import requests


from snippy.plugins import Const
from snippy.plugins import Parser
from snippy.plugins import Schema
from snippy.plugins import Cause


def snippy_import_hook(logger, infile):
    """Import content for Snippy tool.

    This is an import hook that must return an iterator object. The iterator
    must be iterable class that implements ``next`` and ``len`` methods. The
    JSON structures stored in the iterator must pass the ``validate`` method
    in the ``snippy.plugins.Schema`` class.

    The ``snippy.plugins.Parser`` class may be used to parse the source data
    to a JSON content for Snippy.

    ::

        # Tldr man pages hierarchical layers.
        #
        # translations       platforms          pages
        # ============       =========        =========
          pages.it     |
          pages.pt-BR  |
          pages.zh     |
          pages        +---+  common   |
                           |  linux    |
                           |  osx      |
                           |  sunos    |
                           +  windows  +---+  alpine.md
                                           |  apk.md

    =============  ======================================================================
    Term           Decscription
    =============  ======================================================================
    *page*         |  One tldr page like ``alpine.md`` or ``apk.md``.

    *platform*     |  One platform like ``linux`` or ``osx``.

    *translation*  |  One tldr man page translation like ``pages.it`` or ``pages.zh``.
    =============  ======================================================================

    Args:
        logger (obj): Logger to be used with the plugin.
        infile (str): Value from the Snippy ``--file`` command line option.

    Returns:
        obj: Iterator object that stores the content from plugin to Snippy tool.

    Examples
    --------
    >>> from snippy.plugins import Const
    >>> from snippy.plugins import Parser
    >>> from snippy.plugins import Schema
    >>>
    >>> class SnippyTldr(object):
    >>>
    >>>     def __init__(self, logger, file):
    >>>         self._logger = logger
    >>>         self._uri = file
    >>>         self._schema = Schema()
    >>>         self._content = []
    >>>         self._i = 0
    >>>
    >>>         self._read_tldr_files()
    >>>
    >>>     def __len__(self):
    >>>         return len(self._content)
    >>>
    >>>     def __iter__(self):
    >>>         return self
    >>>
    >>>     def next(self):
    >>>         if self._i < len(self):
    >>>             content = self._content[self._i]
    >>>             self._i += 1
    >>>         else:
    >>>             raise StopIteration
    >>>
    >>>         return content
    >>>
    >>>     __next__ = next  # Python 3 compatible iterator.
    >>>
    >>>     def _read_tldr_files(self):
    >>>         with open('alpine.md', 'w') as infile:
    >>>             tldr = self._parse_file(infile.read())
    >>>             if self._schema.validate(tldr):
    >>>                 self.notes.append(tldr)
    >>>
    >>>     def _parse_file(self, infile)
    >>>         content = {}
    >>>         content['category'] = Const.SNIPPET
    >>>         content['data'] = Parser.format_data(['first line', 'second line'])
    >>>
    >>>         return content
    """

    return SnippyTldr(logger, infile)


class SnippyTldr(object):  # pylint: disable=too-many-instance-attributes
    """Plugin to import tldr man pages for snippy."""

    GITHUB_API = "https://api.github.com/repos/tldr-pages/tldr/"
    GITHUB_RAW = "https://raw.githubusercontent.com/tldr-pages/tldr/"
    TLDR_DEFAULT_URI = "https://github.com/tldr-pages/tldr/tree/master/pages/linux"
    TLDR_PLATFORMS = ("common", "linux", "osx", "sunos", "windows")

    RE_MATCH_GITHUB_URL = re.compile(
        r"""
        http[s]?://github.com/tldr-pages/tldr/(tree|blob)/
        """,
        re.VERBOSE,
    )

    # Match examples like 'pages', 'pages.pt-BR' and 'pages.it'.
    RE_MATCH_TLDR_TRANSLATION = r"pages(?:\.[a-zA-Z0-9-]+)?"

    # Match all known tldr platforms.
    RE_MATCH_TLDR_PLATFORM = r"%s" % "|".join(TLDR_PLATFORMS)

    # A 'blob' URI should be always used with URIs pointing to a file. Someone
    # may accidentally use a GitHub 'tree' URI with a tldr page. A 'tree' URL
    # pointing to a tldr page is still accepted just to be flexible.
    RE_CATCH_GITHUB_PAGE = re.compile(
        r"""
        (?:
            raw.githubusercontent.com/tldr-pages/tldr  # GitHub raw content URL.
            |                                          # or
            tldr/(?:blob|tree)                         # GitHub blob (or tree) URL.
        )/
        (?P<branch>.*)/         # Catch branches like 'master' or 'waldyrious/alt-syntax'.
        (?P<translation>.*)/    # Catch translations like 'pages' or 'pages.pt-BR'.
        (?P<platform>.*)/       # Catch platform like 'common' or 'linux'.
        (?P<page>.*[.]md)       # Catch tldr Markdown page.
        """,
        re.VERBOSE,
    )

    RE_CATCH_GITHUB_PLATFORM = re.compile(
        r"""
        (?:http[s]?://github.com/tldr-pages/tldr/(?:blob|tree))/  # GitHub URL.
        (?P<branch>.*)/         # Catch branches like 'master' or 'waldyrious/alt-syntax'.
        (?P<translation>.*)/    # Catch translations like 'pages' or 'pages.pt-BR'.
        (?P<platform>%s)        # Catch platform like 'common' or 'linux'
        (?:[/]?|$)              # Match optional trailing slash or end of string.
        """
        % RE_MATCH_TLDR_PLATFORM,
        re.VERBOSE,
    )

    RE_CATCH_GITHUB_TRANSLATION = re.compile(
        r"""
        (?:http[s]?://github.com/tldr-pages/tldr/(?:blob|tree))/  # GitHub  URL.
        (?P<branch>.*)/         # Catch branches like 'master' or 'waldyrious/alt-syntax'.
        (?P<translation>%s)     # Catch translations like 'pages' or 'pages.pt-BR'.
        (?:[/]?|$)              # Match optional trailing slash or end of string.
        """
        % RE_MATCH_TLDR_TRANSLATION,
        re.VERBOSE,
    )

    # User may give the file path in different ways. This regexp tries to get the
    # tldr platform out from the file path. The platform is needed for 'groups'
    # and 'tags' attributes. If the file path does not contain the tldr platform,
    # it cannot be read from the Markdown page and the value is not stored.
    #
    # Examples that work with this regexp:
    #
    #   1. /path/to/tldr/pages/linux/
    #   2. ./tldr/pages/linux/alpine.md
    #   3. ./tldr/pages.it/linux/alpine.md
    #   4. ../tldr/pages.pt-BR/linux/alpine.md
    #   5. ./pages/linux/
    #   6. ./alpine.md
    #   7. alpine.md
    RE_CATCH_LOCAL_TLDR_PAGES = re.compile(
        r"""
        (?:[.])?                        # Match optional leading dot like in './alpine.md'.
        (?:.*/tldr/)?                   # Match optional tldr project root path.
        (?P<translation>%s)?[/]?        # Catch optional translation.
        (?P<platform>%s)?[/]?           # Catch optional platform.
        (?P<page>[a-zA-Z0-9-]+[.]md)?   # Catch optional tldr page.
        """
        % (RE_MATCH_TLDR_TRANSLATION, RE_MATCH_TLDR_PLATFORM),
        re.VERBOSE,
    )

    RE_CATCH_TLDR_HEADER = re.compile(
        r"""
        [\#]+\s+         # Match Markdown headers token.
        (?P<header>\S+)  # Catch the header.
        """,
        re.VERBOSE,
    )

    RE_CATCH_TLDR_DESCRIPTION = re.compile(
        r"""
        [\#]+\s+[\S\s]+       # Match first line header.
        \n\n                  # Match one empty line after the header.
        [>]{1}\s+             # Match Markdown quote before description.
        (?P<description>.*?)  # Catch description ungreedely.
        \n\n                  # Match one empty line after the description.
        """,
        re.DOTALL | re.VERBOSE,
    )

    RE_CATCH_TLDR_SNIPPETS = re.compile(
        r"""
        [>]{1}\s+.*?      # Match description.
        \n\n              # Match empty line after description.
        (?P<snippets>.*)  # Catch tldr man page snippet.
        """,
        re.DOTALL | re.VERBOSE,
    )

    RE_CATCH_TLDR_SNIPPET = re.compile(
        r"""
        (?P<snippet>.*?)          # Catch a singpe snippet that contains a header and the snippet.
        (?=\n{2}[-]{1}\s{1}\S|$)  # Lookahead next snippet marked by list token or end of a string.
        """,
        re.DOTALL | re.VERBOSE,
    )

    RE_CATCH_TLDR_SNIPPET_COMMAND = re.compile(
        r"""
        \s?[-]{1}\s+       # Match optional leading whitespaces and first Markdown list token.
        (?P<comment>.*)\n  # Catch one line comment.
        \s+[`]             # Match whitespaces and the first backtick before the command.
        (?P<command>.*)    # Catch one line command.
        [`]                # Match the backtick after the command.
        """,
        re.DOTALL | re.VERBOSE,
    )

    RE_MATCH_STRING_LAST_COLUMN = re.compile(
        r"""
        [:]{1}$  # Match optional last column in multiline string.
        """,
        re.MULTILINE | re.VERBOSE,
    )

    RE_MATCH_MKDN_BLOCK_QUOTE_TOKEN = re.compile(
        r"""
        \n[>]{1}  # Match Markdown block quote after newline.
        """,
        re.MULTILINE | re.VERBOSE,
    )

    RE_CATCH_FIRST_SENTENCE = re.compile(
        r"""
        ^(?P<sentence>.*?[\.!?])  # Match the first sentence.
        """,
        re.MULTILINE | re.VERBOSE,
    )

    def __init__(self, logger, uri):
        self._logger = logger
        self._uri = self._get_uri(uri)
        self._schema = Schema()
        self._snippets = []
        self._i = 0

        self._read_tldr_pages()

    def __len__(self):
        """Return count of the snippets.

        Returns:
            int: The len of the iterator object.
        """

        return len(self._snippets)

    def __iter__(self):
        return self

    def next(self):
        """Return the next tldr man page.

        The returned pages are pre-formatted for Snippy tool.

        Returns:
            dict: The next tldr mage in interator.
        """

        if self._i < len(self):
            note = self._snippets[self._i]
            self._i += 1
        else:
            raise StopIteration

        return note

    def _get_uri(self, uri):
        """Format URI from the user.

        This method makes sure that the URI or path received from user is in
        correct format.

        The trailing slash is added if the URI is not pointing to a file. The
        trailing slash allows ``ulrjoin`` to add path objects like filenames
        to the URI without removing the last object in the URI path.

        Args:
            uri (str): URI or path received from the ``--file`` CLI option.

        Returns:
            str: Formatted URI for the plugin.
        """

        uri_ = uri if uri else self.TLDR_DEFAULT_URI
        _, file_extension = os.path.splitext(urlparse(uri_).path)
        if file_extension != ".md" and not uri_.endswith("/"):
            uri_ = uri_ + "/"

        return uri_

    def _read_tldr_pages(self):
        """Read all ``tldr pages`` from the URI."""

        pages = self._get_tlrd_pages(self._uri)
        for translation in pages:
            for platform in pages[translation]:
                self._read_pages(platform, pages[translation][platform])

    def _get_tlrd_pages(self, uri):
        """Get all ``tldr pages``.

        Read all tldr pages from the given URI. The pages are returned in a
        dictionary that contains keys for translations and tldr platforms.
        The tldr pages are in a list of full GitHub raw URLs under each
        platform.

        Args:
            uri (str): URI where the tldr pages are read.

        Returns:
            dict: All tldr pages with GitHib raw URL.
        """

        def count(data):
            """Count tldr pages and print log.

            Args:
                data (dict): All read tldr pages in a dictionary.
            """

            pages = 0
            platforms = 0
            translations = 0
            for translation in data:
                translations = translations + 1
                for platform in data[translation]:
                    platforms = platforms + 1
                    pages = pages + len(data[translation][platform])

            self._logger.debug(
                "read total of %d tldr pages from %d translations and %d platforms",
                pages,
                translations,
                platforms,
            )

        pages = {}
        match = self.RE_CATCH_GITHUB_PAGE.search(uri)
        if match and match.group("page"):
            self._logger.debug(
                "read tldr page: %s :from branch: %s",
                match.group("page"),
                match.group("branch"),
            )
            pages = {match.group("translation"): {match.group("platform"): (uri,)}}
            count(pages)

            return pages

        match = self.RE_CATCH_GITHUB_PLATFORM.search(uri)
        if match and match.group("platform"):
            self._logger.debug(
                "read tldr pages from platform: %s :from branch: %s",
                match.group("platform"),
                match.group("branch"),
            )
            pages = self._get_github_tldr_pages(
                match.group("branch"),
                (match.group("translation"),),
                (match.group("platform"),),
            )
            count(pages)

            return pages

        match = self.RE_CATCH_GITHUB_TRANSLATION.search(uri)
        if match and match.group("translation"):
            pages = self._get_github_tldr_pages(
                match.group("branch"),
                (match.group("translation"),),
                self.TLDR_PLATFORMS,
            )
            count(pages)

            return pages

        match = self.RE_CATCH_LOCAL_TLDR_PAGES.search(uri)
        if match:
            translation = match.groupdict().get("translations", "undefined")
            platform = match.groupdict().get("platform", "undefined")
            if os.path.isfile(uri) and os.access(uri, os.R_OK):
                pages = {translation: {platform: (uri,)}}
                count(pages)
            elif os.path.isdir(uri) and os.access(uri, os.R_OK):
                # Try to read under a platform or all platforms.
                files = glob(os.path.join(uri, "*.md"))
                if files:
                    pages = {translation: {platform: tuple(files)}}
                else:
                    pages[translation] = {}
                    platforms = os.listdir(uri)
                    for platform in platforms:
                        if platform in self.TLDR_PLATFORMS:
                            files = glob(os.path.join(uri + platform, "*.md"))
                            pages[translation][platform] = tuple(files)
                count(pages)
            else:
                Cause.push(
                    Cause.HTTP_FORBIDDEN,
                    "local tldr pages cannot be read: {}".format(uri),
                )

        return pages

    def _get_github_tldr_pages(self, branch, translations, platforms):
        """Get tldr pages.

        Method takes a list of translations and platforms to try to read all
        the needed tldr pages with as less GitHub API requests as possible.

        Args:
            branch (str): GitHub branch.
            translations (tuple): List of translations to read under the branch.
            platforms (tuple): List of platforms to read under the branch.

        Returns:
            dict: Tldr pages under given translations and platforms.
        """

        def read_translations(url, data, pages):
            """Read translations from the data.

            Args:
                url (str): URL to be added with translations, platforms and tldr pages.
                data (dict): GitHub JSON dictionary for a branch translations.
                pages (dict): Tldr pages stored under the branch.
            """

            for translation in translations:
                url_ = self._join_paths(url, translation)
                translation_url = next(
                    tree for tree in data["tree"] if tree["path"] == translation
                )["url"]
                platform_data = requests.get(translation_url).json()
                pages[translation] = {}
                read_platforms(url_, platforms, platform_data, pages[translation])

        def read_platforms(url, platforms, data, pages):
            """Read platforms from the data.

            Args:
                url (str): URL to be added with platforms and tldr pages.
                data (dict): GitHub JSON dictionary for a branch platforms.
                pages (dict): Tldr pages stored under each platforms.
            """

            for platform in platforms:
                pages[platform] = []
                try:
                    platform_url = next(
                        tree for tree in data["tree"] if tree["path"] == platform
                    )["url"]
                    pages_data = requests.get(platform_url).json()
                    url_ = self._join_paths(url, platform)
                    read_pages(url_, pages_data, pages[platform])
                except StopIteration:
                    pass

        def read_pages(url, data, pages):
            """Read tldr pages under the data

            Args:
                url (str): URL to be used with the read tldr pages.
                data (dict): GitHub JSON dictionary for a branch tldr pages.
                pages (dict): Tldr pages stored under a platform.
            """

            for tree in data["tree"]:
                if tree["type"] == "blob" and tree["path"].endswith(".md"):
                    pages.append(self._join_paths(url, tree["path"]))

        pages = {}
        repo_url = self._join_paths(self.GITHUB_API, "branches")
        repo_url = self._join_paths(repo_url, branch)
        resp = requests.get(repo_url)
        if self.is_api_error(resp):
            return pages
        data = resp.json()
        branch_url = data["commit"]["commit"]["tree"]["url"]
        translations_data = requests.get(branch_url).json()
        url = self._join_paths(self.GITHUB_RAW, branch)
        read_translations(url, translations_data, pages)

        return pages

    def _read_pages(self, platform, pages):
        """Read tldr pages from the platform.

        Args:
            platform (str): A tldr platform where the pages are read.
            pages (tuple): List of tldr pages under the platform.
        """

        for uri in pages:
            self._read_tldr_page(uri, platform)

    def _read_tldr_page(self, uri, platform):
        """Read a tldr page.

        Args:
            uri (str): URI or path where the tldr file is read.
            platform (str): Platform where the page is stored.
        """

        snippet = ""
        uri = self.RE_MATCH_GITHUB_URL.sub(self.GITHUB_RAW, uri)
        source = uri
        if "http" in urlparse(uri).scheme:
            self._logger.debug("request tldr page: %s", uri)
            page = requests.get(uri).text
        else:
            with open(uri, "r") as infile:
                self._logger.debug("read tldr page: %s", uri)
                page = infile.read()
            source = ""

        snippet = self._parse_tldr_page(source, platform, page)
        if snippet:  # and self._schema.validate(snippet):
            self._snippets.append(snippet)
        else:
            self._logger.debug("failed to parse tldr man page: %s :from: %s", uri, page)

    @staticmethod
    def _join_paths(uri, path_object):
        """Join URI or path to an object.

        Args:
            uri (str): URI or path base.
            path_object (str): Path object to be added to the URI.

        Returns:
            str: Joined URI or path.
        """

        if "http" in urlparse(uri).scheme:
            uri_ = uri
            if not uri_.endswith("/"):
                uri_ = uri_ + "/"
            path = urljoin(uri_, path_object)
        else:
            path = os.path.join(uri, path_object)

        return path

    def is_api_error(self, http):
        """Test if GitHub API response was an error.

        Args:
            http (obj): Request package response object.

        Returns:
            bool: True in case of REST API error response.
        """

        if http.status_code != 200:
            if http.headers.get("X-RateLimit-Remaining", "0") == "0":
                Cause.push(Cause.HTTP_FORBIDDEN, "github api rate limit reached")
            else:
                Cause.push(
                    Cause.HTTP_FORBIDDEN,
                    "github api failure:  {}".format(http.status_code),
                )
            self._logger.debug(
                "github api response %s with headers: %s"
                % (http.status_code, http.headers)
            )
            return True

        return False

    def _parse_tldr_page(self, source, platform, page):
        """Parse and validate one tldr man page.

        The method parses and validates one tldr man page to a snippet
        data structure for the Snippy tool.

        Args:
            source (str): A link where the tldr man page was read.
            platform (str): The platfrom where the tldr page belongs.
            page (str): A tldr man page in a text string.

        Returns:
            dict: Validated JSON structure from a tldr man page.
        """

        snippet = {}
        snippet["category"] = Const.SNIPPET
        snippet["data"] = self._read_tldr_data(page)
        snippet["brief"] = self._read_tldr_brief(page)
        snippet["description"] = self._read_tldr_description(page)
        snippet["name"] = self._read_tldr_name(page)
        snippet["groups"] = Parser.format_groups(Const.SNIPPET, platform)
        snippet["tags"] = Parser.format_tags(Const.SNIPPET, platform)
        snippet["links"] = Parser.format_links(Const.SNIPPET, source)
        snippet["source"] = source

        return snippet

    def _read_tldr_data(self, tldr):
        """Parse and format tldr man page ``data`` attribute.

        Args
            tldr (str): A tldr snippet in a text string.

        Returns:
            tuple: Formatted list of tldr man page snippets.
        """

        data = []
        match = self.RE_CATCH_TLDR_SNIPPETS.search(tldr)
        if match:
            snippets = self.RE_CATCH_TLDR_SNIPPET.findall(match.group("snippets"))
            if any(snippets):
                snippets = self._format_list(snippets)
                for snippet in snippets:
                    match = self.RE_CATCH_TLDR_SNIPPET_COMMAND.search(snippet)
                    if match:
                        comment = self.RE_MATCH_STRING_LAST_COLUMN.sub(
                            ".", match.group("comment")
                        )
                        data.append(
                            match.group("command") + Const.SNIPPET_COMMENT + comment
                        )
                    else:
                        self._logger.debug(
                            "parser was not able to read tldr snippet: %s", snippet
                        )
            else:
                self._logger.debug(
                    "parser did not find tldr snippets from snippet section: %s",
                    snippets,
                )
        else:
            self._logger.debug("parser did not find tldr snippets at all: %s", tldr)

        return Parser.format_data(Const.SNIPPET, data)

    def _read_tldr_brief(self, tldr):
        """Parse and format tldr man page ``brief`` attribute.

        Args
            tldr (str): A tldr snippet in a text string.

        Returns:
            str: Utf-8 encoded unicode string.
        """

        brief = ""
        match = self.RE_CATCH_TLDR_DESCRIPTION.search(tldr)
        if match:
            brief = self._format_brief(match.group("description"))

        return Parser.format_brief(Const.SNIPPET, brief)

    def _read_tldr_description(self, tldr):
        """Parse and format tldr man page ``description`` attribute.

        Args
            tldr (str): A tldr snippet in a text string.

        Returns:
            str: Utf-8 encoded unicode string.
        """

        description = ""
        match = self.RE_CATCH_TLDR_DESCRIPTION.search(tldr)
        if match:
            description = self._format_description(match.group("description"))

        return Parser.format_description(Const.SNIPPET, description)

    def _read_tldr_name(self, tldr):
        """Parse and format tldr man page ``name`` attribute.

        Args
            tldr (str): A tldr snippet in a text string.

        Returns:
            str: Utf-8 encoded unicode string.
        """

        name = ""
        match = self.RE_CATCH_TLDR_HEADER.search(tldr)
        if match:
            name = match.group("header")

        return Parser.format_name(Const.SNIPPET, name)

    @staticmethod
    def _format_list(data):
        """Remove empty strings and trim newlines from a list.

        Args
            data (list): List of strings.

        Returns:
            list: Formatted list of tldr man page snippets.
        """

        list_ = [value.strip() for value in data]
        list_ = list(filter(None, list_))

        return list_

    def _format_brief(self, brief):
        """Format brief description for tldr man page.

        Remove additional Markdown tokens like '>' and limit the length of
        the string to be more suitable for content ``brief`` attribute.

        The last dot is removed because it is not considered part of the
        ``brief`` attribute for styling issue.

        Args
            brief (str): Brief read from the tldr man page.

        Returns:
            str: Tldr specific format for the ``brief`` attribute.
        """

        brief = self.RE_MATCH_MKDN_BLOCK_QUOTE_TOKEN.sub("", brief)
        match = self.RE_CATCH_FIRST_SENTENCE.search(brief)
        if match:
            brief = self._limit_string(match.group("sentence").rstrip("."), 40)

        return brief

    def _format_description(self, description):
        """Format tldr man page description.

        Remove additional Markdown tokens like '>' from the description.

        Args
            description (str): Description read from the tldr man page.

        Returns:
            str: Tldr specific format for the ``description`` attribute.
        """

        return self.RE_MATCH_MKDN_BLOCK_QUOTE_TOKEN.sub("", description)

    @staticmethod
    def _limit_string(string_, len_):
        """Limit the string length"""

        return string_ if len(string_) <= len_ else string_[0 : len_ - 3] + "..."

    # Python 3 compatible iterator [1].
    #
    # [1] https://stackoverflow.com/a/28353158
    __next__ = next
