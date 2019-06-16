#!/usr/bin/env python
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

"""Snippy-tldr is a plugin to import tldr man pages for snippy."""

import re

import requests

from snippy.constants import Constants as Const


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


class SnippyTldr(object):  # pylint: disable=too-few-public-methods
    """Plugin to import tldr man pages for snippy."""

    # A Snippy tool specific separator for snippet and comment.
    SNIPPET_COMMENT = "  #  "

    RE_CATCH_TLDR_FILENAME = re.compile(
        r"""
        .*[\/]         # Match greedily the last leading forward slash before the filename.
        (\S+[.]{1}md)  # Catch filename with the md file extension.
        [\"]{1}        # Match trailing quotation mark in HTML after filename
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

    def __init__(self, logger, uri, validator, parser):
        self._logger = logger
        self._validate = validator
        self._parse = parser
        self._uri = uri
        self._notes = []
        self._i = 0

        self._read_tldr_pages()

    def __len__(self):
        """Return count of the notes.

        Returns:
            int: The len of the iterator object.
        """

        return len(self._notes)

    def __iter__(self):
        return self

    def next(self):
        """Return the next note.

        Returns:
            dict: The next note in interator.
        """

        if self._i < len(self):
            note = self._notes[self._i]
            self._i += 1
        else:
            raise StopIteration

        return note

    def _read_tldr_pages(self):
        """Read tldr man pages."""

        response = requests.get(
            "https://github.com/tldr-pages/tldr/tree/master/pages/linux"
        )
        files = sorted(set(self.RE_CATCH_TLDR_FILENAME.findall(response.text)))
        self._logger.debug("scanned: %s :tld notes", len(files))
        files = files[:4]
        for filename in files:
            print("parse page: %s" % filename)
            tldr_page = (
                "https://raw.githubusercontent.com/tldr-pages/tldr/master/pages/linux/"
                + filename
            )
            note = self._parse_tldr_page(requests.get(tldr_page).text, tldr_page)
            if note:
                self._notes.append(note)
            else:
                self._logger.debug("failed to parse tldr man page", tldr_page)
        print(self._notes)
        print("len: %s", len(self._notes))

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
        print("===")
        print(snippet)
        print("===")

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
                snippets = self._beautify_snippets(snippets)
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

        return tuple(data)

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
            brief = match.group("description").replace("\n", " ").replace("\r", "")

        return brief

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
            description = (
                match.group("description").replace("\n", " ").replace("\r", "")
            )

        return description

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

        return name

    @staticmethod
    def _beautify_snippets(snippets):
        """Remove empty strings and trim newlines from list of tldr snippets.

        Args
            snippets (list): List of raw capture from tldr man page snippet.

        Returns:
            list: Formatted list of tldr man page snippets.
        """

        snippets = map(Const.TEXT_TYPE.strip, snippets)
        snippets = list(filter(None, snippets))

        return snippets

    # Python 3 compatible iterator [1].
    #
    # [1] https://stackoverflow.com/a/28353158
    __next__ = next
