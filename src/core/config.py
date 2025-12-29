import os
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class NetworkConfig(BaseModel):
    local_subnet: str = Field(default="192.168.1.0/24")
    connection_timeout: int = Field(default=5)
    tailscale_enabled: bool = Field(default=True)
    ubuntu_tailscale_ip: Optional[str] = None
    macbook_tailscale_ip: Optional[str] = None

class MCPConfig(BaseModel):
    server_host: str = Field(default="0.0.0.0")
    server_port: int = Field(default=8765)
    secret_key: str = Field(default="")

class SecurityConfig(BaseModel):
    jwt_secret: str = Field(default="")
    jwt_expiration: int = Field(default=3600)

class AIConfig(BaseModel):
    openai_api_key: str = Field(default="")
    model: str = Field(default="gpt-4")
    temperature: float = Field(default=0.7)

class LogConfig(BaseModel):
    level: str = Field(default="INFO")
    log_file: str = Field(default="logs/conexao_vpn.log")

class Settings(BaseModel):
    network: NetworkConfig = Field(default_factory=NetworkConfig)
    mcp: MCPConfig = Field(default_factory=MCPConfig)
    security: SecurityConfig = Field(default_factory=SecurityConfig)
    ai: AIConfig = Field(default_factory=AIConfig)
    log: LogConfig = Field(default_factory=LogConfig)
    
    @classmethod
    def load_from_env(cls) -> "Settings":
        return cls(
            network=NetworkConfig(
                local_subnet=os.getenv("LOCAL_NETWORK_SUBNET", "192.168.1.0/24"),
                connection_timeout=int(os.getenv("CONNECTION_TIMEOUT", "5")),
                tailscale_enabled=os.getenv("TAILSCALE_ENABLED", "true").lower() == "true",
                ubuntu_tailscale_ip=os.getenv("UBUNTU_TAILSCALE_IP"),
                macbook_tailscale_ip=os.getenv("MACBOOK_TAILSCALE_IP"),
            ),
            mcp=MCPConfig(
                server_host=os.getenv("MCP_SERVER_HOST", "0.0.0.0"),
                server_port=int(os.getenv("MCP_SERVER_PORT", "8765")),
                secret_key=os.getenv("MCP_SECRET_KEY", ""),
            ),
            security=SecurityConfig(
                jwt_secret=os.getenv("JWT_SECRET", ""),
                jwt_expiration=int(os.getenv("JWT_EXPIRATION", "3600")),
            ),
            ai=AIConfig(
                openai_api_key=os.getenv("OPENAI_API_KEY", ""),
            ),
            log=LogConfig(
                level=os.getenv("LOG_LEVEL", "INFO"),
                log_file=os.getenv("LOG_FILE", "logs/conexao_vpn.log"),
            ),
        )

settings = Settings.load_from_env()
