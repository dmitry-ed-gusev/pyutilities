#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Some useful/convenient functions related to GIT.

    Created:  Dmitrii Gusev, 03.05.2019
    Modified: Dmitrii Gusev, 25.11.2022
"""

import logging
from subprocess import Popen
from pyutilities.utils.common_utils import myself
from pyutilities.exception import PyUtilitiesException
from pyutilities.defaults import MSG_MODULE_ISNT_RUNNABLE

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

# useful constants
GIT_EXECUTABLE = "git"


# todo: save currently set global proxy and restore it after this class
class PyGit:
    """Class represents GIT functionality"""

    def __init__(self, git_url, http=None, https=None):
        log.info("Initializing PyGit class.")
        # init internal state
        self.__git_url = git_url
        # set up proxy if specified
        # self.set_global_proxy(http, https)

    def set_global_proxy(self, http=None, https=None):  # todo: unit tests! make it decorator?
        """Set specified proxies (http/https) for local git instance as a global variables."""
        log.debug(f"{myself()}() is working.")
        log.info(f"Setting proxies: http -> [{http}], https -> [{https}]")
        if http:
            log.info(f"Setting HTTP proxy: {http}")
            process = Popen([GIT_EXECUTABLE, "config", "--global", "http.proxy", http])
            process.wait()
        if https:
            log.info(f"Setting HTTPS proxy: {https}")
            process = Popen([GIT_EXECUTABLE, "config", "--global", "https.proxy", https])
            process.wait()

    def clean_global_proxy(self):  # todo: unit tests! make it decorator?
        """Clear git global proxies (both http/https)."""
        log.debug(f"{myself()}() is working.")
        log.info("Cleaning up git global proxies.")
        process = Popen([GIT_EXECUTABLE, "config", "--global", "--unset", "http.proxy"])
        process.wait()
        process = Popen([GIT_EXECUTABLE, "config", "--global", "--unset", "https.proxy"])
        process.wait()

    def __generate_repo_url(self, repo):
        """Generates repository URL for other methods. Internal method."""
        url = self.__git_url + "/" + repo + ".git"
        # log.debug(f"Generated url [{url}]")  # <- shows password in cmd line...
        return url

    def clone(self, repo, location):
        """Clone specified repository."""
        log.info(f"Clone repo [{repo}].")
        try:
            process = Popen([GIT_EXECUTABLE, "clone", self.__generate_repo_url(repo)], cwd=location)
            process.wait()

            if process.returncode != 0:
                raise PyUtilitiesException(f"Process returned non zero exit code [{process.returncode}]!")
        except AttributeError as se:
            log.error(f"Error while cloning repo [{repo}]! {se}")

    def pull(self, repo, location):
        """Pull (update) specified repository."""
        log.info(f"Pull repo [{repo}]")
        try:
            process = Popen([GIT_EXECUTABLE, "pull"], cwd=location)
            process.wait()

            if process.returncode != 0:
                raise PyUtilitiesException(f"Process returned non zero exit code [{process.returncode}]!")
        except AttributeError as se:
            log.error(f"Error while updating repo [{repo}]! {se}")

    def gc(self, repo, location):
        """execute gc() - garbage collection - for repository."""
        log.info(f"Calling gc() for repo [{repo}]")
        try:
            process = Popen([GIT_EXECUTABLE, "gc"], cwd=location)
            process.wait()

            if process.returncode != 0:
                raise PyUtilitiesException(f"Process returned non zero exit code [{process.returncode}]!")
        except AttributeError as se:
            log.error(f"Error while calling gc() for [{repo}]! {se}")


class GitException(Exception):
    """GIT Exception, used if something is wrong with/in GIT interaction."""


if __name__ == "__main__":
    print(MSG_MODULE_ISNT_RUNNABLE)
