import json
import operator
import os
import sys
import time

import pysbd
import spacy

from src.backend.parse.parse_jd_sections import JobDescriptionParser
from src.backend.utils.html_utils import HtmlUtils


CUR_DIR = os.path.dirname(os.path.realpath(__file__))

class NounPhraseExtractor:
    def __init__(self) -> None:
        self.spacy_nlp = spacy.load('en_core_web_lg')
        self.pysbd_seg = pysbd.Segmenter(language="en", clean=False)
        self.stopwords = self.spacy_nlp.Defaults.stop_words
        self.html_parser = JobDescriptionParser()

    def process_text(self, text):
        result = []

        # input text can be html containing html tags
        text = HtmlUtils.extract_text(text)

        text = self.clean_text(text)

        sentences = self.pysbd_seg.segment(text)

        for sentence in sentences:
            doc = self.spacy_nlp(sentence)
            for np in doc.noun_chunks:
                term = np.text.lower()
                if term in self.stopwords:
                    continue
                else:
                    result.append(self.normalize_term(term))

        return result

    def clean_text(self, text):
        result = text.replace('\u2019', "'").replace('\u2013', "-").replace('\n', ' ')
        return result.strip()

    def normalize_term(self, term):
        words_to_ignore = { 'a', 'an', 'our', 'your', 'the', 'its', 'his', 'her', 'their' }
        tokens = term.split()
        result = []
        for token in tokens:
            if token not in words_to_ignore:
                result.append(token)
        return " ".join(result)

def count_one_file(in_file, np_counter, term_freqs):
    # in_file = 'job_data_new_york_city__ny.json'
    with open(in_file, 'r') as fp:
        job_list = json.load(fp)

    print(f"\nlen(job_list) = {len(job_list)}\n")

    for job in job_list:
        job_title = job['JobTitle']
        job_desc = job['JobDescription']
        print(f"job_title: {job_title}")

        terms = np_counter.process_text(job_desc)

        print(f"len(terms) = {len(terms)}")

        for term in terms:
            if term in term_freqs:
                term_freqs[term] = term_freqs[term] + 1
            else:
                term_freqs[term] = 1

    return len(job_list)

def main(argv):
    term_freqs = {}
    np_counter = NounPhraseExtractor()

    in_dir = os.path.join(CUR_DIR, '../scrape_result/')

    total_jobs = 0
    for filename in os.listdir(in_dir):
        in_file = os.path.join(in_dir, filename)
        if not os.path.isfile(in_file) or not in_file.endswith('.json'):
            continue

        total_jobs += count_one_file(in_file, np_counter, term_freqs)

        print(f"\nlen(term_freqs) = {len(term_freqs)}\n")

    print(f"\nlen(term_freqs) = {len(term_freqs)}\n")

    # sort words by frequency in descending order
    sorted_dict = dict(sorted(term_freqs.items(), key=lambda item: item[1], reverse=True))

    max_count = 50
    for idx, item in enumerate(sorted_dict.items()):
        if idx < max_count:
            print(f"{item[0]}\t{item[1]}")
        else:
            break

    with open('term_freqs.json', 'w') as fp:
        fp.write(json.dumps(sorted_dict, indent=2))

    print(f"\ntotal_jobs = {total_jobs}, term_count = {len(sorted_dict)}\n")


if __name__ == "__main__":
    start_time = time.time()

    main(sys.argv)

    end_time = time.time()

    print("\ntime: {} sec\n".format(round(end_time - start_time, 3)))
