"""
Excel Loader Class
Author: Michael Kohlegger
Date: Jan. 2025
"""


from pandas import read_excel
from os.path import join
from .util import clean_data


class ExcelLoader:

    """Loads excel files as is from a source file into memory.

    :param file: The name of the file including file extension
    :type filee: str
    :param title: A string that describes the columns of the DataFrame
    :type title: str
    """

    def __init__(self, file, title, *args, **kwargs):

        self.file = file
        self.title = title
        self.data = None

        self.__load_data(*args, **kwargs)


    def __load_data(self, *args, **kwargs):
        """Loads the specified file as DataFrame (only internal use).

        Data are read in as is. By specifying object as dtype,
        type inferencing is deactivated in pandas and all columns
        are treated as string columns
        """

        self.data = read_excel(
            io=self.file,
            dtype=object,
            *args,
            **kwargs
        )

        n_col = len(self.data.columns)
        n_row = len(self.data)


    def __clean_data(self):
        """Cleans the column names of the DataFrame (only internal use)."""

        self.data = clean_data(self.data)


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
            return df
        return self.data


    def get_columns(self):
        """Returns a list of columns from the contained DataFrame.

        :return: Column names as python list object.
        :rtype: list
        """

        return list(self.data.columns)
