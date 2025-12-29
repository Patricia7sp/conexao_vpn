import asyncio
import json
from typing import Any, Dict, Optional
import websockets
from websockets.client import WebSocketClientProtocol

from ..core.config import settings
from ..utils.logger import setup_logger
from ..utils.network_detector import NetworkDetector

logger = setup_logger("mcp_client", settings.log.level, settings.log.log_file)

class MCPClient:
    def __init__(self, server_ip: str, server_port: int, token: str):
        self.server_ip = server_ip
        self.server_port = server_port
        self.token = token
        self.websocket: Optional[WebSocketClientProtocol] = None
        self.request_counter = 0
        self.pending_requests: Dict[str, asyncio.Future] = {}
        self.network_detector = NetworkDetector(
            settings.network.local_subnet,
            server_ip,
            settings.network.connection_timeout
        )
    
    async def connect(self) -> bool:
        try:
            network_status = await self.network_detector.detect_network_status()
            logger.info(f"Network status: {network_status.connection_type}")
            
            if not network_status.can_reach_ubuntu:
                logger.error("Cannot reach Ubuntu server")
                return False
            
            uri = f"ws://{self.server_ip}:{self.server_port}"
            self.websocket = await websockets.connect(uri)
            
            auth_message = json.dumps({"token": self.token})
            await self.websocket.send(auth_message)
            
            response = await self.websocket.recv()
            auth_result = json.loads(response)
            
            if auth_result.get("status") == "authenticated":
                logger.info("Successfully authenticated with MCP server")
                asyncio.create_task(self._receive_messages())
                return True
            else:
                logger.error(f"Authentication failed: {auth_result}")
                return False
                
        except Exception as e:
            logger.error(f"Connection error: {e}")
            return False
    
    async def _receive_messages(self):
        try:
            async for message in self.websocket:
                data = json.loads(message)
                request_id = data.get("request_id")
                
                if request_id in self.pending_requests:
                    future = self.pending_requests.pop(request_id)
                    if "error" in data:
                        future.set_exception(Exception(data["error"]))
                    else:
                        future.set_result(data.get("result"))
        except websockets.exceptions.ConnectionClosed:
            logger.warning("Connection closed by server")
        except Exception as e:
            logger.error(f"Error receiving messages: {e}")
    
    async def _send_request(self, tool: str, params: Dict[str, Any]) -> Any:
        if not self.websocket or self.websocket.closed:
            raise ConnectionError("Not connected to server")
        
        self.request_counter += 1
        request_id = f"req_{self.request_counter}"
        
        message = json.dumps({
            "request_id": request_id,
            "tool": tool,
            "params": params
        })
        
        future = asyncio.Future()
        self.pending_requests[request_id] = future
        
        await self.websocket.send(message)
        
        try:
            result = await asyncio.wait_for(future, timeout=30.0)
            return result
        except asyncio.TimeoutError:
            self.pending_requests.pop(request_id, None)
            raise TimeoutError(f"Request {request_id} timed out")
    
    async def list_files(self, path: str, recursive: bool = False) -> Dict[str, Any]:
        return await self._send_request("list_files", {"path": path, "recursive": recursive})
    
    async def read_file(self, path: str, encoding: str = "utf-8") -> Dict[str, Any]:
        return await self._send_request("read_file", {"path": path, "encoding": encoding})
    
    async def write_file(self, path: str, content: str, encoding: str = "utf-8") -> Dict[str, Any]:
        return await self._send_request("write_file", {
            "path": path,
            "content": content,
            "encoding": encoding
        })
    
    async def execute_command(self, command: str, cwd: Optional[str] = None) -> Dict[str, Any]:
        return await self._send_request("execute_command", {"command": command, "cwd": cwd})
    
    async def get_system_info(self) -> Dict[str, Any]:
        return await self._send_request("get_system_info", {})
    
    async def search_files(self, path: str, pattern: str, content_search: bool = False) -> Dict[str, Any]:
        return await self._send_request("search_files", {
            "path": path,
            "pattern": pattern,
            "content_search": content_search
        })
    
    async def disconnect(self):
        if self.websocket and not self.websocket.closed:
            await self.websocket.close()
            logger.info("Disconnected from MCP server")
    
    async def __aenter__(self):
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()
