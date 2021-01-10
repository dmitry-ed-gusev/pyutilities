#!/usr/bin/env python
# coding=utf-8

"""

    Some useful/convenient functions related to GIT.

    13.05.2019 Module is in DRAFT state.

    Created:  Dmitrii Gusev, 03.05.2019
    Modified: Dmitrii Gusev, 27.05.2019

"""

from subprocess import Popen
from pyutilities.pylog import init_logger, myself
from pyutilities.pyexception import PyUtilsException

# useful constants
GIT_EXECUTABLE = 'git'


# todo: save currently set global proxy and restore it after this class
class PyGit:
    """ Class represents GIT functionality """

    def __init__(self, git_url,  http=None, https=None):
        self.log = init_logger(__name__, add_null_handler=False)
        self.log.info("Initializing PyGit class.")
        # init internal state
        self.__git_url = git_url
        # set up proxy if specified
        # self.set_global_proxy(http, https)

    def set_global_proxy(self, http=None, https=None):  # todo: unit tests! make it decorator?
        """ Set specified proxies (http/https) for local git instance as a global variables. """
        self.log.debug(f"{myself()}() is working.")
        self.log.info(f"Setting proxies: http -> [{http}], https -> [{https}]")
        if http:
            self.log.info(f"Setting HTTP proxy: {http}")
            process = Popen([GIT_EXECUTABLE, 'config', '--global', 'http.proxy', http])
            process.wait()
        if https:
            self.log.info(f"Setting HTTPS proxy: {https}")
            process = Popen([GIT_EXECUTABLE, 'config', '--global', 'https.proxy', https])
            process.wait()

    def clean_global_proxy(self):  # todo: unit tests! make it decorator?
        """ Clear git global proxies (both http/https). """
        self.log.debug(f"{myself()}() is working.")
        self.log.info("Cleaning up git global proxies.")
        process = Popen([GIT_EXECUTABLE, 'config', '--global', '--unset', 'http.proxy'])
        process.wait()
        process = Popen([GIT_EXECUTABLE, 'config', '--global', '--unset', 'https.proxy'])
        process.wait()

    def __generate_repo_url(self, repo):
        """  Generates repository URL for other methods. Internal method. """
        url = self.__git_url + '/' + repo + '.git'
        # self.log.debug(f"Generated url [{url}]")  # <- shows password in cmd line...
        return url

    def clone(self, repo, location):
        """ Clone specified repository. """
        self.log.info(f"Clone repo [{repo}].")
        try:
            process = Popen([GIT_EXECUTABLE, 'clone', self.__generate_repo_url(repo)], cwd=location)
            process.wait()

            if process.returncode != 0:
                raise PyUtilsException(f"Process returned non zero exit code [{process.returncode}]!")
        except AttributeError as se:
            self.log.error(f'Error while cloning repo [{repo}]! {se}')

    def pull(self, repo, location):
        """ Pull (update) specified repository. """
        self.log.info(f"Pull repo [{repo}]")
        try:
            process = Popen([GIT_EXECUTABLE, 'pull'], cwd=location)
            process.wait()

            if process.returncode != 0:
                raise PyUtilsException(f"Process returned non zero exit code [{process.returncode}]!")
        except AttributeError as se:
            self.log.error(f'Error while updating repo [{repo}]! {se}')

    def gc(self, repo, location):
        """ execute gc() - garbage collection - for repository. """
        self.log.info(f"Calling gc() for repo [{repo}]")
        try:
            process = Popen([GIT_EXECUTABLE, 'gc'], cwd=location)
            process.wait()

            if process.returncode != 0:
                raise PyUtilsException(f"Process returned non zero exit code [{process.returncode}]!")
        except AttributeError as se:
            self.log.error(f'Error while calling gc() for [{repo}]! {se}')


class GitException(Exception):
    """GIT Exception, used if something is wrong with/in GIT interaction."""


if __name__ == '__main__':
    print("pyutilities.pygit: Don't try to execute library as a standalone app!")
