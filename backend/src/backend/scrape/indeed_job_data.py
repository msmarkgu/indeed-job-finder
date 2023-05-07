import json

class IndeedJobData:
    def __init__(self, title: str, compmany: str, company_location: str,
                 job_type: str, salary: str, desc: str, post_date: str, apply_link: str) -> None:
        self.job_title = title
        self.company_name = compmany
        self.company_location = company_location
        self.job_type = job_type
        self.salary_info = salary
        self.job_description = desc
        self.post_date = post_date
        self.apply_link = apply_link

    def to_json(self):
        return {
            'JobTitle': self.job_title,
            'CompanyName': self.company_name,
            'CompanyLocation': self.company_location,
            'JobType': self.job_type,
            'SalaryInfo': self.salary_info,
            'JobDescription': self.job_description,
            "PostDate": self.post_date,
            "ApplyLink": self.apply_link
        }
