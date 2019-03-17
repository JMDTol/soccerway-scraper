import time
import tkinter as tk
from tkinter import filedialog
from scraper import scrape_match
from write_to_spread import spread
from season import season_scrape


def input_urls():
    """
    Check whether the user wants to scrape an entire season or manually enter URLs for each match.
    :return: List of match URLs.
    """
    if input('Scrape entire season? (y/n): ') == 'y':
        season_url = input('Enter season URL: ')
        url_list = season_scrape(season_url)
        if input('Continue? (y/n): ') != 'y':
            exit()
    else:
        url_list = input("Enter match URLs (split multiple URLs with ','): ").split(',')

    return url_list


def scrape_urls(url_list, spreadsheet_path):
    """
    Scrape each URL pausing at intervals to prevent requests from being denied.
    :param url_list: List of match URLs.
    :param spreadsheet_path: Path to spreadsheet data is to be written to.
    :return:
    """
    pause = 0
    for url in url_list:
        if pause == 10:
            time.sleep(10)
            spread(scrape_match(url), spreadsheet_path)
            pause = 0
        else:
            time.sleep(2)
            spread(scrape_match(url), spreadsheet_path)
            pause += 1

    print('=' * 100 + f'\nComplete - {len(url_list)} matches added')


if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askopenfilename()
    try:
        matches_to_scrape = input_urls()
        scrape_urls(matches_to_scrape, path)
    except IndexError:
        print('=' * 50)
        print('Invalid URLs entered')
