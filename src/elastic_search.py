from src.enums.enums import StaticNum, Path
from src.query_expansion import QueryExpansion

import tqdm
import json
import config
from elasticsearch import Elasticsearch


class ElasticSearch:
    def __init__(self, query, need_indexing=False, should_expand_query=True):
        self.client = Elasticsearch(
            cloud_id=config.CLOUD_ID,
            basic_auth=("elastic", config.ELASTIC_PASSWORD)
        )
        self.query = query
        self.should_expand_query = should_expand_query
        if self.should_expand_query:
            self.qe = QueryExpansion(self.query.split())
            self.qe()
        self.body = {}
        self.need_indexing = need_indexing
        self.related_titles = list()
        self.final_results = dict()

    def __call__(self):
        self.create_body_match_query()
        self.get_result()
        self.elastic_merge_results()

    def index_data(self):
        with open(Path.DATA_PATH.value, "r", encoding="utf-8") as text_file:
            news_dict = json.loads(text_file.read())

        for i in tqdm.tqdm(range(len(news_dict))):
            temp_doc = news_dict[str(i)]
            self.client.index(index="news", id=i + 1, document=temp_doc)

    def create_body_match_query(self, num=StaticNum.DOC_RELATED_NUM.value):
        self.body = {
            "from": 0,
            "size": num,
            "query": {
                "match": {
                    "content": self.query
                }
            }
        }

    def get_result(self, is_qe=False):
        res = self.client.search(index="news", body=self.body)['hits']['hits']
        titles = list()
        for idx, i in enumerate(res):
            titles.append(i['_source']['_id'])
        if is_qe:
            return titles
        else:
            self.related_titles = titles

    def elastic_merge_results(self, num=StaticNum.DOC_RELATED_NUM.value):
        self.query = self.qe.expand_query(0.7)
        self.create_body_match_query()
        qe_results = self.get_result(True)
        res = [*self.related_titles[:num], *qe_results[:num]]
        res = list(dict.fromkeys(res))
        for idx, title in enumerate(res):
            print(f"{idx + 1}\t{title}")
