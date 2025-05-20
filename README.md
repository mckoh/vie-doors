# VIE-Doors Integration ✈

[![Docker Image CI](https://github.com/mckoh/vie-doors/actions/workflows/docker-image.yml/badge.svg)](https://github.com/mckoh/vie-doors/actions/workflows/docker-image.yml)

![Beschriftung Brandschutztüre](docs/bst.jpg)

Dieses Repository enthält Python Code zur Integration von Anlagendaten über Brandschutz- und Fluchttüren. Der Gesamte Code befindet sich im Modulordner `viedoors`. Die zu integrierenden Daten befinden sich im Ordner `data`. Als Frontend dient eine Streamlit-App, die wie folgt gestartet werden kann:

```sh
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Loading of Files

Mit Hilfe des Loader-Moduls können die Quelldatein geladen werden. Dabei werden Spalten und Worksheets aufgeräumt und alle Daten in einem `pandas.DataFrame` zusammengefasst.

```python
from viedoors import CADLoader, BSTLoader, FLTLoader
from viedoors import HMLoader, FMLoader, NPALoader

c = CADLoader(file="data/420_gesamt_20250122.xlsx", title="CAD")
c.get_data(prefixed=True)

n = NPALoader(file="data/NPA_Tuer Aufnahme Obj420.xlsx", title="NPA")
n.get_data(prefixed=True)

b = BSTLoader(file="data/Sisando_BST_Obj420.xlsx", title="BST")
b.get_data(prefixed=True)

f = FLTLoader(file="data/Sisando_FLT_Obj420.xlsx", title="FLT")
f.get_data(prefixed=True)

h = HMLoader(file="data/Schrack_HM_Obj.420.xls", title="HM")
h.get_data(prefixed=True)

# Achtung: Diese Daten werden nicht aus einem Excel-File geladen, sondern
# aus einem serialisierten Pandas-Objekt
f = FMLoader()
f.get_data(prefixed=True)
```

## Merging of Files

Mit Hilfe des Merge-Moduls können die geladenen Quelldateien anschließend zusammengeführt werden. Dabei werden die Pandas-Objekte in der Reihenfolge der Übergabe an die `FileMerger`-Klasse zusammengeführt. Die Join-Methode kann dabei definiert werden.


```python
from pandas import DataFrame, concat
from viedoors import CADLoader, NPALoader, FileMerger, HMLoader, count_duplicates
from viedoors import BSTLoader, FLTLoader, FMLoader, eliminate_duplicates

obj = "420"

cad = CADLoader(file=f"data/{obj}/cad.xlsx", title="CAD")
npa = NPALoader(file=f"data/{obj}/npa.xlsx", title="NPA")
hm = HMLoader(file=f"data/{obj}/hm.xls", title="HM")
bst = BSTLoader(file=f"data/{obj}/bst.xlsx", title="BST")
flt = FLTLoader(file=f"data/{obj}/flt.xlsx", title="FLT")
fm = FMLoader()

df_npa = npa.get_data(prefixed=True)
df_cad = cad.get_data(prefixed=True)
df_hm = hm.get_data(prefixed=True)
df_bst = bst.get_data(prefixed=True)
df_flt = flt.get_data(prefixed=True)
df_fm = fm.get_data(prefixed=True)

merger = FileMerger(files=[df_cad, df_npa, df_hm, df_bst, df_flt, df_fm], how="left")
merge = merger.get_data_merge()

merge.to_excel("420_match_file.xlsx")
```

Mit Hilfe der `eliminate_duplicates`-Funktion können anschließend Duplikate im Merge auf Basis des Abgleichs zweier Spalten eliminiert werden. Die Funktion gibt abschließend den bereinigten Merge zurück. Zusätzlich dazu wird auch ein Dictionary-Objekt mit den AKS-Nummern der eliminierten Zeilen und deren Anzahl zurückgegeben.

Um die Info der eliminierten Zeilen auch über mehrere Stufen hinweg weitergeben zu können, kann der Funktion auch ein bereits erstelltes Info-Dictionary mitgegeben werden.

```python
merge, info = eliminate_duplicates(
    merge,
    "CAD___gar_tuernummer_alt",
    "NPA___alte_tuernummer"
)

merge, info = eliminate_duplicates(
    merge,
    "CAD___gar_tuernummer_alt",
    "HM___tuer_nr_alt",
    info
)

merge, info = eliminate_duplicates(
    merge,
    "CAD___gar_flucht_tuer_nr",
    "NPA___fluchtwegs_tuer_nr",
    info
)

merge, info = eliminate_duplicates(
    merge,
    "NPA___alte_tuernummer",
    "FM___brandmeldernr",
    info
)
```

## Analyse von Matches/Non-Matches

Mit Hilfe der Funktion `count_duplicates(df_cad)` können außerdem die Duplikate in den einzelnen Dataframes gezählt werden.

Die ``FileMerger`` Klasse kann ebenfalls verwendet werden, um die Nicht-Matches zwischen zwei Dataframes zu prüfen. Dazu können diese beiden Dataframes an die Merge-Klasse übergeben werden und anschließend die Methode `find_non_matching_rows()` genutzt werden.

```python
fm = FileMerger(files=[df_cad, df_npa], how="inner")
nm = fm.find_non_matching_rows()
```
