"""
API route definitions
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
import uuid

from ...application.services.chat_application_service import ChatApplicationService
from ...application.schemas.chat_schemas import (
    ChatSessionResponse, ChatMessageResponse, CreateSessionRequest,
    SendMessageRequest, ToolExecutionResponse
)
from ...infrastructure.dependencies import get_chat_service

api_router = APIRouter()

# Chat endpoints
@api_router.post("/sessions", response_model=ChatSessionResponse)
async def create_chat_session(
    request: CreateSessionRequest,
    chat_service: ChatApplicationService = Depends(get_chat_service)
):
    """Create a new chat session"""
    try:
        session = await chat_service.create_session(request.title)
        return ChatSessionResponse.from_domain(session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/sessions", response_model=List[ChatSessionResponse])
async def get_chat_sessions(
    chat_service: ChatApplicationService = Depends(get_chat_service)
):
    """Get all chat sessions"""
    try:
        sessions = await chat_service.get_all_sessions()
        return [ChatSessionResponse.from_domain(session) for session in sessions]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/sessions/{session_id}", response_model=ChatSessionResponse)
async def get_chat_session(
    session_id: str,
    chat_service: ChatApplicationService = Depends(get_chat_service)
):
    """Get a specific chat session"""
    try:
        session = await chat_service.get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        return ChatSessionResponse.from_domain(session)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/sessions/{session_id}/messages", response_model=ChatMessageResponse)
async def send_message(
    session_id: str,
    request: SendMessageRequest,
    chat_service: ChatApplicationService = Depends(get_chat_service)
):
    """Send a message to a chat session"""
    try:
        message = await chat_service.send_message(session_id, request.content)
        return ChatMessageResponse.from_domain(message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/sessions/{session_id}/messages", response_model=List[ChatMessageResponse])
async def get_session_messages(
    session_id: str,
    chat_service: ChatApplicationService = Depends(get_chat_service)
):
    """Get all messages for a session"""
    try:
        messages = await chat_service.get_session_messages(session_id)
        return [ChatMessageResponse.from_domain(msg) for msg in messages]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Sandbox endpoints
@api_router.post("/sandbox/shell")
async def execute_shell_command(
    command: str,
    chat_service: ChatApplicationService = Depends(get_chat_service)
):
    """Execute a shell command in the sandbox"""
    try:
        result = await chat_service.execute_shell_command(command)
        return {"result": result, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/sandbox/file")
async def file_operation(
    operation: str,
    path: str,
    content: Optional[str] = None,
    chat_service: ChatApplicationService = Depends(get_chat_service)
):
    """Perform file operations in the sandbox"""
    try:
        result = await chat_service.file_operation(operation, path, content)
        return {"result": result, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
