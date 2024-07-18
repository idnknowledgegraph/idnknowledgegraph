from SPARQLWrapper import SPARQLWrapper, JSON
from django.conf import settings

def run_query(query):
    sparql = SPARQLWrapper(settings.FUSEKI_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

def run_update(query):
    sparql = SPARQLWrapper(settings.FUSEKI_URL)
    sparql.setQuery(query)
    sparql.setMethod('POST')
    sparql.query()
