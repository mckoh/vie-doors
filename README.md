# VIE-Doors Integration ✈

[![Docker Image CI](https://github.com/mckoh/vie-doors/actions/workflows/docker-image.yml/badge.svg)](https://github.com/mckoh/vie-doors/actions/workflows/docker-image.yml)

Dieses Repository enthält Python Code zur Integration von Anlagendaten über Brandschutz- und Fluchttüren. Der Gesamte Code befindet sich im Modulordner `viedoors`. Die zu integrierenden Daten befinden sich im Ordner `data`. Als Frontend dient eine Streamlit-App, die wie folgt gestartet werden kann:

```sh
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Code-Struktur

### Hauptklassen

* ``ExcelLoader``:  🔍[Code Dokumentation](docs/excelloader.md)
* ``FileMerger``:  🔍[Code Dokumentation](docs/filemerger.md)

### Subklassenß

* ``CADLoader``:  🔍[Code Dokumentation](docs/cadloader.md)
* ``BSTLoader``:  🔍[Code Dokumentation](docs/bstloader.md)
* ``FLTLoader``:  🔍[Code Dokumentation](docs/fltloader.md)
* ``HMLoader``:  🔍[Code Dokumentation](docs/hmloader.md)
* ``NPALoader``:  🔍[Code Dokumentation](docs/npaloader.md)
* ``FMLoader``:  🔍[Code Dokumentation](docs/fmloader.md)

## Merge-Logik – Beschreibung

Der Merge-Prozess wird immer von links nach rechts durchgeführt und verwendet die **CAD**-Daten als Basis. Als Merge-Logik kommt daher immer der Right-Join zum Tragen, weshalb der Merge stets alle Datensätze aus CAD enthält und dort, wo es Übereinstimmungen gibt, auch jene Daten aus der angefügten Datei.

## Anwendungsbeispiel: Laden

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

##  Anwendungsbeispiel: Merging

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

## Anwendungsbeispiel: Analyse von Matches/Non-Matches

Mit Hilfe der Funktion `count_duplicates(df_cad)` können außerdem die Duplikate in den einzelnen Dataframes gezählt werden.

Die ``FileMerger`` Klasse kann ebenfalls verwendet werden, um die Nicht-Matches zwischen zwei Dataframes zu prüfen. Dazu können diese beiden Dataframes an die Merge-Klasse übergeben werden und anschließend die Methode `find_non_matching_rows()` genutzt werden.

```python
fm = FileMerger(files=[df_cad, df_npa], how="inner")
nm = fm.find_non_matching_rows()
```

## Code Dokumentation

### 📘 Klasse: `ExcelLoader`

#### 🔍 Zweck
Die Klasse `ExcelLoader` lädt Excel-Dateien samt aller enthaltenen Sheets in den Arbeitsspeicher und bereitet sie strukturiert auf. Dabei werden leere Zeilen entfernt, Spalten optional bereinigt und bei Bedarf mit einem Titel präfixiert. Die Daten werden als `pandas.DataFrame` verwaltet.

#### 🧩 Attribute

| Attribut   | Typ     | Beschreibung                                                        |
|------------|----------|----------------------------------------------------------------------|
| `file`     | `str`    | Dateiname inkl. Dateiendung                                          |
| `title`    | `str`    | Titelpräfix zur Kennzeichnung von Spalten                            |
| `data`     | `DataFrame` | Geladene Daten aus der Excel-Datei                                 |

#### 🔧 Konstruktor

```python
ExcelLoader(file, title, *args, **kwargs)
```

Initialisiert das Objekt und lädt die Daten aus der Excel-Datei. Zusätzliche Parameter werden direkt an `read_excel_all_sheets()` weitergegeben, was eine hohe Flexibilität erlaubt.

#### 🛠️ Methoden

##### `__load_data(*args, **kwargs)`
- Lädt sämtliche Sheets aus der Excel-Datei als einheitlichen `DataFrame`
- Alle Spalten werden als Strings (`object`) gelesen, um Typ-Inferenz zu verhindern
- Vollständig leere Zeilen werden automatisch entfernt

##### `__remove_duplicates()`
- Entfernt doppelte Zeilen aus dem geladenen `DataFrame`

##### `__clean_data()`
- Führt eine Bereinigung der Spaltennamen durch, z. B. Entfernen von Leerzeichen oder Sonderzeichen
- Verwendet die externe Funktion `clean_data()`

##### `get_data(prefixed=False) -> DataFrame`
- Gibt den geladenen `DataFrame` zurück
- Falls `prefixed=True`, werden alle Spalten mit dem `title` versehen (z. B. `HM___tuernummer`)
- Zusätzlich wird eine `"merge"`-Spalte aus `"integration_aks"` generiert – mit oder ohne Präfix, je nach Einstellung

##### `get_columns() -> list`
- Gibt eine Liste der Spaltennamen im geladenen DataFrame zurück

#### 📎 Beispiel

```python
loader = ExcelLoader("tuerdaten.xlsx", "HM")
df = loader.get_data(prefixed=True)
cols = loader.get_columns()
```

#### 📌 Hinweise

- Die Klasse nimmt an, dass die Datei mehrere Sheets enthalten kann und behandelt sie entsprechend
- `read_excel_all_sheets()` muss sicherstellen, dass alle relevanten Sheets korrekt konsolidiert werden
- Die `"merge"`-Spalte dient als Schlüssel für spätere Datenverknüpfungen
- Es wird vorausgesetzt, dass `integration_aks` eine eindeutige Referenzspalte ist

### 📦 Klasse: `FileMerger`

#### 🔍 Zweck
Die Klasse `FileMerger` dient zur schrittweisen Zusammenführung mehrerer `pandas.DataFrame`-Objekte anhand einer gemeinsamen Spalte (Standard: `"merge"`). Sie bietet Funktionen zur Detektion nicht übereinstimmender Zeilen, Duplikaten sowie zur optionalen Bereinigung anhand benutzerdefinierter Kriterien.

#### 🧩 Attribute

| Attribut       | Typ                 | Beschreibung                                                                 |
|----------------|---------------------|------------------------------------------------------------------------------|
| `files`        | `list[DataFrame]`   | Liste der DataFrames, die zusammengeführt werden sollen                     |
| `how`          | `str`               | Join-Strategie (`"left"`, `"right"`, `"inner"`, `"outer"`)                  |
| `column`       | `str`               | Name der Spalte, nach der gemerged wird                                     |
| `data_merge`   | `DataFrame`         | Ergebnis des Merges nach Ausführung                                          |

#### 🔧 Konstruktor
```python
FileMerger(files, how="left", column="merge")
```

Initialisiert das Objekt und führt automatisch den Merge der übergebenen Dateien aus. Es müssen mindestens zwei DataFrames übergeben werden.

#### 🛠️ Methoden

##### `__merge()`
Führt intern den schrittweisen Merge aller übergebenen Dateien von links nach rechts durch.

##### `find_non_matching_rows() -> DataFrame`
Identifiziert alle Zeilen, die **nur im zweiten** der beiden übergebenen Dateien vorkommen. Nur verwendbar bei genau zwei Dateien.

##### `find_duplicates() -> DataFrame`
Gibt alle doppelten Zeilen zurück, basierend auf der `"merge"`-Spalte. Ebenfalls nur für genau zwei Dateien geeignet.

##### `get_data_merge(eliminate=False) -> DataFrame or (DataFrame, DataFrame)`
Gibt das zusammengeführte Ergebnis zurück. Optional können Duplikate auf Grundlage zusätzlicher Schlüsselspalten mit der externen Funktion `eliminate_duplicates()` entfernt werden. Rückgabe dann inkl. Infotabelle mit eliminierten Zeilen.

##### `export_merge(file="dummy.xlsx")`
Speichert das zusammengeführte Ergebnis als Excel-Datei unter dem angegebenen Dateinamen.

#### 🔎 Hinweise zur Verwendung
- **Mindestanzahl an Dateien**: 2
- **Spalte zum Mergen** muss in allen DataFrames vorhanden sein.
- Die Methoden `find_non_matching_rows` und `find_duplicates` sind **nicht kompatibel mit mehr als zwei Dateien**.
- Die externe Hilfsfunktion `eliminate_duplicates` wird zur datengetriebenen Duplikaterkennung genutzt.

#### 📌 Beispielhafte Anwendung
```python
merger = FileMerger([df1, df2], how="left", column="merge")
merged_data = merger.get_data_merge(eliminate=True)
merged_data.to_excel("output.xlsx")
```

### 🛠️ Klasse: `CADLoader`

#### 🔍 Zweck
Die Klasse `CADLoader` lädt CAD-bezogene Excel-Dateien, homogenisiert die Spaltennamen und bereitet eine eindeutige Integrationskennung (`integration_aks`) vor. Diese Kennung dient der späteren Datenverknüpfung.

#### 🧬 Vererbung
Erbt von: [`ExcelLoader`](#)

#### 🧩 Attribute

| Attribut        | Typ       | Beschreibung                                                          |
|-----------------|-----------|------------------------------------------------------------------------|
| `file`          | `str`     | Dateiname inkl. Endung                                                 |
| `title`         | `str`     | Spaltenpräfix für die Datenquelle                                     |
| `data`          | `DataFrame` | Geladene und vorbereitete CAD-Daten                                  |

#### 🔧 Konstruktor

```python
CADLoader(file, title, *args, **kwargs)
```

Initialisiert das Objekt und lädt die CAD-Datei. Dabei werden die Spaltennamen durch die vordefinierte Liste `cad_columns` ersetzt oder ergänzt (bei abweichender Anzahl). Anschließend erfolgt die Verarbeitung einzelner Spalten zur Generierung der `integration_aks`.

#### 🛠️ Verarbeitungsschritte im Konstruktor

##### 📌 Spaltenhomogenisierung
- Vergleicht die Anzahl geladener Spalten mit `cad_columns`
- Verwendet `columns_expander()` zur Anpassung der Spaltenliste

##### 🔧 Spalten-Mapping
Wendet Mapper-Funktionen auf Schlüsselspalten an:
- `gar_tuernummer_bauteil`: via `object_mapper`
- `gar_tuernummer_ebene`: via `level_mapper`
- `gar_tuernummer_nummer`: via `door_mapper`
- `gar_tuernummer_aks_nr`: via `room_mapper`

##### 🧩 Integration Key
Erstellt die eindeutige `integration_aks`-Spalte:
```python
integration_aks = bauteil + " " + ebene + modul + aks_nr + "." + nummer
```

Diese AKS-Nummer bildet die Grundlage für spätere Merge-Vorgänge mit anderen Datenquellen (z. B. NPA, HM, FM).

#### 📎 Beispiel

```python
loader = CADLoader("cad_tueren.xlsx", "CAD")
df = loader.get_data(prefixed=True)
```

#### 📌 Hinweise
- Die Mapper-Funktionen dienen zur Vereinheitlichung von CAD-internen Codes
- Die generierte `integration_aks` sollte in anderen Datenquellen ebenfalls vorkommen
- Die Klasse setzt auf saubere Spaltenstruktur – `cad_columns` muss sorgfältig gepflegt sein

### 🏢 Klasse: `NPALoader`

#### 🔍 Zweck
Der `NPALoader` ist ein spezialisierter Datenimporter, der NPA-Excel-Dateien (z. B. aus der Türplanung) in Speicher lädt, homogenisiert und aufbereitet. Er extrahiert relevante Informationen für die eindeutige Türkennung (`integration_aks`) und bietet ein Matching-Schema zur Verbindung mit FM-Daten via `schlossernummer`.

#### 🧬 Vererbung
Erbt von: `ExcelLoader`

#### 🧩 Attribute

| Attribut         | Typ           | Beschreibung                                                              |
|------------------|---------------|---------------------------------------------------------------------------|
| `file`           | `str`         | Dateiname der NPA-Datei (inkl. Endung)                                    |
| `title`          | `str`         | Kürzel zur Präfixierung der Spalten (z. B. `"NPA"`)                        |
| `data`           | `DataFrame`   | Geladene und bereinigte Daten                                             |

#### 🔧 Konstruktor

```python
NPALoader(file, title)
```

Initialisiert das Objekt und führt folgende Schritte aus:

1. **Spaltenangleichung** mit `npa_columns` via `columns_expander()`
2. **Mapping der AKS-Bestandteile**:
   - `objekt`: über `object_mapper`
   - `ebene`: über `level_mapper`
   - `room`: aus `aks_plan` extrahiert und über `room_mapper` verfeinert
   - `door`: aus `aks_plan` extrahiert und über `door_mapper` verfeinert
3. **Konstruktion der AKS-Nummer**:
```python
integration_aks = objekt + " " + ebene + bauteil + room + "." + door
```
4. **Löschen von Duplikat-Header-Zeilen**
5. **Generierung eines Matching-Schlüssels** `npa_fm_match` aus `schlossernummer`, bestehend aus:
   - `SN1`: Positionskennung
   - `SN2`: Ebene (über `level_mapper`)
   - `SN3`: laufende Nummer

Der Schlüssel wird als:
```python
npa_fm_match = SN1 + "-" + SN2 + "-" + SN3
```

#### 🛠️ Methode: `get_data(prefixed=False)`

##### Beschreibung
Gibt die aufbereiteten Daten zurück. Optional werden alle Spalten mit dem Titelpräfix versehen, und die Spalten `merge` und `npa_fm_match` werden korrekt ergänzt.

##### Parameter

| Name       | Typ    | Beschreibung                                  |
|------------|--------|-----------------------------------------------|
| `prefixed` | `bool` | Wenn `True`, wird Titel als Spaltenpräfix verwendet |

##### Rückgabe
- `DataFrame` mit vollständig vorbereiteten Daten
- Spalte `merge` = `integration_aks`
- Spalte `npa_fm_match` = Matching-Schlüssel zur FM-Zuordnung

#### 📎 Beispiel

```python
loader = NPALoader("npa_daten.xlsx", "NPA")
df = loader.get_data(prefixed=True)
```

#### 📌 Hinweise

- Die Spalte `integration_aks` erlaubt Verknüpfung mit CAD-, HM-, BST-, FLT-Daten
- Der Schlüssel `npa_fm_match` kann zur Zuordnung von Schließplänen (FM) verwendet werden
- Die Klasse entfernt Mehrfach-Header und verarbeitet flexible Spaltenanzahl

### 🗃️ Klasse: `BSTLoader`

#### 🔍 Zweck
`BSTLoader` ist eine spezialisierte Erweiterung von `ExcelLoader` zur Verarbeitung von BST-Excel-Dateien. Sie sorgt für die Harmonisierung von Spaltennamen und bereitet die Daten so vor, dass eine eindeutige Integrationsnummer (`integration_aks`) für spätere Datenverknüpfungen erzeugt wird.

#### 🧬 Vererbung
Erbt von: [`ExcelLoader`](#)

#### 🧩 Attribute

| Attribut   | Typ           | Beschreibung                                                 |
|------------|---------------|---------------------------------------------------------------|
| `file`     | `str`         | Dateiname inkl. Dateiendung                                   |
| `title`    | `str`         | Präfix für Spaltennamen                                       |
| `data`     | `DataFrame`   | Geladene und vorbereitete BST-Daten                          |

#### 🔧 Konstruktor

```python
BSTLoader(file, title, *args, **kwargs)
```

Initialisiert das Objekt und lädt die BST-Daten mithilfe des Elternkonstruktors. Führt anschließend eine Harmonisierung der Spalten durch und bereitet die Daten zur Integration vor.

#### ⚙️ Verarbeitungsschritte

##### 🔄 Spaltenangleichung
- Vergleicht Ist-Spaltenanzahl mit `bst_columns`
- Ergänzt fehlende oder zusätzliche Spalten via `columns_expander`

##### 🧼 Vorbereitung für AKS-Kennung
- Konvertiert relevante Spalten zu Strings
- `ebene` wird über `level_mapper` vereinheitlicht

##### 🆔 Generierung der Integrationsnummer
Erzeugt eine eindeutige Schlüsselspalte für die Datenfusion:
```python
integration_aks = name + " " + ebene + nummer
```

Diese Spalte dient der eindeutigen Identifikation und wird z. B. für Merge-Vorgänge benötigt.

#### 📎 Beispiel

```python
loader = BSTLoader("bst_tueren.xlsx", "BST")
df = loader.get_data(prefixed=True)
```

#### 🧠 Hinweise

- Die auskommentierten Codezeilen deuten auf experimentelle bzw. alternative Ansätze zur Erzeugung von AKS hin (z. B. Zerlegung von Türnummern)
- `room_mapper` und `modul`-Verarbeitung sind aktuell deaktiviert, können bei Bedarf aber wieder eingebunden werden
- Die Klasse setzt voraus, dass die Spalten `name`, `ebene` und `nummer` vorhanden sind

### 🗂️ Klasse: `FLTLoader`

#### 🔍 Zweck
`FLTLoader` ist eine Spezialisierung der `ExcelLoader`-Basisklasse, die FLT-Excel-Dateien verarbeitet. Sie bereinigt die Spaltenstruktur und generiert aus verschiedenen Informationen eine eindeutige Integrationskennung (`integration_aks`) für spätere Datenverknüpfungen.

#### 🧬 Vererbung
Erbt von: [`ExcelLoader`](#)

#### 🧩 Attribute

| Attribut   | Typ         | Beschreibung                                               |
|------------|-------------|-------------------------------------------------------------|
| `file`     | `str`       | Dateiname inkl. Dateiendung                                 |
| `title`    | `str`       | Spaltenpräfix für die Datenquelle                          |
| `data`     | `DataFrame` | Geladene und aufbereitete FLT-Daten                         |

#### 🔧 Konstruktor

```python
FLTLoader(file, title)
```

Initialisiert das Objekt und lädt die Datei mithilfe der `ExcelLoader`-Logik. Dabei werden zwei spezielle Argumente übergeben:

- `skiprows=[0,1]`: Überspringt die ersten zwei Zeilen (z. B. FLT-Metadaten)
- `header=None`: Behandelt die tatsächlichen Spaltennamen separat

#### ⚙️ Verarbeitungsschritte

##### 🧼 Spaltenhomogenisierung
- Vergleicht Ist-Spaltenanzahl mit `flt_columns`
- Nutzt `columns_expander()` zur Angleichung der Struktur

##### 🔄 Spalten-Mapping
Bereitet einzelne Spalten zur Generierung der AKS-Nummer vor:
- `plan_nr`: zerlegt und extrahiert das Objektkennzeichen (`objekt`)
- `ebene`: über `level_mapper` standardisiert
- `raum_nr`: über `room_mapper` vereinheitlicht
- `tuer_nr`: über `door_mapper` verfeinert

##### 🆔 Generierung der `integration_aks`
Erstellt die eindeutige AKS-Nummer zur Identifikation und Datenfusion:

```python
integration_aks = objekt + " " + level + bauteil + raum_nr + "." + tuer_nr
```

#### 📎 Beispiel

```python
loader = FLTLoader("fluchtwege.xlsx", "FLT")
df = loader.get_data(prefixed=True)
```

#### 📌 Hinweise

- Die Klasse geht davon aus, dass die FLT-Datei strukturierte Informationen enthält, die sich durch Präfixe (z. B. `plan_nr`) extrahieren lassen
- Die AKS-Nummer ist für die spätere Verknüpfung mit CAD-, NPA- oder HM-Daten geeignet
- Die vorbereitenden Mapper-Funktionen sorgen für eine normierte Darstellung

### 🏗️ Klasse: `HMLoader`

#### 🔍 Zweck
`HMLoader` ist eine Spezialisierung der `ExcelLoader`-Klasse zur Verarbeitung von Excel-Dateien aus dem HM-Datenbereich. Sie homogenisiert die Spaltenstruktur und bereitet sowohl eine neue als auch eine alte AKS-Nummer zur eindeutigen Türidentifikation auf.

#### 🧬 Vererbung
Erbt von: [`ExcelLoader`](#)

#### 🧩 Attribute

| Attribut        | Typ         | Beschreibung                                                           |
|-----------------|-------------|---------------------------------------------------------------------------|
| `file`          | `str`       | Dateiname der zu ladenden HM-Excel-Datei                                 |
| `title`         | `str`       | Präfix zur Kennzeichnung der Spalten                                     |
| `data`          | `DataFrame` | Geladene und vorbereitete Daten mit neuen & alten Türnummern             |

#### 🔧 Konstruktor

```python
HMLoader(file, title, *args, **kwargs)
```

Lädt die HM-Datei und bereitet alle relevanten Spalten für die Konstruktion von Integrationskennungen (`integration_aks`) und Alt-Nummern auf.

#### ⚙️ Verarbeitungsschritte

##### 🔄 Spaltenhomogenisierung
- Vergleicht geladene Spaltenanzahl mit `hm_columns`
- Nutzt `columns_expander()` zur Anpassung der Struktur bei Abweichungen

##### 🧩 Generierung der neuen AKS-Nummer

Aus `tuer_nr_aks` werden mit Mapping-Funktionen Einzelteile extrahiert:

- `objekt`: Projektbezeichnung
- `modul`: Gebäudemodulkennung
- `room`: Raumkennung (letzte 4 Ziffern eines Teilstrings)
- `door`: Türnummer (nach dem Punkt)
- `ebene`: Gebäudeniveau (über `level_mapper`)

➡️ Zusammengesetzt zur Spalte `integration_aks`:
```python
integration_aks = objekt + " " + ebene + modul + room + "." + door
```

##### 🧾 Verarbeitung der alten AKS-Nummer (`bs_tuere_alt`)
Die Spalte wird in drei Teile zerlegt:
- `old_part_a`: Objektkennung
- `old_part_b`: Gebäudemodul (nach erstem `/`)
- `old_part_c`: Türnummer (nach zweitem `/`)

Diese Vorbereitung erlaubt spätere Vergleiche oder Historienabgleiche.

#### 📎 Beispiel

```python
loader = HMLoader("hardware_daten.xlsx", "HM")
df = loader.get_data(prefixed=True)
```

#### 📌 Hinweise

- Die AKS-Nummer (neu & alt) erlaubt präzise Mappings gegen andere Datenquellen wie CAD, NPA oder BST
- Die Verarbeitung nutzt Kombinationen von `split()` und Mapper-Funktionen für normierte Darstellung
- Die Hilfsspalte `helper_1` wird nach der Konstruktion der AKS-Nummer wieder entfernt

### 🗄️ Klasse: `FMLoader`

#### 🔍 Zweck
`FMLoader` ist eine minimalistische Klasse zum Laden vorverarbeiteter Filemaker-Daten aus einer Pickle-Datei (`fm.pkl`). Zusätzlich generiert sie einen Matching-Schlüssel (`npa_fm_match`) für die spätere Zuordnung zu NPA-Daten.

#### 🧩 Attribute

| Attribut      | Typ         | Beschreibung                                                       |
|---------------|-------------|---------------------------------------------------------------------|
| `data`        | `DataFrame` | Eingeladene Filemaker-Daten aus der Pickle-Datei                   |

#### 🔧 Konstruktor

```python
FMLoader()
```

Beim Initialisieren:
- Wird die Datei `static/fm.pkl` eingelesen
- Es wird der Schlüssel `npa_fm_match` aus den Spalten `FM___bauteil`, `FM___ebene` und `FM___topnr` konstruiert:

```python
npa_fm_match = FM___bauteil + "-" + FM___ebene + "-" + str(FM___topnr)
```

Dieser Schlüssel kann verwendet werden, um mit `NPALoader`-Daten über die Schlossernummer (`schlossernummer`) zu matchen.

#### 🛠️ Methoden

##### `get_data(prefixed=True) -> DataFrame`
- Gibt den gespeicherten DataFrame zurück
- Das Argument `prefixed` ist aktuell ohne funktionale Auswirkung (alle Spalten sind schon vorpräfixiert)

##### `get_columns() -> list`
- Gibt eine Liste der Spaltennamen im geladenen DataFrame zurück

#### 📎 Beispiel

```python
fm_loader = FMLoader()
fm_data = fm_loader.get_data()
cols = fm_loader.get_columns()
```

#### 📌 Hinweise

- Die Datei `fm.pkl` muss zuvor korrekt erzeugt und im Pfad `static/` abgelegt worden sein
- Die Methode `get_data()` bietet aktuell keine zusätzliche Datenbearbeitung an – dafür ist die Pickle-Datei bereits vorbereitet
- Der generierte Schlüssel `npa_fm_match` harmonisiert das Format für spätere Merge-Vorgänge mit NPA-Daten

