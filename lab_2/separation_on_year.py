import re
import os
from typing import List


def creade_file(start: int, end: int, data: List, folder: str) -> None:
    name_of_file = os.path.join(folder, str(start) + "_" + str(end) + ".csv")
    out_file = open(name_of_file, "w+")
    for param in data:
        out_file.write(param)
    out_file.close


def create(data: List, folder: str) -> None:
    start = re.search(r"\d.*\d{4}", data[0])
    start = start[0].replace("-", "")
    end = re.search(r"\d.*\d{4}", data[len(data) - 1])
    end = end[0].replace("-", "")
    creade_file(start, end, data, folder)


def separation(data: List, year: int):
    new_data = []
    for row in data:
        a = re.search(r"\d{4}", row)
        if a[0] == str(year):
            new_data.append(row)
    return new_data


def separetion_year(folder: str):
    data = []
    our_file = open("dataset.csv", "r")
    for param in our_file:
        data.append(param)
    year = 2008
    while year < 2023:
        new_data = separation(data, year)
        create(new_data, folder)
        # print(new_data)
        year += 1


if __name__ == "__main__":
    separetion_year()
