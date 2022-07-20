from src.enums.enums import StaticNum, Path
from src.query_expansion import QueryExpansion

import pickle
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.preprocessing import PreProcessing


class TfidfSearch:
    def __init__(self, query, should_expand_query=True, need_training=False):
        self.pre_processor = PreProcessing()
        self.pre_processor()
        self.query = query
        self.should_expand_query = should_expand_query
        if self.should_expand_query:
            self.qe = QueryExpansion(self.query.split())
            self.qe()
        self.tfidf = None
        self.tfidf_tran = None
        self.need_training = need_training
        self.query_vec = list()
        self.related_titles = list()

    def __call__(self):
        if self.need_training:
            self.create_tf_idf_doc_term_matrix()
            self.save_tf_idf()
        self.load_tf_idf()
        self.calculate_query_tf_idf()
        self.tf_idf_results()
        if self.should_expand_query:
            self.tf_idf_merge_results()
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

    def calculate_query_tf_idf(self):
        self.query_vec = self.tfidf.transform([self.query])

    def tf_idf_results(self, query_vec=None, is_qe=False):
        if is_qe:
            return cosine_similarity(self.tfidf_tran, query_vec).reshape((-1,))
        else:
            self.related_titles = cosine_similarity(self.tfidf_tran, self.query_vec).reshape((-1,))

    def tf_idf_print_results(self):
        for idx, title in enumerate(np.array(self.related_titles).argsort()[-10:][::-1]):
            print(f"{idx + 1}\t{self.pre_processor.news_df.iloc[title, 0]}")

    def tf_idf_merge_results(self, num=StaticNum.DOC_RELATED_NUM.value):
        qe_query = self.qe.expand_query(0.85)
        qe_query_vec = self.tfidf.transform([qe_query])
        qe_results = self.tf_idf_results(qe_query_vec, True)
        res = [*np.array(self.related_titles).argsort()[-num:][::-1], *qe_results.argsort()[-num:][::-1]]
        res = list(dict.fromkeys(res))
        for idx, title in enumerate(res):
            print(f"{idx + 1}\t{self.pre_processor.news_df.iloc[title, 0]}")
