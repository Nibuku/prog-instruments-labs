import sys

from loguru import logger
import requests
from bs4 import BeautifulSoup as bs

HEADERS = {
    "Accept": "*/*",
    "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
}
URL = "https://www.gismeteo.ru/diary/4618/"
LAST_YEAR = 2022
LAST_MONTH = 10
DATABASE = "dataset.csv"

log_format = "<green>{time:YYYY-MM-DD}</green> | " + "<level>{message}</level>"
logger.add(sys.stdout, format=log_format, level="INFO")


def get_html(url: str) -> requests.Response:
    """
    Sends an HTTP GET request to the specified URL.
    parametrs:
    url: URL to send the request to.
    return:
    req: requests.Response containing the server's response to the HTTP request.
    """
    try:
        req = requests.get(url, headers=HEADERS)
        logger.info(f"the request has been completed")
        return req
    except Exception as ex:
        logger.error(f"The request could not be completed: {ex.message}\n{ex.args}\n")


def clean_content(parameters: list) -> list:
    """
    Filters out specific elements from a list based on their position.
    parametrs:
    parameters: list of items to be filtered.
    return:
    new_weather: new filtered list
    """
    new_weather = []
    count = 0
    for number in parameters:
        if not count == 3 and not count == 4 and not count == 8 and not count == 9:
            new_weather.append(number)
        count += 1
        if count == 11:
            count = 0

    return new_weather


def get_content(html: str) -> list:
    """
    Parses the HTML content from <td> elements with a specific class.
    parametrs:
    html: string with HTML.
    return:
    all_number: list of text from <td> elements that contain the class 'first'.
    """
    soup = bs(html, "html.parser")
    all_number = []
    try:
        for item in soup.find_all("td"):
            if item.find('<td class="first">') != -1:
                all_number.append(item.get_text())
    except Exception as ex:
        logger.error(f"Error while parsing HTML content:{ex.message}\n{ex.args}\n")
    all_number = clean_content(all_number)
    return all_number


def fetch_weather_data() -> None:
    """Fetches weather data and saves it to a CSV file."""
    first_year = 2008
    first_month = 1
    try:
        with open(DATABASE, "w+") as out_file:
            out_file.write(
                "Number,"
                + "Day temperature,"
                + "Day pressure,"
                + "Day wind,"
                + "Night temperature,"
                + "Night pressure,"
                + "Night wind"
                + "\n"
            )
    except Exception as ex:
        logger.error(
            f"Work with the file was not completed successfully:{ex.message}\n{ex.args}\n"
        )

    while first_year <= LAST_YEAR:
        while first_month <= 12:
            if first_month == LAST_MONTH and first_year == LAST_YEAR:
                break
            full_url = URL + str(first_year) + "/" + str(first_month) + "/"
            html = get_html(full_url)
            main_list = get_content(html.text)
            index = 0
            while index < len(main_list):
                month = ""
                day = ""
                if int(main_list[index]) < 10:
                    day = "0" + main_list[index]
                else:
                    day = main_list[index]
                if first_month < 10:
                    month = "0" + str(first_month)
                else:
                    month = str(first_month)
                try:
                    out_file.write(str(first_year) + "-" + month + "-" + day + ",")
                    out_file.write(
                        main_list[index + 1]
                        + ","
                        + main_list[index + 2]
                        + ","
                        + main_list[index + 3]
                        + ","
                        + main_list[index + 4]
                        + ","
                        + main_list[index + 5]
                        + ","
                        + main_list[index + 6]
                        + "\n"
                    )
                    index += 7
                except Exception as ex:
                    logger.error(
                        f"Data could not be written to a file:{ex.message}\n{ex.args}\n"
                    )
            first_month += 1
        first_year += 1
        first_month = 1
