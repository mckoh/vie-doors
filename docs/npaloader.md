### 🏢 Klasse: `NPALoader`

#### 🔍 Zweck
Der `NPALoader` ist ein spezialisierter Datenimporter, der NPA-Excel-Dateien (z. B. aus der Türplanung) in Speicher lädt, homogenisiert und aufbereitet. Er extrahiert relevante Informationen für die eindeutige Türkennung (`integration_aks`) und bietet ein Matching-Schema zur Verbindung mit FM-Daten via `schlossernummer`.

#### 🧬 Vererbung
Erbt von: `ExcelLoader`

---

#### 🧩 Attribute

| Attribut         | Typ           | Beschreibung                                                              |
|------------------|---------------|---------------------------------------------------------------------------|
| `file`           | `str`         | Dateiname der NPA-Datei (inkl. Endung)                                    |
| `title`          | `str`         | Kürzel zur Präfixierung der Spalten (z. B. `"NPA"`)                        |
| `data`           | `DataFrame`   | Geladene und bereinigte Daten                                             |

---

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

---

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

---

#### 📎 Beispiel

```python
loader = NPALoader("npa_daten.xlsx", "NPA")
df = loader.get_data(prefixed=True)
```

---

#### 📌 Hinweise

- Die Spalte `integration_aks` erlaubt Verknüpfung mit CAD-, HM-, BST-, FLT-Daten
- Der Schlüssel `npa_fm_match` kann zur Zuordnung von Schließplänen (FM) verwendet werden
- Die Klasse entfernt Mehrfach-Header und verarbeitet flexible Spaltenanzahl
