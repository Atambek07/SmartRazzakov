# modules/community_hub/infrastructure/integrations/search/elastic.py
import logging
from typing import List, Dict, Optional
from uuid import UUID
from elasticsearch import AsyncElasticsearch, NotFoundError
from elasticsearch.helpers import async_bulk
from . import BaseSearchClient, SearchResult, SearchError

logger = logging.getLogger(__name__)


class ElasticSearchClient(BaseSearchClient):
    """Реализация поиска через Elasticsearch"""

    def __init__(self, hosts: List[str], timeout: int = 30):
        self.client = AsyncElasticsearch(
            hosts=hosts,
            timeout=timeout,
            max_retries=3,
            retry_on_timeout=True
        )
        self.index_settings = {
            "settings": {
                "index": {
                    "number_of_shards": 1,
                    "number_of_replicas": 1
                },
                "analysis": {
                    "analyzer": {
                        "tag_analyzer": {
                            "type": "custom",
                            "tokenizer": "standard",
                            "filter": ["lowercase"]
                        }
                    }
                }
            },
            "mappings": {
                "properties": {
                    "name": {"type": "text"},
                    "description": {"type": "text"},
                    "tags": {
                        "type": "text",
                        "analyzer": "tag_analyzer",
                        "fields": {
                            "keyword": {"type": "keyword"}
                        }
                    },
                    "community_id": {"type": "keyword"},
                    "created_at": {"type": "date"},
                    "updated_at": {"type": "date"}
                }
            }
        }

    async def ensure_index_exists(self, index: str):
        """Создание индекса если не существует"""
        if not await self.client.indices.exists(index=index):
            await self.client.indices.create(
                index=index,
                body=self.index_settings
            )

    async def index_document(self, index: str, doc_id: str, document: Dict) -> bool:
        try:
            await self.ensure_index_exists(index)
            resp = await self.client.index(
                index=index,
                id=doc_id,
                body=document,
                refresh=True
            )
            return resp['result'] in ['created', 'updated']
        except Exception as e:
            logger.error(f"Failed to index document: {str(e)}")
            raise SearchError(f"Indexing failed: {str(e)}")

    async def search(
            self,
            index: str,
            query: str,
            filters: Optional[Dict] = None,
            facets: Optional[List[str]] = None,
            page: int = 1,
            size: int = 20
    ) -> SearchResult:
        try:
            body = {
                "query": {
                    "bool": {
                        "must": [
                            {
                                "query_string": {
                                    "query": query,
                                    "fields": ["name^3", "description", "tags^2"]
                                }
                            }
                        ]
                    }
                },
                "from": (page - 1) * size,
                "size": size
            }

            if filters:
                body["query"]["bool"]["filter"] = [
                    {"term": {k: v}} for k, v in filters.items()
                ]

            if facets:
                body["aggs"] = {
                    facet: {"terms": {"field": f"{facet}.keyword"}}
                    for facet in facets
                }

            resp = await self.client.search(
                index=index,
                body=body
            )

            items = [hit["_source"] for hit in resp["hits"]["hits"]]
            facets_result = {
                k: {bucket["key"]: bucket["doc_count"] for bucket in v["buckets"]}
                for k, v in resp.get("aggregations", {}).items()
            }

            return SearchResult(
                items=items,
                total=resp["hits"]["total"]["value"],
                facets=facets_result
            )
        except Exception as e:
            logger.error(f"Search failed: {str(e)}")
            raise SearchError(f"Search operation failed: {str(e)}")

    async def bulk_index(self, index: str, documents: List[Dict]):
        """Массовая индексация документов"""
        try:
            await self.ensure_index_exists(index)
            actions = [
                {
                    "_index": index,
                    "_id": doc["id"],
                    "_source": doc
                }
                for doc in documents
            ]
            success, _ = await async_bulk(self.client, actions)
            return success
        except Exception as e:
            logger.error(f"Bulk indexing failed: {str(e)}")
            raise SearchError(f"Bulk indexing failed: {str(e)}")

    async def delete_document(self, index: str, doc_id: str) -> bool:
        try:
            resp = await self.client.delete(
                index=index,
                id=doc_id,
                refresh=True
            )
            return resp['result'] == 'deleted'
        except NotFoundError:
            return False
        except Exception as e:
            logger.error(f"Failed to delete document: {str(e)}")
            raise SearchError(f"Deletion failed: {str(e)}")

    async def close(self):
        """Закрытие соединения"""
        await self.client.close()