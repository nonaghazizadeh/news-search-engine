from src.requirements.numpy_encoder import NumpyEncoder
from src.enums.enums import Path

import fasttext
import json
import numpy as np


class QueryExpansion:
    def __init__(self, need_training=False):
        self.numpy_encoder = NumpyEncoder
        self.fasttext_model = fasttext.load_model(Path.QE_FASTTEXT_MODEL_PATH.value)
        with open(Path.QE_FASTTEXT_DATA_PATH.value) as f:
            self.lines = f.read()
        self.words = self.lines.split()
        self.word2vec = dict()
        if need_training:
            self.calculate_word2vec()
            self.save_word2vec()
        self.load_word2vec()

    def calculate_word2vec(self):
        for word in self.words:
            self.word2vec[word] = self.fasttext_model[word]

    def save_word2vec(self):
        with open(Path.QE_ALL_EMBEDDING_PATH.value, 'w', encoding="utf-8") as f:
            json.dump(self.word2vec, f, cls=self.numpy_encoder)

    def load_word2vec(self):
        with open(Path.QE_ALL_EMBEDDING_PATH.value, 'r', encoding="utf-8") as f:
            self.word2vec = json.loads(f.read())

    def expand_query(self, query, cosine_threshold=0.9):
        query_words = query.split()
        q_word2vec = dict()
        for q_word in query_words:
            q_word2vec[q_word] = self.fasttext_model[q_word]

        most_similar_query = ''
        query_words = query.split()
        for q_word in query_words:
            max_cosine_similarity = 0
            most_similar_word = ''
            for k, v in self.word2vec.items():
                cosine_similarity = np.dot(np.array(v), np.array(q_word2vec[q_word])) / (
                        np.linalg.norm(np.array(v)) * np.linalg.norm(np.array(q_word2vec[q_word])))
                k = k.replace("\u200e", "")
                k = k.replace("\xad", "")
                k = k.replace("\n", " ")
                if max_cosine_similarity < cosine_similarity < cosine_threshold and k != q_word:
                    max_cosine_similarity = cosine_similarity
                    most_similar_word = k
            most_similar_query = most_similar_query + " " + most_similar_word
        return most_similar_query.strip()

    @staticmethod
    def expand_query_rocchio(q_avg, nr_avg, r_avg):
        temp_sum = np.sum([np.array(q_avg), r_avg], axis=0)
        new_q_avg = np.subtract(temp_sum, nr_avg)
        return new_q_avg
