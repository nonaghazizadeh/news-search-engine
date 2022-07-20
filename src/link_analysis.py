import numpy as np
from src.preprocessing import *
from sklearn.preprocessing import normalize
import networkx as nx
from src.enums.enums import Path


class LinkAnalysis:
    def __init__(self, input_category, page_rank_mode=True, need_training=False):
        self.pre_processor = PreProcessing(on_title=True)
        self.pre_processor()
        self.input_category = input_category
        self.selected_df = pd.DataFrame()
        self.selected_removed_tokenized_words = []
        self.similarity_mat = np.zeros((len(self.selected_df), len(self.selected_df)), dtype=float)
        self.graph = None
        self.page_rank = None
        self.hubs = None
        self.authorities = None
        self.page_rank_mode = page_rank_mode
        self.need_training = need_training

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

    @staticmethod
    def get_top_n_news(values, n=5):
        top_n = np.argsort(list(values))[::-1][:n]
        return top_n

    def page_rank_results(self):
        for news_id in self.get_top_n_news(self.page_rank.values()):
            print(self.selected_df.iloc[news_id]['title'])
            print('-------------------------------')

    def hits_algorithm(self):
        self.hubs, self.authorities = nx.hits(self.graph)

    def hits_results(self):
        print("AUTHORITIES")
        for news_id in self.get_top_n_news(self.authorities.values()):
            print(self.selected_df.iloc[news_id]['title'])
            print('-------------------------------')
        print("HUBS")
        for news_id in self.get_top_n_news(self.hubs.values()):
            print(self.selected_df.iloc[news_id]['title'])
            print('-------------------------------')
