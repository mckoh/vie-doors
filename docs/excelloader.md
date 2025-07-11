### 📘 Klasse: `ExcelLoader`

#### 🔍 Zweck
Die Klasse `ExcelLoader` lädt Excel-Dateien samt aller enthaltenen Sheets in den Arbeitsspeicher und bereitet sie strukturiert auf. Dabei werden leere Zeilen entfernt, Spalten optional bereinigt und bei Bedarf mit einem Titel präfixiert. Die Daten werden als `pandas.DataFrame` verwaltet.

---

#### 🧩 Attribute

| Attribut   | Typ     | Beschreibung                                                        |
|------------|----------|----------------------------------------------------------------------|
| `file`     | `str`    | Dateiname inkl. Dateiendung                                          |
| `title`    | `str`    | Titelpräfix zur Kennzeichnung von Spalten                            |
| `data`     | `DataFrame` | Geladene Daten aus der Excel-Datei                                 |

---

#### 🔧 Konstruktor

```python
ExcelLoader(file, title, *args, **kwargs)
```

Initialisiert das Objekt und lädt die Daten aus der Excel-Datei. Zusätzliche Parameter werden direkt an `read_excel_all_sheets()` weitergegeben, was eine hohe Flexibilität erlaubt.

---

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

---

#### 📎 Beispiel

```python
loader = ExcelLoader("tuerdaten.xlsx", "HM")
df = loader.get_data(prefixed=True)
cols = loader.get_columns()
```

---

#### 📌 Hinweise

- Die Klasse nimmt an, dass die Datei mehrere Sheets enthalten kann und behandelt sie entsprechend
- `read_excel_all_sheets()` muss sicherstellen, dass alle relevanten Sheets korrekt konsolidiert werden
- Die `"merge"`-Spalte dient als Schlüssel für spätere Datenverknüpfungen
- Es wird vorausgesetzt, dass `integration_aks` eine eindeutige Referenzspalte ist
