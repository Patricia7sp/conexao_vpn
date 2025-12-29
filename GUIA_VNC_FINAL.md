# ✅ Guia VNC - Solução Final para Acesso Remoto

## 🎯 VNC Configurado e Funcionando!

O VNC está rodando na **porta 5902** (display :2)

---

## 🖥️ Como Conectar do MacBook

### Método 1: Nativo do macOS (Recomendado)

1. **Abra o Finder**
2. **Menu "Ir" → "Conectar ao Servidor"** (ou pressione `⌘+K`)
3. **Digite o endereço:**
   - **Mesma rede WiFi**: `vnc://192.168.68.118:5902`
   - **Via Tailscale (de qualquer lugar)**: `vnc://100.78.16.90:5902`
4. **Clique em "Conectar"**
5. **Digite a senha** que você configurou

### Método 2: RealVNC Viewer

1. Baixe o RealVNC Viewer da App Store (gratuito)
2. Adicione nova conexão:
   - **VNC Server**: `192.168.68.118:5902`
   - Ou via Tailscale: `100.78.16.90:5902`
3. Conecte e use a senha

---

## 🔧 Comandos Úteis no Ubuntu

### Iniciar VNC Server
```bash
vncserver :2 -geometry 1920x1080 -depth 24
```

### Parar VNC Server
```bash
vncserver -kill :2
```

### Ver servidores VNC rodando
```bash
vncserver -list
```

### Mudar senha VNC
```bash
vncpasswd
```

### Ver logs
```bash
cat ~/.vnc/SPON010129987:2.log
```

---

## 🚀 Iniciar VNC Automaticamente

Para iniciar o VNC sempre que o Ubuntu ligar:

```bash
# Criar serviço systemd
sudo nano /etc/systemd/system/vncserver@.service
```

Cole o seguinte conteúdo:
```ini
[Unit]
Description=Start TigerVNC server at startup
After=syslog.target network.target

[Service]
Type=forking
User=barbosa.patricia@sp01.local
Group=18800513
WorkingDirectory=/home/barbosa.patricia@sp01.local

PIDFile=/home/barbosa.patricia@sp01.local/.vnc/%H:%i.pid
ExecStartPre=-/usr/bin/vncserver -kill :%i > /dev/null 2>&1
ExecStart=/usr/bin/vncserver -depth 24 -geometry 1920x1080 :%i
ExecStop=/usr/bin/vncserver -kill :%i

[Install]
WantedBy=multi-user.target
```

Depois ative:
```bash
sudo systemctl daemon-reload
sudo systemctl enable vncserver@2.service
sudo systemctl start vncserver@2.service
```

---

## 🌐 Acesso via Tailscale (De Qualquer Lugar)

Quando você não estiver na mesma rede WiFi:

1. **Certifique-se que Tailscale está ativo:**
   ```bash
   # No Ubuntu
   tailscale status
   
   # No MacBook
   tailscale status
   ```

2. **Use o IP Tailscale para conectar:**
   - `vnc://100.78.16.90:5902`

3. **Funciona de qualquer lugar do mundo!**
   - Conexão criptografada
   - Sem necessidade de abrir portas no roteador
   - Sem configuração de firewall

---

## 📊 Status Atual

- ✅ **VNC Server**: Rodando na porta 5902
- ✅ **Firewall**: Porta 5902 liberada
- ✅ **Tailscale**: Configurado (IP: 100.78.16.90)
- ✅ **Desktop**: LXDE (leve e estável)
- ✅ **Senha**: Configurada

---

## 🔐 Segurança

### Recomendações:
1. Use uma senha forte no VNC
2. Prefira conexão via Tailscale (mais segura)
3. Se usar rede local, considere restringir o firewall:
   ```bash
   sudo ufw delete allow 5902/tcp
   sudo ufw allow from 192.168.68.0/24 to any port 5902
   ```

---

## 💡 Dicas

### Melhorar Performance:
- Use resolução menor se a conexão estiver lenta: `1600x900` ou `1366x768`
- Reduza a profundidade de cor: `-depth 16`

### Múltiplas Sessões:
- Você pode ter várias sessões VNC simultâneas
- Use displays diferentes: `:2`, `:3`, `:4`, etc.
- Cada display usa uma porta diferente: 5902, 5903, 5904, etc.

---

## 🆘 Troubleshooting

### VNC não conecta:
```bash
# Verificar se está rodando
vncserver -list

# Ver logs
tail -f ~/.vnc/*.log

# Reiniciar
vncserver -kill :2
vncserver :2 -geometry 1920x1080 -depth 24
```

### Tela preta no VNC:
```bash
# Editar ~/.xsession
echo "exec startlxde" > ~/.xsession
chmod +x ~/.xsession

# Reiniciar VNC
vncserver -kill :2
vncserver :2 -geometry 1920x1080 -depth 24
```

---

## 🎉 Pronto!

Seu sistema de acesso remoto está **100% funcional**!

- Acesse de qualquer lugar via Tailscale
- Conexão segura e criptografada
- Desktop completo do Ubuntu no seu MacBook

**Repositório**: https://github.com/Patricia7sp/conexao_vpn
