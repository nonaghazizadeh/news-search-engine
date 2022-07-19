from enum import Enum


class Path(Enum):
    DATA_PATH = '../data/news.json'
    NEW_STOPWORD_PATH = '../custom_requirements/new_stopwords.txt'
    STOPWORD_PATH = '../custom_requirements/new_stopwords.txt'
    PROCESSED_DATA_PATH = '../models/preprocessed_data/data.plk'
    TFIDF_PATH = '../models/tfidf_search/tfidf.pk'
    TFIDF_TRAN_PATH = '../models/tfidf_search/tfidf_tran.npz'
    FASTTEXT_DATA_PATH = '../models/fasttext_search/fasttext_data.txt'
    FASTTEXT_MODEL_PATH = '../models/fasttext_search/fasttext.bin'
    FASTTEXT_EMBEDDING_PATH = '../models/fasttext_search/fasttext_vectors_emb.json'
    CLASSIFICATION_NB_FASTTEXT_EMBEDDING_PATH = '../models/classification_naive_bayes_improved/fasttext/fasttext_vectors_emb.json'
    CLASSIFICATION_NB_FASTTEXT_MODEL_PATH = '../models/classification_naive_bayes_improved/fasttext/fasttext.bin'
    CLASSIFICATION_NB_PATH = '../models/classification_naive_bayes_improved/naive_bayes_model.sav'
    CLASSIFICATION_NB_RESULT_PATH = '../results/predicted_naive_bayes_improved.csv'
    CLUSTERING_FASTTEXT_EMBEDDING_PATH = '../models/clustering/fasttext/fasttext_vectors_emb.json'
    CLUSTERING_FASTTEXT_MODEL_PATH = '../models/clustering/fasttext/fasttext.bin'
    CLUSTERING_PATH = '../models/clustering/kmeans_clustering.pkl'
    LINK_ANALYSIS_PATH = '../models/link_analysis/graph.gml'
    QE_FASTTEXT_DATA_PATH = '../models/QE_fasttext/fasttext_data.txt'
    QE_FASTTEXT_MODEL_PATH = '../models/QE_fasttext/fasttext.bin'
    QE_ALL_EMBEDDING_PATH = '../models/QE_fasttext/all_words_vectors_emb_fasttext.json'


class StaticNum(Enum):
    DOC_RELATED_NUM = 10
