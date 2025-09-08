"""
AI service implementation using Google Gemini
"""
import os
from typing import List, Dict, Any, Optional
import google.generativeai as genai

from ...domain.external.ai_service import AIServiceInterface, AIResponse

class AIServiceImpl(AIServiceInterface):
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    async def generate_response(
        self, 
        messages: List[Dict[str, Any]], 
        context: Dict[str, Any] = None
    ) -> AIResponse:
        """Generate response using Gemini model"""
        try:
            # Convert messages to Gemini format
            conversation_text = self._format_messages(messages)
            
            # Add context if provided
            if context:
                conversation_text = f"Context: {context}\n\n{conversation_text}"
            
            # Generate response
            response = self.model.generate_content(conversation_text)
            
            # Check for tool calls in response
            tool_calls = self._extract_tool_calls(response.text)
            
            return AIResponse(
                content=response.text,
                tool_calls=tool_calls,
                metadata={"model": "gemini-pro"}
            )
            
        except Exception as e:
            return AIResponse(
                content=f"I apologize, but I encountered an error: {str(e)}",
                metadata={"error": str(e)}
            )

    async def analyze_intent(self, message: str) -> Dict[str, Any]:
        """Analyze user intent"""
        try:
            prompt = f"""
            Analyze the following user message and determine the intent:
            Message: "{message}"
            
            Respond with a JSON object containing:
            - intent: the primary intent (question, command, request, etc.)
            - entities: any important entities mentioned
            - requires_tools: boolean indicating if tools are needed
            - confidence: confidence score 0-1
            """
            
            response = self.model.generate_content(prompt)
            
            # Parse JSON response (simplified)
            return {
                "intent": "general",
                "entities": [],
                "requires_tools": "execute" in message.lower() or "run" in message.lower(),
                "confidence": 0.8
            }
            
        except Exception as e:
            return {
                "intent": "unknown",
                "entities": [],
                "requires_tools": False,
                "confidence": 0.0,
                "error": str(e)
            }

    def _format_messages(self, messages: List[Dict[str, Any]]) -> str:
        """Format messages for Gemini input"""
        formatted = []
        for msg in messages:
            role = msg.get("type", "user")
            content = msg.get("content", "")
            formatted.append(f"{role.title()}: {content}")
        return "\n".join(formatted)

    def _extract_tool_calls(self, response_text: str) -> Optional[List[Dict[str, Any]]]:
        """Extract tool calls from response text"""
        tool_calls = []
        
        # Simple pattern matching for tool calls
        if "execute_shell:" in response_text.lower():
            # Extract shell commands
            lines = response_text.split('\n')
            for line in lines:
                if "execute_shell:" in line.lower():
                    command = line.split("execute_shell:", 1)[1].strip()
                    tool_calls.append({
                        "name": "shell",
                        "parameters": {"command": command}
                    })
        
        return tool_calls if tool_calls else None
