import json
import os
import re
import sys

from src.backend.parse.jd_desc_parser import JobDescriptionParser

CUR_DIR = os.path.dirname(os.path.realpath(__file__))

def main(argv):
    in_dir  = '../scrape_result'
    out_dir = '../analyze_result'

    #in_file = os.path.join(CUR_DIR, in_dir, 'job_data_raleigh__nc.json')
    #out_file = os.path.join(CUR_DIR, out_dir, "parsed_data_raleigh__nc.json")

    in_file = os.path.join(CUR_DIR, in_dir, 'job_data_new_york_city__ny.json')
    out_file = os.path.join(CUR_DIR, out_dir, "parsed_data_new_york_city__ny.json")

    with open(in_file, 'r') as fp:
        job_list = json.load(fp)

    my_parser = JobDescriptionParser()

    result = []
    for idx, job in enumerate(job_list):
        if idx > 500:
            break

        job_title = job['JobTitle']
        companyName = job['CompanyName']
        job_desc = job['JobDescription']
        print(f"\nidx = {idx}, job_title: {job_title}")

        sections = my_parser.parse_sections(job_desc)

        for key, value in sections.items():
            print(f"\ntitle: {key}\ncontent: {value}\n")

        print(f"sections = {len(sections)}")

        data = {}
        data['JobTitle'] = job_title
        data['CompanyName'] = companyName
        data['JobDescription'] = sections

        result.append(data)

    with open(out_file, 'w') as fp:
        fp.write(json.dumps(result, indent=2))

if __name__ == "__main__":
    main(sys.argv)
