"""
Excel Loader Class for HM Files
Author: Michael Kohlegger
Date: Jan. 2025
"""

from .excel_loader import ExcelLoader
from .columns import hm_columns
from .util import columns_expander


class HMLoader(ExcelLoader):

    """Loads HM excel files as is from a source file into memory.

    The loader will replace the column names of the excel file
    with homogenized column names. If the Excel file unintendedly
    contains more columns, the loader will expand the column list with
    dummy columns.

    :param file_name: The name of the file including file extension
    :type file_name: str
    :param file_path: The path where the data file is located
    :type file_path: str
    :param title: A string that describes the columns of the DataFrame
    :type title: str
    """

    def __init__(self, file_name, file_path, title, *args, **kwargs):
        super().__init__(file_name, file_path, title, *args, **kwargs)

        n_cols = len(self.data.columns)
        n_labels = len(hm_columns)
        delta = n_cols - n_labels

        self.data.columns = columns_expander(hm_columns, delta)
