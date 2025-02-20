"""
Coding Utilities
Author: Michael Kohlegger
Date: Jan. 2025
"""

from pandas import read_excel, concat
from xlrd import open_workbook
import openpyxl as xl


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
    "08":  "08",
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
    """Mapper function for pandas.map() that deals with floor values.

    :param level: Input value of level.
    :type level: str
    """
    if level is None:
        return None
    if not isinstance(level, str):
        raise TypeError(f"level must be string but was {type(level)}.")
    level = level.replace(" ", "")
    if level in LEVEL_DICTIONARY.keys():
        return LEVEL_DICTIONARY[level]
    return "##"


def door_mapper(door):
    """Mapper function for pandas.map() that deals with door values.

    :param door: Input value of door.
    :type door: str
    """
    if door is None:
        return None
    if not isinstance(door, str):
        raise TypeError(f"door must be string but was {type(door)}.")
    return f"{door:>02}"


def room_mapper(room):
    """Mapper function for pandas.map() that deals with room values.

    :param door: Input value of room.
    :type door: str
    """
    if room is None:
        return None
    if not isinstance(room, str):
        raise TypeError(f"room must be string but was {type(room)}.")
    return f"{room:>04}"


def clean_data(df):
    """Function that cleans columns of a pandas.DataFrame.

    :param df: DataFrame with values.
    :type door: pandas.DataFrame
    """

    d = df.dropna(axis=1, how="all")
    new_columns = []
    replace_chars = ",.;:!§$%&/)=?+*#'}]"
    for col in d.columns:
        col = col.lower()
        for char in replace_chars:
            col = col.replace(char, "")
        col = col.replace("ü", "ue")
        col = col.replace("ä", "ae")
        col = col.replace("ö", "oe")
        col = col.replace("ß", "ss")
        col = col.replace(" ", "_")
        col = col.replace("-", "_")
        col = col.replace("(", "_")
        col = col.replace("[", "_")
        col = col.replace("{", "_")
        new_columns.append(col)
    d.columns = new_columns
    return d


def object_mapper(x):
    """Mapper function for pandas.map() that deals with object values.

    :param x: Input value of object.
    :type x: str
    """
    if x is None:
        return None
    return x.split("_")[0]


def columns_expander(columns, delta, prefix="dummy_"):
    """Expands a column list with dummy columns.

    :param  columns: Base columns list that should be expanded.
    :type columns: list
    :param delta: Number of additional columns that should be added.
    :type delta: int
    :param prefix: Prefix that should be added to column number.
    :type prefix: str
    :return: New list of columns
    :rtype: list
    """

    assert isinstance(prefix, str), f"prefix must be str but was {type(prefix)}."
    assert isinstance(delta, int), f"delta must be int but was {type(delta)}."
    assert isinstance(columns, list), f"cols must be a list object but was {type(columns)}."
    return columns + [prefix+str(i) for i in range(1, delta+1)]


def read_excel_all_sheets(excel_file, is_flt=False, *args, **kwargs):
    """Loads an Excelfile with all included worksheets into one dataframe.

    :param excel_file: Name of the Excel file
    :return: DataFrame with all Data
    :rtype: pandas.DataFrame
    """

    if excel_file.endswith(".xlsx"):
        wb = xl.load_workbook(excel_file)
        sheet_names = wb.sheetnames
    else:
        wb = open_workbook(excel_file, on_demand=True)
        sheet_names = wb.sheet_names()

    if is_flt:
        sheet_names = sheet_names[1:]

    if len(sheet_names) > 1:
        base = read_excel(excel_file, sheet_name=sheet_names[0], *args, **kwargs)

        for sheet_name in sheet_names[1:]:
            df = read_excel(excel_file, sheet_name=sheet_name, *args, **kwargs)
            base = concat([base, df], ignore_index=True)
    else:
        base = read_excel(excel_file, *args, **kwargs)

    return base
