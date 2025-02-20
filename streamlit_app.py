import streamlit as st
from io import BytesIO
from pandas import ExcelWriter
from viedoors import BSTLoader, FLTLoader, HMLoader, FMLoader
from viedoors import CADLoader, NPALoader, FileMerger
from zipfile import ZipFile


st.set_page_config(
    page_title="VIE Door Integrator",
    page_icon="📃",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None
)

if "default_merge_disabled" not in st.session_state:
    st.session_state["default_merge_disabled"] = True

def set_session_state():
    if st.session_state["default_merge_disabled"]:
        st.session_state["default_merge_disabled"] = False
    else:
        st.session_state["default_merge_disabled"] = True

# SIDE BAR
# -------------------------------------------------
st.sidebar.header("Einstellungen")

join_type = st.sidebar.selectbox(
    "Integrationstyp auswählen",
    [
        "Links nach Rechts",
        "Rechts nach Links",
        "Vollständige Übereinstimmung",
        "Alles"
    ]
)

join_type_description = st.sidebar.empty()

default_merge = st.sidebar.checkbox(
    "'merge'-Spalte zum Zusammenführen verwenden (Default)",
    value=True,
    on_change=set_session_state
)

merge_column_name = st.sidebar.text_input(
    label="Name der Matching-Spalte",
    disabled=st.session_state["default_merge_disabled"]
)

if merge_column_name == "":
    merge_column_name = "merge"

if join_type == "Links nach Rechts":
    j = "left"
    join_type_description.markdown(">**Erklärung zum gewählten Join-Typ:** \
        Datensätze werden von Links nach Rechts zusammengeführt. Die Ergebnismenge \
        enthält **alle Datensätze der linken (ersten) Datei** und **jene der zweiten \
        (rechten) Datei, die mit jenen der ersten Datei übereinstimmen**. Falls keine \
        Übereinstimmung gefunden wird, werden die restlichen Datensätze aus der rechten \
        Tabelle mit Platzhalterwerten gefüllt.")

elif join_type == "Rechts nach Links":
    j = "right"
    join_type_description.markdown(">**Erklärung zum gewählten Join-Typ:** Datensätzen \
        erden von Rechts nach Links zusammengeführt. Die Ergebnismenge enthält **alle \
        Datensätze der rechten (zweiten) Datei** und **jene der ersten (linken) Datei, \
        die mit jenen der ersten Datei übereinstimmen**. Falls keine Übereinstimmung \
        gefunden wird, werden die restlichen Datensätze aus der rechten Tabelle mit \
        Platzhalterwerten gefüllt.")

elif join_type == "Alles":
    j = "outer"
    join_type_description.markdown(">**Erklärung zum gewählten Join-Typ:** Datensätze \
        werden vollständig zusammengeführt. Die Ergebnismenge enthält **alle Datensätze \
        der linken (ersten) Datei** und **alle Datensätze der zweiten (rechten) Datei**. \
        Falls keine Übereinstimmung gefunden wird, werden die restlichen Datensätze aus \
        der rechten Tabelle mit Platzhalterwerten gefüllt.")

elif join_type == "Vollständige Übereinstimmung":
    j = "inner"
    join_type_description.markdown(">**Erklärung zum gewählten Join-Typ:** Datensätze \
        werden nur dort zusammengeführt, wo es Übereinstimmungen gibt. Die Ergebnismenge \
        enthält **alle Datensätze der linken (ersten) Datei die einen entsprechenden \
        Datensatz in der zweiten (rechten) Datei besitzen**.")


# MAIN PAGE
# -------------------------------------------------

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

        l = [df_cad, df_npa, df_hm, df_bst, df_flt, df_fm]

        # If Right Joins is used, turn the list upside down and do a left-join
        if j == "right":
            l = l[::-1]
            j = "left"

        merger = FileMerger(files=l, how=j, column=merge_column_name)
        merge = merger.get_data_merge()


        # DOWNLOAD
        buffer = BytesIO()

        with ExcelWriter(buffer, engine='xlsxwriter') as writer:

            merge.to_excel(writer, sheet_name='all_matches')

            for dataset in [df_npa, df_bst, df_flt, df_hm, df_fm]:

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
                    nm.to_excel(writer, sheet_name=f"nomatch_{name}")


        st.download_button(
            label="Zusammengeführte Daten als Excel herunterladen",
            data=buffer,
            file_name="VIE-DOORS_merge_download.xlsx",
            mime="application/vnd.ms-excel",
            type="primary"
        )