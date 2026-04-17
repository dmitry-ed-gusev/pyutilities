# -*- coding: utf-8 -*-

"""
Cmd line module for th pyutilities library - integration with CLI.

Created:  Dmitrii Gusev, 17.04.2026
Modified: Dmitrii Gusev, 17.04.2026
"""

import click
from pyutilities import __version__

MSG_VERSION = f"\nPy Utilities, version: {__version__}, (C) Dmitrii Gusev, 2018-2026.\n"


@click.group()
@click.help_option("-h", "--help")
@click.version_option(__version__, "-v", "--version", message=MSG_VERSION)
@click.pass_context
def pyutils(ctx):
    """Module [Py Utilities], (C) Dmitrii Gusev, 2018-2026."""
    click.echo("")


@pyutils.command("version")
def version():
    click.echo(__version__ + "\n")
