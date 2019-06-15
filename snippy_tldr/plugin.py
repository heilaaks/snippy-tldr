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


def snippy_import_hook(validator, parser, uri):
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

    tldr = SnippyTldr(validator, parser, uri)

    return tldr


class SnippyTldr(object):  # pylint: disable=too-few-public-methods
    """Plugin to import tldr man pages for snippy."""

    def __init__(self, validator, parser, uri):
        self._validate = validator
        self._parse = parser
        self._uri = uri
        self._notes = []
        self._i = 0

        self._parse_notes()

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

    def _parse_notes(self):
        """Parse notes."""

        self._notes.append({
            'category': 'snippet',
            'data': 'docker ps',
            'brief': 'print containers',
            'description': 'long description',
            'name': 'note name',
            'groups': ('docker',),
            'tags': ('tags', 'tag2'),
            'links': ('http://link.html',),
            'source': 'note source',
            'versions': ('tldr>=0.10.0',),
            'languages': ('python>=0.10.0',),
            'filename': 'filename.txt'})

    # Python 3 compatible iterator [1].
    #
    # [1] https://stackoverflow.com/a/28353158
    __next__ = next
