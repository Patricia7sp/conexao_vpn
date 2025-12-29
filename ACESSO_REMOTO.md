# Guia de Acesso Remoto Completo ao Ubuntu

## 🎯 Objetivo
Acessar o notebook Ubuntu remotamente do MacBook como se estivesse usando localmente.

## 🔧 Opções de Acesso Remoto

### Opção 1: RDP (Recomendado) ⭐
**Melhor para**: Acesso completo à área de trabalho com melhor performance

**Vantagens:**
- ✅ Nativo no macOS (Microsoft Remote Desktop)
- ✅ Melhor performance
- ✅ Suporte a áudio
- ✅ Compartilhamento de clipboard
- ✅ Redirecionamento de impressora

**Como usar:**

1. **No Ubuntu (já configurado pelo script):**
   ```bash
   sudo systemctl status xrdp  # Verificar se está rodando
   ```

2. **No MacBook:**
   - Baixe o app "Microsoft Remote Desktop" da App Store
   - Clique em "Add PC"
   - Configure:
     - **PC name**: `192.168.68.118` (mesma rede) ou `100.78.16.90` (Tailscale)
     - **User account**: Seu usuário do Ubuntu
     - **Password**: Sua senha do Ubuntu
   - Clique em conectar

---

### Opção 2: VNC
**Melhor para**: Alternativa ao RDP

**Como usar:**

1. **No Ubuntu:**
   ```bash
   chmod +x scripts/setup_vnc.sh
   ./scripts/setup_vnc.sh
   vncserver :1 -geometry 1920x1080 -depth 24
   ```

2. **No MacBook:**
   - Use o app "Screen Sharing" nativo
   - Ou baixe "RealVNC Viewer"
   - Conecte em: `192.168.68.118:5901`

---

### Opção 3: SSH + X11 Forwarding
**Melhor para**: Executar aplicações gráficas específicas

**Como usar:**

1. **No MacBook:**
   ```bash
   # Instalar XQuartz (servidor X11 para macOS)
   brew install --cask xquartz
   
   # Conectar via SSH com X11
   ssh -X barbosa.patricia@192.168.68.118
   
   # Executar aplicações gráficas
   nautilus &  # Gerenciador de arquivos
   gedit &     # Editor de texto
   firefox &   # Navegador
   ```

---

### Opção 4: SSH Simples
**Melhor para**: Terminal e comandos

**Como usar:**

```bash
# Do MacBook
ssh barbosa.patricia@192.168.68.118

# Ou via Tailscale
ssh barbosa.patricia@100.78.16.90
```

---

## 🌐 Conexão via Tailscale (Fora da Rede Local)

Quando você não estiver na mesma rede WiFi:

1. **Certifique-se que Tailscale está ativo em ambas máquinas:**
   ```bash
   # Ubuntu
   tailscale status
   
   # MacBook
   tailscale status
   ```

2. **Use o IP do Tailscale:**
   - Ubuntu: `100.78.16.90`
   - MacBook: `100.77.109.29`

3. **Conecte normalmente usando o IP do Tailscale**

---

## 🚀 Acesso Dinâmico com MCP + Agentes IA

O sistema MCP que criamos oferece:

### Modo Interativo Inteligente
```bash
# No MacBook
cd ~/conexao_vpn
source vpn/bin/activate
python scripts/start_client.py --server-ip 192.168.68.118 --token SEU_TOKEN
```

**Funcionalidades:**
- 🤖 Agentes IA gerenciam conexão automaticamente
- 📁 Acesso a arquivos com busca inteligente
- 💻 Execução de comandos remotos
- 📊 Informações do sistema
- 🔍 Busca semântica em projetos

---

## 📋 Resumo Rápido

| Método | Uso | Performance | Facilidade |
|--------|-----|-------------|------------|
| **RDP** | Área de trabalho completa | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **VNC** | Área de trabalho completa | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **SSH + X11** | Apps gráficas específicas | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **SSH** | Terminal/comandos | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **MCP + IA** | Acesso inteligente | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

---

## 🔐 Segurança

- ✅ Todas conexões via Tailscale são criptografadas
- ✅ RDP usa autenticação do Ubuntu
- ✅ SSH usa chaves ou senha
- ✅ MCP usa tokens JWT

---

## 🆘 Troubleshooting

### RDP não conecta
```bash
# Ubuntu
sudo systemctl restart xrdp
sudo ufw allow 3389/tcp
```

### VNC não conecta
```bash
# Ubuntu
vncserver -kill :1
vncserver :1 -geometry 1920x1080 -depth 24
```

### SSH não conecta
```bash
# Ubuntu
sudo systemctl restart ssh
sudo ufw allow 22/tcp
```
