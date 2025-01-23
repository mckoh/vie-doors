import streamlit as st
from viedoors import BSTLoader, FLTLoader, HMLoader, FMLoader
from viedoors import CADLoader, NPALoader

st.title("VIE-Doors Data Integrator")

st.markdown("Unterhalb können die Files ausgewählt werden, die im weiteren Verlauf integriert werden. Bitte beachten Sie, dass alle 6 Files aufeinander abgestimmt sein, und Daten über dasselbe Objekt (z.B. 420) enthalten müssen.")

bst = st.file_uploader("Sisando BST File", "xlsx")
flt = st.file_uploader("Sisando FLT File", "xlsx")
hm = st.file_uploader("Schrack HM File", "xls")
npa = st.file_uploader("NPA File", "xlsx")
fm = st.file_uploader("Filemaker File", "xlsx")
cad = st.file_uploader("CAD File", "xlsx")

if st.button("Load Data"):

    if bst is not None and flt is not None and hm is not None and \
        npa is not None and fm is not None and cad is not None:

        bst_data = BSTLoader(file=bst, title="BST")
        flt_data = FLTLoader(file=flt, title="FLT")
        hm_data = HMLoader(file=hm, title="FLT")
        npa_data = NPALoader(file=npa, title="FLT")
        fm_data = FMLoader(file=fm, title="FLT")
        cad_data = CADLoader(file=cad, title="FLT")

        st.write("All files successfully loaded.")
        # st.dataframe(bst_data.get_data())