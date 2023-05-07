import dotenv
import json
import logging
import os
import random
import sys
import time
import traceback
import urllib.parse

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.backend.utils.common_utils import CommonUtils
from src.backend.scrape.indeed_job_data import IndeedJobData
from src.backend.scrape.scrape_helper import ScrapeHelper
from src.backend.scrape.scrape_request import ScrapeRequest

CUR_DIR = os.path.dirname(os.path.realpath(__file__))

class IndeedScraper:
    def __init__(self, log_level=logging.INFO, headless=False, log_file=None) -> None:
        self.what_job = ''  # e.g., 'Senior Software Engineer'
        self.location = ''  # e.g., 'Seattle, WA'
        self.last_days= ''  # e.g., 14
        self.max_page = ''  # e.g., 10
        self.out_file = ''  # e.g., 'job_data_seattle.json'
        self.vjk_key  = ''  # e.g., '&vjk=917f3457d7c513fb'

        self.logger = CommonUtils.init_logger(log_level, self.__class__.__name__, log_file)

        dotenv.load_dotenv(os.path.join(CUR_DIR, '../.env'))

        # e.g., '~/OpenSource/Selenium/bin/firefox-112.0.1/firefox'
        self.browser_path = os.getenv("BROWSER_PATH_FIREFOX")
        # e.g., '~/OpenSource/Selenium/bin/firefox-106+/geckodriver'
        self.driver_path  = os.getenv("DRIVER_PATH_FIREFOX")
        # e.g., 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0'
        self.user_agent   = os.getenv("BROWSER_USER_AGENT")

        self.logger.info(f"browser_path={self.browser_path}")
        self.logger.info(f"driver_path={self.driver_path}")

        self.url_template=r'https://www.indeed.com/jobs?q={}&l={}&sort={}&fromage={}&radius={}&sc={}&vjk={}&filter=0'  # Note: "&filter=0" will prevent Indeed from dynamically removing job postings during search

        self.driver = self.create_driver(headless)

    def create_driver(self, headless=False):
        options = webdriver.FirefoxOptions()
        options.headless = headless
        options.add_argument("--disable-notifications")
        options.add_argument("-private")
        options.add_argument(self.user_agent)
        options.binary_location = self.browser_path

        service = Service(self.driver_path)

        driver = webdriver.Firefox(service=service, options=options)

        driver.maximize_window()
        driver.implicitly_wait(10)

        return driver

    def open_url(self, target_url):
        self.driver.get(target_url)

    def dispose(self):
        self.driver.quit()

    # Indeed seems to use '+' for '%20' (url encoded space char)
    # e.g., raw input: 'Seattle, WA', after url encode: 'Seattle%2C%20WA',
    # Indeed changes it to: 'Seattle%2C+WA', as seen in the browser address bar.
    def url_quote(self, text):
        t = urllib.parse.quote(text.encode('utf8'))
        t = t.replace('%20', '+')
        return t

    def random_sleep(self, a=3, b=10):
        time.sleep(a + (b-a) * random.random())

    def scroll_to_element(self, element):
        if element:
            # Javascript expression to scroll to a particular element
            # arguments[0] refers to the first argument that is later passed
            # in to execute_script method
            js_code = "arguments[0].scrollIntoView();"
            # Execute the JS script
            self.driver.execute_script(js_code, element)
        else:
            pass

    def get_target_url(self, what_job, location, last_days, max_page, out_file, vjk_key):
        self.what_job = what_job
        self.location = location
        self.last_days = last_days
        self.max_page = max_page
        self.out_file = out_file
        self.vjk_key  = vjk_key

        job_what=self.url_quote(self.what_job)  # 'senior+software+engineer'
        job_where=self.url_quote(self.location)  # 'Seattle%2C+WA'
        fromage=self.last_days  # '7'
        sort='date'
        radius='100'
        explevel='0kf%3Aexplvl%28SENIOR_LEVEL%29jt%28fulltime%29%3B'
        session_key = self.vjk_key

        # url='https://www.indeed.com/jobs?q=senior+software+engineer&l=Seattle%2C+WA&sc=0kf%3Aexplvl%28SENIOR_LEVEL%29jt%28fulltime%29%3B&radius=100&fromage=7&vjk=fcdf2552798b5674

        target_url=self.url_template.format(job_what, job_where, sort, fromage, radius, explevel, session_key)

        return target_url

    # 1. How to handle NoSuchElementError:
    # https://reflect.run/articles/everything-you-need-to-know-about-nosuchelementexception-in-selenium/
    # 2. How to handle "Element is not clickable at point (x,y) because another element obscured it":
    # https://stackoverflow.com/questions/67394146/selenium-and-python-element-not-clickable-at-point-x-y-because-another-elemen
    def process_current_page(self, page_num, job_data):

        # job cards are in the left pane
        try:
            current_page = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
                (By.XPATH, "//div[@class='jobsearch-LeftPane']"))
            )
        except Exception as ex:
            current_page = None
            self.logger.error(f"failed to locate left pane! Exception: {ex}")
            traceback.print_exc()

        if not current_page:
            return 0

        try:
            job_cards = current_page.find_elements(By.XPATH, ".//td[@class='resultContent']")
        except Exception as ex:
            job_cards = None
            self.logger.error(f"failed to find job cards! Exception: {ex}")
            traceback.print_exc()

        if not job_cards:
            return 0

        self.logger.info(f"location = {self.location}, page_num = {page_num}, job_cards.size = {len(job_cards)}")

        job_count=0
        for job_card in job_cards:
            job_count += 1

            self.scroll_to_element(job_card)

            salary_div = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='salaryInfoAndJobType']")))

            elem_tag = job_card.get_attribute('tagName')
            elem_id = job_card.get_attribute('id')
            elem_class = job_card.get_attribute('class')
            inner_text = job_card.get_attribute('innerText')
            self.logger.debug(f"\npage#={page_num}, job#={job_count}, text={inner_text}")

            job_title = 'TBD'
            job_link = job_card.find_element(By.XPATH, ".//a[starts-with(@class, 'jcs-JobTitle') and (starts-with(@id, 'job_') or starts-with(@id, 'sj_'))]")
            if job_link:
                job_title = job_link.get_attribute("innerText")
            else:
                continue

            self.logger.debug(f"\tjob_title={job_title}")

            company_name = 'TBD'
            company_span = job_card.find_element(By.XPATH, ".//span[@class='companyName']")
            if company_span:
                company_name = company_span.get_attribute("innerText")

            self.logger.debug(f"\tcompany_name={company_name}")

            company_location = 'TBD'
            location_div = job_card.find_element(By.XPATH, ".//div[@class='companyLocation']")
            if location_div:
                company_location = location_div.get_attribute("innerText")

            self.logger.debug(f"\tcompany_location={company_location}")

            job_type = 'TBD'
            salary_div = job_card.find_element(By.XPATH, ".//div[@class='heading6 tapItem-gutter metadataContainer noJEMChips salaryOnly']")
            if salary_div:
                job_type = salary_div.get_attribute("innerText")

            self.logger.debug(f"\tjob_type={job_type}")

            post_date = ''
            container_div = job_card.find_element(By.XPATH, "ancestor::div[contains(@class,'job_seen_beacon')]")
            if container_div:
                date_span = container_div.find_element(By.XPATH, ".//descendant::span[@class='date']")
                if date_span:
                    post_date = date_span.get_attribute('innerText')
            self.logger.debug(f"\tpost_date = {post_date}")

            salary_info = 'TBD'
            job_description = 'TBD'

            try:
                #job_card.click()
                job_link.click()
            except Exception as ex:
                self.logger.error(f"Exception: {ex}")

                if str(ex).find("is not clickable at point") != -1:
                    try:
                        parent = job_card.find_element_by_xpath('..')
                        parent.click()
                    except Exception as ex2:
                        self.logger.error(f"Exception2: {ex2}")

                traceback.print_exc()

            try:
                salary_div = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@id='salaryInfoAndJobType']")))

                if salary_div:
                    salary_info = salary_div.get_attribute('innerText')

                details_div = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                    (By.XPATH, "//div[@id='jobDescriptionText']"))
                )

                if details_div:
                    #job_description = details_div.get_attribute('innerText')
                    job_description = details_div.get_attribute('innerHTML')
            except Exception as ex:
                self.logger.error(f"Exception: {ex}")
                traceback.print_exc()

            apply_link = job_link.get_attribute('href')
            apply_link_span = None
            try:
                #apply_link_span = self.driver.find_element(By.ID, "//span[@id,'indeed-apply-widget']")
                apply_link_span = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "//span[@id, 'indeed-apply-widget']"))
                )
                if apply_link_span:
                    apply_link = apply_link_span.get_attribute("data-indeed-apply-joburl")
            except Exception as ex:
                self.logger.error(f"Exception: {ex}")
                traceback.print_exc()

            if apply_link_span is None:
                try:
                    #apply_link_anchor = self.driver.find_element(By.XPATH, "//a[@contenthtml='Apply on company site']")
                    apply_link_anchor = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@contenthtml='Apply on company site']"))
                    )
                    if apply_link_anchor:
                        apply_link = apply_link_anchor.get_attribute("href")
                except Exception as ex:
                    self.logger.error(f"Exception: {ex}")
                    traceback.print_exc()

            self.logger.debug(f"\tapply_link = {apply_link}")

            job_data.append(IndeedJobData(
                job_title,
                company_name,
                company_location,
                job_type,
                salary_info,
                job_description,
                ScrapeHelper.parse_job_post_date(post_date),
                apply_link)
            )

            self.logger.info(f"page#={page_num}, job#={job_count}: \ntitle={job_title}, \ncompany={company_name}, \nsalary={salary_info}")

            # on average to wait 5 sec before loading the next job card
            self.random_sleep(3, 7)

        self.logger.info(f"job_count = {job_count}")

        return job_count

    def do_search(self, what_job, location, last_days, max_page, out_file, vjk_key):
        target_url = self.get_target_url(what_job, location, last_days, max_page, out_file, vjk_key)

        self.logger.info(f"target_url = {target_url}")

        #self.driver.get(target_url)
        self.open_url(target_url)

        job_data = []

        page_count=0
        job_count=0
        while page_count < self.max_page:
            page_count += 1

            self.logger.info(f"\n========== Location: {self.location}, Page: {page_count} ==========")

            try:
                job_count += self.process_current_page(page_num=page_count, job_data=job_data)
            except Exception as ex:
                self.logger.error(f"Exception in page={page_count}: {ex}")
                traceback.print_exc()

            next_page = None
            try:
                #element = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.ID, "someId"))
                locator = (By.XPATH, "//a[@data-testid='pagination-page-next']")
                next_page = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located(locator)
                    and
                    EC.element_to_be_clickable(locator)
                )
            except Exception as ex:
                self.logger.error(f"There are no more pages to load!")
                traceback.print_exc()

            if next_page:
                try:
                    next_page.click()
                except Exception as ex:
                    self.logger.error(f"failed to click next page! Exception: {ex}")
                    traceback.print_exc()

                self.random_sleep(5, 10)
            else:
                break

        self.logger.info(f"\ntotal_pages_processed = {page_count}, total_jobs_found = {job_count}\n")

        with open(self.out_file, 'w') as fp:
            fp.write(json.dumps(job_data, default=lambda x: x.to_json(), indent=2))

        return job_count

    @staticmethod
    def run_job(search_request: ScrapeRequest) -> None:
        location = search_request.location
        what_job = search_request.what_job
        last_days = search_request.last_days
        max_page = search_request.max_page
        date_str = search_request.date_str
        vjk_key  = '' # '8d154102de0392d0'

        out_file = ScrapeHelper.get_filename_for_location(location)

        out_dir = os.path.join(CUR_DIR, f"../../../data/scrape_result/{date_str}")
        out_path = os.path.join(out_dir, out_file)

        message = ""
        if not ScrapeHelper.check_result_exists(out_path):
            message = "A new search started"

            log_file = out_path.replace(".json", ".log")

            scraper = IndeedScraper(headless=True, log_file=log_file)

            job_count = scraper.do_search(what_job, location, last_days, max_page, out_path, vjk_key)
            print(f"location = {location}, jobs_found = {job_count}")
        else:
            message = "Found existing result"

        print(message)

        return message

def main(argv):
    scraper = IndeedScraper()
    scraper.open_url("https://www.google.com")
    time.sleep(3)
    scraper.dispose()

if __name__ == "__main__":
    main(sys.argv)
