### 🛠️ Klasse: `CADLoader`

#### 🔍 Zweck
Die Klasse `CADLoader` lädt CAD-bezogene Excel-Dateien, homogenisiert die Spaltennamen und bereitet eine eindeutige Integrationskennung (`integration_aks`) vor. Diese Kennung dient der späteren Datenverknüpfung.

#### 🧬 Vererbung
Erbt von: [`ExcelLoader`](#)

---

#### 🧩 Attribute

| Attribut        | Typ       | Beschreibung                                                          |
|-----------------|-----------|------------------------------------------------------------------------|
| `file`          | `str`     | Dateiname inkl. Endung                                                 |
| `title`         | `str`     | Spaltenpräfix für die Datenquelle                                     |
| `data`          | `DataFrame` | Geladene und vorbereitete CAD-Daten                                  |

---

#### 🔧 Konstruktor

```python
CADLoader(file, title, *args, **kwargs)
```

Initialisiert das Objekt und lädt die CAD-Datei. Dabei werden die Spaltennamen durch die vordefinierte Liste `cad_columns` ersetzt oder ergänzt (bei abweichender Anzahl). Anschließend erfolgt die Verarbeitung einzelner Spalten zur Generierung der `integration_aks`.

---

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

---

#### 📎 Beispiel

```python
loader = CADLoader("cad_tueren.xlsx", "CAD")
df = loader.get_data(prefixed=True)
```

---

#### 📌 Hinweise
- Die Mapper-Funktionen dienen zur Vereinheitlichung von CAD-internen Codes
- Die generierte `integration_aks` sollte in anderen Datenquellen ebenfalls vorkommen
- Die Klasse setzt auf saubere Spaltenstruktur – `cad_columns` muss sorgfältig gepflegt sein
