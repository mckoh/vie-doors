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

---

#### 🔧 Konstruktor
```python
FileMerger(files, how="left", column="merge")
```

Initialisiert das Objekt und führt automatisch den Merge der übergebenen Dateien aus. Es müssen mindestens zwei DataFrames übergeben werden.

---

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

---

#### 🔎 Hinweise zur Verwendung
- **Mindestanzahl an Dateien**: 2
- **Spalte zum Mergen** muss in allen DataFrames vorhanden sein.
- Die Methoden `find_non_matching_rows` und `find_duplicates` sind **nicht kompatibel mit mehr als zwei Dateien**.
- Die externe Hilfsfunktion `eliminate_duplicates` wird zur datengetriebenen Duplikaterkennung genutzt.

---

#### 📌 Beispielhafte Anwendung
```python
merger = FileMerger([df1, df2], how="left", column="merge")
merged_data = merger.get_data_merge(eliminate=True)
merged_data.to_excel("output.xlsx")
```
