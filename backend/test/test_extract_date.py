import datetime
import os
import sys
import unittest

from src.backend.scrape.scrape_helper import ScrapeHelper

class TestExtractDate(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        return

    def test(self):
        expect_delta = 3
        input_str = f'Posted {expect_delta} days ago'

        post_date = ScrapeHelper.parse_job_post_date(input_str)

        print(f"post_date = {post_date}")

        prev_date = datetime.datetime.strptime(post_date, "%Y-%m-%d").date()
        curr_date = datetime.datetime.today()
        curr_date_str = datetime.datetime.today().strftime('%Y-%m-%d')

        print(f"curr_date = {curr_date_str}")

        date_obj1 = datetime.date(prev_date.year, prev_date.month, prev_date.day)
        date_obj2 = datetime.date(curr_date.year, curr_date.month, curr_date.day)

        actual_delta = date_obj2 - date_obj1

        print(f"expect_delta = {expect_delta}, actual_delta = {actual_delta}")

        self.assertEqual(expect_delta, actual_delta.days)

# to run test from command line:
# (py3.8) ~/OpenSource/Selenium$ python -m unittest -v test.test_nlp_utils
if __name__ == '__main__':
    unittest.main()
