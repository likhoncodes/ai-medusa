"""
Dependency injection for FastAPI
"""
from functools import lru_cache
from ..application.services.chat_application_service import ChatApplicationService

@lru_cache()
def get_chat_service() -> ChatApplicationService:
    """Get chat application service instance"""
    return ChatApplicationService()
