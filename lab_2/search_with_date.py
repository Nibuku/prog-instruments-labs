import datetime
import os
import re
from threading import Thread


def day(this_day: str) -> datetime:
    """
    Converts a date string in the format "YYYY-MM-DD" to a datetime.date object.
    parametrs:
    this_day: string in the format "YYYY-MM-DD"
    return: datetime.date object
    """
    year = re.search(r"\d{4}", this_day)
    day = re.search(r"\b\d{2}", this_day)
    month = re.search(r"\-\d{2}\-", this_day)
    month = month[0].replace("-", "")
    return datetime.date(int(year[0]), int(month), int(day[0]))


def search(file: Thread, date: datetime) -> str:
    """
    Searches for a specific date in the file.
    parametrs:
    file: A file-like object or Thread containing the file to be searched.
    date: The date to search for in the file.
    return: line containing the date if found, otherwise "None".
    """
    for row in file:
        new_date = re.search(r"\d{2}\-\d{2}\-\d{4}", row)
        year = re.search(r"\d{4}", new_date[0])
        day = re.search(r"\b\d{2}", new_date[0])
        month = re.search(r"\-\d{2}\-", new_date[0])
        month = month[0].replace("-", "")
        if date == datetime.date(int(year[0]), int(month), int(day[0])):
            return str(row)
    return "None"


def search_in_all(date: datetime) -> None:
    """
    Searches for a specific date in the file "dataset.csv". Prints 'None' if the date is not found.
    parametrs:
    date: The date to search.
    """
    flag = 0
    file = open("dataset.csv", "r")
    flag = search(file, date)
    file.close
    if flag == 1:
        print(None)


def search_in_year(date: datetime) -> None:
    """
    Searches for the date in all files in the directory by year.
    Returns a string with the date, if found, otherwise "None".
    parametrs:
    data: The date to search.
    return:
    flag: string with result.
    """
    flag = ""
    for row in os.listdir("2"):
        file = open(os.path.join("2", row), "r")
        flag = search(file, date)
        file.close
        if flag != "None":
            return flag
    return flag


def search_in_week(date: datetime) -> None:
    """
    Searches for the date in all files in the directory by week.
    Returns a string with the date, if found, otherwise "None".
    parametrs:
    data: date to search.
    return:
    flag: string with result.
    """
    flag = ""
    for row in os.listdir("3"):
        file = open(os.path.join("3", row), "r")
        flag = search(file, date)
        file.close
        if flag != "":
            return flag
    if flag == "":
        return flag


def date_in_str(str: str) -> None:
    """
    Converts a date string in the "YYYYMMDD" format to a datetime.date object.
    parametrs:
    date_str: string representing the date in the format "YYYYMMDD".
    return: datetime.date object.
    """
    str = int(str)
    day = str % 100
    str = int(str / 100)
    month = str % 100
    str = int(str / 100)
    year = str
    return datetime.date(year, month, day)


def search_in_week_fast(date: datetime) -> str:
    """
    Searches for the date in the files, 
    checking whether the date falls within the specified range
    parametrs:
    date: The date to search for.
    return: line containing the date if found, otherwise "None".
    """
    for row in os.listdir("3"):
        first_date = re.search(r"\d{8}", row)
        last_date = re.search(r"_\d{8}", row)
        last_date = int(last_date[0].replace("_", ""))
        first_date = date_in_str(first_date[0])
        last_date = date_in_str(last_date)
        if date >= first_date and date <= last_date:
            file = open(os.path.join("3", row), "r")
            return search(file, date)
    return "None"


def search_in_data_and_date(date: datetime) -> str:
    """
    Searches for a specific date and retrieves corresponding data.
    parametrs:
    date: date to search for.
    return: line containing the date if found, otherwise "None".
    """
    result = ""
    count = 0
    flag = 0
    file_date = open(os.path.join("1", "file_with_date.csv"), "r")
    for row in file_date:
        count += 1
        new_date = re.search(r"\d{2}\-\d{2}\-\d{4}", row)
        year = re.search(r"\d{4}", new_date[0])
        day = re.search(r"\b\d{2}", new_date[0])
        month = re.search(r"\-\d{2}\-", new_date[0])
        month = month[0].replace("-", "")
        if date == datetime.date(int(year[0]), int(month), int(day[0])):
            flag = 1
            break
    file_date.close
    if flag == 1:
        file_data = open(os.path.join("1", "file_with_data.csv"), "r")
        for row in file_data:
            count -= 1
            if count == 0:
                result = str(row)
                file_data.close
                return result
        file_data.close
    result = "None"
    return result


def next(count: int) -> int:
    """
    Prints a string at the specified index and returns the updated index.
    parametrs:
    count: index of the line to print
    return: updated index
    """
    file = open("dataset.csv", "r")
    data = []
    for row in file:
        data.append(row)
    print(data[count])
    file.close
    count += 1
    return count
