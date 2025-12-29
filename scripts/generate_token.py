#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.server.mcp_server import MCPServer
from src.core.config import settings

def main():
    if not settings.security.jwt_secret:
        print("ERRO: JWT_SECRET não configurado no arquivo .env")
        print("Por favor, configure JWT_SECRET no arquivo .env")
        sys.exit(1)
    
    server = MCPServer()
    
    client_id = input("Digite o ID do cliente (ex: macbook-pro): ")
    token = server.generate_token(client_id)
    
    print("\n" + "="*60)
    print("TOKEN GERADO COM SUCESSO!")
    print("="*60)
    print(f"\nCliente: {client_id}")
    print(f"Token: {token}")
    print("\nGuarde este token em local seguro.")
    print("Use este token para conectar o cliente ao servidor.")
    print("="*60)

if __name__ == "__main__":
    main()
