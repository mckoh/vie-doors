### 🗃️ Klasse: `BSTLoader`

#### 🔍 Zweck
`BSTLoader` ist eine spezialisierte Erweiterung von `ExcelLoader` zur Verarbeitung von BST-Excel-Dateien. Sie sorgt für die Harmonisierung von Spaltennamen und bereitet die Daten so vor, dass eine eindeutige Integrationsnummer (`integration_aks`) für spätere Datenverknüpfungen erzeugt wird.

#### 🧬 Vererbung
Erbt von: [`ExcelLoader`](#)

---

#### 🧩 Attribute

| Attribut   | Typ           | Beschreibung                                                 |
|------------|---------------|---------------------------------------------------------------|
| `file`     | `str`         | Dateiname inkl. Dateiendung                                   |
| `title`    | `str`         | Präfix für Spaltennamen                                       |
| `data`     | `DataFrame`   | Geladene und vorbereitete BST-Daten                          |

---

#### 🔧 Konstruktor

```python
BSTLoader(file, title, *args, **kwargs)
```

Initialisiert das Objekt und lädt die BST-Daten mithilfe des Elternkonstruktors. Führt anschließend eine Harmonisierung der Spalten durch und bereitet die Daten zur Integration vor.

---

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

---

#### 📎 Beispiel

```python
loader = BSTLoader("bst_tueren.xlsx", "BST")
df = loader.get_data(prefixed=True)
```

---

#### 🧠 Hinweise

- Die auskommentierten Codezeilen deuten auf experimentelle bzw. alternative Ansätze zur Erzeugung von AKS hin (z. B. Zerlegung von Türnummern)
- `room_mapper` und `modul`-Verarbeitung sind aktuell deaktiviert, können bei Bedarf aber wieder eingebunden werden
- Die Klasse setzt voraus, dass die Spalten `name`, `ebene` und `nummer` vorhanden sind
