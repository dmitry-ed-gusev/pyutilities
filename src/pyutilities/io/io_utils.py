# -*- coding: utf-8 -*-

"""
IO Utilities module.

Created:  Dmitrii Gusev, 04.04.2017
Modified: Dmitrii Gusev, 02.01.2025
"""

import errno
import gzip
import logging
import os
import shutil
import sys
from os import walk

import yaml

from pyutilities.defaults import DEFAULT_ENCODING, MSG_MODULE_ISNT_RUNNABLE
from pyutilities.exception import PyUtilitiesException
from pyutilities.utils.string_utils import convert_bytes

# configure logger on module level. it isn't a good practice, but it's convenient.
# don't forget to set disable_existing_loggers=False, otherwise logger won't get its config!
log = logging.getLogger(__name__)
# to avoid errors like 'no handlers' for libraries it's necessary/convenient to add NullHandler.
log.addHandler(logging.NullHandler())


def _list_files(path, files_buffer, out_to_console=False):
    """Internal function for listing (recursively) all files in specified directory. Don't use it directly,
    use list_files() instead - it is a public method (not this one!).
    :param path: path to iterate through
    :param files_buffer: buffer list for collection files
    :param out_to_console: out to console processing file
    """

    for dirpath, _, filenames in walk(path):  # yields tuple (dirpath, dirnames, filenames)
        for filename in filenames:
            abs_path = dirpath + "/" + filename
            if out_to_console:  # debug output
                if sys.stdout.encoding is not None:  # sometimes encoding may be null!
                    print(abs_path.encode(sys.stdout.encoding, errors="replace"))
                else:
                    print(abs_path)
            files_buffer.append(abs_path)


def list_files(path, out_to_console=False):
    """List all files in a specified path and return list of found files.
    :param path: path to directory
    :param out_to_console: do or don't output to system console
    :return: list of files
    """

    log.debug("list_files() is working. Path [%s].", path)
    if not path or not path.strip():  # fail-fast #1
        raise IOError("Can't list files in empty path!")
    if not os.path.exists(path) or not os.path.isdir(path):  # fail-fast #2
        raise IOError(f"Path [{path}] doesn't exist or not a directory!")
    files = []  # type: ignore
    _list_files(path, files, out_to_console)
    return files


def str2file(filename: str, content: str, overwrite_file: bool = False, encoding: str = DEFAULT_ENCODING):
    """Write string/text content to the provided file."""

    log.debug("str2file(): saving content to file: [%s].", filename)

    if os.path.exists(filename) and not overwrite_file:  # file exists and we don't want to overwrite it
        raise PyUtilitiesException(f"File [{filename}] exists but overwrite is [{overwrite_file}]!")

    if not os.path.exists(os.path.dirname(filename)):  # create a dir for file
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open(filename, "w", encoding=encoding) as f:  # write content to a file
        f.write(content)


def file2str(filename: str, encoding: str = DEFAULT_ENCODING) -> str:
    """Read content from the provided file as string/text."""

    log.debug("file2str(): reading content from file: [%s].", filename)

    if not filename:  # fail-fast behavior (empty path)
        raise PyUtilitiesException("Specified empty file path!")
    if not os.path.exists(os.path.dirname(filename)):  # fail-fast behavior (non-existent path)
        raise PyUtilitiesException(f"Specified path [{filename}] doesn't exist!")

    with open(filename, mode="r", encoding=encoding) as infile:
        return infile.read()


def read_yaml(file_path: str, encoding: str = DEFAULT_ENCODING):
    """Parses single YAML file and return its contents as object (dictionary).
    :param file_path: path to YAML file to load settings from
    :return python object with YAML file contents
    """

    log.debug("parse_yaml() is working. Parsing YAML file [%s].", file_path)

    if not file_path or not file_path.strip():  # fail-fast check
        raise IOError("Empty path to YAML file!")

    with open(file_path, "r", encoding=encoding) as cfg_file:  # reading file
        cfg_file_content = cfg_file.read()
        if "\t" in cfg_file_content:  # no tabs allowed in file content
            raise IOError(f"Config file [{file_path}] contains 'tab' character!")
        return yaml.load(cfg_file_content, Loader=yaml.FullLoader)


def compress_file(input_file, output_file):
    """Compressing input file with the gzip algorithm."""

    with open(input_file, "rb") as f_in:
        with gzip.open(output_file, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)


def file_size(file_path: str) -> str:
    """Function will return the file size in readable format with the highest size mark - KB/MB/GB/TB."""

    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes(file_info.st_size)

    return "unknown"


if __name__ == "__main__":
    print(MSG_MODULE_ISNT_RUNNABLE)
