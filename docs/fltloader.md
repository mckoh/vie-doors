### 🗂️ Klasse: `FLTLoader`

#### 🔍 Zweck
`FLTLoader` ist eine Spezialisierung der `ExcelLoader`-Basisklasse, die FLT-Excel-Dateien verarbeitet. Sie bereinigt die Spaltenstruktur und generiert aus verschiedenen Informationen eine eindeutige Integrationskennung (`integration_aks`) für spätere Datenverknüpfungen.

#### 🧬 Vererbung
Erbt von: [`ExcelLoader`](#)

---

#### 🧩 Attribute

| Attribut   | Typ         | Beschreibung                                               |
|------------|-------------|-------------------------------------------------------------|
| `file`     | `str`       | Dateiname inkl. Dateiendung                                 |
| `title`    | `str`       | Spaltenpräfix für die Datenquelle                          |
| `data`     | `DataFrame` | Geladene und aufbereitete FLT-Daten                         |

---

#### 🔧 Konstruktor

```python
FLTLoader(file, title)
```

Initialisiert das Objekt und lädt die Datei mithilfe der `ExcelLoader`-Logik. Dabei werden zwei spezielle Argumente übergeben:

- `skiprows=[0,1]`: Überspringt die ersten zwei Zeilen (z. B. FLT-Metadaten)
- `header=None`: Behandelt die tatsächlichen Spaltennamen separat

---

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

---

#### 📎 Beispiel

```python
loader = FLTLoader("fluchtwege.xlsx", "FLT")
df = loader.get_data(prefixed=True)
```

---

#### 📌 Hinweise

- Die Klasse geht davon aus, dass die FLT-Datei strukturierte Informationen enthält, die sich durch Präfixe (z. B. `plan_nr`) extrahieren lassen
- Die AKS-Nummer ist für die spätere Verknüpfung mit CAD-, NPA- oder HM-Daten geeignet
- Die vorbereitenden Mapper-Funktionen sorgen für eine normierte Darstellung
