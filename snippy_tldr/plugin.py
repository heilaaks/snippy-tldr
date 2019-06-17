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

"""Snippy-tldr is a plugin to import tldr man pages for Snippy."""

import os
import re

try:
    from urllib.parse import urljoin
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urljoin, urlparse

import requests

try:
    from snippy.plugins import Const
    from snippy.plugins import Parser
except ImportError:
    pass


def snippy_import_hook(logger, uri, validator, parser):
    """Import notes for Snippy.

    This is an import hook that returns an iterator object. The iterator must
    be an iterable class that implements next() and len() methods. The iterator
    must return JSON structures that pass the ``validate.note()``.

    If suitable, the ``parse`` object may be used to parse the source data to
    JSON note for Snippy.

    Args
        validate (obj): A ``SnippyNotesValidator`` object to validate JSON notes.
        parse (obj): A ``SnippyNotesParser`` to parse notes attributes.
        uri (str): The value of ``-f|--file`` command line option from Snippy tool.

    Returns:
        obj: Iterator object to store JSON notes.

    Examples
    --------
    >>> def __init__(self, validator, parser, uri):
    >>>     self.validate = Validator
    >>>     self.parse = parser
    >>>     self.uri = uri
    >>>     self._parse_notes()
    >>>
    >>> def _parse_notes(self):
    >>>     filename = 'notes-list.md'
    >>>     with open(filename, 'w') as infile:
    >>>         note = self._parse_note(infile)
    >>>         if validate.note(note):
    >>>             self.notes.append(note)
    >>>
    >>> def _parse_note(self, infile)
    >>>     note = {}
    >>>     note['category'] = self.parse
    """

    tldr = SnippyTldr(logger, uri, validator, parser)

    return tldr


