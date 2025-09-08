"""
External AI service interface
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class AIResponse:
    content: str
    tool_calls: Optional[List[Dict[str, Any]]] = None
    metadata: Optional[Dict[str, Any]] = None

class AIServiceInterface(ABC):
    @abstractmethod
    async def generate_response(
        self, 
        messages: List[Dict[str, Any]], 
        context: Dict[str, Any] = None
    ) -> AIResponse:
        """Generate AI response from messages and context"""
        pass

    @abstractmethod
    async def analyze_intent(self, message: str) -> Dict[str, Any]:
        """Analyze user intent from message"""
        pass
