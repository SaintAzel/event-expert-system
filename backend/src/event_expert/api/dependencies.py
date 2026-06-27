from functools import lru_cache

from ..modules.knowledge import KnowledgeService


@lru_cache
def get_knowledge_service() -> KnowledgeService:
    """
    Singleton Knowledge Service.
    """
    return KnowledgeService()