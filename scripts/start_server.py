#!/usr/bin/env python3
import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.server.mcp_server import MCPServer
from src.core.config import settings
from src.utils.logger import setup_logger

logger = setup_logger("start_server", settings.log.level, settings.log.log_file)

async def main():
    logger.info("Iniciando servidor MCP no Ubuntu...")
    logger.info(f"Host: {settings.mcp.server_host}")
    logger.info(f"Port: {settings.mcp.server_port}")
    
    server = MCPServer()
    
    try:
        await server.start()
    except KeyboardInterrupt:
        logger.info("Servidor interrompido pelo usuário")
    except Exception as e:
        logger.error(f"Erro ao iniciar servidor: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
