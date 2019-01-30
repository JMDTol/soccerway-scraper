from scraper import soccerway_scraper
from tkinter import filedialog
from write_to_spread import spread
from get_urls import get_urls
import tkinter as tk


root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()

check = input('Scrape entire season?: ')

if check == 'y':
    url = input('Enter season URL: ')
    url_list = get_urls(url)
else:
    url = input("Enter match URLs (split multiple URLs with ','): ")
    url_list = url.split(',')

for url in url_list:
    output = soccerway_scraper(url)
    spread(output, file_path)

print("=" * 70 + "\nComplete - {} matches added".format(len(url_list)))
