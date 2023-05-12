import json
import logging
import os
import re
import sys

from src.utils.common_utils import CommonUtils
from src.utils.html_utils import HtmlUtils

CUR_DIR = os.path.dirname(os.path.realpath(__file__))

class JobDescriptionParser:
    def __init__(self) -> None:
        self.default_title = 'BEGIN'
        self.logger = CommonUtils.init_logger(logging.INFO, self.__class__.__name__)

    def check_section_title(self, raw_text):
        clean_text = HtmlUtils.extract_text(raw_text) # html tags dropped
        return self.is_section_title(raw_text, clean_text)

    def is_section_title(self, raw_text, clean_text):
        if not clean_text or clean_text.endswith(','):
            return False

        words = clean_text.split()

        is_list_item = self.inside_list_tag(raw_text, words)
        if is_list_item:
            return False

        # Rule 1: the title often is inside <b> tag
        if self.inside_bold_tag(raw_text, words):
            return True

        # Rule 2: section title has all words starting with uppercase letter.
        all_start_with_uppercase = all(w[0].isupper() for w in words)
        if len(words) <= 5 and all_start_with_uppercase:
            return True

        starts_with_uppercase = words[0][0].isupper()
        ends_with_uppercase   = words[-1][0].isupper()

        # Rule 3: the title often ends with ':'
        if words[-1].endswith(':') and starts_with_uppercase:
            return True

        # Rule 4: the title often ends with '?'
        if words[-1].endswith('?') and starts_with_uppercase:
            return True

        # Rule 5: title starts and ends with upper case, has at most 5 words:
        if len(words) < 6 and starts_with_uppercase and ends_with_uppercase:
            return True

        # Rule 6: title has ':' inside, has at most 7 words.
        if len(words) < 8 and clean_text.find(':') > 5:
            return True

        return False

    def inside_bold_tag(self, raw_text, words):
        first_word_index = raw_text.find(words[0])
        last_word_index = raw_text.find(words[-1])

        bold_tag_start = raw_text.rfind('<b>', first_word_index)
        bold_tag_end = raw_text.find('</b>', last_word_index)

        return bold_tag_start < first_word_index and bold_tag_end > last_word_index

    # check if the line is inside a bullet
    def inside_list_tag(self, raw_text, words):
        first_word_index = raw_text.find(words[0])
        last_word_index = raw_text.find(words[-1])

        list_start = raw_text.rfind('<li>', first_word_index)
        list_end = raw_text.find('</li>', last_word_index)

        return list_start < first_word_index and last_word_index < list_end

    def set_title_content(self, dict_sections, title_str, content_list):
        existing_value = dict_sections.get(title_str, '')
        new_value = u" ".join(content_list).strip()

        if len(title_str)==0 and len(new_value)==0:
            return

        if len(title_str)==0 and len(new_value)>0:
           title_str = self.default_title
           dict_sections[title_str] = new_value
           content_list.clear()
           return

        # the same title might appear more than once in the same JD, e.g., "Job Type: Full-time"
        if len(new_value) > 0:
            if len(existing_value) > 0:
                dict_sections[title_str] = existing_value + ' | ' + new_value
            else:
                dict_sections[title_str] = new_value

        content_list.clear()
        return

    def parse_sections(self, html):
        html = html.replace('<br>', '\n')
        lines = html.split('\n')

        self.logger.debug(f"lines = {len(lines)}")

        sections = {}

        line_count = 0
        total_lines = len(lines)
        curr_line = ''
        prev_title = ''
        curr_title = ''
        content_buffer = []
        while(line_count < total_lines):
            curr_line = lines[line_count].strip()     # contain html tags
            clean_line = HtmlUtils.extract_text(curr_line) # html tags dropped
            line_count += 1

            if len(clean_line) == 0:
                continue

            if self.is_section_title(curr_line, clean_line):
                self.logger.debug(f"title line: {clean_line}")
                self.logger.debug(f"content_buffer: {len(content_buffer)}")

                # this line is a title that starts a new section,
                # so set the content buffer to the previous title.
                self.set_title_content(sections, prev_title, content_buffer)

                # check if can further split, e.g., clean_line = "Job Type: Full-time"
                colon_idx = clean_line.find(':')
                if colon_idx > 2 and colon_idx < len(clean_line) - 2:
                    curr_title = clean_line[0:colon_idx].strip()
                    sections[curr_title] = clean_line[colon_idx+1:].strip()
                else:
                    curr_title = clean_line

                # get ready to move to the next line
                prev_title = curr_title
                curr_title = ''
            else:
                content_buffer.append(clean_line)

            #self.logger.debug(f"line_count = {line_count}")

        # handle the last section
        self.set_title_content(sections, prev_title, content_buffer)

        return sections

def main(argv):
    parser = JobDescriptionParser()

    '''
    html = '<p><b>[Remote] Senior Software Engineer/Mobile SDK Developer </b><br><b>Location: United States </b><br>'

    print(f"html = {html}")
    print(f"sections = {parser.parse_sections(html)}")
    '''

    html = '<li>Strong proficiency in the following tech stack: </li>'
    print(f"html = {html}")
    print(f"is_section_title = {parser.check_section_title(html)}")

if __name__ == "__main__":
    main(sys.argv)
