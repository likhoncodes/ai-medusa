# Backend Development Instructions

## FastAPI Domain-Driven Architecture

### Layer Structure
\`\`\`
app/
├── domain/              # Business logic layer
│   ├── models/         # Domain entities
│   ├── services/       # Business services
│   └── external/       # External service interfaces
├── application/         # Application layer
│   ├── services/       # Use case orchestration
│   └── schemas/        # API request/response models
├── infrastructure/      # Infrastructure layer
│   ├── repositories/   # Data access implementations
│   └── services/       # External service implementations
└── interfaces/         # Interface layer
    └── api/           # REST API routes
\`\`\`

### Domain Layer Patterns

#### Domain Models
\`\`\`python
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ChatMessage(BaseModel):
    id: str
    content: str
    role: str  # 'user' | 'assistant'
    session_id: str
    created_at: datetime
    metadata: Optional[dict] = None
\`\`\`

#### Domain Services
\`\`\`python
from abc import ABC, abstractmethod

class ChatService(ABC):
    @abstractmethod
    async def process_message(self, message: str, session_id: str) -> str:
        pass
    
    @abstractmethod
    async def get_chat_history(self, session_id: str) -> List[ChatMessage]:
        pass
\`\`\`

### Application Layer

#### Use Case Services
\`\`\`python
from fastapi import Depends
from app.domain.services.chat_service import ChatService
from app.application.schemas.chat_schemas import ChatRequest, ChatResponse

class ChatApplicationService:
    def __init__(self, chat_service: ChatService):
        self.chat_service = chat_service
    
    async def handle_chat_request(self, request: ChatRequest) -> ChatResponse:
        # Orchestrate business logic
        response = await self.chat_service.process_message(
            request.message, 
            request.session_id
        )
        return ChatResponse(message=response, session_id=request.session_id)
\`\`\`

#### API Schemas
\`\`\`python
from pydantic import BaseModel, Field
from typing import Optional

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    message: str
    session_id: str
    timestamp: datetime
\`\`\`

### Infrastructure Layer

#### Repository Pattern
\`\`\`python
from abc import ABC, abstractmethod
from typing import List, Optional

class ChatRepository(ABC):
    @abstractmethod
    async def save_message(self, message: ChatMessage) -> ChatMessage:
        pass
    
    @abstractmethod
    async def get_messages_by_session(self, session_id: str) -> List[ChatMessage]:
        pass

class SQLChatRepository(ChatRepository):
    def __init__(self, db_session):
        self.db = db_session
    
    async def save_message(self, message: ChatMessage) -> ChatMessage:
        # Implementation with SQLAlchemy
        pass
\`\`\`

#### External Service Implementation
\`\`\`python
from app.domain.external.ai_service import AIService
import google.generativeai as genai

class GeminiAIService(AIService):
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    async def generate_response(self, prompt: str) -> str:
        try:
            response = await self.model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            # Proper error handling
            raise AIServiceError(f"Gemini API error: {str(e)}")
\`\`\`

### API Layer

#### Route Implementation
\`\`\`python
from fastapi import APIRouter, Depends, HTTPException
from app.application.services.chat_application_service import ChatApplicationService
from app.application.schemas.chat_schemas import ChatRequest, ChatResponse

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])

@router.post("/message", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    service: ChatApplicationService = Depends(get_chat_service)
):
    try:
        return await service.handle_chat_request(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
\`\`\`

### Error Handling

#### Custom Exceptions
\`\`\`python
class DomainException(Exception):
    """Base domain exception"""
    pass

class AIServiceError(DomainException):
    """AI service related errors"""
    pass

class ValidationError(DomainException):
    """Data validation errors"""
    pass
\`\`\`

#### Global Error Handler
\`\`\`python
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

@app.exception_handler(DomainException)
async def domain_exception_handler(request: Request, exc: DomainException):
    return JSONResponse(
        status_code=400,
        content={"error": "Domain Error", "detail": str(exc)}
    )
\`\`\`

### Dependency Injection

\`\`\`python
from functools import lru_cache
from app.core.config import Settings

@lru_cache()
def get_settings():
    return Settings()

def get_chat_service() -> ChatService:
    settings = get_settings()
    ai_service = GeminiAIService(settings.gemini_api_key)
    repository = SQLChatRepository(get_db_session())
    return ChatServiceImpl(ai_service, repository)
