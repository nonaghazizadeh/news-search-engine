from enum import Enum


class Path(Enum):
    DATA_PATH = 'data/news.json'
    DATA_PATH_TRAN = 'data/news_12.json'
    NEW_STOPWORD_PATH = 'custom_requirements/new_stopwords.txt'
    STOPWORD_PATH = 'custom_requirements/new_stopwords.txt'
    PROCESSED_DATA_PATH = 'models/preprocessed_data/data.plk'
    TRAN_PROCESSED_DATA_PATH = 'models/preprocessed_data/tran_data.plk'
    CLF_PROCESSED_DATA_PATH = 'models/preprocessed_data/clf_data.plk'
    TITLE_PROCESSED_DATA_PATH = 'models/preprocessed_data/title_data.plk'
    TFIDF_PATH = 'models/tfidf_search/tfidf.pk'
    TFIDF_TRAN_PATH = 'models/tfidf_search/tfidf_tran.npz'
    FASTTEXT_DATA_PATH = 'models/fasttext_search/fasttext_data.txt'
    FASTTEXT_MODEL_PATH = 'models/fasttext_search/fasttext.bin'
    FASTTEXT_EMBEDDING_PATH = 'models/fasttext_search/fasttext_vectors_emb.json'
    TRANSFORMERS_MODEL_PATH = 'models/transformers_search/transformer_model.model'
    TRANSFORMERS_TOKENIZER_PATH = 'models/transformers_search/transformer_tokenizer'
    TRANSFORMERS_EMBEDDING_PATH = 'models/transformers_search/transformer_vectors_emb.json'
    CLASSIFICATION_LR_FASTTEXT_EMBEDDING_PATH = 'models/classification_logistic_regression_improved/fasttext/fasttext_vectors_emb.json'
    CLASSIFICATION_LR_FASTTEXT_MODEL_PATH = 'models/classification_logistic_regression_improved/fasttext/fasttext.bin'
    CLASSIFICATION_LR_PATH = 'models/classification_logistic_regression_improved/logistic_regression_model.sav'
    CLASSIFICATION_LR_RESULT_PATH = 'results/predicted_logistic_regression_improved.csv'
    CLASSIFICATION_TRANSFORMERS_PATH = 'models/classification_transformers'
    CLASSIFICATION_TRANSFORMERS_TRAINING_ARG_PATH = 'results'
    CLASSIFICATION_TRANSFORMERS_TOKENIZER_PATH = 'models/classification_transformers/transformer_tokenizer'
    CLASSIFICATION_TRANSFORMERS_RESULT_PATH = 'results/predicted_transformers.csv'
    CLUSTERING_FASTTEXT_EMBEDDING_PATH = 'models/clustering/fasttext/fasttext_vectors_emb.json'
    CLUSTERING_FASTTEXT_MODEL_PATH = 'models/clustering/fasttext/fasttext.bin'
    CLUSTERING_PATH = 'models/clustering/kmeans_clustering.pkl'
    QE_FASTTEXT_DATA_PATH = 'models/QE_fasttext/fasttext_data.txt'
    QE_FASTTEXT_MODEL_PATH = 'models/QE_fasttext/fasttext.bin'
    QE_ALL_EMBEDDING_PATH = 'models/QE_fasttext/all_words_vectors_emb_fasttext.json'
    LINK_ANALYSIS_IRAN_PATH = 'models/link_analysis/graph_iran.gml'
    LINK_ANALYSIS_WORLD_PATH = 'models/link_analysis/graph_world.gml'
    LINK_ANALYSIS_ECONOMY_PATH = 'models/link_analysis/graph_economy.gml'
    LINK_ANALYSIS_SOCIETY_PATH = 'models/link_analysis/graph_society.gml'
    LINK_ANALYSIS_CITY_PATH = 'models/link_analysis/graph_city.gml'
    LINK_ANALYSIS_DISTRICT_PATH = 'models/link_analysis/graph_district.gml'
    LINK_ANALYSIS_LIFE_PATH = 'models/link_analysis/graph_life.gml'
    LINK_ANALYSIS_IT_PATH = 'models/link_analysis/graph_it.gml'
    LINK_ANALYSIS_SCIENCE_PATH = 'models/link_analysis/graph_science.gml'
    LINK_ANALYSIS_CULTURE_PATH = 'models/link_analysis/graph_culture.gml'
    LINK_ANALYSIS_SPORT_PATH = 'models/link_analysis/graph_sport.gml'


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
    CLASSIFICATION_NB_TEST_SIZE = 0.3
    CLASSIFICATION_NB_RANDOM_STATE = 0
    FASTTEXT_MIN_COUNT = 4


class ModelName(Enum):
    MODEL_NAME = 'SajjadAyoubi/distil-bigbird-fa-zwnj'


class MapCategoryToPath(Enum):
    CategoryToPath = {
        'سیاسی': Path.LINK_ANALYSIS_IRAN_PATH.value,
        'جهان': Path.LINK_ANALYSIS_WORLD_PATH.value,
        'اقتصاد': Path.LINK_ANALYSIS_ECONOMY_PATH.value,
        'جامعه': Path.LINK_ANALYSIS_SOCIETY_PATH.value,
        'شهر': Path.LINK_ANALYSIS_CITY_PATH.value,
        'محله': Path.LINK_ANALYSIS_DISTRICT_PATH.value,
        'زندگی': Path.LINK_ANALYSIS_LIFE_PATH.value,
        'فناوری اطلاعات': Path.LINK_ANALYSIS_IT_PATH.value,
        'دانش': Path.LINK_ANALYSIS_SCIENCE_PATH.value,
        'فرهنگ و هنر': Path.LINK_ANALYSIS_CULTURE_PATH.value,
        'ورزش': Path.LINK_ANALYSIS_SPORT_PATH.value
    }
