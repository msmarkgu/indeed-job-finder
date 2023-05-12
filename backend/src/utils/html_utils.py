import json
import os
import re
import sys

from bs4 import BeautifulSoup, NavigableString, Comment

class HtmlUtils:
    @staticmethod
    def is_tag_visible(element):
        return not isinstance(element, Comment)

    @staticmethod
    def extract_text(html):
        soup = BeautifulSoup(html, 'html.parser')
        # "string=True": find all tags having text value, regardless what the text is.
        texts = soup.findAll(string=True)
        visible_texts = filter(HtmlUtils.is_tag_visible, texts)
        visible_text = u" ".join(t for t in (s.strip() for s in visible_texts) if t)
        return visible_text.strip()

