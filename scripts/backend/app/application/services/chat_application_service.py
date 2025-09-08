"""
Application service for chat orchestration
"""
from typing import List, Optional, Dict, Any
import uuid

from ...domain.models.chat import ChatSession, ChatMessage, MessageType
from ...domain.services.chat_service import ChatDomainService
from ...infrastructure.repositories.chat_repository import ChatRepository
from ...infrastructure.services.ai_service_impl import AIServiceImpl
from ...infrastructure.services.sandbox_service_impl import SandboxServiceImpl

class ChatApplicationService:
    def __init__(self):
        self.chat_repository = ChatRepository()
        self.ai_service = AIServiceImpl()
        self.sandbox_service = SandboxServiceImpl()
        self.chat_domain_service = ChatDomainService(
            self.ai_service, 
            self.sandbox_service
        )

    async def create_session(self, title: str = "New Chat") -> ChatSession:
        """Create and persist a new chat session"""
        session = await self.chat_domain_service.create_session(title)
        await self.chat_repository.save_session(session)
        return session

    async def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Retrieve a chat session by ID"""
        return await self.chat_repository.get_session(session_id)

    async def get_all_sessions(self) -> List[ChatSession]:
        """Retrieve all chat sessions"""
        return await self.chat_repository.get_all_sessions()

    async def send_message(self, session_id: str, content: str) -> ChatMessage:
        """Send a message and process AI response"""
        session = await self.chat_repository.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")

        # Process the message through domain service
        response_message = await self.chat_domain_service.process_user_message(
            session, content
        )
        
        # Save updated session
        await self.chat_repository.save_session(session)
        
        return response_message

    async def get_session_messages(self, session_id: str) -> List[ChatMessage]:
        """Get all messages for a session"""
        session = await self.chat_repository.get_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        return session.messages

    async def execute_shell_command(self, command: str) -> Dict[str, Any]:
        """Execute shell command in sandbox"""
        return await self.sandbox_service.execute_shell(command)

    async def file_operation(self, operation: str, path: str, content: Optional[str] = None) -> Dict[str, Any]:
        """Perform file operations in sandbox"""
        return await self.sandbox_service.file_operation(operation, path, content)

    async def delete_session(self, session_id: str) -> bool:
        """Delete a chat session"""
        return await self.chat_repository.delete_session(session_id)