class SnippyTldr(object):  # pylint: disable=too-many-instance-attributes
    """Plugin to import tldr man pages for snippy."""

    TLDR_URI = "https://github.com/tldr-pages/tldr/tree/master/pages/linux"
    TLDR_PAGES = ("common", "linux", "osx", "sunos", "windows")

    RE_CATCH_TLDR_FILENAME = re.compile(
        r"""
        .*[\/]         # Match greedily the last leading forward slash before the filename.
        (\S+[.]{1}md)  # Catch filename with the md file extension.
        [\"]{1}        # Match trailing quotation mark in HTML after filename
        """,
        re.VERBOSE,
    )

    RE_CATCH_TLDR_PAGE = re.compile(
        r"""
        /tldr-pages/tldr/tree/\S+/pages/  # Match HTML page to find the pages.
        (?P<page>.*)                      # Catch tldr page.
        ["]                               # Match trailing quotation mark.
        """,
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
        [\#]+\s+\S+           # Match first line header.
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

    def __init__(self, logger, uri, validator, parser):
        self._logger = logger
        self._validate = validator
        self._parse = parser
        self._uri = uri if uri else self.TLDR_URI
        self._uri_scheme = urlparse(self._uri).scheme
        self._uri_path = urlparse(self._uri).path
        self._snippets = []
        self._i = 0

        print("uri: %s", self._uri)
        print("scheme: %s", self._uri_scheme)
        print("path: %s", self._uri_path)

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
        """Return the next snippet.

        Returns:
            dict: The next note in interator.
        """

        if self._i < len(self):
            note = self._snippets[self._i]
            self._i += 1
        else:
            raise StopIteration

        return note

    def _read_tldr_pages(self):
        """Read tldr man pages."""

        filenames = self._get_tlrd_filenames(self._uri)
        for page in filenames:
            self._read_page(page, filenames[page])

    def _get_tlrd_filenames(self, uri):
        """Get all tldr filenames.

        Read all tldr man page snippet filenames under the URI.

        Args:
            uri (str): URI where the tldr snippets are read.

        Returns:
            dict: Tldr pages and files in each page.
        """

        filenames = {}
        last_object = os.path.basename(os.path.normpath(uri))
        if last_object == "pages":
            self._logger.debug("read all tldr man pages from: %s", uri)
            pages = self._get_tldr_pages()
            for page in pages:
                print("page: %s" % page)
                self._get_tlrd_filenames(page)
        elif ".md" in last_object:
            self._logger.debug("read one tldr man page snippet: %s", uri)
            print("file: %s" % uri)
        elif uri in ("/tldr/pages", "tldr-pages/tldr"):
            self._logger.debug("read tldr man page: %s", uri)
            print("group: %s" % uri)
        else:
            self._logger.debug("unknown tldr man page path: %s", uri)

        return filenames

    def _get_tldr_pages(self):
        """Read tldr pages from URI or file path.

        The give URI is pointing to ``tldr/pages/``. The URI may be a remote
        or localhost URI. There can be any amount of pages under the URI but
        only the known tldr pages are read. Unknown directories from the URI
        given by user are discarded.

        The returned list of tldr pages is in format that allows reading the
        tldr snippets under each tldr page.

        Returns:
            list: Tldr man pages with URI or file path.
        """

        pages = []
        if "http" in self._uri_scheme:
            html = requests.get(self._uri).text
            pages = self.RE_CATCH_TLDR_PAGE.findall(html)
        else:
            try:
                pages = os.listdir(self._uri_path)
            except FileNotFoundError:
                self._logger.debug(
                    "localhost path was not accessible: %s", self._uri_path
                )

        # Pick only the known tldr pages and format the list of pages to be
        # file paths or URLs to be directly usable by caller.
        pages = sorted(list(set(self.TLDR_PAGES) & set(pages)))
        pages_ = []
        for page in pages:
            if "http" in self._uri_scheme:
                pages_.append(urljoin(self._uri, page))
            else:
                pages_.append(os.path.join(self._uri, page))
        self._logger.debug("parsed tldr pages: %s", pages)

        return pages_

    def _read_page(self, page, files):
        """Read snippets from the tldr man page.

        Args:
            page (str): Name of the tldr page.
            filenames (tuple): List of filenames under the page.
        """

        for uri in files:
            tldr_page = self._read_tldr_file(uri)
            snippet = self._parse_tldr_page(tldr_page, page)
            if snippet:
                self._snippets.append(snippet)
            else:
                self._logger.debug(
                    "failed to parse tldr man page: %s :from: %s", uri, tldr_page
                )

    def _read_tldr_file(self, uri):
        """Read tldr file."""

        tldr_page = ""
        if "http" in self._uri_scheme:
            tldr_page = requests.get(uri).text
        else:
            with open(uri, "r") as infile:
                tldr_page = infile.read()

        return tldr_page

    def _parse_tldr_page(self, page, source):
        """Parse and valudate one tldr man page.

        The method parses and validates one tldr man page to a snippet
        data structure for Snippy tool.

        Args
            page (str): A tldr man page in text string.
            source (str): A link where the tldr man page was read.

        Returns:
            dict: Validated JSON structure from a tldr man page.
        """

        snippet = {}
        snippet["category"] = Const.SNIPPET
        snippet["data"] = self._read_tldr_data(page)
        snippet["brief"] = self._read_tldr_brief(page)
        snippet["description"] = self._read_tldr_description(page)
        snippet["name"] = self._read_tldr_name(page)
        snippet["source"] = source

        return snippet

    def _read_tldr_data(self, page):
        """Parse and format tldr man page ``data`` attribute.

        Args
            page (str): A tldr man page in utf-8 encoded text string.

        Returns:
            tuple: Formatted list of tldr man page snippets.
        """

        data = []
        match = self.RE_CATCH_TLDR_SNIPPETS.search(page)
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
            self._logger.debug("parser did not find tldr snippets at all: %s", page)

        return Parser.format_data(Const.SNIPPET, data)

    def _read_tldr_brief(self, page):
        """Parse and format tldr man page ``brief`` attribute.

        Args
            page (str): A tldr man page in utf-8 encoded text string.

        Returns:
            str: Utf-8 encoded unicode string.
        """

        brief = ""
        match = self.RE_CATCH_TLDR_DESCRIPTION.search(page)
        if match:
            brief = self._format_brief(match.group("description"))

        return Parser.format_brief(Const.SNIPPET, brief)

    def _read_tldr_description(self, page):
        """Parse and format tldr man page ``description`` attribute.

        Args
            page (str): A tldr man page in utf-8 encoded text string.

        Returns:
            str: Utf-8 encoded unicode string.
        """

        description = ""
        match = self.RE_CATCH_TLDR_DESCRIPTION.search(page)
        if match:
            description = self._format_description(match.group("description"))

        return Parser.format_description(Const.SNIPPET, description)

    def _read_tldr_name(self, page):
        """Parse and format tldr man page ``name`` attribute.

        Args
            page (str): A tldr man page in utf-8 encoded text string.

        Returns:
            str: Utf-8 encoded unicode string.
        """

        name = ""
        match = self.RE_CATCH_TLDR_HEADER.search(page)
        if match:
            name = match.group("header")

        return Parser.format_name(Const.SNIPPET, name)

    @staticmethod
    def _format_list(list_):
        """Remove empty strings and trim newlines from a list.

        Args
            list_ (list): List of strings.

        Returns:
            list: Formatted list of tldr man page snippets.
        """

        list_ = map(Const.TEXT_TYPE.strip, list_)
        list_ = list(filter(None, list_))

        return list_

    def _format_brief(self, brief):
        """Format brief description for tldr man page.

        Remove additional Markdown tokens like '>' and limit the length of
        the string to be more suitable for content ``brief`` attribute.

        Args
            brief (str): Brief read from the tldr man page.

        Returns:
            str: Tldr specific format for the ``brief`` attribute.
        """

        brief = self.RE_MATCH_MKDN_BLOCK_QUOTE_TOKEN.sub("", brief)
        match = self.RE_CATCH_FIRST_SENTENCE.search(brief)
        if match:
            brief = self._limit_string(match.group("sentence"), 40)

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
