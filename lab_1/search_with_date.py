from datetime import date
import datetime
import re
import os
from threading import Thread
from typing import List


def day(this_day:str) -> datetime:
    year = re.search(r"\d{4}", this_day)
    day = re.search(r"\b\d{2}", this_day)
    month = re.search(r"\-\d{2}\-", this_day)
    month = month[0].replace("-", "")
    return datetime.date(int(year[0]), int(month), int(day[0]))

    
def search(file: Thread, date: datetime) -> str:
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
    flag = 0
    file = open("dataset.csv", "r")
    flag = search(file, date)
    file.close
    if flag == 1:
        print(None)


def search_in_year(date: datetime) -> None:
    flag = ''
    for row in os.listdir("2"):
        file = open(os.path.join("2", row), "r")
        flag = search(file, date)
        file.close
        if flag != "None":
            return flag
    return flag


def search_in_week(date: datetime) -> None:
    flag = ''
    for row in os.listdir("3"):
        file = open(os.path.join("3", row), "r")
        flag = search(file, date)
        file.close
        if flag != "":
            return flag
    if flag == "":
        return flag


def date_in_str(str: str) -> None:
    str = int(str)
    day = str % 100
    str = int(str / 100)
    month = str % 100
    str = int(str / 100)
    year = str
    return datetime.date(year, month, day)


def search_in_week_fast(date: datetime) -> str:
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


#def search_in_week(date: datetime) -> str:
 #   result = ""
  #  flag = 0
   # for row in os.listdir("3"):
    #    file = open(os.path.join("3", row), "r")
     #   flag = search(file, date)
      #  file.close
       # if flag == 0:
        #    break
    #if flag == 1:
     #   return "None"


def search_in_data_and_date(date: datetime) -> str:
    result = ''
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
    result = 'None'
    return result
    


def next(count: int) -> int:
    file = open("dataset.csv", "r")
    data = []
    for row in file:
        data.append(row)
    print(data[count])
    file.close
    count += 1
    return count

#date = datetime.date(2013,1,1)
##print(search_in_data_and_date(date))
#print(type(search_in_year(date)))