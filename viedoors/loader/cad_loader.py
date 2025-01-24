"""
Excel Loader Class for CAD Files
Author: Michael Kohlegger
Date: Jan. 2025
"""

from .excel_loader import ExcelLoader
from .columns import cad_columns
from .util import columns_expander
from .util import door_mapper, level_mapper, room_mapper, object_mapper


class CADLoader(ExcelLoader):

    """Loads CAD excel files as is from a source file into memory.

    The loader will replace the column names of the excel file
    with homogenized column names. If the Excel file unintendedly
    contains more columns, the loader will expand the column list with
    dummy columns.

    The class prepares all necessary columns and concatenates them into a new
    column 'integration_aks' that can be used for joining.

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
        n_labels = len(cad_columns)
        delta = n_cols - n_labels

        self.data.columns = columns_expander(cad_columns, delta)

        # Prepare the parts for AKS
        self.data["gar_tuernummer_bauteil"] = self.data["gar_tuernummer_bauteil"].map(object_mapper)
        self.data["gar_tuernummer_ebene"] = self.data["gar_tuernummer_ebene"].map(level_mapper)
        self.data["gar_tuernummer_nummer"] = self.data["gar_tuernummer_nummer"].map(door_mapper)
        self.data["gar_tuernummer_aks_nr"] = self.data["gar_tuernummer_aks_nr"].map(room_mapper)

        # Prepare the AKS-Number
        self.data["integration_aks"] = self.data["gar_tuernummer_bauteil"] + " " + \
            self.data["gar_tuernummer_ebene"] + \
            self.data["gar_tuernummer_modul"] + \
            self.data["gar_tuernummer_aks_nr"] + "." + \
            self.data["gar_tuernummer_nummer"]