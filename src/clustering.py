import json
from src.preprocessing import *
import random
import pickle
from sklearn.cluster import KMeans
from sklearn.metrics import davies_bouldin_score
from sklearn import metrics
import numpy as np
import fasttext
from src.enums.enums import Path


class Clustering:
    def __init__(self, text_for_get_with_same_cluster=None, prediction_mode=False, need_training=False):
        self.pre_processor = PreProcessing()
        self.pre_processor()
        self.fasttext_docs_embedding = None
        self.target_categories = list()
        self.category_dictionary = dict()
        self.final_news_dict = dict()
        self.x = list()
        self.y = list()
        self.doc_titles = list()
        self.model = None
        self.fasttext_model = None
        self.text_for_get_with_same_cluster = text_for_get_with_same_cluster
        self.need_training = need_training
        self.prediction_mode = prediction_mode
        self.rss_evaluation = 0
        self.davies_bouldin = 0
        self.silhouette = 0
        self.purity_score = 0

    def __call__(self):
        self.load_fasttext_embedding()
        self.prepare_documents_and_categories()
        self.create_x_y_clustering()
        if self.need_training:
            self.fit_kmeans_clustering()
            self.save_kmeans_model()
        y_predicted = self.predict_kmeans_model(self.x)
        self.load_kmeans_model()
        if self.prediction_mode:
            self.load_fasttext()
            embedding = [self.fasttext_model[self.text_for_get_with_same_cluster]]
            cluster_num = self.predict_kmeans_model(embedding)
            return self.samples_from_cluster(y_predicted, cluster_num[0])
        else:
            self.print_clusters(y_predicted)
            self.evaluate_clustering(y_predicted)

    def load_fasttext_embedding(self):
        with open(Path.CLUSTERING_FASTTEXT_EMBEDDING_PATH.value, 'r', encoding="utf-8") as f:
            self.fasttext_docs_embedding = json.loads(f.read())

    def load_fasttext(self):
        self.fasttext_model = fasttext.load_model(Path.CLUSTERING_FASTTEXT_MODEL_PATH.value)

    def prepare_documents_and_categories(self):
        self.final_news_dict = self.pre_processor.news_df.to_dict('index')
        self.target_categories = self.pre_processor.news_df['subject'].unique()
        self.target_categories = self.target_categories.tolist()
        category_dictionary_reverted = dict(enumerate(self.target_categories))
        self.category_dictionary = dict((v, k) for k, v in category_dictionary_reverted.items())

    def create_x_y_clustering(self):
        doc_num = {_: 0 for _ in self.category_dictionary.values()}
        shuffled_data = random.sample(sorted(self.final_news_dict), len(self.final_news_dict))

        for i in tqdm.tqdm(range(0, len(shuffled_data))):
            doc = shuffled_data[i]
            if self.final_news_dict[doc]['subject'] in self.category_dictionary:
                doc_num[self.category_dictionary[self.final_news_dict[doc]['subject']]] += 1
                self.y.append(self.category_dictionary[self.final_news_dict[doc]['subject']])
                self.x.append(self.fasttext_docs_embedding[doc])
                self.doc_titles.append(self.final_news_dict[doc]['title'])

    def fit_kmeans_clustering(self, n_clusters=11, n_init=50, max_iter=1000, tol=1e-8):
        self.model = KMeans(n_clusters=n_clusters, n_init=n_init, max_iter=max_iter, tol=tol).fit(self.x)

    def save_kmeans_model(self):
        pickle.dump(self.model, open(Path.CLUSTERING_PATH.value, "wb"))

    def load_kmeans_model(self):
        self.model = pickle.load(open(Path.CLUSTERING_PATH.value, "rb"))

    def predict_kmeans_model(self, x):
        y = self.model.predict(x)
        return y

    def samples_from_cluster(self, y_predicted, category_id, k=5):
        c = 0
        ls = []
        for predicted_category, doc_title in zip(y_predicted, self.doc_titles):
            if predicted_category == category_id:
                ls.append(doc_title)
                c += 1
            else:
                continue
            if c == k:
                break
        return ls

    def evaluate_clustering(self, y_predicted):
        self.rss_evaluation = self.model.inertia_
        self.davies_bouldin = davies_bouldin_score(self.x, y_predicted)
        self.silhouette = metrics.silhouette_score(self.x, y_predicted)
        contin_matrix = metrics.cluster.contingency_matrix(self.y, y_predicted)
        self.purity_score = np.sum(np.amax(contin_matrix, axis=0)) / np.sum(contin_matrix)
        print(f'RSS = {self.rss_evaluation}')
        print(f'Davies Bouldin score = {self.davies_bouldin}')
        print(f'Silhouette score = {self.silhouette}')
        print(f'Purity score = {self.purity_score}')

    @staticmethod
    def print_clusters(y_predicted):
        for i in range(0, 11):
            print(f'cluster {i}\t:   {y_predicted.tolist().count(i)}')
        print('-----------------------------------------------------')
