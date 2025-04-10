"""
Coding Utilities
Author: Michael Kohlegger
Date: Mar. 2025
"""

from pandas import concat, DataFrame


def eliminate_duplicates(merge, col_a, col_b, elimination_info=None):
    """Eliminates duplicate rows based on a comparison of col_a and col_b

    :param merge: Base DataFrame to be used
    :param col_a: The left column that should be matched
    :param col_b: The right column that should be matched
    :return: The DataFrame without duplicates
    :rtype: pandas.DataFrame
    """

    # Prepare an info dictionary to store elimination info
    if elimination_info is None:
        elimination_info = {}
    else:
        elimination_info = elimination_info

    for i, aks in enumerate(merge["merge"].unique()):
        merge_sub = merge.loc[merge["merge"]==aks]

        if len(merge_sub) > 1:
            consolidated = merge_sub.loc[merge_sub[col_a]==merge_sub[col_b]]
            if len(consolidated) == 0:
                consolidated = merge_sub
        else:
            consolidated = merge_sub

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