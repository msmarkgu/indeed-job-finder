import os
import sys
import unittest

from src.backend.utils.nlp_utils import NlpUtils

class TestNlpUtils(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        return

    def test_split_sentences(self):
        text = "The Enterprise Cloud Operations Engineer position will oversee Cloud operations to ensure the environments health, stability, manage the daily cloud based systems utilizing AWS, Azure, and Google cloud platforms to ensure the availability, performance, scalability and security of cloud based systems. The Engineer is an expert in 24/7 operations with high performing and scaling systems that meet a high degree of uptime. An expert in all facets of Cloud hosting operations with the ability to effectively communicate with customers, and internal stake holders. The ideal candidate will have expert knowledge in Kubernetes (AKS/EKS) and has previous hands-on experience in containerized environments using DevOps practices."

        #print(text)
        sentences = NlpUtils.split_sentences(text)

        self.assertEqual(4, len(sentences))

# to run test from command line:
# (py3.8) ~/OpenSource/Selenium$ python -m unittest -v test.test_nlp_utils
if __name__ == '__main__':
    unittest.main()
