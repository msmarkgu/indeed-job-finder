import json
import os
import re
import string
import sys
import time

import spacy

from src.parse.parse_jd_sections import JobDescriptionParser

CUR_DIR = os.path.dirname(os.path.realpath(__file__))

class TechWordCounter:
    def __init__(self) -> None:
        self.spacy_nlp = spacy.load('en_core_web_lg')
        self.words_to_keep = self.load_words_to_keep()
        self.words_to_skip = self.load_words_to_skip()
        self.html_parser = JobDescriptionParser()

    def load_words_to_keep(self):
        words = {}  # map lowercase to formal word, e.g., java --> Java

        words_file = os.path.join(CUR_DIR, "../resources", "additional-words-to-keep.txt")
        with open(words_file, 'r') as fp:
            all_lines = fp.readlines()

        for line in all_lines:
            word = line.strip()
            if word and not word.startswith('#'):
                words[word.lower()] = word

        return words

    def load_words_to_skip(self):
        words = set()

        words_file = os.path.join(CUR_DIR, "../resources", "google-english-words-20k.txt")
        with open(words_file, 'r') as fp:
            all_lines = fp.readlines()

        for line in all_lines:
            words.add(line.lower().strip())

        words_file = os.path.join(CUR_DIR, "../resources", "additional-words-to-skip.txt")
        with open(words_file, 'r') as fp:
            all_lines = fp.readlines()

        for line in all_lines:
            words.add(line.lower().strip())

        return words

    def process_text(self, text):
        result = set()

        # input text can be html containing html tags
        text = self.html_parser.extract_text(text)

        text = self.clean_text(text)

        # use Spacy to tokenize and lemmatize
        doc = self.spacy_nlp(text)

        for token in doc:
            token_text = token.text.strip()
            token_lemma = token.lemma_.strip()  # get the root form of a word

            if (token_text.lower() in self.words_to_keep):
                result.add(self.words_to_keep[token_text.lower()])  # keep the normal form
                continue

            if not (self.can_ignore(token_text)
                    or token_text.lower() in self.words_to_skip
                    or token_lemma.lower() in self.words_to_skip):
                result.add(token_text)
                continue

        return result

    def clean_text(self, text):
        result = text \
            .replace('\u2019', "'") \
            .replace('\u2013', "-") \
            .replace('\u00b7', '-') \
            .replace('\n', ' ')
        return result.strip()

    def can_ignore(self, token):
        if (len(token)<=1 or token.isnumeric()
            or any(p in token for p in string.punctuation)
            or re.match('\d{2-}(K|M|B)', token.upper())  # e.g., "300K"
            or re.match('\d+x\d+', token.lower())  # e.g., "4x10"
            or re.match('\d+mbps', token.lower())  # e.g., "5Mbps"
            or re.match('\d+\w+',  token.lower())  # e.g., '635326BR'
            ):
            return True
        return False

def count_one_file(in_file, word_counter, word_freqs):
    # in_file = 'job_data_new_york_city__ny.json'
    with open(in_file, 'r') as fp:
        job_list = json.load(fp)

    print(f"\nlen(job_list) = {len(job_list)}\n")

    for job in job_list:
        job_title = job['JobTitle']
        job_desc = job['JobDescription']
        print(f"\tjob_title: {job_title}")

        words = word_counter.process_text(job_desc)

        print(f"\tlen(words) = {len(words)}")

        for word in words:
            if word in word_freqs:
                word_freqs[word] = word_freqs[word] + 1
            else:
                word_freqs[word] = 1

    return len(job_list)

def main(argv):
    word_freqs = {}
    word_counter = TechWordCounter()

    in_dir = os.path.join(CUR_DIR, '../scrape_result/')

    total_jobs = 0
    for filename in os.listdir(in_dir):
        in_file = os.path.join(in_dir, filename)
        if not os.path.isfile(in_file) or not in_file.endswith('.json'):
            continue

        total_jobs += count_one_file(in_file, word_counter, word_freqs)

        print(f"\nlen(word_freqs) = {len(word_freqs)}\n")

    # sort words by frequency in descending order
    sorted_dict = dict(sorted(word_freqs.items(), key=lambda item: item[1], reverse=True))

    max_count = 50
    for idx, item in enumerate(sorted_dict.items()):
        if idx < max_count:
            print(f"{item[0]}\t{item[1]}")
        else:
            break

    with open('word_freqs.json', 'w') as fp:
        fp.write(json.dumps(sorted_dict, indent=2))

    print(f"\ntotal_jobs = {total_jobs}, word_count = {len(sorted_dict)}\n")

if __name__ == "__main__":
    start_time = time.time()

    main(sys.argv)

    end_time = time.time()

    print("\ntime: {} sec\n".format(round(end_time - start_time, 3)))
