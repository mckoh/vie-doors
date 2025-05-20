from .merger.util import count_duplicates
from pandas import isna
from math import prod


def calculate_duplicate_info(df_cad, df_npa, df_bst, df_flt, df_hm, elimination_info):

    l = [df_cad, df_npa, df_bst, df_flt, df_hm]

    dp_cad = count_duplicates(df_cad)
    dp_cad.rename(columns={"Anzahl Duplikate": f"Anzahl Duplikate CAD-File"}, inplace=True)

    for i, dataset in enumerate([df_npa, df_bst, df_flt, df_hm]):

        name = dataset.columns[0].split("___")[0]+"-File"
        dp = count_duplicates(dataset)
        dp.rename(columns={"Anzahl Duplikate": f"Anzahl Duplikate {name}"}, inplace=True)

        dp_cad = dp_cad.merge(dp, on='AKS-Nummer', how='outer')

    dp_cad.index = dp_cad["AKS-Nummer"]
    dp_cad.drop("AKS-Nummer", axis=1, inplace=True)

    # FILL THE EMPTY CELLS
    c = [
        "Anzahl Duplikate CAD-File",
        "Anzahl Duplikate NPA-File",
        "Anzahl Duplikate BST-File",
        "Anzahl Duplikate FLT-File",
        "Anzahl Duplikate HM-File"
    ]

    for i, column in enumerate(c):

        def fill_empty(x, aks):
            if isna(x):
                if aks in list(l[i]["merge"].values):
                    return 1
                else:

                    return 0
            return int(x)

        for j in range(len(dp_cad)):
            dp_cad.loc[dp_cad.iloc[j].name, column] = fill_empty(dp_cad[column].iloc[j], dp_cad.iloc[j].name)

    # CREATE FINAL COLUMN

    for j in range(len(dp_cad)):
        dp_cad.loc[dp_cad.iloc[j].name, "Zeilen im Merge nach Zusammenführen"] = prod([v for v in dp_cad.iloc[j].to_list() if v > 1]) if dp_cad["Anzahl Duplikate CAD-File"].iloc[j] > 0 else 0

    dp_cad = dp_cad.merge(elimination_info, on="AKS-Nummer", how='outer')

    dp_cad.fillna(0, inplace=True)

    dp_cad["Verbleibende Zeilen im Merge"] = dp_cad["Zeilen im Merge nach Zusammenführen"] - dp_cad["Zeilen die durch Zusatzattribute eliminiert werden konnten"]

    return dp_cad
