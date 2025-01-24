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
    :param how: Joining strategy (inner, outer, left, right)
    :type how: str
    :default how: "left"
    """

    def __init__(self, files, how="left"):
        assert len(files) > 1, f"Number of files must be at least 2 but was {len(files)}."
        self.files = files
        self.data_merge = files[0]
        self.how = how
        self.__merge()

    def __merge(self):
        """Iteratively merges the files from left to right in the list (only internal).

        :return: None
        :rtype: None
        """

        for file in self.files[1:]:
            old_merge = self.data_merge.copy()
            self.data_merge = merge(
                left=old_merge,
                right=file,
                on="merge",
                how=self.how
            )


    def get_data_merge(self):
        """Returns the finally merged data as pandas.DataFrame.

        :return: Merged data.
        :rtype: pandas.DataFrame
        """

        return self.data_merge


    def merge_success_rate(self):
        """Calculates the ratio between successful and total lines"""

        total = 0
        for file in self.files:
            if len(file) > total:
                total = len(file)
        successful = len(self.data_merge)

        return successful / total


    def export_merge(self, file="dummy.xlsx"):
        """Exports the merged data as Excel file.

        :param file: File name and location of the output file.
        :type file: str
        """
        self.data_merge.to_excel(file)