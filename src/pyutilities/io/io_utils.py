#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    IO Utilities module.

    Created:  Dmitrii Gusev, 04.04.2017
    Modified: Dmitrii Gusev, 22.11.2022
"""

import os
import sys
import yaml
import errno
import logging
from os import walk
from pyutilities.exception import PyUtilitiesException
from pyutilities.defaults import MSG_MODULE_ISNT_RUNNABLE

# configure logger on module level. it isn't a good practice, but it's convenient.
# don't forget to set disable_existing_loggers=False, otherwise logger won't get its config!
log = logging.getLogger(__name__)
# to avoid errors like 'no handlers' for libraries it's necessary/convenient to add NullHandler.
log.addHandler(logging.NullHandler())


def _list_files(path, files_buffer, out_to_console=False):
    """
    Internal function for listing (recursively) all files in specified directory.
    Don't use it directly, use list_files()
    :param path: path to iterate through
    :param files_buffer: buffer list for collection files
    :param out_to_console: out to console processing file
    """
    # print "STDOUT encoding ->", sys.stdout.encoding  # <- just a debug output
    # todo: line for python 2 -> for (dirpath, dirnames, filenames) in walk(unicode(path)):
    for (dirpath, dirnames, filenames) in walk(path):
        for filename in filenames:
            abs_path = dirpath + "/" + filename
            if out_to_console:  # debug output
                if sys.stdout.encoding is not None:  # sometimes encoding may be null!
                    print(abs_path.encode(sys.stdout.encoding, errors="replace"))
                else:
                    print(abs_path)
            files_buffer.append(abs_path)


def list_files(path, out_to_console=False):
    """
    List all files in a specified path and return list of found files.
    :param path: path to directory
    :param out_to_console: do or don't output to system console
    :return: list of files
    """
    log.debug("list_files() is working. Path [{}].".format(path))
    if not path or not path.strip():  # fail-fast #1
        raise IOError("Can't list files in empty path!")
    if not os.path.exists(path) or not os.path.isdir(path):  # fail-fast #2
        raise IOError("Path [{}] doesn't exist or not a directory!".format(path))
    files = []
    _list_files(path, files, out_to_console)
    return files


def str_2_file(filename: str, content: str, overwrite_file: bool = False):
    """Write string/text content to the provided file."""
    log.debug(f"str_2_file(): saving content to file: [{filename}].")

    if os.path.exists(filename) and not overwrite_file:  # file exists and we don't want to overwrite it
        raise PyUtilitiesException(f"File [{filename}] exists but overwrite is [{overwrite_file}]!")

    if not os.path.exists(os.path.dirname(filename)):  # create a dir for file
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open(filename, "w") as f:  # write content to a file
        f.write(content)


def file_2_str(filename: str) -> str:
    """Read content from the provided file as string/text."""
    log.debug(f"file_2_str(): reading content from file: [{filename}].")

    if not filename:  # fail-fast behaviour (empty path)
        raise PyUtilitiesException("Specified empty file path!")
    if not os.path.exists(os.path.dirname(filename)):  # fail-fast behaviour (non-existent path)
        raise PyUtilitiesException(f"Specified path [{filename}] doesn't exist!")

    with open(filename, mode="r") as infile:
        return infile.read()


def read_yaml(file_path: str):
    """Parses single YAML file and return its contents as object (dictionary).
    :param file_path: path to YAML file to load settings from
    :return python object with YAML file contents
    """
    log.debug("parse_yaml() is working. Parsing YAML file [{}].".format(file_path))
    if not file_path or not file_path.strip():
        raise IOError("Empty path to YAML file!")
    with open(file_path, "r") as cfg_file:
        cfg_file_content = cfg_file.read()
        if "\t" in cfg_file_content:  # no tabs allowed in file content
            raise IOError(f"Config file [{file_path}] contains 'tab' character!")
        return yaml.load(cfg_file_content, Loader=yaml.FullLoader)


if __name__ == "__main__":
    print(MSG_MODULE_ISNT_RUNNABLE)
