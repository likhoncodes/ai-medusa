"""
Domain service for chat business logic
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

from ..models.chat import ChatSession, ChatMessage, MessageType, MessageStatus, ToolExecution
from ..external.ai_service import AIServiceInterface
from ..external.sandbox_service import SandboxServiceInterface

class ChatDomainService:
    def __init__(self, ai_service: AIServiceInterface, sandbox_service: SandboxServiceInterface):
        self.ai_service = ai_service
        self.sandbox_service = sandbox_service

    async def create_session(self, title: str = "New Chat") -> ChatSession:
        """Create a new chat session"""
        session_id = str(uuid.uuid4())
        return ChatSession(
            id=session_id,
            title=title,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

    async def add_message(self, session: ChatSession, content: str, message_type: MessageType) -> ChatMessage:
        """Add a message to the chat session"""
        message_id = str(uuid.uuid4())
        message = ChatMessage(
            id=message_id,
            session_id=session.id,
            type=message_type,
            content=content,
            timestamp=datetime.utcnow()
        )
        session.messages.append(message)
        session.updated_at = datetime.utcnow()
        return message

    async def process_user_message(self, session: ChatSession, content: str) -> ChatMessage:
        """Process a user message and generate AI response"""
        # Add user message
        user_message = await self.add_message(session, content, MessageType.USER)
        
        # Generate AI response
        try:
            ai_response = await self.ai_service.generate_response(
                messages=[msg.dict() for msg in session.messages],
                context=session.context
            )
            
            # Add AI response
            assistant_message = await self.add_message(
                session, ai_response.content, MessageType.ASSISTANT
            )
            assistant_message.status = MessageStatus.COMPLETED
            
            # Handle tool calls if any
            if ai_response.tool_calls:
                for tool_call in ai_response.tool_calls:
                    await self.execute_tool(session, tool_call)
            
            return assistant_message
            
        except Exception as e:
            error_message = await self.add_message(
                session, f"Error processing message: {str(e)}", MessageType.SYSTEM
            )
            error_message.status = MessageStatus.ERROR
            return error_message

    async def execute_tool(self, session: ChatSession, tool_call: Dict[str, Any]) -> ToolExecution:
        """Execute a tool call in the sandbox"""
        execution_id = str(uuid.uuid4())
        execution = ToolExecution(
            id=execution_id,
            tool_name=tool_call["name"],
            parameters=tool_call["parameters"]
        )
        
        try:
            execution.status = MessageStatus.PROCESSING
            result = await self.sandbox_service.execute_tool(
                tool_call["name"], 
                tool_call["parameters"]
            )
            
            execution.result = result
            execution.status = MessageStatus.COMPLETED
            execution.completed_at = datetime.utcnow()
            
            # Add tool result as message
            tool_message = await self.add_message(
                session, 
                f"Tool '{tool_call['name']}' executed successfully", 
                MessageType.TOOL
            )
            tool_message.metadata = {"execution_id": execution_id, "result": result}
            
        except Exception as e:
            execution.status = MessageStatus.ERROR
            execution.error_message = str(e)
            execution.completed_at = datetime.utcnow()
            
            # Add error message
            await self.add_message(
                session, 
                f"Tool execution failed: {str(e)}", 
                MessageType.SYSTEM
            )
        
        return execution
