from src.enums.enums import StaticNum, Path

import pickle
from scipy import sparse
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.preprocessing import PreProcessing


class TfidfSearch:
    def __init__(self, qe_ins, need_training=False):
        self.pre_processor = PreProcessing()
        self.pre_processor()
        self.qe = qe_ins
        self.tfidf = None
        self.tfidf_tran = None
        self.query_vec = list()
        self.related_titles = list()
        self.final_results = dict()
        if need_training:
            self.create_tf_idf_doc_term_matrix()
            self.save_tf_idf()
        self.load_tf_idf()

    def __call__(self, query, qe_en):
        self.calculate_query_tf_idf(query)
        self.tf_idf_results()
        if qe_en:
            self.tf_idf_merge_results(query)
        else:
            self.tf_idf_print_results()

    def create_tf_idf_doc_term_matrix(self):
        vocabulary = set()
        for doc in self.pre_processor.news_df.clean_keyword:
            vocabulary.update(doc.split(','))
        vocabulary = list(vocabulary)

        self.tfidf = TfidfVectorizer(vocabulary=vocabulary, use_idf=True, dtype=np.float32)
        self.tfidf_tran = self.tfidf.fit_transform([' '.join(doc) for doc in self.pre_processor.tokenized_words])

    def save_tf_idf(self):
        with open(Path.TFIDF_PATH.value, 'wb') as f:
            pickle.dump(self.tfidf, f)
        sparse.save_npz(Path.TFIDF_TRAN_PATH.value, self.tfidf_tran)

    def load_tf_idf(self):
        with open(Path.TFIDF_PATH.value, 'rb') as f:
            self.tfidf = pickle.load(f)

        self.tfidf_tran = sparse.load_npz(Path.TFIDF_TRAN_PATH.value)

    def calculate_query_tf_idf(self, query):
        self.query_vec = self.tfidf.transform([query])

    def tf_idf_results(self, query_vec=None, is_qe=False):
        if is_qe:
            return cosine_similarity(self.tfidf_tran, query_vec).reshape((-1,))
        else:
            self.related_titles = cosine_similarity(self.tfidf_tran, self.query_vec).reshape((-1,))

    def tf_idf_print_results(self, num=StaticNum.DOC_RELATED_NUM.value):
        self.final_results = dict()
        for idx, ix in enumerate(np.array(self.related_titles).argsort()[-num:][::-1]):
            self.final_results[idx] = {"title": self.pre_processor.news_df.iloc[ix, 0],
                                       "link": self.pre_processor.news_df.iloc[ix, 2]}
        for idx, i in self.final_results.items():
            print(f"title: {i['title']}\n link: {i['link']}\n\n")

    def tf_idf_merge_results(self, query, num=StaticNum.DOC_RELATED_NUM.value):
        self.final_results = dict()
        qe_query = self.qe.expand_query(query, cosine_threshold=0.85)
        qe_query_vec = self.tfidf.transform([qe_query])
        qe_results = self.tf_idf_results(qe_query_vec, True)
        res = [*np.array(self.related_titles).argsort()[-num:][::-1], *qe_results.argsort()[-num:][::-1]]
        res = list(dict.fromkeys(res))
        for idx, ix in enumerate(res):
            self.final_results[idx] = {"title": self.pre_processor.news_df.iloc[ix, 0],
                                       "link": self.pre_processor.news_df.iloc[ix, 2]}

        for idx, i in self.final_results.items():
            print(f"title: {i['title']}\n link: {i['link']}\n\n")
