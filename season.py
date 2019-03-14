from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup
import time


def season_scrape(url):
    """
    Get the URL for every match in a season.
    :param url: Soccerway URL for the season.
    :return: List of match URLs.
    """
    driver = webdriver.Chrome()
    driver.fullscreen_window()
    driver.get(url)

    # Click privacy policy if present.
    try:
        driver.find_element_by_class_name('qc-cmp-button').click()
    except NoSuchElementException:
        pass

    # Organize matches by game week
    element = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.ID, 'page_competition_1_block_competition_matches_summary_5_1_2'))
    )
    element.click()

    time.sleep(0.5)
    previous_clicks = num_previous_clicks(innerhtml_soup(driver))

    # Create a list containing match URLs for the final game week before clicking 'previous'
    url_list = get_urls(innerhtml_soup(driver))
    for i in range(previous_clicks):
        driver.find_element_by_class_name('previous').click()
        time.sleep(1)
        url_list += get_urls(innerhtml_soup(driver))

    driver.quit()
    print('=' * 100 + '\n{} matches found'.format(len(set(url_list))))

    return url_list


def num_previous_clicks(soup):
    """
    Work out how many times the 'Previous' button should be clicked.
    :param soup:
    :return:
    """
    number_weeks = soup.find(id='page_competition_1_block_competition_matches_summary_5_page_dropdown')
    last_week = number_weeks.contents[-1]
    previous_clicks = int(last_week.text) - 1

    return previous_clicks


def get_urls(soup):
    """
    Extract URL for each match in that game week.
    :param soup:
    :return: List of match URLs.
    """
    urls = []
    for info in soup.findAll('td', class_='info-button button'):
        for link in info.find_all('a', href=True):
            urls.append('https://us.soccerway.com' + link.get('href'))
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
