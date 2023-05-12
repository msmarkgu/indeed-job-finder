import datetime
import logging
import os
import sys

from src.scrape.indeed_scraper import IndeedScraper
from src.scrape.scrape_helper import ScrapeHelper

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
TODAY = datetime.datetime.today().strftime('%Y-%m-%d')

def main(argv):
    out_dir = os.path.join(CUR_DIR, f"../../data/scrape_result/{TODAY}")

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    what_job = 'Senior Software Engineer'
    last_days = 14
    max_page = 10
    vjk_key  = '' #'8d154102de0392d0'
    headless = False

    location = 'Seattle, WA'
    #location = 'New York City, NY'
    #location = 'Atlanta, GA'
    #location = 'San Francisco, CA'
    #location = 'Los Angeles, CA'

    # f"job_data_{location.lower().replace(' ', '_').replace(',', '_')}.json"
    out_file = ScrapeHelper.get_filename_for_location(location)

    # location, out_file = ('Boston, MA', 'job_data_boston.json')
    # location, out_file = ('Austin, TX', 'job_data_austin.json')
    # location, out_file = ('Chicago, IL', 'job_data_chicago.json')
    # location, out_file = ('Seattle, WA', 'job_data_seattle.json')
    # location, out_file = ('Portland, OR', 'job_data_portland.json')

    out_path = os.path.join(out_dir, out_file)

    print(f'out_file = {out_path}')

    log_file = out_path.replace(".json", ".log")

    print(f'log_file = {log_file}')

    scraper = IndeedScraper(log_level=logging.DEBUG, headless=headless, log_file=log_file)

    job_count = scraper.do_search(what_job, location, last_days, max_page, out_path, vjk_key)
    print(f"location = {location}, jobs_found = {job_count}")

    scraper.dispose()

if __name__ == "__main__":
    main(sys.argv)
