from src.enums.enums import StaticNum, Path

import tqdm
import json
from src.config import *
from elasticsearch import Elasticsearch


class ElasticSearch:
    def __init__(self, qe_ins, need_indexing=False, ):
        self.client = Elasticsearch(
            cloud_id=CLOUD_ID,
            basic_auth=("elastic", ELASTIC_PASSWORD)
        )
        self.qe = qe_ins
        self.body = {}
        self.need_indexing = need_indexing
        self.related_titles = dict()
        self.final_results = dict()

    def __call__(self, query):
        self.create_body_match_query(query)
        self.get_result()
        self.elastic_merge_results(query)

    def index_data(self):
        with open(Path.DATA_PATH.value, "r", encoding="utf-8") as text_file:
            news_dict = json.loads(text_file.read())

        for i in tqdm.tqdm(range(len(news_dict))):
            temp_doc = news_dict[str(i)]
            self.client.index(index="news", id=i + 1, document=temp_doc)

    def create_body_match_query(self, query, num=StaticNum.DOC_RELATED_NUM.value):
        self.body = {
            "from": 0,
            "size": num,
            "query": {
                "match": {
                    "content": query
                }
            }
        }

    def get_result(self, is_qe=False):
        res = self.client.search(index="news", body=self.body)['hits']['hits']
        titles_and_link = dict()
        for idx, i in enumerate(res):
            idx = idx + len(self.related_titles) if is_qe else idx
            titles_and_link[idx] = {"title": i['_source']['title'], "link": i['_source']['link']}
        if is_qe:
            return titles_and_link
        else:
            self.related_titles = titles_and_link

    def elastic_merge_results(self, query):
        qe_query = self.qe.expand_query(query, 0.8)
        self.create_body_match_query(qe_query)
        qe_results = self.get_result(True)
        self.related_titles.update(qe_results)
        self.final_results = self.related_titles
