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

"""helper: Test case helper methods."""

import responses


class classproperty(object):  # pylint: disable=too-few-public-methods, invalid-name
    """Implement classproperty.

    Decorator that mimics object property [1].

    [1] https://stackoverflow.com/a/3203659
    """

    def __init__(self, getter):
        self._getter = getter

    def __get__(self, _, owner):
        """Get property of a class."""

        return self._getter(owner)


class GitHubApi(object):
    """Helper methods for GitHub API testing."""

    @classmethod
    def mock(cls, expect):
        """Mock HTTP methods.

        Mock HTTP responses based on HTTP Archive (HAR) formatted dictionary.
        In case of tldr page testing against the GitHub, HTTP request method
        is always a HTTP GET method.

        Args:
            expect (dict): HAR formatted dictionary with expected HTTP methods.

        Returns:
            obj: Responses object that mocks the Requests module.
        """

        for http in expect:
            if "text" in http["response"]["content"]:
                responses.add(
                    responses.GET,
                    http["request"]["url"],
                    body=http["response"]["content"]["text"],
                    status=http["response"]["status"],
                )
            else:
                responses.add(
                    responses.GET,
                    http["request"]["url"],
                    json=http["response"]["content"]["json"],
                    status=http["response"]["status"],
                )

        return responses

    @classmethod
    def validate(cls, expect, actual):
        """Assert expected REST API calls to actual values.

        Validate actual HTTP responses against expected responses that are
        in a HTTP Archive (HAR) formatted dictionary.

        Args:
            expect (dict): Expected values in HAR formatted dictionary.
            actual (obj): Actual calls in the Responses object.

        Returns:
            bool: Always True if all asserts passed.
        """

        for i, http in enumerate(expect):
            assert actual.calls[i].request.method == "GET"
            assert http["request"]["url"] == actual.calls[i].request.url
            for header in http["request"]["headers"]:
                assert header["name"] in actual.calls[i].request.headers

        return True

    @classproperty
    def branch(cls):  # pylint: disable=no-self-argument, no-self-use
        """GitHub API response for branch.

        Returns:
            dict: GitHub API response for branch.
        """

        branch = {
            "name": "master",
            "commit": {
                "sha": "d496b0c18f450c4504c0c643ade531e79fdd1484",
                "node_id": "MDY6Q29tbWl0MTUwMTk5NjI6ZDQ5NmIwYzE4ZjQ1MGM0NTA0YzBjNjQzYWRlNTMxZTc5ZmRkMTQ4NA==",
                "commit": {
                    "message": "astyle: reword description (#3150)",
                    "tree": {
                        "sha": "67c429acf561194366a25a28fe73fb33ec0739dc",
                        "url": "https://api.github.com/repos/tldr-pages/tldr/git/trees/67c429acf561194366a25a28fe73fb33ec0739dc",
                    },
                },
            },
        }

        return branch

    @classproperty
    def translations(cls):  # pylint: disable=no-self-argument, no-self-use
        """GitHub API response for translations under the branch.

        Returns:
            dict: GitHub API response for translations under the branch.
        """

        translations = {
            "sha": "67c429acf561194366a25a28fe73fb33ec0739dc",
            "url": "https://api.github.com/repos/tldr-pages/tldr/git/trees/67c429acf561194366a25a28fe73fb33ec0739dc",
            "tree": [
                {
                    "path": ".editorconfig",
                    "type": "blob",
                    "sha": "197cb78962bd0973086f89d4421138e1d82f9080",
                    "size": 235,
                    "url": "https://api.github.com/repos/tldr-pages/tldr/git/blobs/197cb78962bd0973086f89d4421138e1d82f9080",
                },
                {
                    "path": "pages.pt-BR",
                    "mode": "040000",
                    "type": "tree",
                    "sha": "6b55cdc79c194f1951f3cd75f8908732d8a6e451",
                    "url": "https://api.github.com/repos/tldr-pages/tldr/git/trees/6b55cdc79c194f1951f3cd75f8908732d8a6e451",
                },
                {
                    "path": "pages",
                    "mode": "040000",
                    "type": "tree",
                    "sha": "64605406ef576220cbb6b59f64c525778e1bc6b8",
                    "url": "https://api.github.com/repos/tldr-pages/tldr/git/trees/64605406ef576220cbb6b59f64c525778e1bc6b8",
                },
            ],
        }

        return translations

    @classproperty
    def platforms(cls):  # pylint: disable=no-self-argument, no-self-use
        """GitHub API response for platforms under translation.

        Returns:
            dict: GitHub API response for platforms under translation.
        """

        platforms = {
            "sha": "64605406ef576220cbb6b59f64c525778e1bc6b8",
            "url": "https://api.github.com/repos/tldr-pages/tldr/git/trees/64605406ef576220cbb6b59f64c525778e1bc6b8",
            "tree": [
                {
                    "path": "common",
                    "mode": "040000",
                    "type": "tree",
                    "sha": "63f4c272b4bc0a80c0f9f805766de29bac0bc055",
                    "url": "https://api.github.com/repos/tldr-pages/tldr/git/trees/63f4c272b4bc0a80c0f9f805766de29bac0bc055",
                },
                {
                    "path": "linux",
                    "mode": "040000",
                    "type": "tree",
                    "sha": "9ec6d298a44e3ff1b47f1a6d98942826a598c54a",
                    "url": "https://api.github.com/repos/tldr-pages/tldr/git/trees/9ec6d298a44e3ff1b47f1a6d98942826a598c54a",
                },
            ],
        }

        return platforms

    @classproperty
    def pages(cls):  # pylint: disable=no-self-argument, no-self-use
        """GitHub API response for pages under platform.

        Returns:
            dict: GitHub API response for pages under platform..
        """

        pages = {
            "sha": "9ec6d298a44e3ff1b47f1a6d98942826a598c54a",
            "url": "https://api.github.com/repos/tldr-pages/tldr/git/trees/9ec6d298a44e3ff1b47f1a6d98942826a598c54a",
            "tree": [
                {
                    "path": "add-apt-repository.md",
                    "mode": "100644",
                    "type": "blob",
                    "sha": "154a62ebd45b38671f1ec4604eeaa8932a55f85c",
                    "size": 402,
                    "url": "https://api.github.com/repos/tldr-pages/tldr/git/blobs/154a62ebd45b38671f1ec4604eeaa8932a55f85c",
                },
                {
                    "path": "adduser.md",
                    "mode": "100644",
                    "type": "blob",
                    "sha": "c495e0cd9bd62bf6b7360dd60ab6b25d0232dc05",
                    "size": 653,
                    "url": "https://api.github.com/repos/tldr-pages/tldr/git/blobs/c495e0cd9bd62bf6b7360dd60ab6b25d0232dc05",
                },
            ],
        }

        return pages

    @classproperty
    def default(cls):  # pylint: disable=no-self-argument, no-self-use
        """The default GitHub API API calls.

        Returns:
            dict: GitHub API response for pages under platform..
        """

        default = [
            {
                "request": {
                    "url": "https://api.github.com/repos/tldr-pages/tldr/branches/master",
                    "headers": {},
                },
                "response": {"status": 200, "content": {"json": GitHubApi.branch}},
            },
            {
                "request": {
                    "url": "https://api.github.com/repos/tldr-pages/tldr/git/trees/67c429acf561194366a25a28fe73fb33ec0739dc",
                    "headers": {},
                },
                "response": {
                    "status": 200,
                    "content": {"json": GitHubApi.translations},
                },
            },
            {
                "request": {
                    "url": "https://api.github.com/repos/tldr-pages/tldr/git/trees/64605406ef576220cbb6b59f64c525778e1bc6b8",
                    "headers": {},
                },
                "response": {"status": 200, "content": {"json": GitHubApi.platforms}},
            },
            {
                "request": {
                    "url": "https://api.github.com/repos/tldr-pages/tldr/git/trees/9ec6d298a44e3ff1b47f1a6d98942826a598c54a",
                    "headers": {},
                },
                "response": {"status": 200, "content": {"json": GitHubApi.pages}},
            },
            {
                "request": {
                    "url": "https://raw.githubusercontent.com/tldr-pages/tldr/master/pages/linux/add-apt-repository.md",
                    "headers": {},
                },
                "response": {
                    "status": 200,
                    "content": {"text": TldrPage.add_apt_repository},
                },
            },
            {
                "request": {
                    "url": "https://raw.githubusercontent.com/tldr-pages/tldr/master/pages/linux/adduser.md",
                    "headers": {},
                },
                "response": {"status": 200, "content": {"text": TldrPage.adduser}},
            },
        ]

        return default


