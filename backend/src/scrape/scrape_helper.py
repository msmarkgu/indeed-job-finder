import datetime
import json
import os
import re
import sys
import typing


CUR_DIR = os.path.dirname(os.path.realpath(__file__))
TODAY = datetime.datetime.today().strftime('%Y-%m-%d')

from src.scrape.indeed_job_data import IndeedJobData

class ScrapeHelper:

    DATA_DIR = os.path.join(CUR_DIR, f"../../data/scrape_result")

    # e.g., location="Seattle, WA", filename="job_data_seattle__wa.json"
    @staticmethod
    def get_filename_for_location(location: str, prefix: str = "job_data") -> str:
        json_file = f"{prefix}_{location.lower().replace(' ', '_').replace(',', '_')}.json"
        return json_file

    @staticmethod
    def read_job_list(location: str, date_str: str) -> typing.List[IndeedJobData]:

        job_file = ScrapeHelper.get_filename_for_location(location)

        file_path = os.path.join(ScrapeHelper.DATA_DIR, f"./{date_str}/", job_file)

        print(f"job_file_path = {file_path}")

        if not os.path.exists(file_path):
            return []

        with open(file_path, 'r') as fp:
            job_list = json.load(fp)

        return job_list

    @staticmethod
    def read_job_logs(location: str, date_str: str) -> typing.List[str]:

        job_file = ScrapeHelper.get_filename_for_location(location)

        log_file = job_file.replace(".json", ".log")

        file_path = os.path.join(ScrapeHelper.DATA_DIR, f"./{date_str}/", log_file)

        print(f"log_file_path = {file_path}")

        job_logs = []
        if os.path.exists(file_path):
            with open(file_path, 'r') as fp:
                job_logs = [line.rstrip('\n') for line in fp]

        return job_logs

    # e.g., input post_date = 'today' or '2 day ago', output = '2023-05-06'.
    @staticmethod
    def parse_job_post_date(post_date: str) -> str:
        if not post_date:
            return TODAY

        post_date = post_date.lower()

        if 'today' in post_date or 'just now' in post_date or 'just posted' in post_date:
            return TODAY

        match = re.search(r'\d+', post_date)
        if match:
            days_ago = match.group()
            today = datetime.datetime.now()
            delta = datetime.timedelta(days = float(days_ago))
            x = today - delta
            return x.strftime('%Y-%m-%d')

        return TODAY

    @staticmethod
    def check_result_exists(file_path: str) -> bool:
        if not os.path.exists(file_path):
            return False

        with open(file_path, 'r') as fp:
            lines = fp.readlines()

        if len(lines) == 0:
            return False

        return True
