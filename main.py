from scraper import scrape_match
from tkinter import filedialog
from write_to_spread import spread
from get_urls import get_urls
from openpyxl import load_workbook
import tkinter as tk
import time


# Open a dialog box to choose a spreadsheet for the data to be written to.
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()

# Load chosen workbook and set the first worksheet as the destination for the data.
wb = load_workbook(file_path)
ws = wb.worksheets[0]

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
        output = scrape_match(url)
        spread(output, ws)
        pause = 0
    else:
        time.sleep(1)
        output = scrape_match(url)
        spread(output, ws)
        pause += 1

wb.save(file_path)

print("=" * 100 + "\nComplete - {} matches added".format(len(url_list)))
