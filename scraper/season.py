from time import sleep
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


def get_urls_season(url_path):
    """
    Get the URL for every match in a season.
    :param url_path: Soccerway URL path for the season
    :return: List of match URLs
    """
    driver = webdriver.Chrome()
    driver.fullscreen_window()
    driver.get("https://us.soccerway.com" + url_path)
    click_privacy_policy(driver)

    url_list = cycle_through_game_weeks(driver)
    url_list.reverse()

    driver.quit()

    print("=" * 100)
    print(f"{len(set(url_list))} matches found")

    if input("Continue? (y/n): ") != "y":
        exit()

    return url_list


def click_privacy_policy(driver):
    try:
        driver.find_element_by_class_name("qc-cmp-button").click()
    except NoSuchElementException:
        pass


def cycle_through_game_weeks(driver):
    season_urls = get_fixture_urls(innerhtml_soup(driver))

    while is_previous_button_enabled(driver):
        click_previous_button(driver)
        sleep(2)

        urls = get_fixture_urls(innerhtml_soup(driver))

        # Arrange in chronological order
        urls.reverse()
        season_urls += urls

    return season_urls


def is_previous_button_enabled(driver):
    return driver.find_element_by_id(
        "page_competition_1_block_competition_matches_summary_5_previous"
    ).get_attribute("class") != "previous disabled"


def click_previous_button(driver):
    driver.find_element_by_id(
        "page_competition_1_block_competition_matches_summary_5_previous"
    ).click()


def get_fixture_urls(soup):
    """
    Extract URL for each match in that game week.
    :param soup:
    :return: List of match URLs
    """
    urls = []
    for elem in soup.select(".info-button.button > a"):
        urls.append(urlparse(elem.get("href")).path)
    return urls


def innerhtml_soup(driver):
    """
    Get soup from innerHTML.
    :param driver:
    :return:
    """
    html = driver.find_element_by_tag_name("html").get_attribute("innerHTML")
    soup = BeautifulSoup(html, "html.parser")
    return soup
