import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

import pysbd

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Define stop words and punctuation to remove
stop_words = set(stopwords.words('english'))
punctuation = set(string.punctuation)

class NlpUtils:

    pysbd_seg = pysbd.Segmenter(language="en", clean=False)

    @staticmethod
    def tokenize(text):
        # Tokenize the text
        tokens = word_tokenize(text)
        return tokens

    # Preprocess the text data
    @staticmethod
    def preprocess_text(text):
        # Tokenize the text
        tokens = word_tokenize(text)

        # Remove stop words and punctuation
        filtered_tokens = [token for token in tokens if token not in stop_words and token not in punctuation]

        # Convert all text to lowercase
        normalized_tokens = [token.lower() for token in filtered_tokens]

        # Join the normalized tokens back into a single string
        normalized_text = ' '.join(normalized_tokens)

        return normalized_text

    @staticmethod
    def split_sentences(text):
        sentences = NlpUtils.pysbd_seg.segment(text)
        return sentences