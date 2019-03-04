from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup
import time


def get_urls(url):
    """
    Get the URL for every match in a season.
    :param url: Soccerway URL for match.
    :return: List of URLs.
    """
    driver = webdriver.Firefox()
    driver.fullscreen_window()
    driver.get(url)

    # Click privacy policy if present.
    try:
        driver.find_element_by_class_name('qc-cmp-button').click()
    except NoSuchElementException:
        pass

    element = WebDriverWait(driver, 5).until(
        ec.presence_of_element_located((By.ID, 'page_competition_1_block_competition_matches_summary_5_1_2'))
    )
    element.click()

    time.sleep(0.5)

    html = driver.find_element_by_tag_name('html').get_attribute('innerHTML')
    game_week_soup = BeautifulSoup(html, 'html.parser')

    # Check the number of game weeks in the season.  Previous button is then clicked (number of game weeks - 1) times.
    previous_clicks = 0
    for week in game_week_soup.findAll(id='page_competition_1_block_competition_matches_summary_5_page_dropdown'):
        number_weeks = (week.contents[-1])
        previous_clicks = int(number_weeks.contents[0]) - 1

    url_list = []
    for info in game_week_soup.findAll('td', class_='info-button button'):
        for link in info.find_all('a', href=True):
            url_list.append('https://us.soccerway.com' + link.get('href'))

    for i in range(previous_clicks):
        driver.find_element_by_class_name('previous').click()
        time.sleep(1)
        html = driver.find_element_by_tag_name('html').get_attribute('innerHTML')
        game_week_soup = BeautifulSoup(html, 'html.parser')
        for info in game_week_soup.findAll('td', class_='info-button button'):
            for link in info.find_all('a', href=True):
                url_list.append('https://us.soccerway.com' + link.get('href'))

    driver.quit()

    print('=' * 100 + '\n{} matches found'.format(len(set(url_list))))

    return url_list
