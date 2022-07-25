from src.preprocessing import PreProcessing
from src.enums.enums import StaticNum

import pandas as pd


class BooleanSearch:
    def __init__(self, qe_ins):
        self.pre_processor = PreProcessing()
        self.pre_processor()
        self.qe = qe_ins
        self.boolean_df = pd.DataFrame()
        self.related_titles = list()
        self.final_results = dict()

    def __call__(self, query, qe_en):
        self.create_boolean_retrieval_matrix(query)
        self.boolean_retrieval_result()
        if qe_en:
            self.boolean_merge_results(query)
        else:
            self.boolean_print_results()

    def create_boolean_retrieval_matrix(self, query):
        query_words = query.split()
        boolean_retrieval = [[0 for _ in range(len(query_words))] for __ in
                             range(len(self.pre_processor.news_df))]
        for i in range(len(self.pre_processor.news_df)):
            keywords = self.pre_processor.news_df.iloc[i].clean_keyword
            for j, q_word in enumerate(query_words):
                if q_word in keywords.split(","):
                    boolean_retrieval[i][j] = 1
        self.boolean_df = pd.DataFrame(boolean_retrieval, columns=query_words)

    def boolean_retrieval_result(self, is_qe=False):
        converted_df = self.boolean_df.all(axis='columns')
        converted_df = converted_df.to_frame('res')
        boolean_related_docs_index = converted_df.index[converted_df['res'] == True].tolist()
        boolean_related_docs_index = list(dict.fromkeys(boolean_related_docs_index))
        if is_qe:
            return boolean_related_docs_index
        else:
            self.related_titles = boolean_related_docs_index

    def boolean_print_results(self, num=StaticNum.DOC_RELATED_NUM.value):
        self.final_results = dict()
        for idx, ix in enumerate(self.related_titles[:num]):
            self.final_results[idx] = {"title": self.pre_processor.news_df.iloc[ix, 0],
                                       "link": self.pre_processor.news_df.iloc[ix, 2]}

        for idx, i in self.final_results.items():
            print(f"title: {i['title']}\n link: {i['link']}\n\n")

    def boolean_merge_results(self, query, num=StaticNum.DOC_RELATED_NUM.value):
        self.final_results = dict()
        new_query = self.qe.expand_query(query, cosine_threshold=0.7)
        self.create_boolean_retrieval_matrix(new_query)
        qe_results = self.boolean_retrieval_result(True)
        res = [*self.related_titles[:num], *qe_results[:num]]
        res = list(dict.fromkeys(res))
        for idx, ix in enumerate(res):
            self.final_results[idx] = {"title": self.pre_processor.news_df.iloc[ix, 0],
                                       "link": self.pre_processor.news_df.iloc[ix, 2]}
        for idx, i in self.final_results.items():
            print(f"title: {i['title']}\n link: {i['link']}\n\n")
