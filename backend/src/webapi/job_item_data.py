import json

class JobItemData:
    def __init__(self, id, title, company, location,
                 jobtype, salary, desc, post_date, apply_link) -> None:
        self.job_id = id
        self.job_title = title
        self.company_name = company
        self.company_location = location
        self.job_type = jobtype
        self.salary_info = salary
        self.job_description = desc
        self.post_date = post_date
        self.apply_link = apply_link

    def to_json(self):
        return {
            'jobId': self.job_id,
            'jobTitle': self.job_title,
            'companyName': self.company_name,
            'companyLocation': self.company_location,
            'jobType': self.job_type,
            'salaryInfo': self.salary_info,
            'jobDescription': self.job_description,
            'postDate': self.post_date,
            'applyLink': self.apply_link
        }
