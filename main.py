from scraper import scrape_match
from tkinter import filedialog
from write_to_spread import spread
from get_urls import get_urls
import tkinter as tk
import time


# Open a dialog box to choose a spreadsheet for the data to be written to.
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()

check1 = input('Scrape entire season?: ')

if check1 == 'y':
    url = input('Enter season URL: ')
    url_list = get_urls(url)
    check2 = input('Continue?: ')
    if check2 != 'y':
        exit()
else:
    url = input("Enter match URLs (split multiple URLs with ','): ")
    url_list = url.split(',')

print("=" * 100)

# Pause loop every ten iterations to prevent requests being denied.
pause = 0

for url in url_list:
    if pause == 10:
        time.sleep(10)
        spread(scrape_match(url), file_path)
        pause = 0
    else:
        time.sleep(1)
        spread(scrape_match(url), file_path)
        pause += 1

print("=" * 100 + "\nComplete - {} matches added".format(len(url_list)))
