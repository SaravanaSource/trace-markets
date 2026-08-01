from app.ingestion.base_ingestion import BaseIngestion
from app.services.http_client import HttpClient

class APIIngestion (BaseIngestion):

    source = 'api'

    def __init__(self):
        super().__init__()
        self.client = HttpClient() 


    def fetch(self):
        return self.client.get(
            # "https://jsonplaceholder.typicode.com/posts/1"
            "https://jsonplaceholder.typicode.com/does-not-exist" # test
        )
        