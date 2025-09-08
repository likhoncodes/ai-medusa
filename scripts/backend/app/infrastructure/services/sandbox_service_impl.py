"""
Sandbox service implementation for secure code execution
"""
import subprocess
import os
import tempfile
import shutil
from typing import Dict, Any, Optional
import asyncio
import json

from ...domain.external.sandbox_service import SandboxServiceInterface

class SandboxServiceImpl(SandboxServiceInterface):
    def __init__(self, sandbox_dir: str = "/tmp/sandbox"):
        self.sandbox_dir = sandbox_dir
        os.makedirs(sandbox_dir, exist_ok=True)

    async def execute_shell(self, command: str) -> Dict[str, Any]:
        """Execute shell command in sandbox environment"""
        try:
            # Create isolated environment
            env = os.environ.copy()
            env['PATH'] = '/usr/local/bin:/usr/bin:/bin'
            
            # Execute command with timeout
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.sandbox_dir,
                env=env
            )
            
            stdout, stderr = await asyncio.wait_for(
                process.communicate(), 
                timeout=30.0
            )
            
            return {
                "stdout": stdout.decode('utf-8'),
                "stderr": stderr.decode('utf-8'),
                "return_code": process.returncode,
                "command": command
            }
            
        except asyncio.TimeoutError:
            return {
                "stdout": "",
                "stderr": "Command timed out after 30 seconds",
                "return_code": -1,
                "command": command
            }
        except Exception as e:
            return {
                "stdout": "",
                "stderr": str(e),
                "return_code": -1,
                "command": command
            }

    async def file_operation(self, operation: str, path: str, content: Optional[str] = None) -> Dict[str, Any]:
        """Perform file operations in sandbox"""
        safe_path = os.path.join(self.sandbox_dir, path.lstrip('/'))
        
        try:
            if operation == "read":
                if os.path.exists(safe_path):
                    with open(safe_path, 'r') as f:
                        return {
                            "content": f.read(),
                            "path": path,
                            "operation": operation,
                            "success": True
                        }
                else:
                    return {
                        "error": "File not found",
                        "path": path,
                        "operation": operation,
                        "success": False
                    }
                    
            elif operation == "write":
                os.makedirs(os.path.dirname(safe_path), exist_ok=True)
                with open(safe_path, 'w') as f:
                    f.write(content or "")
                return {
                    "message": "File written successfully",
                    "path": path,
                    "operation": operation,
                    "success": True
                }
                
            elif operation == "delete":
                if os.path.exists(safe_path):
                    os.remove(safe_path)
                    return {
                        "message": "File deleted successfully",
                        "path": path,
                        "operation": operation,
                        "success": True
                    }
                else:
                    return {
                        "error": "File not found",
                        "path": path,
                        "operation": operation,
                        "success": False
                    }
                    
            elif operation == "list":
                if os.path.exists(safe_path):
                    files = os.listdir(safe_path)
                    return {
                        "files": files,
                        "path": path,
                        "operation": operation,
                        "success": True
                    }
                else:
                    return {
                        "error": "Directory not found",
                        "path": path,
                        "operation": operation,
                        "success": False
                    }
            else:
                return {
                    "error": f"Unknown operation: {operation}",
                    "path": path,
                    "operation": operation,
                    "success": False
                }
                
        except Exception as e:
            return {
                "error": str(e),
                "path": path,
                "operation": operation,
                "success": False
            }

    async def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific tool with parameters"""
        if tool_name == "shell":
            return await self.execute_shell(parameters.get("command", ""))
        elif tool_name == "file":
            return await self.file_operation(
                parameters.get("operation", "read"),
                parameters.get("path", ""),
                parameters.get("content")
            )
        else:
            return {
                "error": f"Unknown tool: {tool_name}",
                "tool": tool_name,
                "parameters": parameters,
                "success": False
            }
