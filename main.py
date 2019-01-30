from scraper import soccerway_scraper
from tkinter import filedialog
from write_to_spread import spread
from get_urls import get_urls
import tkinter as tk
import time


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

# Pause loop every ten iterations to prevent requests being denied.
pause = 0

for url in url_list:
    if pause == 10:
        time.sleep(10)
        x = 0
    else:
        time.sleep(3)
        output = soccerway_scraper(url)
        spread(output, file_path)
        pause += 1

print("=" * 70 + "\nComplete - {} matches added".format(len(url_list)))
