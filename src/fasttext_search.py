from src.preprocessing import PreProcessing
from src.query_expansion import QueryExpansion
from src.enums.enums import StaticNum, Path
from src.requirements.numpy_encoder import NumpyEncoder

import json
import fasttext
import tqdm
import numpy as np


class FasttextSearch:
    def __init__(self, qe_ins, need_training=False):
        self.pre_processor = PreProcessing()
        self.pre_processor()
        self.numpy_encoder = NumpyEncoder
        self.qe = qe_ins
        self.data = ''
        self.model = None
        self.docs_embedding = dict()
        self.query_embedding = list()
        self.related_titles = dict()
        self.final_results = dict()
        if need_training:
            self.create_fasttext_data()
            self.save_fasttext_data()
            self.train_fasttext()
            self.save_fasttext()
            self.calculate_doc_embedding()
            self.save_doc_embedding()
        self.load_fasttext()
        self.load_doc_embedding()

    def __call__(self, query, qe_en):
        self.calculate_query_embedding(query)
        self.fasttext_results()
        if qe_en:
            self.fasttext_merge_results()
        else:
            self.fasttext_print_results()

    def create_fasttext_data(self):
        tokens_list = self.pre_processor.news_df.clean_keyword.tolist()
        for doc in tqdm.tqdm(tokens_list):
            self.data += ' '.join(doc.split(",")) + '\n'

    def save_fasttext_data(self):
        with open(Path.FASTTEXT_DATA_PATH.value, 'w') as text_file:
            text_file.write(self.data)

    def train_fasttext(self):
        self.model = fasttext.train_unsupervised(Path.FASTTEXT_DATA_PATH.value, model='skipgram',
                                                 minCount=StaticNum.FASTTEXT_MIN_COUNT.value)

    def save_fasttext(self):
        self.model.save_model(Path.FASTTEXT_MODEL_PATH.value)

    def load_fasttext(self):
        self.model = fasttext.load_model(Path.FASTTEXT_MODEL_PATH.value)

    def calculate_doc_embedding(self):
        for idx, doc in tqdm.tqdm(enumerate(self.pre_processor.news_df.clean_keyword)):
            doc_sum = np.zeros(100)
            for word in doc.split(','):
                doc_sum = np.sum([doc_sum, self.model[word]], axis=0)
            self.docs_embedding[idx] = doc_sum / len(doc.split(','))

    def save_doc_embedding(self):
        with open(Path.FASTTEXT_EMBEDDING_PATH.value, 'w', encoding="utf-8") as f:
            json.dump(self.docs_embedding, f, cls=NumpyEncoder)

    def load_doc_embedding(self):
        with open(Path.FASTTEXT_EMBEDDING_PATH.value, 'r', encoding="utf-8") as f:
            self.docs_embedding = json.loads(f.read())

    def calculate_query_embedding(self, query):
        query_sum = np.zeros(100)
        query_words = query.split()
        for q_word in query_words:
            query_sum = np.sum([query_sum, self.model[q_word]], axis=0)
        self.query_embedding = query_sum / len(query_words)

    def fasttext_results(self, query_embedding=None, is_qe=False):
        query_embedding = query_embedding if is_qe else self.query_embedding
        docs_cosine_similarity = {}
        for idx, doc_embedding in self.docs_embedding.items():
            docs_cosine_similarity[idx] = np.dot(np.array(doc_embedding), query_embedding) / (
                    np.linalg.norm(np.array(doc_embedding)) * np.linalg.norm(query_embedding))
        docs_cosine_similarity = reversed(sorted(docs_cosine_similarity.items(), key=lambda x: x[1]))
        docs_cosine_similarity = dict(docs_cosine_similarity)
        if is_qe:
            return docs_cosine_similarity
        else:
            self.related_titles = docs_cosine_similarity

    def find_non_related_docs_avg(self, num=StaticNum.DOC_RELATED_NUM.value):
        doc_sum = np.zeros(100)
        for idx, doc_id in enumerate((list(self.related_titles.items()))[-10:]):
            doc_sum = np.sum([doc_sum, self.docs_embedding[doc_id[0]]], axis=0)
        avg_non_related = doc_sum / num
        return avg_non_related

    def find_related_docs_avg(self, num=StaticNum.DOC_RELATED_NUM.value):
        doc_sum = np.zeros(100)
        for idx, doc_id in enumerate((list(self.related_titles.items()))[:10]):
            doc_sum = np.sum([doc_sum, self.docs_embedding[doc_id[0]]], axis=0)
        avg_related = doc_sum / num
        return avg_related

    def fasttext_print_results(self):
        self.final_results = dict()
        for idx, doc_id in enumerate((list(self.related_titles.items()))[:10]):
            self.final_results[idx] = {"title": self.pre_processor.news_df.iloc[int(doc_id[0])].title,
                                       "link": self.pre_processor.news_df.iloc[int(doc_id[0])].link}
        for idx, i in self.final_results.items():
            print(f"title: {i['title']}\n link: {i['link']}\n\n")

    def fasttext_merge_results(self, num=StaticNum.DOC_RELATED_NUM.value):
        self.final_results = dict()
        nr_doc_avg = self.find_non_related_docs_avg()
        r_doc_avg = self.find_related_docs_avg()
        new_query_embedding = self.qe.expand_query_rocchio(self.query_embedding, nr_doc_avg, r_doc_avg)
        qe_results = self.fasttext_results(new_query_embedding, True)
        res = [*(list(qe_results.items()))[:num], *(list(self.related_titles.items()))[:num]]
        res = list(dict.fromkeys(res))
        for idx, doc_id in enumerate(res):
            self.final_results[idx] = {"title": self.pre_processor.news_df.iloc[int(doc_id[0])].title,
                                       "link": self.pre_processor.news_df.iloc[int(doc_id[0])].link}
        for idx, i in self.final_results.items():
            print(f"title: {i['title']}\n link: {i['link']}\n\n")
