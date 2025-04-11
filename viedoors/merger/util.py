"""
Coding Utilities
Author: Michael Kohlegger
Date: Mar. 2025
"""

from pandas import concat, DataFrame


def eliminate_duplicates(merge, col_a, col_b, elimination_info=None):
    """Eliminates duplicate rows based on a comparison of col_a and col_b

    This method offers the possibility to pass a former elimination info that
    the elimination info of this run is appended to. This is useful, when you
    try to eliminate duplicated over multiple iterations of calling eliminate_duplicates.

    :param merge: Base DataFrame to be used
    :param col_a: The left column that should be matched
    :param col_b: The right column that should be matched
    :param elimination_info: A dictionary with elimination info of a previous step that is appended to
    :return: The DataFrame without duplicates and dictionary with info on eliminated rows per aks
    :rtype: pandas.DataFrame, dict
    """

    # Prepare an info dictionary to store elimination info (aks and count of
    # eliminated)
    if elimination_info is None:
        elimination_info = {}
    else:
        elimination_info = elimination_info

    # Look at every unique aks in the dataframe and filter the dataframe for that
    # aks to see if there are aks duplicates
    for i, aks in enumerate(merge["merge"].unique()):
        merge_sub = merge.loc[merge["merge"]==aks]

        # the next step is only done, when there are multiple lines in the filtered
        # dataframe (as only then we have duplicates)
        if len(merge_sub) > 1:

            # check if duplicates can be merged using additional attributes
            consolidated = merge_sub.loc[merge_sub[col_a]==merge_sub[col_b]]

            # if duplicates cannot be merged, use the former filtered dataframe
            # else use the dataframe with consolidated lines
            if len(consolidated) == 0:
                consolidated = merge_sub
        else:
            consolidated = merge_sub

        # merge the current consolidation with the consolidation of the previous
        # iteration. If this is the first iteration, create a new dataframe
        if i == 0:
            new_merge = consolidated
        else:
            new_merge = concat([new_merge, consolidated])

        # Check how many rows have been eliminated and store in dictionary
        eliminated_rows = len(merge_sub) - len(consolidated)
        if eliminated_rows > 0:
            if aks not in elimination_info.keys():
                elimination_info[aks] = eliminated_rows
            else:
                elimination_info[aks] += eliminated_rows

    return new_merge, elimination_info


def count_duplicates(dataframe):
    """Searches for duplicate values in the given dataframe and counts them

    :param dataframe: The DataFrame to be parsed
    :return: The DataFrame without duplicates
    :rtype: pandas.DataFrame
    """
    duplicate_entries = DataFrame(dataframe["merge"].value_counts())
    duplicate_entries.columns =["Anzahl Duplikate"]
    duplicate_entries["AKS-Nummer"] = duplicate_entries.index
    duplicate_entries.index = range(len(duplicate_entries))
    return duplicate_entries[["AKS-Nummer", "Anzahl Duplikate"]].loc[duplicate_entries["Anzahl Duplikate"]>1]