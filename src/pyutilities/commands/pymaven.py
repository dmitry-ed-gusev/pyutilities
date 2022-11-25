#!/usr/bin/env python
# coding=utf-8

"""
    Some useful/convenient functions related to Maven build tool.
    Functions are incapsulated in PyMaven class.

    Created:  Dmitrii Gusev, 02.05.2019
    Modified: Dmitrii Gusev, 25.11.2022
"""

import os
import platform
import logging

from subprocess import Popen
from pyutilities.utils.common_utils import myself
from pyutilities.exception import PyUtilitiesException
from pyutilities.defaults import MSG_MODULE_ISNT_RUNNABLE

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class PyMaven:
    """Class represents maven functionality."""

    def __init__(self, mvn_settings: str | None = None):
        # self.log = init_logger(__name__, add_null_handler=False)
        # log.info("Initializing Maven class.")
        # select maven executable
        self.__mvn_exec = self.get_mvn_executable()
        log.info(f"Selected maven executable [{self.__mvn_exec}].")

        self.__mvn_settings: str | None
        # init special maven settings - calculate path
        if mvn_settings:
            abs_settings_path = os.path.abspath(mvn_settings)
            if not os.path.exists(abs_settings_path):  # fail-fast for non-existent settings
                raise FileNotFoundError
            self.__mvn_settings = abs_settings_path
        else:
            self.__mvn_settings = None
        log.info(f"Loaded special maven settings [{self.__mvn_settings}].")

    def get_mvn_executable(self):
        """Return Maven executable, depending on OS (windows-family or not)."""
        log.debug(f"{myself()}() is working.")
        if "windows" in platform.system().lower():
            return "mvn.cmd"
        else:
            return "mvn"

    def append_mvn_settings(self, cmd: list):
        log.debug(f"{myself()}() is working.")
        if self.__mvn_settings is not None:
            cmd.extend(["-s", self.__mvn_settings])
        return cmd

    def build(self, location: str):
        log.debug(f"{myself()}() is working.")
        log.info(f"Building repo in location [{location}].")
        try:
            cmd = self.append_mvn_settings([self.__mvn_exec, "clean", "install"])
            process = Popen(cmd, cwd=location)
            process.wait()
            # check exit code
            if process.returncode != 0:
                raise PyUtilitiesException(f"Process returned non zero exit code [{process.returncode}]!")
        except AttributeError as se:
            log.error(f"Error building repo in location [{location}]! {se}")

    def javadoc(self, location: str):
        log.debug(f"{myself()}() is working.")
        log.info(f"Downloading javadoc for repo [{location}].")
        try:
            cmd = self.append_mvn_settings([self.__mvn_exec, "dependency:resolve", "-Dclassifier=javadoc"])
            process = Popen(cmd, cwd=location)
            process.wait()
            # check exit code
            if process.returncode != 0:
                raise PyUtilitiesException(f"Process returned non zero exit code [{process.returncode}]!")
        except AttributeError as se:
            log.error(f"Error downloading javadoc for repo [{location}]! {se}")

    def sources(self, location):
        log.debug(f"{myself()}() is working.")
        log.info(f"Downloading sources for repo [{location}].")
        try:
            cmd = self.append_mvn_settings([self.__mvn_exec, "dependency:resolve", "-Dclassifier=sources"])
            process = Popen(cmd, cwd=location)
            process.wait()
            # check exit code
            if process.returncode != 0:
                raise PyUtilitiesException(f"Process returned non zero exit code [{process.returncode}]!")
        except AttributeError as se:
            log.error(f"Error downloading sources for repo [{location}]! {se}")


if __name__ == "__main__":
    print(MSG_MODULE_ISNT_RUNNABLE)
