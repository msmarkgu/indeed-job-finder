import datetime
import logging
import os
import sys
import time


from src.scrape.indeed_scraper import IndeedScraper
from src.scrape.scrape_helper import ScrapeHelper

CUR_DIR = os.path.dirname(os.path.realpath(__file__))
TODAY = datetime.today().strftime('%Y-%m-%d')

def main(argv):
    out_dir = os.path.join(CUR_DIR, f"../../data/scrape_result/{TODAY}")

    if not os.path.exists(out_dir):
        os.makedir(out_dir)

    locations_file = os.path.join(CUR_DIR, "../../../resources/us-top20-tech-job-cities.txt")

    with open(locations_file, 'r') as fp:
        locations = fp.readlines()

    what_job = 'Senior Software Engineer'
    last_days = 14
    max_page = 10
    vjk_key  = '917f3457d7c513fb'
    headless = False

    for location in locations:
        location = location.strip()
        if location.startswith('#') or not location.strip():
            continue

        # f"job_data_{location.lower().replace(' ', '_').replace(',', '_')}.json"
        out_file = ScrapeHelper.get_filename_for_location(location)

        out_path = os.path.join(out_dir, out_file)

        print(f'location = {location}, out_file = {out_file}')

        log_file = out_path.replace(".json", ".log")

        print(f'log_file = {log_file}')

        scraper = IndeedScraper(log_level=logging.DEBUG, headless=headless, log_file=log_file)

        job_count = scraper.do_search(what_job, location, last_days, max_page, out_path, vjk_key)

        print(f"location = {location}, jobs_found = {job_count}")

        scraper.dispose()

        time.sleep(10)  # pause 10 sec between locations


if __name__ == "__main__":
    main(sys.argv)
