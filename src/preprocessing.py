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