class TldrPage(object):
    """Helper methods for tldr page examples."""

    @classproperty
    def add_apt_repository(cls):  # pylint: disable=no-self-argument, no-self-use
        """Add-apt-repository tldr page from Linux platform.

        Returns:
            str: The add-apt-repository tldr page in a text string.
        """

        text = (
            "# add-apt-repository",
            "",
            "> Manages apt repository definitions.",
            "",
            "- Add a new apt repository:",
            "",
            "`add-apt-repository {{repository_spec}}`",
            "",
            "- Remove an apt repository:",
            "",
            "`add-apt-repository --remove {{repository_spec}}`",
            "",
            "- Update the package cache after adding a repository:",
            "",
            "`add-apt-repository --update {{repository_spec}}`",
            "",
            "- Enable source packages:",
            "",
            "`add-apt-repository --enable-source {{repository_spec}}`",
        )

        return "\n".join(text)

    @classproperty
    def adduser(cls):  # pylint: disable=no-self-argument, no-self-use
        """Adduser tldr page from English translated Linux platform.

        Returns:
            str: The adduser tldr page in a text string.
        """

        text = (
            "# adduser",
            "",
            "> User addition utility.",
            "",
            "- Create a new user with a default home directory and prompt the user to set a password:",
            "",
            "`adduser {{username}}`",
            "",
            "- Create a new user without a home directory:",
            "",
            "`adduser --no-create-home {{username}}`",
            "",
            "- Create a new user with a home directory at the specified path:",
            "",
            "`adduser --home {{path/to/home}} {{username}}`",
            "",
            "- Create a new user with the specified shell set as the login shell:",
            "",
            "`adduser --shell {{path/to/shell}} {{username}}`",
            "",
            "- Create a new user belonging to the specified group:",
            "",
            "`adduser --ingroup {{group}} {{username}}`",
            "",
            "- Add an existing user to the specified group:",
            "",
            "`adduser {{username}} {{group}}`",
        )

        return "\n".join(text)

    @classproperty
    def pushd(cls):  # pylint: disable=no-self-argument, no-self-use
        """Pushd tldr page from English translated Linux platform.

        Returns:
            str: The pushd tldr page in a text string.
        """

        text = (
            "# pushd",
            "",
            "> Place a directory on a stack so it can be accessed later.",
            "> See also `popd` to switch back to original directory.",
            "",
            "- Switch to directory and push it on the stack:",
            "",
            "`pushd < {{directory}}`",
            "",
            "- Switch first and second directories on the stack:",
            "",
            "`pushd`",
            "",
            "- Rotate stack by making the 5th element the top of the stack:",
            "",
            "`pushd +4`",
        )

        return "\n".join(text)


