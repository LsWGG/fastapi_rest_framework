from elasticsearch import AsyncElasticsearch

from core.setting import settings

if settings.ES_USERNAME and settings.ES_PASSWORD:
    es: AsyncElasticsearch = AsyncElasticsearch(hosts=settings.ES_HOST,
                                                http_auth=(settings.ES_USERNAME, settings.ES_PASSWORD))
else:
    es: AsyncElasticsearch = AsyncElasticsearch(hosts=settings.ES_HOST)
