"""
Excel Loader Class for NPA Files
Author: Michael Kohlegger
Date: Jan. 2025
"""

from .excel_loader import ExcelLoader
from .columns import npa_columns
from .util import columns_expander
from .util import level_mapper, object_mapper, door_mapper, room_mapper


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

        # Prepare the parts for AKS
        self.data["objekt"] = self.data["objekt"].astype(str).map(object_mapper)
        self.data["ebene"] = self.data["ebene"].astype(str).map(level_mapper)
        self.data["aks_plan"] = self.data["aks_plan"].astype(str)
        self.data["room"] = self.data["aks_plan"].astype(str).map(lambda x: x.split(".")[0] if len(x.split("."))>1 else x)
        self.data["door"] = self.data["aks_plan"].astype(str).map(lambda x: x.split(".")[1] if len(x.split("."))>1 else x)
        self.data["room"] = self.data["room"].map(room_mapper)
        self.data["door"] = self.data["door"].map(door_mapper)

        # Prepare the AKS-Number
        self.data["integration_aks"] = self.data["objekt"] + " " + \
            self.data["ebene"] + \
            self.data["bauteil"] + \
            self.data["room"] + "." + \
            self.data["door"]

        # Delete multiple header rows that are copied into the data
        self.data.drop(self.data.loc[self.data["objekt"]=="Objekt"].index, axis=0, inplace=True)

        # TODO Dev: #30 match the NPA and the FM data using Schlussnummer column
        self.data["SN1"] = self.data["schlossernummer"].map(lambda x: x.replace(" ", "")+"//").map(lambda x: x.split("/")[0])
        self.data["SN2"] = self.data["schlossernummer"].map(lambda x: x.replace(" ", "")+"//").map(lambda x: x.split("/")[1]).map(level_mapper)
        self.data["SN3"] = self.data["schlossernummer"].map(lambda x: x.replace(" ", "")+"//").map(lambda x: x.split("/")[2])
        self.data["npa_fm_match"] = self.data["SN1"]+"-"+self.data["SN2"]+"-"+self.data["SN3"]
        self.data.drop("SN1", axis=1, inplace=True)
        self.data.drop("SN2", axis=1, inplace=True)
        self.data.drop("SN3", axis=1, inplace=True)


    def get_data(self, prefixed=False):
        """Returns the stored DataFrame and prefixes all columns with title

        :param prefixed: Boolean attribute wether to include title prefix.
        :type prefixed: bool
        :return: Data as pandas.DataFrame.
        :rtype: pandas.DataFrame
        """

        if prefixed:
            df = self.data.copy()
            df.columns = [self.title+"___"+c for c in self.data.columns]
            df["merge"] = df[self.title+"___"+"integration_aks"]
            df["npa_fm_match"] = df[self.title+"___"+"npa_fm_match"]
        else:
            df = self.data.copy()
            df["merge"] = df["integration_aks"]
            df["npa_fm_match"] = df["npa_fm_match"]

        return df