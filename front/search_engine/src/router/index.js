import Vue from 'vue'
import VueRouter from 'vue-router'
import BooleanSearchPage from '../views/BooleanSearchPage.vue'
import TFIDFSearchPage from '../views/TFIDFSearchPage.vue'
import FasttextSearchPage from '../views/FasttextSearchPage.vue'
import TransformerSearchPage from '../views/TransformerSearchPage.vue'
import ElasticSearchPage from '../views/ElasticSearchPage.vue'
import ClassificationTransformersPage from '../views/ClassificationTransformersPage.vue'
import ClassificationLogisticRegressionPage from '../views/ClassificationLogisticRegressionPage.vue'
import ClusteringPage from '../views/ClusteringPage.vue'
import HITSLinkAnalysisPage from '../views/HITSLinkAnalysisPage.vue'
import PageRankLinkAnalysisPage from '../views/PageRankLinkAnalysisPage.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'BooleanSearchPage',
    component: BooleanSearchPage
  },
  {
    path: '/boolean',
    name: 'BooleanSearchPage',
    component: BooleanSearchPage
  },
  {
    path: '/tfidf',
    name: 'TFIDFSearchPage',
    component: TFIDFSearchPage
  },
  {
    path: '/fasttext',
    name: 'FasttextSearchPage',
    component: FasttextSearchPage
  },
  {
    path: '/transformer',
    name: 'TransformerSearchPage',
    component: TransformerSearchPage
  },
  {
    path: '/elastic',
    name: 'ElasticSearchPage',
    component: ElasticSearchPage
  },
  {
    path: '/classification-transformers',
    name: 'ClassificationTransformersPage',
    component: ClassificationTransformersPage
  },
  {
    path: '/classification-logistic-regression',
    name: 'ClassificationLogisticRegressionPage',
    component: ClassificationLogisticRegressionPage
  },
  {
    path: '/clustering',
    name: 'ClusteringPage',
    component: ClusteringPage
  },
  {
    path: '/hits',
    name: 'HITSLinkAnalysisPage',
    component: HITSLinkAnalysisPage
  },
  {
    path: '/pagerank',
    name: 'PageRankLinkAnalysisPage',
    component: PageRankLinkAnalysisPage
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
