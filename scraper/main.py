import tkinter as tk
from time import sleep
from tkinter import filedialog
from urllib.parse import urlparse
from scraper import scrape_match
from write_to_spread import spread
from season import get_urls_season


def input_urls():
    """
    Check whether the user wants to scrape an entire season or manually enter
    URLs for each match.
    :return: List of match URLs
    """
    if input('Scrape entire season? (y/n): ') == 'y':
        season_url = input('Enter season URL: ')
        match_urls = get_urls_season(season_url)
        if input('Continue? (y/n): ') != 'y':
            exit()
    else:
        urls = input("Enter match URLs (split multiple URLs with ','): ")
        match_urls = [urlparse(url).path for url in urls.split(',')]

    return match_urls


def scrape_urls(url_list, spreadsheet_path):
    """
    Scrape each URL pausing at intervals to prevent requests from being denied.
    :param url_list: List of match URLs
    :param spreadsheet_path: Path to spreadsheet data is to be written to
    :return:
    """
    for counter, url in enumerate(url_list):
        if counter % 10 == 0 and counter != 0:
            sleep(10)
        else:
            sleep(2)

        spread(scrape_match(url), spreadsheet_path)

    print('=' * 100)
    print(f'Complete - {len(url_list)} matches added')


def main():
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askopenfilename()
    try:
        matches_to_scrape = input_urls()
        scrape_urls(matches_to_scrape, path)
    except IndexError:
        print('=' * 100)
        print('Invalid URLs entered')


if __name__ == '__main__':
    main()
