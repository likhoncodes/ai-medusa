"""
Infrastructure layer repository for chat persistence
"""
from typing import List, Optional, Dict, Any
import json
import os
from datetime import datetime

from ...domain.models.chat import ChatSession, ChatMessage

class ChatRepository:
    def __init__(self, storage_path: str = "data/sessions"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)

    async def save_session(self, session: ChatSession) -> None:
        """Save chat session to file storage"""
        session_file = os.path.join(self.storage_path, f"{session.id}.json")
        session_data = {
            "id": session.id,
            "title": session.title,
            "created_at": session.created_at.isoformat(),
            "updated_at": session.updated_at.isoformat(),
            "context": session.context,
            "is_active": session.is_active,
            "messages": [
                {
                    "id": msg.id,
                    "session_id": msg.session_id,
                    "type": msg.type.value,
                    "content": msg.content,
                    "metadata": msg.metadata,
                    "timestamp": msg.timestamp.isoformat(),
                    "status": msg.status.value,
                    "parent_id": msg.parent_id
                }
                for msg in session.messages
            ]
        }
        
        with open(session_file, 'w') as f:
            json.dump(session_data, f, indent=2)

    async def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Retrieve chat session from file storage"""
        session_file = os.path.join(self.storage_path, f"{session_id}.json")
        
        if not os.path.exists(session_file):
            return None
            
        with open(session_file, 'r') as f:
            session_data = json.load(f)
        
        # Reconstruct session object
        messages = []
        for msg_data in session_data.get("messages", []):
            message = ChatMessage(
                id=msg_data["id"],
                session_id=msg_data["session_id"],
                type=msg_data["type"],
                content=msg_data["content"],
                metadata=msg_data.get("metadata", {}),
                timestamp=datetime.fromisoformat(msg_data["timestamp"]),
                status=msg_data["status"],
                parent_id=msg_data.get("parent_id")
            )
            messages.append(message)
        
        session = ChatSession(
            id=session_data["id"],
            title=session_data["title"],
            created_at=datetime.fromisoformat(session_data["created_at"]),
            updated_at=datetime.fromisoformat(session_data["updated_at"]),
            messages=messages,
            context=session_data.get("context", {}),
            is_active=session_data.get("is_active", True)
        )
        
        return session

    async def get_all_sessions(self) -> List[ChatSession]:
        """Retrieve all chat sessions"""
        sessions = []
        
        for filename in os.listdir(self.storage_path):
            if filename.endswith('.json'):
                session_id = filename[:-5]  # Remove .json extension
                session = await self.get_session(session_id)
                if session:
                    sessions.append(session)
        
        # Sort by updated_at descending
        sessions.sort(key=lambda s: s.updated_at, reverse=True)
        return sessions

    async def delete_session(self, session_id: str) -> bool:
        """Delete a chat session"""
        session_file = os.path.join(self.storage_path, f"{session_id}.json")
        
        if os.path.exists(session_file):
            os.remove(session_file)
            return True
        return False
