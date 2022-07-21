from enum import Enum


class Path(Enum):
    DATA_PATH = '../data/news.json'
    DATA_PATH_TRAN = '../data/news_12.json'
    NEW_STOPWORD_PATH = '../custom_requirements/new_stopwords.txt'
    STOPWORD_PATH = '../custom_requirements/new_stopwords.txt'
    PROCESSED_DATA_PATH = '../models/preprocessed_data/data.plk'
    TRAN_PROCESSED_DATA_PATH = '../models/preprocessed_data/tran_data.plk'
    CLF_PROCESSED_DATA_PATH = '../models/preprocessed_data/clf_data.plk'
    TITLE_PROCESSED_DATA_PATH = '../models/preprocessed_data/title_data.plk'
    TFIDF_PATH = '../models/tfidf_search/tfidf.pk'
    TFIDF_TRAN_PATH = '../models/tfidf_search/tfidf_tran.npz'
    FASTTEXT_DATA_PATH = '../models/fasttext_search/fasttext_data.txt'
    FASTTEXT_MODEL_PATH = '../models/fasttext_search/fasttext.bin'
    FASTTEXT_EMBEDDING_PATH = '../models/fasttext_search/fasttext_vectors_emb.json'
    TRANSFORMERS_MODEL_PATH = '../models/transformers_search/transformer_model.model'
    TRANSFORMERS_TOKENIZER_PATH = '../models/transformers_search/transformer_tokenizer'
    TRANSFORMERS_EMBEDDING_PATH = '../models/transformers_search/transformer_vectors_emb.json'
    CLASSIFICATION_NB_FASTTEXT_EMBEDDING_PATH = '../models/classification_naive_bayes_improved/fasttext/fasttext_vectors_emb.json'
    CLASSIFICATION_NB_FASTTEXT_MODEL_PATH = '../models/classification_naive_bayes_improved/fasttext/fasttext.bin'
    CLASSIFICATION_NB_PATH = '../models/classification_naive_bayes_improved/naive_bayes_model.sav'
    CLASSIFICATION_NB_RESULT_PATH = '../results/predicted_naive_bayes_improved.csv'
    CLASSIFICATION_TRANSFORMERS_PATH = '../models/classification_transformers'
    CLASSIFICATION_TRANSFORMERS_TRAINING_ARG_PATH = '../results'
    CLASSIFICATION_TRANSFORMERS_TOKENIZER_PATH = '../models/classification_transformers/transformer_tokenizer'
    CLASSIFICATION_TRANSFORMERS_RESULT_PATH = '../results/predicted_transformers.csv'
    CLUSTERING_FASTTEXT_EMBEDDING_PATH = '../models/clustering/fasttext/fasttext_vectors_emb.json'
    CLUSTERING_FASTTEXT_MODEL_PATH = '../models/clustering/fasttext/fasttext.bin'
    CLUSTERING_PATH = '../models/clustering/kmeans_clustering.pkl'
    LINK_ANALYSIS_PATH = '../models/link_analysis/graph.gml'
    QE_FASTTEXT_DATA_PATH = '../models/QE_fasttext/fasttext_data.txt'
    QE_FASTTEXT_MODEL_PATH = '../models/QE_fasttext/fasttext.bin'
    QE_ALL_EMBEDDING_PATH = '../models/QE_fasttext/all_words_vectors_emb_fasttext.json'


class StaticNum(Enum):
    DOC_RELATED_NUM = 10
    CLASSIFICATION_TRANSFORMERS_EPOCH = 3
    CLASSIFICATION_TRANSFORMERS_BATCH_SIZE = 16
    CLASSIFICATION_TRANSFORMERS_LABELS_NUM = 11
    CLASSIFICATION_TRANSFORMERS_WEIGHT_DECAY = 0.01
    CLASSIFICATION_TRANSFORMERS_BLOCK_SIZE = 32
    CLASSIFICATION_TRANSFORMERS_TEST_SIZE = 0.1
    CLASSIFICATION_TRANSFORMERS_VAL_SIZE = 0.5
    CLASSIFICATION_TRANSFORMERS_RANDOM_STATE = 0
    CLASSIFICATION_NB_TEST_SIZE = 0.1
    CLASSIFICATION_NB_RANDOM_STATE = 0
    FASTTEXT_MIN_COUNT = 4


class ModelName(Enum):
    MODEL_NAME = 'SajjadAyoubi/distil-bigbird-fa-zwnj'
