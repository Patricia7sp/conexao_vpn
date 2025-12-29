import asyncio
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

from ..client.mcp_client import MCPClient
from ..agents.orchestrator import AgentOrchestrator
from ..core.config import settings
from ..utils.logger import setup_logger

console = Console()
logger = setup_logger("cli", settings.log.level, settings.log.log_file)

class VPNConnectionCLI:
    def __init__(self, server_ip: str, token: str):
        self.server_ip = server_ip
        self.token = token
        self.client = None
        self.orchestrator = AgentOrchestrator(server_ip)
    
    async def connect(self):
        console.print("[bold blue]Conectando ao servidor Ubuntu...[/bold blue]")
        
        connection_status = await self.orchestrator.check_and_ensure_connection()
        
        if connection_status.get("success") or connection_status.get("can_reach"):
            console.print(f"[bold green]✓[/bold green] {connection_status.get('message', 'Conectado com sucesso')}")
            console.print(f"[dim]Tipo de conexão: {connection_status.get('connection_type', 'unknown')}[/dim]")
            
            self.client = MCPClient(self.server_ip, settings.mcp.server_port, self.token)
            connected = await self.client.connect()
            
            if connected:
                console.print("[bold green]✓ Cliente MCP conectado[/bold green]")
                return True
        
        console.print("[bold red]✗ Falha na conexão[/bold red]")
        return False
    
    async def list_files_interactive(self):
        path = Prompt.ask("Digite o caminho", default="~")
        recursive = Prompt.ask("Busca recursiva?", choices=["sim", "não"], default="não") == "sim"
        
        console.print(f"[dim]Listando arquivos em {path}...[/dim]")
        result = await self.client.list_files(path, recursive)
        
        if "error" in result:
            console.print(f"[bold red]Erro: {result['error']}[/bold red]")
            return
        
        table = Table(title=f"Arquivos em {path}")
        table.add_column("Nome", style="cyan")
        table.add_column("Tipo", style="magenta")
        table.add_column("Tamanho", style="green")
        
        for file in result.get("files", [])[:50]:
            size = f"{file.get('size', 0):,} bytes" if file.get('size') else "N/A"
            table.add_row(file["name"], file["type"], size)
        
        console.print(table)
        console.print(f"[dim]Total: {result.get('count', 0)} arquivos[/dim]")
    
    async def read_file_interactive(self):
        path = Prompt.ask("Digite o caminho do arquivo")
        
        console.print(f"[dim]Lendo arquivo {path}...[/dim]")
        result = await self.client.read_file(path)
        
        if "error" in result:
            console.print(f"[bold red]Erro: {result['error']}[/bold red]")
            return
        
        content = result.get("content", "")
        console.print(Panel(content[:1000], title=f"Conteúdo de {path}", border_style="blue"))
        
        if len(content) > 1000:
            console.print(f"[dim]... (mostrando primeiros 1000 caracteres de {len(content)})[/dim]")
    
    async def search_files_interactive(self):
        path = Prompt.ask("Digite o caminho base", default="~")
        pattern = Prompt.ask("Digite o padrão de busca (ex: *.py)")
        
        console.print(f"[dim]Buscando arquivos...[/dim]")
        result = await self.client.search_files(path, pattern)
        
        if "error" in result:
            console.print(f"[bold red]Erro: {result['error']}[/bold red]")
            return
        
        results = result.get("results", [])
        for i, file_path in enumerate(results[:20], 1):
            console.print(f"{i}. [cyan]{file_path}[/cyan]")
        
        console.print(f"[dim]Total: {result.get('count', 0)} arquivos encontrados[/dim]")
    
    async def get_system_info_interactive(self):
        console.print("[dim]Obtendo informações do sistema...[/dim]")
        result = await self.client.get_system_info()
        
        if "error" in result:
            console.print(f"[bold red]Erro: {result['error']}[/bold red]")
            return
        
        table = Table(title="Informações do Sistema Ubuntu")
        table.add_column("Propriedade", style="cyan")
        table.add_column("Valor", style="green")
        
        for key, value in result.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    table.add_row(f"{key}.{sub_key}", str(sub_value))
            else:
                table.add_row(key, str(value))
        
        console.print(table)
    
    async def execute_command_interactive(self):
        command = Prompt.ask("Digite o comando")
        cwd = Prompt.ask("Diretório de trabalho (opcional)", default="")
        
        console.print(f"[dim]Executando comando: {command}...[/dim]")
        result = await self.client.execute_command(command, cwd if cwd else None)
        
        if "error" in result:
            console.print(f"[bold red]Erro: {result['error']}[/bold red]")
            return
        
        console.print(f"[bold]Return Code:[/bold] {result.get('returncode')}")
        
        if result.get("stdout"):
            console.print(Panel(result["stdout"], title="STDOUT", border_style="green"))
        
        if result.get("stderr"):
            console.print(Panel(result["stderr"], title="STDERR", border_style="red"))
    
    async def show_menu(self):
        while True:
            console.print("\n[bold cyan]═══ Menu Principal ═══[/bold cyan]")
            console.print("1. Listar arquivos")
            console.print("2. Ler arquivo")
            console.print("3. Buscar arquivos")
            console.print("4. Informações do sistema")
            console.print("5. Executar comando")
            console.print("6. Status da conexão")
            console.print("0. Sair")
            
            choice = Prompt.ask("Escolha uma opção", choices=["0", "1", "2", "3", "4", "5", "6"])
            
            try:
                if choice == "0":
                    break
                elif choice == "1":
                    await self.list_files_interactive()
                elif choice == "2":
                    await self.read_file_interactive()
                elif choice == "3":
                    await self.search_files_interactive()
                elif choice == "4":
                    await self.get_system_info_interactive()
                elif choice == "5":
                    await self.execute_command_interactive()
                elif choice == "6":
                    status = await self.orchestrator.check_and_ensure_connection()
                    console.print(Panel(str(status), title="Status da Conexão", border_style="blue"))
            except Exception as e:
                console.print(f"[bold red]Erro: {e}[/bold red]")
                logger.error(f"Error in menu: {e}")
    
    async def disconnect(self):
        if self.client:
            await self.client.disconnect()
        console.print("[bold yellow]Desconectado[/bold yellow]")

@click.command()
@click.option('--server-ip', default=None, help='IP do servidor Ubuntu')
@click.option('--token', default=None, help='Token de autenticação')
def main(server_ip, token):
    if not server_ip:
        server_ip = settings.network.ubuntu_tailscale_ip or Prompt.ask("Digite o IP do servidor Ubuntu")
    
    if not token:
        token = Prompt.ask("Digite o token de autenticação", password=True)
    
    cli = VPNConnectionCLI(server_ip, token)
    
    async def run():
        try:
            if await cli.connect():
                await cli.show_menu()
        finally:
            await cli.disconnect()
    
    asyncio.run(run())

if __name__ == "__main__":
    main()
