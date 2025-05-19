import streamlit as st
from io import BytesIO
from pandas import ExcelWriter, DataFrame, notna, isna
from math import prod
from viedoors import BSTLoader, FLTLoader, HMLoader, FMLoader, count_duplicates
from viedoors import CADLoader, NPALoader, FileMerger, eliminate_duplicates


REDUCED_COLS = [
    "NPA___feuerwider-stand",
    "NPA___flucht__ja_nein",
    "HM___uz_6_steu", # (Wenn in der Zelle ein Inhalt ist, dann soll ein Ja angezeigt sein)
    "NPA___nottaster__ja_nein",
    "CAD___integration_aks",
    "NPA___fluegel__1_2_3",
    "NPA___sz_magnet__ja_nein"
]

st.set_page_config(
    page_title="VIE Door Integrator",
    page_icon="📃",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

st.title("VIE-Door Integrator")
st.markdown("Unterhalb können die Files ausgewählt werden, die im weiteren Verlauf \
    integriert werden. Bitte beachten Sie, dass alle 6 Files aufeinander abgestimmt \
    sein, und Daten über dasselbe Objekt (z.B. 420) enthalten müssen.")

col_1, col_2 = st.columns(2, gap="medium", vertical_alignment="top", )

with col_1:
    st.subheader("CAD-File auswählen", divider=True)
    cad = st.file_uploader("CAD File", ["xlsx", "xls"], label_visibility="hidden")

    st.subheader("NPA-File auswählen", divider=True)
    npa = st.file_uploader("NPA File", ["xlsx", "xls"], label_visibility="hidden")

    st.subheader("Sisando BST-File auswählen", divider=True)
    bst = st.file_uploader("Sisando BST File", ["xlsx", "xls"], label_visibility="hidden")

    st.subheader("Sisando FLT-File auswählen", divider=True)
    flt = st.file_uploader("Sisando FLT File", ["xlsx", "xls"], label_visibility="hidden")

    st.subheader("Schrack HM-File auswählen", divider=True)
    hm = st.file_uploader("Schrack HM File", "xls", label_visibility="hidden")

    st.subheader("Filemaker Datenbank", divider=True)
    st.markdown("Die Filemaker Datenbank muss hier nicht separat geladen werden. Da die Datenbank sämtliche Türen aller Objekte enthält, wurde sie direkt in die Applikation integriert und wird im Hintergrund automatisch geladen.")


if st.button("Alle Daten laden", type="primary"):

    with col_2:
        st.subheader("CAD-File als Vergleichsbasis", divider=True)
        st.markdown("Die Datensätze aus dem CAD-File dienen im weiteren als Vergleichsgrundlage, um zu bestimmen, wieviele Übereinstimmungen in den einzelnen Datenfiles gefunden werden können. Dazu wird die Anzahl der Datensätze in den Datenfiles mit der Anzahl der Matches zwischen Datenfile und CAD-File bestimmt.")

    if bst is not None and flt is not None and hm is not None and \
        npa is not None and cad is not None:

        cad_data = CADLoader(file=cad, title="CAD")
        df_cad = cad_data.get_data(prefixed=True)

        npa_data = NPALoader(file=npa, title="NPA")
        df_npa = npa_data.get_data(prefixed=True)

        bst_data = BSTLoader(file=bst, title="BST")
        df_bst = bst_data.get_data(prefixed=True)

        flt_data = FLTLoader(file=flt, title="FLT")
        df_flt = flt_data.get_data(prefixed=True)

        hm_data = HMLoader(file=hm, title="HM")
        df_hm = hm_data.get_data(prefixed=True)

        fm_data = FMLoader()
        df_fm = fm_data.get_data(prefixed=True)

        l = [df_cad, df_npa, df_bst, df_flt, df_hm, df_fm]

# MERGING
# -----------------------------------------------------------------------------------

        merger = FileMerger(files=l, how="left", column="merge")
        merge = merger.get_data_merge()

        merge, info = eliminate_duplicates(merge, "CAD___gar_tuernummer_alt", "NPA___alte_tuernummer")
        merge, info = eliminate_duplicates(merge, "CAD___gar_tuernummer_alt", "HM___tuer_nr_alt", info)
        merge, info = eliminate_duplicates(merge, "CAD___gar_flucht_tuer_nr", "NPA___fluchtwegs_tuer_nr", info)
        merge, info = eliminate_duplicates(merge, "NPA___alte_tuernummer", "FM___brandmeldernr", info)

        elimination_info = DataFrame({
            "AKS-Nummer": info.keys(),
            "Zeilen die durch Zusatzattribute eliminiert werden konnten": info.values()
        })

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
            "Selbstschließend"
        ]

        output.columns = clean_column_names

        output = output.iloc[:, [4, 0, 1, 2, 3, 5, 6, 7]]

