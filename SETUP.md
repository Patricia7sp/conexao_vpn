# Guia de Instalação e Configuração

## 📋 Pré-requisitos

### Ubuntu (Lenovo)
- Python 3.8+
- Tailscale instalado e configurado
- Acesso root ou sudo

### MacBook Pro
- Python 3.8+
- Tailscale instalado e configurado

## 🚀 Instalação

### 1. No Ubuntu (Servidor)

```bash
# Clone o projeto
cd ~/
git clone <repo_url> conexao_vpn
cd conexao_vpn

# Crie e ative o ambiente virtual
python3 -m venv vpn
source vpn/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
nano .env
```

**Configure o .env com:**
```env
OPENAI_API_KEY=sua_chave_aqui
MCP_SERVER_HOST=0.0.0.0
MCP_SERVER_PORT=8765
MCP_SECRET_KEY=uma_chave_secreta_forte
JWT_SECRET=outra_chave_secreta_forte
TAILSCALE_ENABLED=true
LOCAL_NETWORK_SUBNET=192.168.1.0/24
```

**Gere um token de autenticação:**
```bash
python scripts/generate_token.py
# Guarde o token gerado - você precisará dele no MacBook
```

**Inicie o servidor:**
```bash
python scripts/start_server.py
```

### 2. No MacBook Pro (Cliente)

```bash
# Clone o projeto
cd ~/
git clone <repo_url> conexao_vpn
cd conexao_vpn

# Crie e ative o ambiente virtual
python3 -m venv vpn
source vpn/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
nano .env
```

**Configure o .env com:**
```env
OPENAI_API_KEY=sua_chave_aqui
UBUNTU_TAILSCALE_IP=100.x.x.x  # IP Tailscale do Ubuntu
TAILSCALE_ENABLED=true
LOCAL_NETWORK_SUBNET=192.168.1.0/24
```

**Inicie o cliente:**
```bash
python scripts/start_client.py --server-ip 100.x.x.x --token SEU_TOKEN_AQUI
```

## 🔧 Configuração do Tailscale

### No Ubuntu:
```bash
# Instalar Tailscale
curl -fsSL https://tailscale.com/install.sh | sh

# Iniciar e autenticar
sudo tailscale up

# Verificar IP
tailscale ip -4
```

### No MacBook:
```bash
# Instalar Tailscale
brew install tailscale

# Iniciar e autenticar
sudo tailscale up

# Verificar IP
tailscale ip -4
```

## 🎯 Uso

### Comandos Disponíveis no Cliente:

1. **Listar arquivos** - Navegar pelo sistema de arquivos do Ubuntu
2. **Ler arquivo** - Visualizar conteúdo de arquivos
3. **Buscar arquivos** - Buscar por padrões de nome
4. **Informações do sistema** - Ver status do Ubuntu
5. **Executar comando** - Executar comandos remotamente
6. **Status da conexão** - Verificar tipo de conexão (local/VPN)

### Exemplo de Uso:

```bash
# Conectar ao servidor
python scripts/start_client.py

# O sistema detectará automaticamente se você está:
# - Na mesma rede local (conexão direta)
# - Em rede diferente (usa Tailscale VPN)

# Navegue pelo menu interativo
```

## 🔐 Segurança

- Tokens JWT com expiração configurável
- Criptografia ponta a ponta via Tailscale
- Autenticação obrigatória para todas as operações
- Logs de todas as ações

## 🤖 Agentes Inteligentes

O sistema usa 3 agentes principais:

1. **Agente de Conectividade**: Monitora e gerencia conexões
2. **Agente de Arquivos**: Busca e organiza arquivos inteligentemente
3. **Agente de Projetos**: Analisa projetos de desenvolvimento

## 📊 Monitoramento

Logs são salvos em: `logs/conexao_vpn.log`

```bash
# Ver logs em tempo real
tail -f logs/conexao_vpn.log
```

## 🐛 Troubleshooting

### Problema: Não consegue conectar

**Solução:**
```bash
# Verificar Tailscale
tailscale status

# Verificar se o servidor está rodando
ps aux | grep mcp_server

# Testar conectividade
ping <ubuntu_tailscale_ip>
```

### Problema: Token inválido

**Solução:**
```bash
# Gerar novo token no Ubuntu
python scripts/generate_token.py
```

### Problema: Erro de dependências

**Solução:**
```bash
# Reinstalar dependências
pip install --upgrade -r requirements.txt
```

## 📝 Notas Importantes

- Mantenha o servidor Ubuntu sempre ligado para acesso remoto
- Configure o Ubuntu para não suspender quando a tampa estiver fechada
- Use senhas fortes para JWT_SECRET e MCP_SECRET_KEY
- Faça backup regular dos tokens gerados
- Monitore os logs para detectar acessos não autorizados
