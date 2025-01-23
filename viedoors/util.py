import pandas 


EG_LABEL = "00"
DA_LABEL = "DA"
ZG_PREFIX = "Z"
K_PREFIX = "K"

LEVEL_DICTIONARY = {
    
    # Cellar
    "K":   K_PREFIX+"1",
    "K1": K_PREFIX+"1",
    "-1":  K_PREFIX+"1",
    "-2":  K_PREFIX+"2",
    
    
    # Ground floor
    "0":   EG_LABEL,
    "00":  EG_LABEL,
    "EG":  EG_LABEL,

    # Upper floors
    "1":   "01",
    "01":  "01",
    "2":   "02",
    "02":  "02",
    "3":   "03",
    "03":  "03",
    "4":   "04",
    "04":  "04",
    "5":   "05",
    "05":  "05",
    "6":   "06",
    "06":  "06",
    "7":   "07",
    "07":  "07",
    "8":   "08",
    "8":  "81",
    "9":   "09",
    "09":  "09",
    "10":  "10",
    "11":  "11",
    "12":  "12",
    "13":  "13",
    "14":  "14",
    "15":  "15",
    "16":  "16",
    "17":  "17",
    "18":  "18",
    "19":  "19",
    "20":  "20",
    "21":  "21",
    "22":  "22",
    "23":  "23",
    "24":  "24",
    "25":  "25",
    "26":  "26",
    "27":  "27",
    "28":  "28",
    "29":  "29",
    "30":  "30",
    "1.OG":"01",
    "2.OG":"02",
    "o1":  "01",

    # Other floors
    "DG":  DA_LABEL,
    "Z1":  ZG_PREFIX+"1",
    "ZG1": ZG_PREFIX+"1",
    "ZG":  ZG_PREFIX+"1",
    "ZG2": ZG_PREFIX+"2",
    "DA":  DA_LABEL,
    "Da":  DA_LABEL,

    # Exceptions
    "": None
}

def level_mapper(level):
    if not isinstance(level, str):
        raise TypeError(f"level must be string but was {type(level)}.")
    level = level.replace(" ", "")
    if level in LEVEL_DICTIONARY.keys():
        return LEVEL_DICTIONARY[level]
    return "##"


def door_mapper(door):
    if not isinstance(door, str):
        raise TypeError(f"door must be string but was {type(door)}.")
    return f"{door:>02}"

def room_mapper(room):
    if not isinstance(room, str):
        raise TypeError(f"room must be string but was {type(room)}.")
    return f"{room:>04}"


def clean_data(df):
    
    d = df.dropna(axis=1, how="all")
    new_columns = []
    for col in d.columns:
        col = col.lower().replace(" ", "_").replace(".", " ").replace("ü", "ue")
        col = col.replace("ä", "ae").replace("ö", "oe").replace("ß", "ss")
        col = col.replace(":", "").replace("?", "").replace("!", "").replace("#", "")
        new_columns.append(col)
    d.columns = new_columns
    return d


def flt_object_mapper(x):
    return x.split("_")[0]