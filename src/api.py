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
        'boolean': BooleanSearch,
        'tfidf': TfidfSearch,
        'transformer': TransformerSearcher,
        'fasttext': FasttextSearch,
        'elasticsearch': ElasticSearch,
        'clustering': Clustering
    }.get(model)

    searcher = model(query)
    searcher()
    return searcher.final_results


@app.get('/category')
def get_category(model: str, query: str):
    model = {
        'transformer': ClassificationTransformers,
        'logistic': ClassificationLogisticRegression
    }.get(model)

    clf = model(query)
    clf()
    return clf.final_results


@app.get('/link')
def get_link(model: str, category: str):
    is_page_rank = True if model == 'rank' else False
    link_analyzer = LinkAnalysis(category, page_rank_mode=is_page_rank)
    link_analyzer()

    if is_page_rank:
        return link_analyzer.pr_final_results
    else:
        return {
            'hub': link_analyzer.hub_final_results,
            'auth': link_analyzer.auth_final_results
        }
