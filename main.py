from scraper import soccerway_scraper
from tkinter import filedialog
from write_to_spread import spread
from openpyxl import load_workbook
import tkinter as tk
import timeit


root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()

url = input("Enter URL (split multiple URLs with ','): ")
url_list = url.split(',')

wb = load_workbook(file_path)
ws = wb.worksheets[0]

start = timeit.default_timer()

for url in url_list:
    output = soccerway_scraper(url)
    spread(output, ws)

wb.save(file_path)

stop = timeit.default_timer()

print("=" * 70)
print('Time: ', stop - start)
print("=" * 70 + "\nComplete - {} matches added".format(len(url_list)))
