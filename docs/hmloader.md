### 🏗️ Klasse: `HMLoader`

#### 🔍 Zweck
`HMLoader` ist eine Spezialisierung der `ExcelLoader`-Klasse zur Verarbeitung von Excel-Dateien aus dem HM-Datenbereich. Sie homogenisiert die Spaltenstruktur und bereitet sowohl eine neue als auch eine alte AKS-Nummer zur eindeutigen Türidentifikation auf.

---

#### 🧬 Vererbung
Erbt von: [`ExcelLoader`](#)

---

#### 🧩 Attribute

| Attribut        | Typ         | Beschreibung                                                           |
|-----------------|-------------|---------------------------------------------------------------------------|
| `file`          | `str`       | Dateiname der zu ladenden HM-Excel-Datei                                 |
| `title`         | `str`       | Präfix zur Kennzeichnung der Spalten                                     |
| `data`          | `DataFrame` | Geladene und vorbereitete Daten mit neuen & alten Türnummern             |

---

#### 🔧 Konstruktor

```python
HMLoader(file, title, *args, **kwargs)
```

Lädt die HM-Datei und bereitet alle relevanten Spalten für die Konstruktion von Integrationskennungen (`integration_aks`) und Alt-Nummern auf.

---

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

---

#### 📎 Beispiel

```python
loader = HMLoader("hardware_daten.xlsx", "HM")
df = loader.get_data(prefixed=True)
```

---

#### 📌 Hinweise

- Die AKS-Nummer (neu & alt) erlaubt präzise Mappings gegen andere Datenquellen wie CAD, NPA oder BST
- Die Verarbeitung nutzt Kombinationen von `split()` und Mapper-Funktionen für normierte Darstellung
- Die Hilfsspalte `helper_1` wird nach der Konstruktion der AKS-Nummer wieder entfernt
