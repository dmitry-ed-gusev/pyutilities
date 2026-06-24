# -*- coding: utf-8 -*-

"""
Useful Excel utilities for improving excel working in python.

Created:  Dmitrii Gusev, 24.06.2026
Modified: Dmitrii Gusev, 24.06.2026
"""

from openpyxl.cell.cell import Cell
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet

from pyutilities.utils.string_utils import is_empty

# - styling constants/defaults
FONT: Font = Font()
FONT_RED: Font = Font(color="FF0000")  # red font
FONT_GREEN: Font = Font(color="00BB00")  # green font
FONT_BOLD: Font = Font(bold=True)
FONT_BOLD_RED: Font = Font(bold=True, color="FF0000")  # red font, bold
FONT_BOLD_GREEN: Font = Font(bold=True, color="00BB00")  # green font, bold
ALIGNMENT_CENTER: Alignment = Alignment(horizontal="center", vertical="center", wrapText=True)


class XlsSheet:
    """Utility class for working with openpyxl excel worksheet."""

    def __init__(self, ws: Worksheet):
        self.__ws = ws

    def init_cell(
        self,
        address: str,
        value: str,
        bold: bool = False,
        aligned: bool = False,
        color: str = None,
        width: int = 0,
    ) -> Cell:
        """Simple yet powerful method for cell initialization. Can init essential cell parameters."""

        cell = self.__ws[address]
        cell.value = value

        if bold:  # font boldness
            cell.font = FONT_BOLD

        if aligned:  # cell text alignment
            cell.alignment = ALIGNMENT_CENTER

        if not is_empty(color):  # cell font coloring/boldness
            if color == "red":
                if bold:
                    cell.font = FONT_BOLD_RED
                else:
                    cell.font = FONT_RED
            elif color == "green":
                if bold:
                    cell.font = FONT_BOLD_GREEN
                else:
                    cell.font = FONT_GREEN

        if width > 0:  # column width
            self.__ws.column_dimensions[cell.column_letter].width = width

        return cell

    def init_cell_bold(
        self, address, value, aligned: bool = False, color: str = None, width: int = 0
    ) -> Cell:
        """TBD"""
        return self.init_cell(
            address=address, value=value, bold=True, aligned=aligned, color=color, width=width
        )

    # pylint: disable=too-many-arguments, too-many-positional-arguments
    def init_cell_addr(
        self,
        row: int,
        column: int,
        value: str,
        bold: bool = False,
        aligned: bool = False,
        color: str = None,
        width: int = 0,
    ) -> Cell:
        """TBD"""

        letter: str = get_column_letter(column)
        return self.init_cell(
            address=f"{letter}{row}", value=value, bold=bold, aligned=aligned, color=color, width=width
        )

    def set_column_width(self, column: str, width: int):
        """TBD"""
        self.__ws.column_dimensions[column].width = width
