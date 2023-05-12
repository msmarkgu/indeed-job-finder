import json
import os
import re
import sys

from bs4 import BeautifulSoup, NavigableString, Comment

CUR_DIR = os.path.dirname(os.path.realpath(__file__))

class JobDescTextExtractor:
    def __init__(self) -> None:
        pass

    def is_tag_visible(self, element):
        return not isinstance(element, Comment)

    def extract_text_as_one_string(self, html) -> str:
        soup = BeautifulSoup(html, 'html.parser')
        # "string=True": find all tags having text value, regardless what the text is.
        texts = soup.findAll(string=True)
        visible_texts = filter(self.is_tag_visible, texts)
        visible_text = u" ".join(t for t in (s.strip() for s in visible_texts) if t)
        return visible_text.strip()

    def extract_text_line_by_line(self, html) -> list:
        html = html.replace('<br>', '\n')
        lines = html.split('\n')
        print(f"lines = {len(lines)}")

        text_list = []

        line_count = 0
        total_lines = len(lines)
        curr_line = ''
        while(line_count < total_lines):
            curr_line = lines[line_count].strip()     # contain html tags
            clean_line = self.extract_text_as_one_string(curr_line) # html tags dropped
            line_count += 1

            if len(clean_line) > 0:
                text_list.append(clean_line)

        return text_list

def main(argv):
    extractor = JobDescTextExtractor()

    html = '''
    <p><b>Secure our Nation, Ignite your Future </b></p>\n <p></p>\n <p>ManTech is looking for a highly motivated and qualified <b>Full Stack Software Developer </b>in San Antonio, TX, and remote. This rewarding and challenging position supports the Department of Defense (DoD) to produce microservice-based software to improve cyberspace operations and defend U.S. vital national security interests. </p>\n <p></p>\n <p><b>Position Responsibilities: </b></p>
    '''

    text1 = extractor.extract_text_line_by_line(html)
    text2 = extractor.extract_text_as_one_string(html)

    print(f"html = {html}\n")

    print(f"text1 = {text1}\n")
    print(f"type(text1) = {type(text1)}, len(text1) = {len(text1)}\n")

    print(f"text2 = {text2}\n,")
    print(f"type(text2) = {type(text2)}, len(text2) = {len(text2)}\n")

if __name__ == "__main__":
    main(sys.argv)
