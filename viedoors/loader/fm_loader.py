"""
Excel Loader Class for Filemaker Files
Author: Michael Kohlegger
Date: Jan. 2025
"""

from pandas import read_pickle


class FMLoader:

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

    def __init__(self):
        self.data = read_pickle("static/fm.pkl")

        # TODO Dev: #30 match the NPA and the FM data using Schlussnummer column
        self.data["npa_fm_match"] = self.data["FM___bauteil"]+"-"+self.data["FM___ebene"]+"-"+self.data["FM___topnr"].astype(str)


    def get_data(self, prefixed=True):
        """Returns the stored DataFrame and prefixes all columns with title"""

        return self.data


    def get_columns(self):
        """Returns a list of columns from the contained DataFrame.

        :return: Column names as python list object.
        :rtype: list
        """

        return list(self.data.columns)


