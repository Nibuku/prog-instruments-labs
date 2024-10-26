import os
import re

import pandas as pd

import checksum as check

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
    """
    Открывает объект DataFrame на основе исходного csv-файла
    :param path: путь до исходого csv-файла
    :return: данные в виде DataFrame
    """
    data = pd.read_csv(
        path,
        encoding="utf-16",
        sep=";",
    )
    return data


def check_row_valid(row: pd.Series) -> bool:
    """
    Проверяет на валидность одну строку DataFrame.
    Если все данные подходят соответствующим регулярным выражениям, возвращает True.
    Иначе False.
    :param row: строка DataFrame
    :return: результат проверки на валидность
    """
    for name_column, value in zip(PATTERNS.keys(), row):
        pattern = PATTERNS[name_column]
        if not re.search(pattern, str(value)):
            return False
    return True


def get_invalid_index(path: str) -> list:
    """
    Получает путь до исходного csv-файла с данными. Вызывает функцию
    open_csv() и создает объект DataFrame, после проверяет каждую его строку с помощью
    функции check_row_valid(). Если результат функции False, то записывает индекс невалидной строки в список.
    :param path: путь до исходного csv-файла
    :return invalid_index: список строк с невалидным индексом
    """
    rows = open_csv(path)
    invalid_index = list()
    for index, row in rows.iterrows():
        if not check_row_valid(row):
            invalid_index.append(index)
    return invalid_index


if __name__ == "__main__":
    list_index = get_invalid_index(
        os.path.join("prog-instruments-labs", "lab_3", "65.csv")
    )
    check.serialize_result(65, check.calculate_checksum(list_index))
