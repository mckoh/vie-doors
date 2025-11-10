"""
Coding Utilities
Author: Michael Kohlegger
Date: Mar. 2025
"""

from pandas import concat, DataFrame, notna


REDUCED_COLS = [
    "NPA___feuerwider-stand",
    "NPA___flucht__ja_nein",
    "HM___uz_6_steu", # (Wenn in der Zelle ein Inhalt ist, dann soll ein Ja angezeigt sein)
    "NPA___nottaster__ja_nein",
    "CAD___integration_aks",
    "NPA___fluegel__1_2_3",
    "NPA___sz_magnet__ja_nein",
    "CAD___gar_tuernummer_alt", # in iteration 08 hinzugefügt
]


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


def clean_merge(merge):
    """Lets you clean-up a completed merge to get an outputable dataframe

    :param merge: The final merge to be cleaned
    :type merge: pandas.DataFrame
    :return: The cleaned merge
    :rtype: pandas.DataFrame
    """

    merge["HM___uz_6_steu"] = merge["HM___uz_6_steu"].map(
        lambda x: "Ja" if notna(x) else ""
    )

    output = merge[REDUCED_COLS].copy()
    output["Selbsschließend"] = ""

    clean_column_names = [
        "Feuerwiderstand",
        "Fluchttüre Ja/Nein",
        "UZ6/Steu. Ja/Nein",
        "Nottaster Ja/Nein",
        "AKS Nummer",
        "Anzahl Flügel 1/2/S",
        "SZ-Magnet Ja/Nein",
        "Türnummer Alt", # in iteration 08 hinzugefügt
        "Selbstschließend",
    ]

    output.columns = clean_column_names

    return output.iloc[:, [4, 0, 1, 2, 3, 7, 5, 6]]


def find_cad_only(merge):
    """Finds all AKS numbers in the merge that are only present in CAD

    :param merge: A Merge Dataframe
    :type merge: pandas.DataFrame
    :return: The located AKS-Numbers as DataFrame
    :rtype: pandas.DataFrame
    """

    cad_only = merge.loc[merge[merge.columns[16:]].isna().all(axis=1)][["merge"]]
    cad_only.columns = ["AKS-Nummer"]
    return cad_only