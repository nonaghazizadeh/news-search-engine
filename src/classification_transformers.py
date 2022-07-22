from src.preprocessing import PreProcessing
from src.requirements.news_dataset import NewsDataset
from src.enums.enums import StaticNum, Path, ModelName

import csv
import numpy as np
from transformers import BigBirdModel, AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, confusion_matrix, accuracy_score


class ClassificationTransformers:
    def __init__(self, text_for_getting_category=None, need_training=False, prediction_mode=True):
        self.pre_processor = PreProcessing(is_clf_tran=True)
        self.pre_processor()
        self.model = None
        self.tokenizer = None
        self.target_categories = list()
        self.x_train = None
        self.x_val = None
        self.x_test = None
        self.y_train = None
        self.y_val = None
        self.y_test = None
        self.train_dataset = None
        self.val_dataset = None
        self.test_dataset = None
        self.text_for_getting_category = text_for_getting_category
        self.need_training = need_training
        self.prediction_mode = prediction_mode
        self.confusion_matrix_evaluate = 0
        self.accuracy_score_evaluate = 0
        self.f1_score_evaluate = 0
        self.final_results = ''

    def __call__(self):
        self.convert_subject_to_id()
        if self.prediction_mode:
            if self.need_training:
                x, y = self.create_x_y_classification()
                self.split_data_train_test_val(x, y)
                self.encoding_and_create_dataset()
                self.train_dataset()
                self.save_transformer_trainer()
            self.load_transformer()
            subject_id = self.predict(self.text_for_getting_category)
            self.final_results = self.target_categories[subject_id[0]]
        else:
            x, y = self.create_x_y_classification()
            self.split_data_train_test_val(x, y)
            if self.need_training:
                self.encoding_and_create_dataset()
                self.train_dataset()
                self.save_transformer_trainer()
            self.load_transformer()
            y_predictions = self.predict()
            self.evaluate_transformer_classification(y_predictions)

    def convert_subject_to_id(self):
        self.target_categories = self.pre_processor.news_df['subject'].unique()
        self.target_categories = self.target_categories.tolist()
        self.pre_processor.news_df['subject_id'] = self.pre_processor.news_df['subject'].factorize()[0]

    def create_x_y_classification(self):
        pre_processed_news_dict = self.pre_processor.news_df.apply(lambda ix: ix.to_dict(), axis=1)
        x = []
        for k, v in pre_processed_news_dict.items():
            x.append(v['clean_text'])
        y = np.array(self.pre_processor.news_df.subject_id.values)
        return x, y

    def split_data_train_test_val(self, x, y, shuffle=True):
        self.x_train, x_test_val, self.y_train, y_test_val = train_test_split(x, y,
                                                                              test_size=StaticNum.CLASSIFICATION_TRANSFORMERS_TEST_SIZE.value,
                                                                              random_state=StaticNum.CLASSIFICATION_TRANSFORMERS_RANDOM_STATE.value,
                                                                              shuffle=shuffle)
        self.x_val, self.x_test, self.y_val, self.y_test = train_test_split(x_test_val, y_test_val,
                                                                            test_size=StaticNum.CLASSIFICATION_TRANSFORMERS_VAL_SIZE.value,
                                                                            random_state=StaticNum.CLASSIFICATION_TRANSFORMERS_RANDOM_STATE.value,
                                                                            shuffle=shuffle)

    def encoding_and_create_dataset(self):
        train_encodings = self.tokenizer(self.x_train, truncation=True, padding=True)
        val_encodings = self.tokenizer(self.x_val, truncation=True, padding=True)
        test_encodings = self.tokenizer(self.x_test, truncation=True, padding=True)
        self.train_dataset = NewsDataset(train_encodings, self.y_train)
        self.val_dataset = NewsDataset(val_encodings, self.y_val)
        self.test_dataset = NewsDataset(test_encodings, self.y_test)

    def train_transformer_classification(self):
        self.model = BigBirdModel.from_pretrained(ModelName.MODEL_NAME.value,
                                                  block_size=StaticNum.CLASSIFICATION_TRANSFORMERS_BLOCK_SIZE.value)
        self.tokenizer = AutoTokenizer.from_pretrained(ModelName.MODEL_NAME.value)
        transformer_model = AutoModelForSequenceClassification.from_pretrained(ModelName.MODEL_NAME.value,
                                                                               num_labels=StaticNum.CLASSIFICATION_TRANSFORMERS_LABELS_NUM.value)
        training_args = TrainingArguments(
            output_dir=Path.CLASSIFICATION_TRANSFORMERS_TRAINING_ARG_PATH.value,
            per_device_train_batch_size=StaticNum.CLASSIFICATION_TRANSFORMERS_BATCH_SIZE.value,
            per_device_eval_batch_size=StaticNum.CLASSIFICATION_TRANSFORMERS_BATCH_SIZE.value,
            num_train_epochs=StaticNum.CLASSIFICATION_TRANSFORMERS_EPOCH.value,
            weight_decay=StaticNum.CLASSIFICATION_TRANSFORMERS_WEIGHT_DECAY.value,
        )

        self.model = Trainer(
            model=transformer_model,
            args=training_args,
            train_dataset=self.train_dataset,
            eval_dataset=self.val_dataset
        )

        self.model.train()

    def save_transformer_trainer(self):
        self.model.save_model(Path.CLASSIFICATION_TRANSFORMERS_PATH.value)

    def load_transformer(self):
        self.model = AutoModelForSequenceClassification.from_pretrained(Path.CLASSIFICATION_TRANSFORMERS_PATH.value,
                                                                        local_files_only=True)
        self.tokenizer = AutoTokenizer.from_pretrained(Path.CLASSIFICATION_TRANSFORMERS_TOKENIZER_PATH.value,
                                                       local_files_only=True)

    def get_prediction(self, text):
        inputs = self.tokenizer(text, padding=True, truncation=True, return_tensors="pt")
        outputs = self.model(**inputs)
        probs = outputs[0].softmax(1)
        return probs.argmax().item()

    def predict(self, x_for_prediction=None):
        x_for_prediction = self.x_test if x_for_prediction is None else [x_for_prediction]
        y_predicted = []
        for idx, x in enumerate(x_for_prediction):
            y_predicted.append(self.get_prediction(x))
        return y_predicted

    def visualize_classification_transformer(self, y_predicted):
        test_comparison = []
        for idx, ix in enumerate(self.x_test):
            predicted_res = self.target_categories[y_predicted[idx]]
            true_res = self.target_categories[self.y_test[idx]]
            test_comparison.append([true_res, predicted_res])
        with open(Path.CLASSIFICATION_TRANSFORMERS_RESULT_PATH.value, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["true_label", "predicted_label"])
            for row in test_comparison:
                writer.writerow(row)

    def evaluate_transformer_classification(self, y_predicted):
        self.confusion_matrix_evaluate = confusion_matrix(self.y_test, y_predicted)
        self.accuracy_score_evaluate = accuracy_score(self.y_test, y_predicted) * 100
        self.f1_score_evaluate = f1_score(self.y_test, y_predicted, average='macro')

        print(f"accuracy score: {self.accuracy_score_evaluate}")
        print('-----------------------------------------------------------------------')
        print(f"f1 score: {self.f1_score_evaluate}")
        print('-----------------------------------------------------------------------')
        print(f"confusion matrix:\n {self.confusion_matrix_evaluate}")
