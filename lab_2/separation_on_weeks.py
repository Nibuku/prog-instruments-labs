import datetime
import os
import re
from datetime import timedelta
from typing import List


def day(this_day:str) -> datetime:
    year = re.search(r"\d{4}", this_day)
    day = re.search(r"\b\d{2}", this_day)
    month = re.search(r"\-\d{2}\-", this_day)
    month = month[0].replace("-", "")
    return datetime.date(int(year[0]), int(month), int(day[0]))


def chouse_day(data:List) -> datetime:
    new_date = re.search(r"\d{2}\-\d{2}\-\d{4}", data[0])
    new_date = day(new_date[0])
    return new_date + timedelta(7)


def create_file(start:str, end:str, data:List) -> None:
    end = end.replace("-", "")
    end = end.replace("\\", "")
    start = start.replace("\\", "")
    start = start.replace("-", "")
    name_of_file = os.path.join("3", start + "_" + end + ".csv")
    out_file = open(name_of_file, "w+")
    for param in data:
        out_file.write(param)
    out_file.close


def create(data: List) -> None:
    start = re.search(r"\d{2}\-\d{2}\-\d{4}", data[0])
    end = chouse_day(start)
    start = day(start[0])
    create_file(str(start), str(end), data)


def separation(data:List, last_day:datetime) -> None:
    new_data = []
    for row in data:
        new_date = re.search(r"\d{2}\-\d{2}\-\d{4}", row)
        new_date = day(new_date[0])
        if new_date < last_day:
            new_data.append(row)
        else:
            return new_data


def create_for_first(data: List) -> None:
    new_date = re.search(r"\d{2}\-\d{2}\-\d{4}", data[0])
    new_date = day(new_date[0])
    #  print(new_date+timedelta(4))
    return new_date + timedelta(4)


def clean_data(data:List, last_day: datetime) -> None:
    date = re.search(r"\d{2}\-\d{2}\-\d{4}", data[0])
    date = day(date[0])
    while date < last_day and len(data) > 7:
        data.pop(0)
        date = re.search(r"\d{2}\-\d{2}\-\d{4}", data[0])
        date = day(date[0])


def main():
    data = []
    our_file = open("dataset.csv", "r")
    for param in our_file:
        data.append(param)
    last_day = create_for_first(data)
    while len(data) > 7:
        new_data = separation(data, last_day)
        create(new_data)
        clean_data(data, last_day)
        last_day = chouse_day(data)
    first = day(data[0])
    last = day(data[len(data) - 1])
    create_file(str(first), str(last), data)


if __name__ == "__main__":
    main()
