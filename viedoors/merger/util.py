"""
Coding Utilities
Author: Michael Kohlegger
Date: Mar. 2025
"""

from pandas import concat

def eliminate_duplicates(merge, col_a, col_b):
    """Eliminates duplicate rows based on a comparison of col_a and col_b

    :param merge: Base DataFrame to be used
    :param col_a: The left column that should be matched
    :param col_b: The right column that should be matched
    :return: The DataFrame without duplicates
    :rtype: pandas.DataFrame
    """

    for i, aks in enumerate(merge["merge"].unique()):
        merge_sub = merge.loc[merge["merge"]==aks]

        if len(merge_sub)>1:
            consolidated = merge_sub.loc[merge_sub[col_a]==merge_sub[col_b]]
            if len(consolidated) == 0:
                consolidated = merge_sub
        else:
            consolidated = merge_sub

        if i == 0:
            new_merge = consolidated
        else:
            new_merge = concat([new_merge, consolidated])

    return new_merge