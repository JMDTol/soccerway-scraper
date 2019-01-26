from scraper import soccerway_scraper
from tkinter import filedialog
from write_to_spread import spread
from get_urls import get_entire_season
import tkinter as tk


root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()

answer = input('Scrape entire season? (y or n): ')

if answer == 'y':
    match_urls = 0
    url = input('Enter URL of season to be scraped (split multiple URLs with ","): ')
    url_list = url.split(',')
    for season in url_list:
        match_urls = get_entire_season(season)
        checkpoint = input('Continue? (y or n): ')
        if checkpoint == 'y':
            for url in match_urls:
                output = soccerway_scraper(url)
                spread(output, file_path)
            print('=' * 70 + '\nComplete - {} matches added'.format(len(match_urls)))
        else:
            break

elif answer == 'n':
    url: str = input('Enter URL (split multiple URLs with ","): ')
    url_list = url.split(',')
    for url in url_list:
        output = soccerway_scraper(url)
        spread(output, file_path)

    print('=' * 70 + '\nComplete - {} matches added'.format(len(url_list)))

else:
    print('Invalid input')
