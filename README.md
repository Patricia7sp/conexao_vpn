# Conexão VPN Inteligente com MCP

Sistema de conexão remota inteligente entre MacBook Pro e Ubuntu usando MCP + LangGraph + CrewAI.

## 🎯 Objetivo

Acessar remotamente todos os dados e recursos do computador Ubuntu (Lenovo) através do MacBook Pro, com gerenciamento autônomo por agentes inteligentes.

## 🏗️ Arquitetura

```
MacBook Pro (Cliente)
    ↓
Agente Inteligente (CrewAI + LangGraph)
    ↓
[Mesma Rede?] ── Sim ──→ Acesso Direto MCP
    └─ Não ──→ Tailscale VPN → Servidor MCP (Ubuntu)
```

## 📦 Componentes

### 1. Servidor MCP (Ubuntu)
- Expor recursos do sistema (arquivos, terminal, documentos)
- Agentes de monitoramento e otimização
- Segurança e autenticação

### 2. Cliente Inteligente (MacBook)
- Detecção automática de rede
- Interface via linguagem natural
- Gerenciamento de conexão

### 3. Sistema de Agentes
- **Agente de Conectividade**: Gerencia redes e fallbacks
- **Agente de Documentos**: Indexação e busca inteligente
- **Agente de Projetos**: Gestão de ambientes de desenvolvimento
- **Agente de Segurança**: Monitoramento e controle de acesso

## 🚀 Funcionalidades

- ✅ Acesso total ao sistema Ubuntu de forma segura
- ✅ Conexão automática (local ou VPN)
- ✅ Interface via comandos naturais
- ✅ Agentes inteligentes para otimização
- ✅ Escalável para múltiplos dispositivos

## 🔧 Instalação

```bash
# Clonar projeto
git clone <repo>
cd conexao_vpn

# Ativar ambiente virtual
source vpn/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

## 📝 Configuração

1. Configurar Tailscale em ambas máquinas
2. Definir variáveis de ambiente no `.env`
3. Iniciar servidor MCP no Ubuntu
4. Conectar cliente no MacBook

## 🔐 Segurança

- Criptografia ponta a ponta
- Autenticação via JWT
- Controle granular de permissões
- Monitoramento de acessos
