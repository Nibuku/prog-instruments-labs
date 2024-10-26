import csv
import re
import os
import pandas as pd

PATTERNS = {
    "email": "^\w+(\.\w+)*@\w+(\.\w+)+$",
    "http_status_message": "^\d{3}(\s\w+)+$",
    "snils": "^\d{11}$",
    "passport": "^(\d{2}\s){2}\d{6}$",
    "ip_v4": "^((25[0-5]|2[0-4]\d|1\d{2}|\d{1,2})\.){3}(25[0-5]|2[0-4]\d|1\d{2}|\d{1,2})$",
    "longitude": "^-?(180|1[0-7]\d|\d{1,2})(\.\d+)?$",
    "hex_color": "^#([a-f0-9]{6}|[a-f0-9]{3})$",
    "isbn": "^(\d{3}-)?\d-\d{5}-\d{3}-\d$",
    "locale_code": "^[a-z]{1,3}(-[a-z]+)?(-[a-z]{2})?$",
    "time": "^([01]\d|2[0-3]):([0-5]\d):([0-5]\d)\.(\d{1,6})$",
}


def open_csv(path: str) -> pd.DataFrame:
    data = pd.read_csv(path,
        encoding="utf-16",
        sep=";",
    )
    return data

def check_row_valid(row: pd.Series)-> bool:
    for name_column, value in zip(PATTERNS.keys(), row):
        pattern=PATTERNS[name_column]
        if not re.search(pattern, str(value)):
            return False
    return True

def get_invalid_index(path: str)->list:
    rows=open_csv(path)
    invalid_index=list()
    for index, row in rows.iterrows():
        if not check_row_valid(row):
            invalid_index.append(index)
    return invalid_index

if __name__ == "__main__":
    list_index=get_invalid_index(os.path.join("prog-instruments-labs", "lab_3", "65.csv"))
    
    
    