"""
Excel Loader Class for Filemaker Files
Author: Michael Kohlegger
Date: Jan. 2025
"""

from .excel_loader import ExcelLoader
from .columns import fm_columns
from .util import columns_expander, level_mapper, room_mapper, door_mapper


class FMLoader(ExcelLoader):

    """Loads Filemaker excel files as is from a source file into memory.

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

    def __init__(self, file, title, *args, **kwargs):
        super().__init__(file, title, *args, **kwargs)

        n_cols = len(self.data.columns)
        n_labels = len(fm_columns)
        delta = n_cols - n_labels

        self.data.columns = columns_expander(fm_columns, delta)

        # Prepare AKS columns
        self.data["bauteil"] = self.data["bauteil"].astype(str)
        self.data["ebene"] = self.data["ebene"].astype(str).map(level_mapper)


        # Prepare the AKS-Number
        self.data["integration_aks"] = self.data["bauteil"] + " " + \
            self.data["ebene"] + \
            self.data["brandmeldernr"] #+ \
            # self.data["raum_nr"] + "." + \
            # self.data["tuer_nr"]
