import json

class ScrapeRequest:
    def __init__(self, loc, job, last, max, date) -> None:
        self.location = loc
        self.what_job = job
        self.last_days = last
        self.max_page = max
        self.date_str = date

    def to_json(self):
        return {
            "Location": self.location,
            "WhatJob": self.what_job,
            "LastDays": self.last_days,
            "MaxPage": self.max_page,
            "DateStr": self.date_str
        }
