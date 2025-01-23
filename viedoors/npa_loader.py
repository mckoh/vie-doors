"""
Excel Loader Class for NPA Files
Author: Michael Kohlegger
Date: Jan. 2025
"""

from .excel_loader import ExcelLoader
from .columns import npa_columns
from .util import columns_expander


class NPALoader(ExcelLoader):

    """Loads NPA excel files as is from a source file into memory.

    The loader will replace the column names of the excel file
    with homogenized column names. If the Excel file unintendedly
    contains more columns, the loader will expand the column list with
    dummy columns.

    :param file: The name of the file including file extension
    :type filee: str
    :param title: A string that describes the columns of the DataFrame
    :type title: str
    """

    def __init__(self, file, title):
        super().__init__(
            file=file,
            title=title
        )
        n_cols = len(self.data.columns)
        n_labels = len(npa_columns)
        delta = n_cols - n_labels

        self.data.columns = columns_expander(npa_columns, delta)