# DOWNLOAD
# -----------------------------------------------------------------------------------

        buffer = BytesIO()

        with ExcelWriter(buffer, engine='xlsxwriter') as writer:

            output.to_excel(writer, sheet_name='Merge')

            # CAD duplicates are written to a separate sheet
            dp_cad = count_duplicates(df_cad)
            dp_cad.rename(columns={"Anzahl Duplikate": f"Anzahl Duplikate CAD-File"}, inplace=True)

            for i, dataset in enumerate([df_npa, df_bst, df_flt, df_hm, df_fm]):

                name = dataset.columns[0].split("___")[0]+"-File"
                fm = FileMerger(files=[df_cad, dataset], how="inner")

                a = len(dataset)
                b = len(fm.get_data_merge().drop_duplicates())
                quotient = round(b / a * 100, 2)
                delta =round(quotient-100, 2)

                with col_2:
                    st.subheader(f"{name} Übereinstimmung mit CAD", divider=True)
                    st.write(f"Von {a} Datensätzen im {name} konnten {b} Datensätze erfolgreich mit dem CAD-Datenfile gematcht werden ({quotient}%). Vollständige Duplikate wuden von diesem Vergleich ausgeschlossen.")
                    st.metric(label=f"{name}", value=f"{quotient}%", delta=f"{delta}%.", border=True, label_visibility="collapsed")

                    nm = fm.find_non_matching_rows()
                    nm.to_excel(writer, sheet_name=f"{name} ohne AKS-Match")

                # This step is scipped for filemaker, as the duplicate
                # detection process does not work sufficiently there
                # FM has i = 5
                if i < 4:
                    dp = count_duplicates(dataset)
                    dp.rename(columns={"Anzahl Duplikate": f"Anzahl Duplikate {name}"}, inplace=True)
                    dp_cad = dp_cad.merge(dp, on='AKS-Nummer', how='outer')


            # FILL THE EMPTY CELLS

            duplicate_aks_numbers = dp_cad["AKS-Nummer"].values

            c = [
                "Anzahl Duplikate CAD-File",
                "Anzahl Duplikate NPA-File",
                "Anzahl Duplikate BST-File",
                "Anzahl Duplikate FLT-File",
                "Anzahl Duplikate HM-File"
            ]

            def fill_empty(x):
                if isna(x):
                    if x in l[i]["merge"]:
                        return 1
                    else:
                        return 0
                return x


            for i, column in enumerate(c):
                dp_cad[column] = dp_cad[column].apply(fill_empty)

            # CREATE FINAL COLUMN

            dp_cad["Zeilen im Merge nach Zusammenführen"] = prod([v for v in dp_cad.iloc[0].to_list()[1:] if v > 1])
            dp_cad = dp_cad.merge(elimination_info, on="AKS-Nummer", how='outer')

            dp_cad.fillna(0, inplace=True)

            dp_cad["Verbleibende Zeilen im Merge"] = dp_cad["Zeilen im Merge nach Zusammenführen"] - dp_cad["Zeilen die durch Zusatzattribute eliminiert werden konnten"]

            dp_cad.to_excel(writer, sheet_name=f"AKS-Duplikate")


        st.download_button(
            label="Zusammengeführte Daten als Excel herunterladen",
            data=buffer,
            file_name="VIE-DOORS_merge_download.xlsx",
            mime="application/vnd.ms-excel",
            type="primary"
        )