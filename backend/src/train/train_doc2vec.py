import json
import typing
import os
import re
import sys

from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from src.utils.nlp_utils import NlpUtils

CUR_DIR = os.path.dirname(os.path.realpath(__file__))

def main(argv):
    in_resume = os.path.join(CUR_DIR, '../analyze_result', 'sample_resume.txt')
    in_corpus = os.path.join(CUR_DIR, '../analyze_result', 'JobDesc_Corpus.txt')
    out_model = os.path.join(CUR_DIR, '../analyze_result', 'JobDesc_Doc2Vec.model')

    with open(in_corpus, 'r') as fp:
        jd_text_list = fp.readlines()  # one line per sentence in Job Desc

    cleaned_text_list = []
    for jd_text in jd_text_list:
        cleaned_text = NlpUtils.preprocess_text(jd_text)
        cleaned_text_list.append(cleaned_text)

    # Create tagged documents
    tagged_data = [TaggedDocument(words=text, tags=[str(i)]) for i, text in enumerate(cleaned_text_list)]

    # Define the Doc2Vec model
    model = Doc2Vec(vector_size=100, window=5, min_count=5, epochs=30, dm=1)

    # Build the vocabulary
    model.build_vocab(tagged_data)

    # Train the Doc2Vec model
    model.train(tagged_data, total_examples=model.corpus_count, epochs=model.epochs)

    # Save the trained model
    model.save(out_model)


if __name__ == "__main__":
    main(sys.argv)