import os
import sys
import time

from src.scrape.indeed_scraper import IndeedScraper

def main(argv):
    print(f"sys.path = {sys.path}")

    scraper = IndeedScraper()
    scraper.open_url("https://www.google.com")

    time.sleep(3)
    
    scraper.dispose()

if __name__ == "__main__":
    main(sys.argv)
