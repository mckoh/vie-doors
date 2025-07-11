### 🗄️ Klasse: `FMLoader`

#### 🔍 Zweck
`FMLoader` ist eine minimalistische Klasse zum Laden vorverarbeiteter Filemaker-Daten aus einer Pickle-Datei (`fm.pkl`). Zusätzlich generiert sie einen Matching-Schlüssel (`npa_fm_match`) für die spätere Zuordnung zu NPA-Daten.

---

#### 🧩 Attribute

| Attribut      | Typ         | Beschreibung                                                       |
|---------------|-------------|---------------------------------------------------------------------|
| `data`        | `DataFrame` | Eingeladene Filemaker-Daten aus der Pickle-Datei                   |

---

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

---

#### 🛠️ Methoden

##### `get_data(prefixed=True) -> DataFrame`
- Gibt den gespeicherten DataFrame zurück
- Das Argument `prefixed` ist aktuell ohne funktionale Auswirkung (alle Spalten sind schon vorpräfixiert)

##### `get_columns() -> list`
- Gibt eine Liste der Spaltennamen im geladenen DataFrame zurück

---

#### 📎 Beispiel

```python
fm_loader = FMLoader()
fm_data = fm_loader.get_data()
cols = fm_loader.get_columns()
```

---

#### 📌 Hinweise

- Die Datei `fm.pkl` muss zuvor korrekt erzeugt und im Pfad `static/` abgelegt worden sein
- Die Methode `get_data()` bietet aktuell keine zusätzliche Datenbearbeitung an – dafür ist die Pickle-Datei bereits vorbereitet
- Der generierte Schlüssel `npa_fm_match` harmonisiert das Format für spätere Merge-Vorgänge mit NPA-Daten
