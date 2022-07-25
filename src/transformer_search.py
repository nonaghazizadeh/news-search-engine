from src.enums.enums import StaticNum, Path, ModelName
from src.preprocessing import PreProcessing
from src.requirements.numpy_encoder import NumpyEncoder

import tqdm
import json
import numpy as np
from transformers import BigBirdModel, AutoTokenizer


class TransformerSearcher:
    def __init__(self, qe_ins, need_training=False):
        self.numpy_encoder = NumpyEncoder
        self.pre_processor = PreProcessing(is_tran=True)
        self.pre_processor()
        self.qe = qe_ins
        self.model = None
        self.tokenizer = None
        self.need_training = need_training
        self.docs_embedding = dict()
        self.query_vec = list()
        self.related_titles = dict()
        self.final_results = dict()
        if self.need_training:
            self.save_transformer_pretrained_model()
            self.create_doc_embedding_avg_transformer()
            self.save_transformer_doc_embedding_avg()
        self.load_transformer_pretrained_model()
        self.load_transformer_doc_embedding_avg()

    def __call__(self, query, qe_en):
        self.transformer_query_embedding(query)
        self.transformers_results()
        if qe_en:
            self.transformer_merge_results()
        else:
            self.transformer_print_results()

    def save_transformer_pretrained_model(self, block_size=32):
        self.model = BigBirdModel.from_pretrained(ModelName.MODEL_NAME.value, block_size=block_size)
        self.tokenizer = AutoTokenizer.from_pretrained(ModelName.MODEL_NAME.value)
        self.model.save_pretrained(Path.TRANSFORMERS_MODEL_PATH.value)
        self.tokenizer.save_pretrained(Path.TRANSFORMERS_TOKENIZER_PATH.value)

    def load_transformer_pretrained_model(self):
        self.model = BigBirdModel.from_pretrained(Path.TRANSFORMERS_MODEL_PATH.value, local_files_only=True)
        self.tokenizer = AutoTokenizer.from_pretrained(Path.TRANSFORMERS_TOKENIZER_PATH.value, local_files_only=True)

    def create_doc_embedding_avg_transformer(self):
        docs_embedding_tran = {}
        for idx, doc in tqdm.tqdm(enumerate(self.pre_processor.news_df.clean_keyword)):
            text = ' '.join(doc.split(','))
            tokens = self.tokenizer(text, return_tensors='pt')
            try:
                output = self.model(**tokens)
            except Exception as e:
                text = ' '.join(doc.split(',')[:1000])
                tokens = self.tokenizer(text, return_tensors='pt')
                output = self.model(**tokens)
            docs_embedding_tran[idx] = output[0][0].detach().numpy()

        for k, v in docs_embedding_tran.items():
            tran_sum = np.zeros(768)
            for idx, word_embedding in enumerate(v):
                tran_sum = np.sum([tran_sum, docs_embedding_tran[k][idx]], axis=0)
            self.docs_embedding[k] = tran_sum / len(docs_embedding_tran[k])

    def save_transformer_doc_embedding_avg(self):
        with open(Path.TRANSFORMERS_EMBEDDING_PATH.value, 'w', encoding="utf-8") as f:
            json.dump(self.docs_embedding, f, cls=self.numpy_encoder)

    def load_transformer_doc_embedding_avg(self):
        with open(Path.TRANSFORMERS_EMBEDDING_PATH.value, 'r', encoding="utf-8") as f:
            self.docs_embedding = json.loads(f.read())
        print(len(self.docs_embedding))

    def transformer_query_embedding(self, query):
        q_tokens_tran = self.tokenizer(query, return_tensors='pt')
        q_output_tran = self.model(**q_tokens_tran)
        query_embedding_tran = q_output_tran[0][0].detach().numpy()
        qsum_tran = np.zeros(768)
        for q_idx, q_word in enumerate(query_embedding_tran):
            qsum_tran = np.sum([qsum_tran, np.array(query_embedding_tran[q_idx])], axis=0)
        self.query_vec = qsum_tran / len(query_embedding_tran)

    def transformers_results(self, query_embedding=None, is_qe=False):
        query_embedding = query_embedding if is_qe else self.query_vec
        docs_cosine_similarity_tran = {}
        for idx, doc_embedding in self.docs_embedding.items():
            docs_cosine_similarity_tran[idx] = np.dot(doc_embedding, query_embedding) / (
                    np.linalg.norm(doc_embedding) * np.linalg.norm(query_embedding))

        docs_cosine_similarity_tran = reversed(sorted(docs_cosine_similarity_tran.items(), key=lambda x: x[1]))
        docs_cosine_similarity_tran = dict(docs_cosine_similarity_tran)
        if is_qe:
            return docs_cosine_similarity_tran
        else:
            self.related_titles = docs_cosine_similarity_tran

    def transformer_find_non_related_docs_avg(self, num=StaticNum.DOC_RELATED_NUM.value):
        tran_sum = np.zeros(768)
        for idx, doc_id in enumerate((list(self.related_titles.items()))[-10:]):
            tran_sum = np.sum([tran_sum, self.docs_embedding[doc_id[0]]], axis=0)
        avg_non_related = tran_sum / num
        return avg_non_related

    def transformer_find_related_docs_avg(self, num=StaticNum.DOC_RELATED_NUM.value):
        tran_sum = np.zeros(768)
        for idx, doc_id in enumerate((list(self.related_titles.items()))[:10]):
            tran_sum = np.sum([tran_sum, self.docs_embedding[doc_id[0]]], axis=0)
        avg_related = tran_sum / num
        return avg_related

    def transformer_print_results(self):
        self.final_results = dict()
        for idx, doc_id in enumerate((list(self.related_titles.items()))[:10]):
            self.final_results[idx] = {"title": self.pre_processor.news_df.iloc[int(doc_id[0])].title,
                                       "link": self.pre_processor.news_df.iloc[int(doc_id[0])].link}

    def transformer_merge_results(self, num=StaticNum.DOC_RELATED_NUM.value):
        self.final_results = dict()
        nr_doc_avg = self.transformer_find_non_related_docs_avg()
        r_doc_avg = self.transformer_find_related_docs_avg()
        new_query_embedding = self.qe.expand_query_rocchio(self.query_vec, np.array(nr_doc_avg), np.array(r_doc_avg))
        qe_results = self.transformers_results(new_query_embedding, True)
        res = [*(list(qe_results.items()))[:num], *(list(self.related_titles.items()))[:num]]
        res = list(dict.fromkeys(res))
        for idx, doc_id in enumerate(res):
            self.final_results[idx] = {"title": self.pre_processor.news_df.iloc[int(doc_id[0])].title,
                                       "link": self.pre_processor.news_df.iloc[int(doc_id[0])].link}
