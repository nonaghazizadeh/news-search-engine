from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.boolean_search import BooleanSearch
from src.tfidf_search import TfidfSearch
from src.transformer_search import TransformerSearcher
from src.fasttext_search import FasttextSearch
from src.elastic_search import ElasticSearch
from src.clustering import Clustering

from src.classification_transformers import ClassificationTransformers
from src.classification_logistic_regression import ClassificationLogisticRegression

from src.link_analysis import LinkAnalysis
from src.query_expansion import QueryExpansion

qe = QueryExpansion()
boolean = BooleanSearch(qe)
tfidf = TfidfSearch(qe)
fasttext = FasttextSearch(qe)
# transformer = TransformerSearcher(qe)
elastic = ElasticSearch(qe)
clustering = Clustering()

clf_logistic_regression = ClassificationLogisticRegression()
# clf_transformer = ClassificationTransformers()

link_analyser = LinkAnalysis()

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/search')
def get_search(model: str, query: str):
    model = {
        'boolean': boolean,
        'tfidf': tfidf,
        # 'transformer': TransformerSearcher,
        'fasttext': fasttext,
        'elasticsearch': elastic,
        'clustering': clustering
    }.get(model)
    print(model)
    model(query)
    return model.final_results


@app.get('/category')
def get_category(model: str, query: str):
    model = {
        # 'transformer': clf_logistic_regression,
        'logistic': clf_logistic_regression
    }.get(model)
    model(query)
    return model.final_results


@app.get('/link')
def get_link(model: str, category: str):
    is_page_rank = True if model == 'rank' else False
    link_analyser(category, page_rank_mode=is_page_rank)

    if is_page_rank:
        return link_analyser.pr_final_results
    else:
        return {
            'hub': link_analyser.hub_final_results,
            'auth': link_analyser.auth_final_results
        }
