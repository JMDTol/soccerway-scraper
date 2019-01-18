from scraper import soccerway_scraper
from tkinter import filedialog
from write_to_spread import spread
import tkinter as tk

root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()

url = input("Enter URL (split multiple URLs with ',': ")
url_list = url.split(",")

for url in url_list:
    output = soccerway_scraper(url)
    spread(file_path, output)
print("complete")