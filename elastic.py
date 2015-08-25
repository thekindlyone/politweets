from elasticsearch import Elasticsearch

class ES():
    def __init__(self): 
        self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

    def search(self,term):
        result=self.es.search(index="sentiment", body={"query": {"match": {'message':term}}})
        return result


