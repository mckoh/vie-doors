"""
Excel Loader Class for FLT Files
Author: Michael Kohlegger
Date: Jan. 2025
"""

from .excel_loader import ExcelLoader
from .columns import flt_columns
from .util import columns_expander, level_mapper, room_mapper, door_mapper


class FLTLoader(ExcelLoader):

    """Loads FLT excel files as is from a source file into memory.

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
            title=title,

            # These two keyword arguments are necessary for flt data
            skiprows=[0,1],
            header=None,
        )
        n_cols = len(self.data.columns)
        n_labels = len(flt_columns)
        delta = n_cols - n_labels

        self.data.columns = columns_expander(flt_columns, delta)

        # Prepare AKS columns
        self.data["objekt"] = self.data["plan_nr"].astype(str).map(lambda x: x.split("_")[0] if x is not None and len(x.split("_"))>1 else None)
        self.data["level"] = self.data["ebene"].astype(str).map(level_mapper)
        self.data["bauteil"] = self.data["bauteil"].astype(str)
        self.data["raum_nr"] = self.data["raum_nr"].astype(str).map(room_mapper)
        self.data["tuer_nr"] = self.data["tuer_nr"].astype(str).map(door_mapper)

        # Prepare the AKS-Number
        self.data["integration_aks"] = self.data["objekt"] + " " + \
            self.data["level"] + \
            self.data["bauteil"] + \
            self.data["raum_nr"] + "." + \
            self.data["tuer_nr"]
