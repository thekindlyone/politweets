from elasticsearch import Elasticsearch

class ES():
    def __init__(self): 
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    def get_count(self):
        return self.es.indices.stats(index='sentiment')['_all']['total']['docs']['count']

    def search(self,term):
        result=self.es.search(index="sentiment", body={"query": {"match": {'message':term}}}, size=self.get_count())
        return result


