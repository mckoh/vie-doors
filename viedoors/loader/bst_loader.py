"""
Excel Loader Class for BST Files
Author: Michael Kohlegger
Date: Jan. 2025
"""

from .excel_loader import ExcelLoader
from .columns import bst_columns
from .util import columns_expander, level_mapper


class BSTLoader(ExcelLoader):

    """Loads BST excel files as is from a source file into memory.

    The loader will replace the column names of the excel file
    with homogenized column names. If the Excel file unintendedly
    contains more columns, the loader will expand the column list with
    dummy columns.

    :param file: The name of the file including file extension
    :type filee: str
    :param title: A string that describes the columns of the DataFrame
    :type title: str
    """

    def __init__(self, file, title, *args, **kwargs):
        super().__init__(file, title, *args, **kwargs)

        n_cols = len(self.data.columns)
        n_labels = len(bst_columns)
        delta = n_cols - n_labels

        self.data.columns = columns_expander(bst_columns, delta)


        # Prepare AKS parts
        self.data["name"] = self.data["name"].astype(str)
        self.data["ebene"] = self.data["ebene"].astype(str).map(level_mapper)
        self.data["nummer"] = self.data["nummer"].astype(str)

        # self.data["tuer_nr_aks"] = self.data["tuer_nr_aks"].astype(str)
        # self.data["door"] = self.data["tuer_nr_aks"].map(lambda x: x.split(".")[1] if len(x.split("."))>1 else None)
        # self.data["helper_1"] = self.data["tuer_nr_aks"].map(lambda x: x.split(".")[0] if len(x.split("."))>1 else None)
        # self.data["helper_1"] = self.data["helper_1"].map(lambda x: x.split(" ")[1] if x is not None and len(x.split(" "))>1 else None)
        # self.data["helper_1"] = self.data["helper_1"].map(lambda x: x.replace(" ", "") if x is not None else None)
        # self.data["room"] = self.data["helper_1"].map(lambda x: x[-4:] if x is not None else None).map(room_mapper)
        # self.data["modul"] = self.data["helper_1"].map(lambda x: x[3:4] if x is not None else None)
        # self.data["ebene"] = self.data["helper_1"].map(lambda x: x[:2] if x is not None else None).map(level_mapper)

        # Prepare the AKS-Number
        self.data["integration_aks"] = self.data["name"] + " " + \
            self.data["ebene"] + \
            self.data["nummer"]