class Snippet(object):
    """Helper methods for parsed tldr pages."""

    @classproperty
    def add_apt_repository(cls):  # pylint: disable=no-self-argument, no-self-use
        """Add-apt-repository tldr page in a snippet.

        Returns:
            dict: Snippet parsed from the add-apt-repository tldr page.
        """

        snippet = {
            "category": "snippet",
            "data": [
                "add-apt-repository {{repository_spec}}  #  Add a new apt repository.",
                "add-apt-repository --remove {{repository_spec}}  #  Remove an apt repository.",
                "add-apt-repository --update {{repository_spec}}  #  Update the package cache after adding a repository.",
                "add-apt-repository --enable-source {{repository_spec}}  #  Enable source packages.",
            ],
            "brief": "Manages apt repository definitions.",
            "description": "Manages apt repository definitions.",
            "name": "add-apt-repository",
            "groups": ["linux"],
            "tags": ["linux"],
            "links": [
                "https://raw.githubusercontent.com/tldr-pages/tldr/master/pages/linux/add-apt-repository.md"
            ],
            "source": "https://raw.githubusercontent.com/tldr-pages/tldr/master/pages/linux/add-apt-repository.md",
        }

        return snippet

    @classproperty
    def adduser(cls):  # pylint: disable=no-self-argument, no-self-use
        """Adduser tldr page in a snippet.

        Returns:
            dict: Snippet parsed from the adduser tldr page.
        """

        snippet = {
            "category": "snippet",
            "data": [
                "adduser {{username}}  #  Create a new user with a default home directory and prompt the user to set a password.",
                "adduser --no-create-home {{username}}  #  Create a new user without a home directory.",
                "adduser --home {{path/to/home}} {{username}}  #  Create a new user with a home directory at the specified path.",
                "adduser --shell {{path/to/shell}} {{username}}  #  Create a new user with the specified shell set as the login shell.",
                "adduser --ingroup {{group}} {{username}}  #  Create a new user belonging to the specified group.",
                "adduser {{username}} {{group}}  #  Add an existing user to the specified group.",
            ],
            "brief": "User addition utility.",
            "description": "User addition utility.",
            "name": "adduser",
            "groups": ["linux"],
            "tags": ["linux"],
            "links": [
                "https://raw.githubusercontent.com/tldr-pages/tldr/master/pages/linux/adduser.md"
            ],
            "source": "https://raw.githubusercontent.com/tldr-pages/tldr/master/pages/linux/adduser.md",
        }

        return snippet

    @classproperty
    def pushd(cls):  # pylint: disable=no-self-argument, no-self-use
        """Pushd tldr page in a snippet.

        Returns:
            dict: Snippet parsed from the pushd tldr page.
        """

        snippet = {
            "category": "snippet",
            "data": [
                "pushd < {{directory}}  #  Switch to directory and push it on the stack.",
                "pushd  #  Switch first and second directories on the stack.",
                "pushd +4  #  Rotate stack by making the 5th element the top of the stack.",
            ],
            "brief": "Place a directory on a stack so it ca...",
            "description": "Place a directory on a stack so it can be accessed later. See also `popd` to switch back to original directory.",
            "name": "pushd",
            "groups": ["linux"],
            "tags": ["linux"],
            "links": [
                "https://raw.githubusercontent.com/tldr-pages/tldr/master/pages/linux/pushd.md"
            ],
            "source": "https://raw.githubusercontent.com/tldr-pages/tldr/master/pages/linux/pushd.md",
        }

        return snippet
