from enums.enums import Path

import json
import pandas as pd
from hazm import *
import tqdm
import codecs


class PreProcessing:
    def __init__(self, is_clf_tran=False, is_tran=False, on_title=False, need_preprocessing=False):
        self.normalizer = Normalizer()
        self.stemmer = Stemmer()
        self.lemmatizer = Lemmatizer()
        self.new_stopwords = \
            [self.normalizer.normalize(x.strip()) for x in codecs.open(
                Path.NEW_STOPWORD_PATH.value, 'r', 'utf-8').readlines()]
        self.stopwords = \
            [self.normalizer.normalize(x.strip()) for x in codecs.open(
                Path.STOPWORD_PATH.value, 'r', 'utf-8').readlines()]
        self.on_title = on_title
        self.need_preprocessing = need_preprocessing
        self.is_clf_tran = is_clf_tran
        self.is_tran = is_tran
        self.tokenized_words = list()
        self.news_dict = dict()
        self.news_df = pd.DataFrame()

    def __call__(self):
        if self.need_preprocessing:
            self.load_data()
            self.normalize_data()
            self.tokenizing_words()
            self.remove_stopwords()
            self.lemmatize_data()
            self.make_clean_data_content()
            self.save_news_df()
        else:
            self.load_news_df()
            self.tokenizing_words()

    def load_data(self):
        path = Path.DATA_PATH.value if not self.is_tran else Path.DATA_PATH_TRAN.value
        with open(path, "r", encoding="utf-8") as text_file:
            self.news_dict = json.loads(text_file.read())

    def normalize_data(self):
        normalized_news_dict = {}
        for idx, value in tqdm.tqdm(self.news_dict.items()):
            if self.on_title:
                normalized_news_dict[idx] = {"title": self.normalizer.normalize(value['title']),
                                             "subject": value["subject"],
                                             "content": value['content']}
            else:
                normalized_news_dict[idx] = {"title": value['title'], "subject": value["subject"],
                                             "content": self.normalizer.normalize(value['content'])}
        self.news_df = pd.DataFrame.from_dict(normalized_news_dict, orient='index')

    def tokenizing_words(self):
        if self.on_title:
            self.tokenized_words = [word_tokenize(_) for _ in self.news_df.title]
        else:
            self.tokenized_words = [word_tokenize(_) for _ in self.news_df.content]

    def remove_stopwords(self):
        removed_tokenized_words = []
        for per_content_words in self.tokenized_words:
            words = []
            for word in per_content_words:
                if word not in self.stopwords + self.new_stopwords:
                    words.append(word)
            removed_tokenized_words.append(words)

        self.news_df['word_tokenize'] = removed_tokenized_words

    def get_lemma_set(self, tok, opt=1):
        if opt == 1:
            return self.stemmer.stem(tok)
        if opt == 2:
            return self.lemmatizer.lemmatize(tok)

    def lemmatize_data(self):
        opt = 2
        lemmatize_stemming_words = []
        for per_content_words in self.news_df.word_tokenize:
            words = []
            for word in per_content_words:
                words.append(self.get_lemma_set(word, opt))
            lemmatize_stemming_words.append(words)
        self.news_df['word_lemmatize'] = lemmatize_stemming_words

    def make_clean_data_content(self):
        if self.is_clf_tran:
            words = []
            for row_words in self.news_df['word_lemmatize']:
                words.append(' '.join(row_words))
            self.news_df['clean_text'] = words
        else:
            words = []
            persian_numbers = ['۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹']
            for row_words in self.news_df['word_lemmatize']:
                final_words = ','.join(row_words)
                final_words = final_words.replace('-', '')
                for persian_num in persian_numbers:
                    if persian_num in list(final_words):
                        final_words.replace(persian_num, '')
                words.append(final_words)
            self.news_df['clean_keyword'] = words
        if self.on_title:
            self.news_df = self.news_df.drop(['word_lemmatize'], axis=1)
        else:
            self.news_df = self.news_df.drop(['word_tokenize', 'word_lemmatize'], axis=1)

    def save_news_df(self):
        if self.is_clf_tran:
            self.news_df.to_pickle(Path.CLF_PROCESSED_DATA_PATH.value)
        elif self.is_tran:
            self.news_df.to_pickle(Path.TRAN_PROCESSED_DATA_PATH.value)
        elif self.on_title:
            self.news_df.to_pickle(Path.TITLE_PROCESSED_DATA_PATH.value)
        else:
            self.news_df.to_pickle(Path.PROCESSED_DATA_PATH.value)

    def load_news_df(self):
        if self.is_clf_tran:
            self.news_df = pd.read_pickle(Path.CLF_PROCESSED_DATA_PATH.value)
        elif self.is_tran:
            self.news_df = pd.read_pickle(Path.TRAN_PROCESSED_DATA_PATH.value)
        elif self.on_title:
            self.news_df = pd.read_pickle(Path.TITLE_PROCESSED_DATA_PATH.value)
        else:
            self.news_df = pd.read_pickle(Path.PROCESSED_DATA_PATH.value)
