"""
Domain models for chat functionality
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum

class MessageType(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"

class MessageStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"

class ChatMessage(BaseModel):
    id: str = Field(..., description="Unique message identifier")
    session_id: str = Field(..., description="Chat session identifier")
    type: MessageType = Field(..., description="Message type")
    content: str = Field(..., description="Message content")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    status: MessageStatus = Field(default=MessageStatus.PENDING)
    parent_id: Optional[str] = Field(None, description="Parent message ID for threading")

class ChatSession(BaseModel):
    id: str = Field(..., description="Unique session identifier")
    title: str = Field(..., description="Session title")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    messages: List[ChatMessage] = Field(default_factory=list)
    context: Dict[str, Any] = Field(default_factory=dict)
    is_active: bool = Field(default=True)

class ToolExecution(BaseModel):
    id: str = Field(..., description="Execution identifier")
    tool_name: str = Field(..., description="Name of the tool")
    parameters: Dict[str, Any] = Field(..., description="Tool parameters")
    result: Optional[Dict[str, Any]] = Field(None, description="Execution result")
    status: MessageStatus = Field(default=MessageStatus.PENDING)
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
