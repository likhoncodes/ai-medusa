"""
External sandbox service interface
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class SandboxServiceInterface(ABC):
    @abstractmethod
    async def execute_shell(self, command: str) -> Dict[str, Any]:
        """Execute shell command in sandbox"""
        pass

    @abstractmethod
    async def file_operation(
        self, 
        operation: str, 
        path: str, 
        content: Optional[str] = None
    ) -> Dict[str, Any]:
        """Perform file operations"""
        pass

    @abstractmethod
    async def execute_tool(
        self, 
        tool_name: str, 
        parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute specific tool with parameters"""
        pass
