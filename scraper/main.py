from time import sleep
from urllib.parse import urlparse

from scraper import scrape_match
from write_to_spread import write_spread
from season import get_urls_season


def main():
    if input("Scrape entire season? (y/n): ") == "y":
        season_url = input("Enter season URL: ")
        match_urls = get_urls_season(urlparse(season_url).path)
    else:
        urls = input("Enter match URLs (split multiple URLs with ','): ")
        match_urls = [urlparse(url).path for url in urls.split(",")]

    for counter, url in enumerate(match_urls, start=1):
        
        # Stagger to prevent requests being denied
        if counter % 10 == 0:
            sleep(10)
        else:
            sleep(2)

        match_data = scrape_match(url)
        write_spread(match_data, path="example_output.xlsx")

    print("=" * 100)
    print(f"Complete - {len(match_urls)} added")


if __name__ == "__main__":
    main()
