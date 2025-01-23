import pandas as pd
import re

# Hilfsfunktion zur Standardisierung der Werte
def standardize_value(value):
    if isinstance(value, str):
        value = value.strip().replace("O", "0").replace("EG", "0")
        value = re.sub(r'\s+', '', value)  # Entfernt überflüssige Leerzeichen
    return value

# Daten laden
npa_df = pd.read_excel("NPA_Tuer Aufnahme Obj420.xlsx")
sisando_bst_df = pd.read_excel("Sisando_BST_Obj420.xlsx")
sisando_flt_df = pd.read_excel("Sisando_FLT_Obj420.xlsx")
schrack_hm_df = pd.read_excel("Schrack_HM_Obj420.xls")
#filemaker_df = pd.read_excel("Tuerliste BFD an VAT20241016.xlsx")

for df in [npa_df, sisando_bst_df, sisando_flt_df, schrack_hm_df]:
    for col in df.columns:
        df[col] = df[col].apply(standardize_value)

# Combine relevant columns to create identifiers
# NPA data
npa_df['AKS_Plan'] = (
    npa_df['Objekt'].fillna('').astype(str) +
    npa_df['Ebene'].fillna('').astype(str) +
    npa_df['Bauteil'].fillna('').astype(str) +
    npa_df['AKS Plan'].fillna('').astype(str)
)
npa_df['AKS_real'] = (
    npa_df['Objekt'].fillna('').astype(str) +
    npa_df['Ebene'].fillna('').astype(str) +
    npa_df['Bauteil'].fillna('').astype(str) +
    npa_df['AKS real'].fillna('').astype(str)
)

# Schrack HM data
schrack_hm_df.rename(columns={
    'TÜRNR(AKS)': 'AKS_Plan',
    'TÜRNRALT': 'Alte Türnummer',
    'TÜRNR. BMA': 'Schlossernummer'
}, inplace=True)

# Sisando BST data
sisando_bst_df['AKS_Plan'] = (
    sisando_bst_df['Name'].fillna('').astype(str) +
    sisando_bst_df['Ebene'].fillna('').astype(str) +
    sisando_bst_df['Nummer'].fillna('').astype(str)
)

# Combine all datasets
all_data = pd.concat([npa_df, sisando_bst_df, sisando_flt_df, schrack_hm_df], ignore_index=True)

# Remove duplicates
unique_data = all_data.drop_duplicates(subset=['AKS_Plan', 'AKS_real', 'Schlossernummer', 'Alte Türnummer'])

# Identify discrepancies
discrepancies = all_data[
    ~all_data.duplicated(subset=['AKS_Plan', 'AKS_real', 'Schlossernummer', 'Alte Türnummer'], keep=False)
]

# Save results to CSV
unique_data.to_csv("Gesamtliste.csv", index=False, encoding='utf-8')
discrepancies.to_csv("Abweichungen.csv", index=False, encoding='utf-8')

#all_data.to_csv("AllData.csv", index=False, encoding='utf-8') #habe ich noch hinzugefügt und sollte eigentlich die Summe der obingen sein oder??

print("Data processing complete.")
print("Unique entries saved to 'Gesamtliste.csv'.")
#print("Discrepancies saved to 'Abweichungen.csv'.")