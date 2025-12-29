# Troubleshooting RDP - Conexão Caindo

## ✅ Problema Resolvido

O problema era que o XFCE não estava configurado corretamente para o xrdp.

### Solução Aplicada:

1. **Criado arquivo `.xsession`:**
   ```bash
   echo "xfce4-session" > ~/.xsession
   ```

2. **Criado arquivo `.xsessionrc`:**
   ```bash
   cat > ~/.xsessionrc << 'EOF'
   #!/bin/bash
   export XDG_SESSION_DESKTOP=xfce
   export XDG_DATA_DIRS=/usr/share/xfce4:/usr/local/share:/usr/share:/var/lib/snapd/desktop
   export XDG_CONFIG_DIRS=/etc/xdg/xfce4:/etc/xdg
   EOF
   chmod +x ~/.xsessionrc
   ```

3. **Reiniciado o serviço:**
   ```bash
   sudo systemctl restart xrdp
   ```

---

## 🔧 Como Conectar Agora

### No MacBook:

1. **Abra o Microsoft Remote Desktop**

2. **Configure:**
   - **PC name**: `192.168.68.118`
   - **User account**: `barbosa.patricia@sp01.local`
   - **Password**: sua senha do Ubuntu

3. **Conecte!**
   - A conexão deve permanecer estável agora
   - Você verá a área de trabalho XFCE

---

## 🐛 Se Ainda Tiver Problemas

### Verificar logs:
```bash
# Ver logs do xrdp
sudo journalctl -u xrdp -f

# Ver logs do sesman
sudo journalctl -u xrdp-sesman -f
```

### Reiniciar serviços:
```bash
sudo systemctl restart xrdp
sudo systemctl restart xrdp-sesman
```

### Verificar se está rodando:
```bash
sudo systemctl status xrdp
sudo netstat -tlnp | grep 3389
```

### Testar conexão de rede:
```bash
# Do MacBook
ping 192.168.68.118
telnet 192.168.68.118 3389
```

---

## 🎯 Alternativas se RDP Não Funcionar

### Opção 1: VNC
```bash
# No Ubuntu
sudo apt install tigervnc-standalone-server
vncserver :1 -geometry 1920x1080 -depth 24

# No MacBook
# Use "Screen Sharing" ou "RealVNC Viewer"
# Conecte em: 192.168.68.118:5901
```

### Opção 2: SSH + X11 Forwarding
```bash
# No MacBook
brew install --cask xquartz
ssh -X barbosa.patricia@192.168.68.118
```

### Opção 3: Chrome Remote Desktop
- Mais fácil de configurar
- Funciona através de firewall/NAT
- https://remotedesktop.google.com/

---

## 📊 Status dos Serviços

```bash
# Verificar tudo de uma vez
sudo systemctl status xrdp xrdp-sesman --no-pager
```

---

## 🔐 Segurança

Se quiser aumentar a segurança:

```bash
# Permitir apenas IPs específicos
sudo ufw delete allow 3389/tcp
sudo ufw allow from 192.168.68.0/24 to any port 3389
```
