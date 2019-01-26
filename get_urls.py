import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


def get_entire_season(url):

    urls = []

    chrome_options = Options()
    chrome_options.add_argument("--kiosk")

    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(url)

    time.sleep(1)

    if driver.find_element_by_class_name('qc-cmp-button'):
        privacy = driver.find_element_by_class_name('qc-cmp-button')
        privacy.click()

    time.sleep(1)

    week = driver.find_element_by_id('page_competition_1_block_competition_matches_summary_5_1_2')
    week.click()

    time.sleep(2)

    html = driver.find_element_by_tag_name('html').get_attribute('innerHTML')
    game_week_soup = BeautifulSoup(html, 'html.parser')

    previous_clicks = 0

    for week in game_week_soup.findAll(id='page_competition_1_block_competition_matches_summary_5_page_dropdown'):
        number_weeks = (week.contents[-1])
        previous_clicks = int(number_weeks.contents[0]) - 1

    for info in game_week_soup.findAll('td', class_='info-button button'):
        for link in info.find_all('a', href=True):
            match_url = 'https://us.soccerway.com' + link.get('href')
            urls.append(match_url)

    for i in range(previous_clicks):
        previous_button = driver.find_element_by_class_name('previous')
        previous_button.click()
        time.sleep(1)
        html = driver.find_element_by_tag_name('html').get_attribute('innerHTML')
        game_week_soup = BeautifulSoup(html, 'html.parser')
        for info in game_week_soup.findAll('td', class_='info-button button'):
            for link in info.find_all('a', href=True):
                match_url = 'https://us.soccerway.com' + link.get('href')
                urls.append(match_url)

    print('{} matches found\n'.format(len(urls)) + '=' * 70)
    return urls
