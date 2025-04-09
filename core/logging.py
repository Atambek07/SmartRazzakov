# core/logging.py
import logging
from elasticsearch import Elasticsearch

class ElasticsearchHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.es = Elasticsearch(['elasticsearch:9200'])
        self.index_name = "eduspace-logs"

    def emit(self, record):
        log_entry = self.format(record)
        self.es.index(
            index=self.index_name,
            body=log_entry
        )

LOGGING = {
    'version': 1,
    'handlers': {
        'elasticsearch': {
            'class': 'core.logging.ElasticsearchHandler',
            'level': 'INFO',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['elasticsearch'],
            'level': 'INFO',
        },
    },
}