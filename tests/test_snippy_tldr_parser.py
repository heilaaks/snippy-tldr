# -*- coding: utf-8 -*-
#
#  SPDX-License-Identifier: AGPL-3.0-or-later
#
#  snippy - software development and maintenance notes manager.
#  Copyright 2019-2020 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""test_snippy_tldr_parser: Test tldr man page import plugin parser."""

from snippy_tldr.plugin import SnippyTldr


class TestSnippyTldrParser(object):  # pylint: disable=too-few-public-methods
    """Test tldr plugin parser."""

    @staticmethod
    def test_tldr_page_parser_001():
        """Test parsing snippet.

        Test case verifies that multiline description with special characters
        is parsed correctly.
        """

        page = (
            "# brew bundle",
            "",
            "> Bundler for Homebrew, Homebrew Cask and the Mac App Store.",
            "> More information: <https://github.com/Homebrew/homebrew-bundle>.",
            "",
            "- Install packages from a Brewfile at the current path:",
            "",
            "`brew bundle`",
            "",
            "- Install packages from a specific Brewfile at a specific path:",
            "",
            "`brew bundle --file={{path/to/file}}`",
            "",
            "- Create a Brewfile from all installed packages:",
            "",
            "`brew bundle dump`",
            "",
            "- Uninstall all formulae not listed in the Brewfile:",
            "",
            "`brew bundle cleanup --force`",
            "",
            "- Check if there is anything to install or upgrade in the Brewfile:",
            "",
            "`brew bundle check`",
            "",
            "- Output a list of all entries in the Brewfile:",
            "",
            "`brew bundle list --all`",
        )
        content = {
            "category": "snippet",
            "data": [
                "brew bundle  #  Install packages from a Brewfile at the current path.",
                "brew bundle --file={{path/to/file}}  #  Install packages from a specific Brewfile at a specific path.",
                "brew bundle dump  #  Create a Brewfile from all installed packages.",
                "brew bundle cleanup --force  #  Uninstall all formulae not listed in the Brewfile.",
                "brew bundle check  #  Check if there is anything to install or upgrade in the Brewfile.",
                "brew bundle list --all  #  Output a list of all entries in the Brewfile.",
            ],
            "brief": "Bundler for Homebrew, Homebrew Cask a...",
            "description": "Bundler for Homebrew, Homebrew Cask and the Mac App Store. More information: <https://github.com/Homebrew/homebrew-bundle>.",  # pylint: disable=line-too-long
            "name": "brew",
            "groups": ["osx"],
            "tags": ["osx"],
            "links": [],
            "source": "",
        }
        snippet = SnippyTldr(  # pylint: disable=protected-access
            Logger(), "../tldr/pages/osx/brew-bundle.md"
        )._parse_tldr_page("", "osx", "\n".join(page))
        assert content == snippet


class Logger(object):  # pylint: disable=too-few-public-methods
    """Logger mock."""

    def debug(self, *args, **kwargs):
        """Dummy debug method."""
