from src.preprocessing import PreProcessing
from src.enums.enums import Path, StaticNum

import json
import numpy as np
import pickle
import csv
import fasttext
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import f1_score, confusion_matrix, accuracy_score


class ClassificationNaiveBayes:
    def __init__(self, text_for_getting_category=None, prediction_mode=False, need_training=False):
        self.pre_processor = PreProcessing()
        self.pre_processor()
        self.model = None
        self.fasttext_model = None
        self.fasttext_docs_embedding = None
        self.target_categories = list()
        self.x_train = None
        self.x_test = None
        self.y_train = None
        self.y_test = None
        self.text_for_getting_category = text_for_getting_category
        self.prediction_mode = prediction_mode
        self.need_training = need_training
        self.confusion_matrix_evaluate = 0
        self.accuracy_score_evaluate = 0
        self.f1_score_evaluate = 0

    def __call__(self):
        if self.prediction_mode:
            self.convert_subject_to_id()
            if self.need_training:
                self.load_fasttext_embedding()
                x, y = self.create_x_y_classification()
                self.split_data_train_test(x, y)
                self.fit_naive_bayes()
                self.save_naive_bayes()
            self.load_fasttext()
            self.load_naive_bayes()
            embedding = [self.fasttext_model[self.text_for_getting_category]]
            subject_id = self.predict_naive_bayes(embedding)
            return self.target_categories[subject_id[0]]
        else:
            self.load_fasttext_embedding()
            x, y = self.create_x_y_classification()
            self.split_data_train_test(x, y)
            if self.need_training:
                self.fit_naive_bayes()
                self.save_naive_bayes()
            self.load_naive_bayes()
            y_predictions = self.predict_naive_bayes(self.x_test)
            self.evaluate_naive_bayes(y_predictions)

    def load_fasttext_embedding(self):
        with open(Path.CLASSIFICATION_NB_FASTTEXT_EMBEDDING_PATH.value, 'r',
                  encoding="utf-8") as f:
            self.fasttext_docs_embedding = json.loads(f.read())

    def load_fasttext(self):
        self.fasttext_model = fasttext.load_model(Path.CLASSIFICATION_NB_FASTTEXT_MODEL_PATH.value)

    def convert_subject_to_id(self):
        self.target_categories = self.pre_processor.news_df['subject'].unique()
        self.target_categories = self.target_categories.tolist()

    def create_x_y_classification(self):
        self.convert_subject_to_id()
        self.pre_processor.news_df['subject_id'] = self.pre_processor.news_df['subject'].factorize()[0]
        x = list()
        for k, v in self.fasttext_docs_embedding.items():
            x.append(v)
        y = np.array(self.pre_processor.news_df.subject_id.values)
        return x, y

    def split_data_train_test(self, x, y, shuffle=True):
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(x, y,
                                                                                test_size=StaticNum.CLASSIFICATION_NB_TEST_SIZE.value,
                                                                                random_state=StaticNum.CLASSIFICATION_NB_RANDOM_STATE.value,
                                                                                shuffle=shuffle)

    def fit_naive_bayes(self):
        self.model = GaussianNB().fit(self.x_train, self.y_train)

    def save_naive_bayes(self):
        with open(Path.CLASSIFICATION_NB_PATH.value, 'wb') as f:
            pickle.dump(self.model, f)

    def load_naive_bayes(self):
        with open(Path.CLASSIFICATION_NB_PATH.value, 'rb') as f:
            self.model = pickle.load(f)

    def predict_naive_bayes(self, x):
        y = self.model.predict(x)
        return y

    def visualize_naive_bayes_csv(self, y_predicted):
        test_comparison = []
        for idx, x in enumerate(self.x_test):
            predicted_res = self.target_categories[y_predicted[idx]]
            true_res = self.target_categories[self.y_test[idx]]
            test_comparison.append([true_res, predicted_res])
        with open(Path.CLASSIFICATION_NB_RESULT_PATH.value, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["true_label", "predicted_label"])
            for row in test_comparison:
                writer.writerow(row)

    def evaluate_naive_bayes(self, y_predicted):
        self.confusion_matrix_evaluate = confusion_matrix(self.y_test, y_predicted)
        self.accuracy_score_evaluate = accuracy_score(self.y_test, y_predicted) * 100
        self.f1_score_evaluate = f1_score(self.y_test, y_predicted, average='macro')

        print(f"accuracy score: {self.confusion_matrix_evaluate}")
        print('-----------------------------------------------------------------------')
        print(f"f1 score: {self.accuracy_score_evaluate}")
        print('-----------------------------------------------------------------------')
        print(f"confusion matrix:\n {self.f1_score_evaluate}")
