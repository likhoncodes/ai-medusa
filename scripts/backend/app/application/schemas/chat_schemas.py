"""
Application layer schemas for API communication
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

from ...domain.models.chat import ChatSession, ChatMessage, MessageType, MessageStatus

class CreateSessionRequest(BaseModel):
    title: str = Field(default="New Chat", description="Session title")

class SendMessageRequest(BaseModel):
    content: str = Field(..., description="Message content")

class ChatMessageResponse(BaseModel):
    id: str
    session_id: str
    type: MessageType
    content: str
    metadata: Dict[str, Any] = {}
    timestamp: datetime
    status: MessageStatus
    parent_id: Optional[str] = None

    @classmethod
    def from_domain(cls, message: ChatMessage) -> "ChatMessageResponse":
        return cls(
            id=message.id,
            session_id=message.session_id,
            type=message.type,
            content=message.content,
            metadata=message.metadata,
            timestamp=message.timestamp,
            status=message.status,
            parent_id=message.parent_id
        )

class ChatSessionResponse(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    messages: List[ChatMessageResponse] = []
    context: Dict[str, Any] = {}
    is_active: bool = True

    @classmethod
    def from_domain(cls, session: ChatSession) -> "ChatSessionResponse":
        return cls(
            id=session.id,
            title=session.title,
            created_at=session.created_at,
            updated_at=session.updated_at,
            messages=[ChatMessageResponse.from_domain(msg) for msg in session.messages],
            context=session.context,
            is_active=session.is_active
        )

class ToolExecutionResponse(BaseModel):
    id: str
    tool_name: str
    parameters: Dict[str, Any]
    result: Optional[Dict[str, Any]] = None
    status: MessageStatus
    started_at: datetime
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None

class ShellCommandRequest(BaseModel):
    command: str = Field(..., description="Shell command to execute")

class FileOperationRequest(BaseModel):
    operation: str = Field(..., description="File operation type (read, write, delete)")
    path: str = Field(..., description="File path")
    content: Optional[str] = Field(None, description="File content for write operations")
