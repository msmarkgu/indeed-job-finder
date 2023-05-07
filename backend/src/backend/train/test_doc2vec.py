import json
import typing
import os
import re
import sys

import gensim
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from src.backend.utils.nlp_utils import NlpUtils

CUR_DIR = os.path.dirname(os.path.realpath(__file__))

def main(argv):
    in_resume = os.path.join(CUR_DIR, '../analyze_result', 'sample_resume.txt')
    in_corpus = os.path.join(CUR_DIR, '../analyze_result', 'JobDesc_Corpus.txt')
    in_model  = os.path.join(CUR_DIR, '../analyze_result', 'JobDesc_Doc2Vec.model')

    jd_matches = os.path.join(CUR_DIR, '../analyze_result', 'JobDesc_Matches.txt')

    with open(in_resume, 'r') as fp:
        input_resume = fp.read()   # input resume as one string

    with open(in_corpus, 'r') as fp:
        jd_text_list = fp.readlines()   # one JD as one string

    print(f"jd_text_list = {len(jd_text_list)}")

    model = gensim.models.Doc2Vec.load(in_model)

    # Test the model by finding the most similar documents for a given query

    query_vec = model.infer_vector(NlpUtils.preprocess_text(input_resume).split())
    similar_docs = model.docvecs.most_similar([query_vec])
    print(similar_docs)



if __name__ == "__main__":
    main(sys.argv)