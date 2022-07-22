from src.preprocessing import PreProcessing
from src.query_expansion import QueryExpansion
from src.enums.enums import StaticNum

import pandas as pd


class BooleanSearch:
    def __init__(self, query, should_expand_query=True):
        self.pre_processor = PreProcessing()
        self.pre_processor()
        self.query_words = query.split()
        self.should_expand_query = should_expand_query
        if self.should_expand_query:
            self.qe = QueryExpansion(self.query_words)
            self.qe()
        self.boolean_df = pd.DataFrame()
        self.related_titles = list()
        self.final_results = dict()

    def __call__(self):
        self.create_boolean_retrieval_matrix()
        self.boolean_retrieval_result()
        if not self.should_expand_query:
            self.boolean_print_results()
        else:
            self.boolean_merge_results()

    def create_boolean_retrieval_matrix(self, query=None, is_qe=False):
        self.query_words = query if is_qe else self.query_words
        boolean_retrieval = [[0 for _ in range(len(self.query_words))] for __ in
                             range(len(self.pre_processor.news_df))]
        for i in range(len(self.pre_processor.news_df)):
            keywords = self.pre_processor.news_df.iloc[i].clean_keyword
            for j, q_word in enumerate(self.query_words):
                if q_word in keywords.split(","):
                    boolean_retrieval[i][j] = 1
        self.boolean_df = pd.DataFrame(boolean_retrieval, columns=self.query_words)

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
        for idx, ix in enumerate(self.related_titles[:num]):
            self.final_results[idx] = {"title": self.pre_processor.news_df.iloc[ix, 0],
                                      "link": self.pre_processor.news_df.iloc[ix, 2]}

        for idx, i in self.final_results.items():
            print(f"title: {i['title']}\n link: {i['link']}\n\n")

    def boolean_merge_results(self, num=StaticNum.DOC_RELATED_NUM.value):
        new_query = self.qe.expand_query(0.7)
        self.create_boolean_retrieval_matrix(new_query.split(), True)
        qe_results = self.boolean_retrieval_result(True)
        res = [*self.related_titles[:num], *qe_results[:num]]
        res = list(dict.fromkeys(res))
        for idx, ix in enumerate(res):
            self.final_results[idx] = {"title": self.pre_processor.news_df.iloc[ix, 0],
                                      "link": self.pre_processor.news_df.iloc[ix, 2]}
        for idx, i in self.final_results.items():
            print(f"title: {i['title']}\n link: {i['link']}\n\n")
