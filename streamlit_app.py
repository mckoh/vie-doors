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

col_1, col_2, col_3 = st.columns(3, gap="medium", vertical_alignment="top")

with col_1:
    cad = st.file_uploader("CAD File", "xlsx")
    npa = st.file_uploader("NPA File", "xlsx")

with col_2:
    bst = st.file_uploader("Sisando BST File", "xlsx")
    flt = st.file_uploader("Sisando FLT File", "xlsx")

with col_3:
    hm = st.file_uploader("Schrack HM File", "xls")
    fm = st.file_uploader("Filemaker File", "xlsx")

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

        merger = FileMerger(files=[df_cad, df_npa, df_hm, df_bst, df_flt, df_fm], how="left")
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
