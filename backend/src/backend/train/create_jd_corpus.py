import json
import os
import re
import sys
import typing

from src.backend.train.jd_text_extractor import JobDescTextExtractor
from src.backend.utils.nlp_utils import NlpUtils

CUR_DIR = os.path.dirname(os.path.realpath(__file__))


# 1 json file contains multiple Job Descriptions
# each JD will be extracted as one string
def extract_one_file(in_file: str, text_extractor: JobDescTextExtractor) -> typing.List[str]:
    # in_file = 'job_data_new_york_city__ny.json'
    with open(in_file, 'r') as fp:
        job_list = json.load(fp)

    print(f"\nlen(job_list) = {len(job_list)}\n")

    result = []
    for job in job_list:
        job_title = job['JobTitle']
        job_desc = job['JobDescription']

        jd_text = text_extractor.extract_text_as_one_string(job_desc)

        print(f"\tjob_title: {job_title}, len(jd_text) = {len(jd_text)}")

        if jd_text:
            result.append(jd_text)

    return result

def main(argv):
    in_dir  = '../scrape_result'
    out_dir = '../analyze_result'

    my_extractor = JobDescTextExtractor()

    in_dir = os.path.join(CUR_DIR, '../scrape_result/')

    total_jobs = 0
    total_sentences = 0
    out_corpus = os.path.join(CUR_DIR, out_dir, "JobDesc_Corpus.txt")
    out_sentences = os.path.join(CUR_DIR, '../analyze_result', 'JobDesc_Sentences.txt')

    if os.path.exists(out_corpus):
        os.remove(out_corpus)

    if os.path.exists(out_sentences):
        os.remove(out_sentences)

    for filename in os.listdir(in_dir):
        in_file = os.path.join(in_dir, filename)
        if not os.path.isfile(in_file) or not in_file.endswith('.json'):
            continue

        jd_text_list = extract_one_file(in_file, my_extractor)

        with open(out_corpus, 'a') as fp_corpus:
            for jd_idx, jd_text in enumerate(jd_text_list):
                fp_corpus.write(jd_text)
                fp_corpus.write('\n')

                sentences = NlpUtils.split_sentences(jd_text)

                print(f"\tjd_idx = {jd_idx}, sentences = {len(sentences)}")

                with open(out_sentences, 'a') as fp_sent:
                    for sent in sentences:
                        fp_sent.write(sent)
                        fp_sent.write('\n')

                total_sentences += len(sentences)

        total_jobs += len(jd_text_list)

    print(f"total_jobs = {total_jobs}, total_sentences = {total_sentences}")


if __name__ == "__main__":
    main(sys.argv)
