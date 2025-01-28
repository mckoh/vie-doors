import streamlit as st
from io import BytesIO
from pandas import ExcelWriter
from viedoors import BSTLoader, FLTLoader, HMLoader, FMLoader
from viedoors import CADLoader, NPALoader, FileMerger


st.set_page_config(
    page_title="VIE Door Integrator",
    page_icon="📃",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items=None
)

st.title("VIE-Door Integrator")

st.markdown("Unterhalb können die Files ausgewählt werden, die im weiteren Verlauf integriert werden. Bitte beachten Sie, dass alle 6 Files aufeinander abgestimmt sein, und Daten über dasselbe Objekt (z.B. 420) enthalten müssen.")

st.sidebar.header("Einstellungen")

join_type = st.sidebar.selectbox("Integrationstyp auswählen", ["Links nach Rechts", "Rechts nach Links", "Vollständige Übereinstimmung", "Alles"])

join_type_description = st.sidebar.empty()

if join_type == "Links nach Rechts":
    j = "left"
    join_type_description.markdown(">**Erklärung zum gewählten Join-Typ:** Datensätze werden von Links nach Rechts zusammengeführt. Die Ergebnismenge enthält **alle Datensätze der linken (ersten) Datei** und **jene der zweiten (rechten) Datei, die mit jenen der ersten Datei übereinstimmen**. Falls keine Übereinstimmung gefunden wird, werden die restlichen Datensätze aus der rechten Tabelle mit Platzhalterwerten gefüllt.")
elif join_type == "Rechts nach Links":
    j = "right"
    join_type_description.markdown(">**Erklärung zum gewählten Join-Typ:** Datensätze werden von Rechts nach Links zusammengeführt. Die Ergebnismenge enthält **alle Datensätze der rechten (zweiten) Datei** und **jene der ersten (linken) Datei, die mit jenen der ersten Datei übereinstimmen**. Falls keine Übereinstimmung gefunden wird, werden die restlichen Datensätze aus der rechten Tabelle mit Platzhalterwerten gefüllt.")
elif join_type == "Alles":
    j = "outer"
    join_type_description.markdown(">**Erklärung zum gewählten Join-Typ:** Datensätze werden vollständig zusammengeführt. Die Ergebnismenge enthält **alle Datensätze der linken (ersten) Datei** und **alle Datensätze der zweiten (rechten) Datei**. Falls keine Übereinstimmung gefunden wird, werden die restlichen Datensätze aus der rechten Tabelle mit Platzhalterwerten gefüllt.")
elif join_type == "Vollständige Übereinstimmung":
    j = "inner"
    join_type_description.markdown(">**Erklärung zum gewählten Join-Typ:** Datensätze werden nur dort zusammengeführt, wo es Übereinstimmungen gibt. Die Ergebnismenge enthält **alle Datensätze der linken (ersten) Datei die einen entsprechenden Datensatz in der zweiten (rechten) Datei besitzen**.")

st.header("Dateien auswählen")

col_1, col_2, col_3 = st.columns(3, gap="medium", vertical_alignment="top", )

with col_1:
    st.subheader("CAD-File", divider=True)
    cad = st.file_uploader("CAD File", "xlsx", label_visibility="hidden")
    st.subheader("### NPA-File", divider=True)
    npa = st.file_uploader("NPA File", "xlsx", label_visibility="hidden")

with col_2:
    st.subheader("Sisando BST-File", divider=True)
    bst = st.file_uploader("Sisando BST File", "xlsx", label_visibility="hidden")
    st.subheader("Sisando FLT-File", divider=True)
    flt = st.file_uploader("Sisando FLT File", "xlsx", label_visibility="hidden")

with col_3:
    st.subheader("Schrack HM-File", divider=True)
    hm = st.file_uploader("Schrack HM File", "xls", label_visibility="hidden")
    st.subheader("Filemaker-File", divider=True)
    fm = st.file_uploader("Filemaker File", "xlsx", label_visibility="hidden")

if st.button("Load Data", type="primary"):

    if bst is not None and flt is not None and hm is not None and \
        npa is not None and fm is not None and cad is not None:

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

        fm_data = FMLoader(file=fm, title="FM")
        df_fm = fm_data.get_data(prefixed=True)

        l = [df_cad, df_npa, df_hm, df_bst, df_flt, df_fm]

        # If Right Joins is used, turn the list upside down and do a left-join
        if j == "right":
            l = l[::-1]
            j = "left"

        merger = FileMerger(files=l, how=j)
        merge = merger.get_data_merge()


        buffer = BytesIO()

        with ExcelWriter(buffer, engine='xlsxwriter') as writer:

            merge.to_excel(writer, sheet_name='Sheet1')
            writer.close()

        st.download_button(
            label="Download Merge Excel",
            data=buffer,
            file_name="VIE-DOORS_merge_download.xlsx",
            mime="application/vnd.ms-excel",
            type="primary"
        )
