import re
import requests
from bs4 import BeautifulSoup as bs

HEADERS = {
    "Accept": "*/*",
    "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"

}
def get_html(url):
    req = requests.get(url, headers=HEADERS)
    return req


def clean_content(parameters):
    new_weather = []
    count = 0
    for number in parameters:
        if not count == 3 and not count == 4 and not count == 8 and not count == 9:
            new_weather.append(number)
        count += 1
        if count == 11:
            count = 0

    return new_weather


def get_content(html):
    soup = bs(html, 'html.parser')
    all_number = []

    for item in soup.find_all("td"):
        if item.find('<td class="first">') != -1:
            all_number.append(item.get_text())

    all_number = clean_content(all_number) 
    return all_number

out_file = open("dataset.csv", 'w+')
first_year = 2008
first_month = 1
out_file.write("Number,"+"Day temperature,"+ "Day pressure,"+"Day wind,"+"Night temperature,"+ "Night pressure,"+ "Night wind"+'\n')
while first_year<=2022:
    while first_month<=12:
        if first_month == 10 and first_year == 2022:
            break
        URL = 'https://www.gismeteo.ru/diary/4618/'
        full_url = URL +str(first_year)+ "/" + str(first_month)+ "/"
        html = get_html(full_url)
        main_list = get_content(html.text)
        index = 0
        while index<len(main_list):
            month = ""
            day = ""
            if int(main_list[index])<10:
                day = "0"+main_list[index]
            else: day = main_list[index]
            if first_month<10:
                month = "0"+str(first_month)
            else: month = str(first_month)
            out_file.write(str(first_year)+'-'+month+'-'+day +',')
            out_file.write(main_list[index+1]+","+ main_list[index+2]+","+ main_list[index+3]+","+ main_list[index+4]+","+main_list[index+5]+","+main_list[index+6]+'\n')
            index+=7
        first_month+=1
    first_year+=1
    first_month = 1
out_file.close()
