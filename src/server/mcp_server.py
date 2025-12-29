import asyncio
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
import websockets
from websockets.server import WebSocketServerProtocol
import jwt
from datetime import datetime, timedelta

from ..core.config import settings
from ..utils.logger import setup_logger

logger = setup_logger("mcp_server", settings.log.level, settings.log.log_file)

class MCPServer:
    def __init__(self):
        self.host = settings.mcp.server_host
        self.port = settings.mcp.server_port
        self.secret_key = settings.mcp.secret_key
        self.clients: Dict[str, WebSocketServerProtocol] = {}
        self.tools = self._register_tools()
    
    def _register_tools(self) -> Dict[str, callable]:
        return {
            "list_files": self.list_files,
            "read_file": self.read_file,
            "write_file": self.write_file,
            "execute_command": self.execute_command,
            "get_system_info": self.get_system_info,
            "search_files": self.search_files,
        }
    
    def generate_token(self, client_id: str) -> str:
        payload = {
            "client_id": client_id,
            "exp": datetime.utcnow() + timedelta(seconds=settings.security.jwt_expiration)
        }
        return jwt.encode(payload, settings.security.jwt_secret, algorithm="HS256")
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        try:
            payload = jwt.decode(token, settings.security.jwt_secret, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Invalid token")
            return None
    
    async def list_files(self, path: str, recursive: bool = False) -> Dict[str, Any]:
        try:
            target_path = Path(path).expanduser()
            if not target_path.exists():
                return {"error": f"Path does not exist: {path}"}
            
            if target_path.is_file():
                return {
                    "type": "file",
                    "path": str(target_path),
                    "size": target_path.stat().st_size
                }
            
            files = []
            pattern = "**/*" if recursive else "*"
            for item in target_path.glob(pattern):
                files.append({
                    "name": item.name,
                    "path": str(item),
                    "type": "file" if item.is_file() else "directory",
                    "size": item.stat().st_size if item.is_file() else None
                })
            
            return {"files": files, "count": len(files)}
        except Exception as e:
            logger.error(f"Error listing files: {e}")
            return {"error": str(e)}
    
    async def read_file(self, path: str, encoding: str = "utf-8") -> Dict[str, Any]:
        try:
            target_path = Path(path).expanduser()
            if not target_path.exists():
                return {"error": f"File does not exist: {path}"}
            
            if not target_path.is_file():
                return {"error": f"Path is not a file: {path}"}
            
            content = target_path.read_text(encoding=encoding)
            return {
                "path": str(target_path),
                "content": content,
                "size": len(content)
            }
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            return {"error": str(e)}
    
    async def write_file(self, path: str, content: str, encoding: str = "utf-8") -> Dict[str, Any]:
        try:
            target_path = Path(path).expanduser()
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(content, encoding=encoding)
            return {
                "path": str(target_path),
                "size": len(content),
                "success": True
            }
        except Exception as e:
            logger.error(f"Error writing file: {e}")
            return {"error": str(e)}
    
    async def execute_command(self, command: str, cwd: Optional[str] = None) -> Dict[str, Any]:
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd
            )
            stdout, stderr = await process.communicate()
            
            return {
                "command": command,
                "returncode": process.returncode,
                "stdout": stdout.decode(),
                "stderr": stderr.decode()
            }
        except Exception as e:
            logger.error(f"Error executing command: {e}")
            return {"error": str(e)}
    
    async def get_system_info(self) -> Dict[str, Any]:
        try:
            import platform
            import psutil
            
            return {
                "platform": platform.system(),
                "platform_release": platform.release(),
                "platform_version": platform.version(),
                "architecture": platform.machine(),
                "hostname": platform.node(),
                "cpu_count": psutil.cpu_count(),
                "memory_total": psutil.virtual_memory().total,
                "memory_available": psutil.virtual_memory().available,
                "disk_usage": {
                    "total": psutil.disk_usage('/').total,
                    "used": psutil.disk_usage('/').used,
                    "free": psutil.disk_usage('/').free
                }
            }
        except Exception as e:
            logger.error(f"Error getting system info: {e}")
            return {"error": str(e)}
    
    async def search_files(self, path: str, pattern: str, content_search: bool = False) -> Dict[str, Any]:
        try:
            target_path = Path(path).expanduser()
            if not target_path.exists():
                return {"error": f"Path does not exist: {path}"}
            
            results = []
            for item in target_path.rglob(pattern):
                if content_search and item.is_file():
                    try:
                        content = item.read_text()
                        if pattern in content:
                            results.append(str(item))
                    except:
                        pass
                else:
                    results.append(str(item))
            
            return {"results": results, "count": len(results)}
        except Exception as e:
            logger.error(f"Error searching files: {e}")
            return {"error": str(e)}
    
    async def handle_message(self, websocket: WebSocketServerProtocol, message: str):
        try:
            data = json.loads(message)
            tool_name = data.get("tool")
            params = data.get("params", {})
            request_id = data.get("request_id")
            
            if tool_name not in self.tools:
                response = {
                    "request_id": request_id,
                    "error": f"Unknown tool: {tool_name}"
                }
            else:
                result = await self.tools[tool_name](**params)
                response = {
                    "request_id": request_id,
                    "result": result
                }
            
            await websocket.send(json.dumps(response))
            logger.info(f"Processed tool: {tool_name}")
            
        except json.JSONDecodeError:
            await websocket.send(json.dumps({"error": "Invalid JSON"}))
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            await websocket.send(json.dumps({"error": str(e)}))
    
    async def handle_client(self, websocket: WebSocketServerProtocol, path: str):
        client_id = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
        logger.info(f"Client connected: {client_id}")
        
        try:
            auth_message = await websocket.recv()
            auth_data = json.loads(auth_message)
            token = auth_data.get("token")
            
            if not token or not self.verify_token(token):
                await websocket.send(json.dumps({"error": "Authentication failed"}))
                await websocket.close()
                return
            
            self.clients[client_id] = websocket
            await websocket.send(json.dumps({"status": "authenticated"}))
            
            async for message in websocket:
                await self.handle_message(websocket, message)
                
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Client disconnected: {client_id}")
        except Exception as e:
            logger.error(f"Error with client {client_id}: {e}")
        finally:
            if client_id in self.clients:
                del self.clients[client_id]
    
    async def start(self):
        logger.info(f"Starting MCP Server on {self.host}:{self.port}")
        async with websockets.serve(self.handle_client, self.host, self.port):
            await asyncio.Future()

async def main():
    server = MCPServer()
    await server.start()

if __name__ == "__main__":
    asyncio.run(main())
