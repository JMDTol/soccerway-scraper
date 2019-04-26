from bs4 import BeautifulSoup
from urllib.parse import urlparse
from time import sleep

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
    driver.get('https://us.soccerway.com' + url_path)

    # Click privacy policy if present.
    try:
        driver.find_element_by_class_name('qc-cmp-button').click()
    except NoSuchElementException:
        pass

    # Get URLs from current page first
    url_list = get_urls(innerhtml_soup(driver))

    prev_id = 'page_competition_1_block_competition_matches_summary_5_previous'
    while (driver.find_element_by_id(prev_id).get_attribute('class') !=
           'previous disabled'):
        driver.find_element_by_id(prev_id).click()
        sleep(2)
        urls = get_urls(innerhtml_soup(driver))
        # Arrange in chronological order
        urls.reverse()
        url_list += urls

    driver.quit()
    url_list.reverse()

    print('=' * 100)
    print(f'{len(set(url_list))} matches found')

    # Exit if incorrect number of URLs found
    if input('Continue? (y/n): ') != 'y':
        exit()

    return url_list


def get_urls(soup):
    """
    Extract URL for each match in that game week.
    :param soup:
    :return: List of match URLs
    """
    urls = []
    for elem in soup.select('.info-button.button > a'):
        url = elem.get('href')
        urls.append(urlparse(url).path)
    return urls


def innerhtml_soup(driver):
    """
    Get soup from innerHTML.
    :param driver:
    :return:
    """
    html = driver.find_element_by_tag_name('html').get_attribute('innerHTML')
    soup = BeautifulSoup(html, 'html.parser')
    return soup
