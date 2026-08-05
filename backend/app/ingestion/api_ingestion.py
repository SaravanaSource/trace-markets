from app.ingestion.base_ingestion import BaseIngestion
from app.services.http_client import HttpClient

from app.dq.required_rule import RequiredRule
from app.dq.datatype_rule import DatatypeRule
from app.dq.range_rule import RangeRule

class APIIngestion (BaseIngestion):

    source = 'api'

    def __init__(self):
        super().__init__()
        self.client = HttpClient() 


    def fetch(self):
        return self.client.get(
             "https://jsonplaceholder.typicode.com/posts/1"
            # "https://jsonplaceholder.typicode.com/does-not-exist" # test
        )


    def get_dq_rules(self):

        return [

            RequiredRule(
                [
                    "userId",
                    "id",
                    "title",
                    "body",
                ]
            ),

            DatatypeRule(
                {
                    "userId": int,
                    "id": int,
                    "title": str,
                    "body": str,
                }
            ),

            RangeRule(
                {
                    "userId": (1, None),
                    "id": (1, None),
                }
            ),

        ]