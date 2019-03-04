from scraper import scrape_match
from tkinter import filedialog
from write_to_spread import spread
from get_urls import get_urls
import tkinter as tk
import time


class Main:
    def __init__(self, spreadsheet_path):
        self.path = spreadsheet_path
        self.url_list = []
        self.pause = 0

    def scraper(self):
        if input('Scrape entire season?: ') == 'y':
            self.url_list = get_urls(input('Enter season URL: '))
            check_url_number = input('Continue?: ')
            if check_url_number != 'y':
                exit()
        else:
            self.url_list = input("Enter match URLs (split multiple URLs with ','): ").split(',')

        for url in self.url_list:
            if self.pause == 10:
                time.sleep(10)
                spread(scrape_match(url), self.path)
                self.pause = 0
            else:
                time.sleep(1)
                spread(scrape_match(url), self.path)
                self.pause += 1

        print("=" * 100 + "\nComplete - {} matches added".format(len(self.url_list)))


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    main = Main(filedialog.askopenfilename())
    main.scraper()
