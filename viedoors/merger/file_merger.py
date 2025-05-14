"""
File Merger Class
Author: Michael Kohlegger
Date: Jan. 2025
"""


from pandas import merge, notna


MERGE_TYPES = {
    "left_only": "Diese Zeile, identifiziert durch ihre AKS-Nummer, war nur im CAD-Datenfile vorhanden, nicht aber in diesem Datenfile.",
    "right_only": "Diese Zeile, identifiziert durch ihre AKS-Nummer, war nur i in diesem Datenfile vorhanden, nicht aber im CAD-Datenfile.",
    "both": "Diese Zeile, identifiziert durch ihre AKS-Nummer, war in diesem Datenfile vorhanden und auch im CAD-Datenfile."
}

REDUCED_COLS = [
    "NPA___feuerwider-stand",
    "NPA___flucht__ja_nein",
    "HM___uz_6_steu", # (Wenn in der Zelle ein Inhalt ist, dann soll ein Ja angezeigt sein)
    "NPA___nottaster__ja_nein",
    "CAD___integration_aks",
    "NPA___fluegel__1_2_3",
    "NPA___sz_magnet__ja_nein",
]


class FileMerger:

    """Merges multiple pandas.DataFrames basted on their 'merge' columns.

    The merge is by default done as a left-join operation starting with the first
    file in the list, expanding to the right. Thus make sure to start with the
    most promising file. By changing the 'how' parameter, you can change the
    joining behavior.

    :param files: A list of pandas.DataFrames.
    :type files: list
    :param how: Joining strategy (inner, outer, left, right)
    :type how: str
    :default how: "left"
    :param column: Name of the merge column
    :type column: str
    :default column: "merge
    """

    def __init__(self, files, how="left", column="merge"):
        assert len(files) > 1, f"Number of files must be at least 2 but was {len(files)}."
        self.files = files
        self.data_merge = files[0]
        self.how = how
        self.column = column
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
                on=self.column,
                how=self.how
            )

    def find_non_matching_rows(self):
        """Finds all lines in that exist in the right but not in the left file.

        This function can only be used, when merging two files. It will
        raise an error if you try to merge multiple files as line comparison
        cannot be done unambigously in this case.

        The return will only contain the columns of the second dataframe.

        :raises: AssertionError when merging more than 2 files
        :return: DataFrame with non-matching lines
        :rtype: pandas.DataFrame
        """

        n_cols_of_first = len(self.files[0].columns)
        assert len(self.files) == 2, f"This function can only be used when merging two datafiles. You tried to merge {len(self.files)}."
        for file in self.files[1:]:
            old_merge = self.data_merge.copy()
            self.data_merge = merge(
                left=old_merge,
                right=file,
                on=self.column,
                how="right",
                indicator=True
            )

        output = self.data_merge[self.data_merge['_merge'] == 'right_only']

        return output.iloc[:,n_cols_of_first:].drop("_merge", axis=1)

    def find_duplicates(self):
        """Finds all duplicates in 'merge' column.

        :raises: AssertionError when merging more than 2 files
        :return: DataFrame with duplicate rows
        :rtype: pandas.DataFrame
        """

        n_cols_of_first = len(self.files[0].columns)
        assert len(self.files) == 2, f"This function can only be used when merging two datafiles. You tried to merge {len(self.files)}."
        for file in self.files[1:]:
            old_merge = self.data_merge.copy()
            self.data_merge = merge(
                left=old_merge,
                right=file,
                on=self.column,
                how="left"
            )

        output = self.data_merge.copy()
        output = output.loc[output.duplicated("merge")]

        return output.iloc[:,n_cols_of_first:]


    def get_data_merge(self, reduce_cols=False):
        """Returns the finally merged data as pandas.DataFrame.

        :param reduce_cols: Switch to tell if only needed columns are returned
        :return: Merged data.
        :rtype: pandas.DataFrame
        """

        if reduce_cols:
            self.data_merge["HM___uz_6_steu"] = self.data_merge["HM___uz_6_steu"].map(
                lambda x: "Ja" if notna(x) else ""
            )
            return self.data_merge[REDUCED_COLS]

        return self.data_merge


    def export_merge(self, file="dummy.xlsx"):
        """Exports the merged data as Excel file.

        :param file: File name and location of the output file.
        :type file: str
        """
        self.data_merge.to_excel(file)