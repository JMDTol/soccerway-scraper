from scraper import scrape_match
from tkinter import filedialog
from write_to_spread import spread
from season import season_scrape
import tkinter as tk
import time


def input_urls():
    if input('Scrape entire season?: ') == 'y':
        season_url = input('Enter season URL: ')
        url_list = season_scrape(season_url)
        if input('Continue?: ') != 'y':
            exit()
    else:
        url_list = input("Enter match URLs (split multiple URLs with ','): ").split(',')

    return url_list


def scrape_urls(url_list, path):
    pause = 0
    for url in url_list:
        if pause == 10:
            time.sleep(10)
            spread(scrape_match(url), path)
            pause = 0
        else:
            time.sleep(1)
            spread(scrape_match(url), path)
            pause += 1

    print("=" * 100 + "\nComplete - {} matches added".format(len(url_list)))


def main():
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askopenfilename()
    matches_to_scrape = input_urls()
    scrape_urls(matches_to_scrape, path)


if __name__ == "__main__":
    main()
