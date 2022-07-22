from src.preprocessing import PreProcessing
from src.enums.enums import Path

import networkx as nx
import numpy as np
import pandas as pd
from sklearn.preprocessing import normalize


class LinkAnalysis:
    def __init__(self, input_category, page_rank_mode=True, need_training=False):
        self.pre_processor = PreProcessing(on_title=True)
        self.pre_processor()
        self.graph = None
        self.input_category = input_category
        self.selected_df = pd.DataFrame()
        self.selected_removed_tokenized_words = list()
        self.similarity_mat = None
        self.page_rank_mode = page_rank_mode
        self.need_training = need_training
        self.page_rank = None
        self.hubs = None
        self.authorities = None
        self.pr_final_results = dict()
        self.hub_final_results = dict()
        self.auth_final_results = dict()

    def __call__(self):
        self.split_related_category_dataframe()
        if self.need_training:
            self.create_similarity_matrix()
            self.create_graph()
            self.save_graph()
        self.load_graph()
        if self.page_rank_mode:
            self.page_rank_algorithm()
            self.page_rank_results()
        else:
            self.hits_algorithm()
            self.hits_results()

    def split_related_category_dataframe(self):
        self.selected_df = self.pre_processor.news_df[self.pre_processor.news_df["subject"] == self.input_category]
        self.selected_removed_tokenized_words = self.selected_df['word_tokenize'].tolist()

    def create_similarity_matrix(self, threshold=4):
        news_num = len(self.selected_df)
        self.similarity_mat = np.zeros((news_num, news_num), dtype=float)
        words_set = [set(ls) for ls in self.selected_removed_tokenized_words]

        for i in range(news_num):
            for j in range(news_num):
                intersect_len = len(words_set[i].intersection(words_set[j]))
                if intersect_len < threshold or i == j:
                    self.similarity_mat[i][j] = 0
                else:
                    self.similarity_mat[i][j] = (intersect_len ** (1.2)) / len(words_set[i])
        self.similarity_mat = normalize(self.similarity_mat, norm='l1')

    def create_graph(self):
        self.graph = nx.from_numpy_array(self.similarity_mat)

    def save_graph(self):
        nx.write_gml(self.graph, Path.LINK_ANALYSIS_PATH.value)

    def load_graph(self):
        self.graph = nx.read_gml(Path.LINK_ANALYSIS_PATH.value)

    def page_rank_algorithm(self, alpha=0.9):
        self.page_rank = nx.pagerank(self.graph, alpha=alpha)

    def page_rank_results(self):
        for idx, news_id in enumerate(self.get_top_n_news(self.page_rank.values())):
            self.pr_final_results[idx] = {"title": self.selected_df.iloc[news_id]['title'],
                                          "link": self.selected_df.iloc[news_id]['link']}
        for idx, i in self.pr_final_results.items():
            print(f"title: {i['title']}\n link: {i['link']}\n\n")
        print(self.pr_final_results)

    def hits_algorithm(self):
        self.hubs, self.authorities = nx.hits(self.graph)

    def hits_results(self):
        print("AUTHORITIES")
        for idx, news_id in enumerate(self.get_top_n_news(self.authorities.values())):
            self.auth_final_results[idx] = {"title": self.selected_df.iloc[news_id]['title'],
                                            "link": self.selected_df.iloc[news_id]['link']}

        for idx, i in self.auth_final_results.items():
            print(f"title: {i['title']}\n link: {i['link']}\n\n")
        print('-------------------------------------')
        print("HUBS")
        for idx, news_id in enumerate(self.get_top_n_news(self.hubs.values())):
            self.hub_final_results[idx] = {"title": self.selected_df.iloc[news_id]['title'],
                                           "link": self.selected_df.iloc[news_id]['link']}

        for idx, i in self.auth_final_results.items():
            print(f"title: {i['title']}\n link: {i['link']}\n\n")

    @staticmethod
    def get_top_n_news(values, n=5):
        top_n = np.argsort(list(values))[::-1][:n]
        return top_n
