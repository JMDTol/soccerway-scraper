from time import sleep
from urllib.parse import urlparse

from scraper import scrape_match
from write_to_spread import write_spread
from season import get_urls_season


def input_urls():
    """
    Check whether the user wants to scrape an entire season or manually enter
    URLs for each match.
    :return: List of match URLs
    """
    if input('Scrape entire season? (y/n): ') == 'y':
        season_url = input('Enter season URL: ')
        match_urls = get_urls_season(urlparse(season_url).path)
    else:
        urls = input("Enter match URLs (split multiple URLs with ','): ")
        match_urls = [urlparse(url).path for url in urls.split(',')]

    return match_urls


def scrape_urls(url_list):
    """
    Scrape each URL pausing at intervals to prevent requests from being denied.
    :param url_list: List of match URLs
    :return:
    """
    for counter, url in enumerate(url_list, start=1):
        if counter % 10 == 0:
            sleep(10)
        else:
            sleep(2)

        match_dict = scrape_match(url)
        write_spread(match_dict, path='example_output.xlsx')

    print('=' * 100)
    print(f'Complete - {counter} added')


def main():
    urls = input_urls()
    scrape_urls(urls)

    
if __name__ == '__main__':
    main()
