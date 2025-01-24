"""
File Merger Class
Author: Michael Kohlegger
Date: Jan. 2025
"""


from pandas import merge


class FileMerger:

    """Merges multiple pandas.DataFrames basted on their 'merge' columns.

    :param files: A list of pandas.DataFrames.
    :type files: list
    """

    def __init__(self, files):
        assert len(files) > 1, f"Number of files must be at least 2 but was {len(files)}."
        self.files = files
        self.data_merge = files[0]

        self.__merge()

    def __merge(self):
        """Iteratively merges the files from left to right in the list (only internal).

        :return: None
        :rtype: None
        """
        for file in self.files[1:]:
            self.data_merge = merge(
                left=self.data_merge,
                right=file,
                on="merge",
                how="outer"
            )#

    def get_data_merge(self):
        """Returns the finally merged data as pandas.DataFrame.

        :return: Merged data.
        :rtype: pandas.DataFrame
        """
        return self.data_merge