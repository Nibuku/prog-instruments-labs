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
        logger.info(
            "Request to URL '{}' completed with status code: {}", url, req.status_code
        )
        return req
    except Exception as ex:
        logger.error(
            "The request could not be completedto URL '{}': {}\nArgs: {}",
            url,
            ex,
            ex.args,
        )


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
        logger.error(
            "Error while parsing HTML content: {}\nArguments: {}",
            ex,
            ex.args,
        )
    all_number = clean_content(all_number)
    logger.info("Parsed {} elements with criteria", len(all_number))
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
            logger.info("File '{}' opened and headers written successfully.", DATABASE)

            while first_year <= LAST_YEAR:
                while first_month <= 12:
                    if first_month == LAST_MONTH and first_year == LAST_YEAR:
                        break
                    full_url = f"{URL}{first_year}/{first_month}/"
                    logger.info("Current URL: {}", full_url)

                    try:
                        html = get_html(full_url)
                        main_list = get_content(html.text)
                        if not main_list:
                            first_month += 1
                            continue
                        logger.info(
                            "Successfully fetched data for year-month: {}-{}.",
                            first_year,
                            first_month,
                        )
                    except Exception as ex:
                        logger.error(
                            "Error fetching data for year-month: {}-{}. Exception: {exception}, Args: {args}",
                            first_year,
                            first_month,
                            ex,
                            ex.args,
                        )
                        first_month += 1
                        continue
                    index = 0
                    while index < len(main_list):
                        day = f"{int(main_list[index]):02d}"
                        month = f"{first_month:02d}"
                        try:
                            out_file.write(
                                f"{first_year}-{month}-{day},"
                                + ",".join(main_list[index + 1 : index + 7])
                                + "\n"
                            )
                            index += 7
                        except Exception as ex:
                            logger.error(
                                "Failed to write data to file for date: {}-{}-{}. Exception: {exception}, Args: {args}",
                                first_year,
                                first_month,
                                day,
                                ex,
                                ex.args,
                            )
                            break
                    first_month += 1
                first_year += 1
                first_month = 1
                logger.info("Weather data fetching and saving completed successfully.")
    except Exception as ex:
        logger.error(
            "Error with opening or working with file '{}'. Exception: {exception}, Args: {args}",
            DATABASE,
            ex,
            ex.args,
        )
