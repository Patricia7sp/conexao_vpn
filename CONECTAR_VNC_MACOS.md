# Como Conectar VNC no macOS

## ✅ Solução para "URLs com o tipo vnc: não são compatíveis"

O macOS não aceita URLs `vnc://` no Finder. Use um destes métodos:

---

## 🎯 Método 1: Screen Sharing (Nativo do macOS) - RECOMENDADO

### Passo a Passo:

1. **Abra o Spotlight** (⌘ + Espaço)

2. **Digite**: `Screen Sharing` e pressione Enter

3. **Na janela que abrir, digite o endereço:**
   - **Mesma rede**: `192.168.68.118:5902`
   - **Via Tailscale**: `100.78.16.90:5902`

4. **Clique em "Connect"**

5. **Digite a senha VNC** que você configurou

6. **Pronto!** Você verá a área de trabalho do Ubuntu

---

## 🎯 Método 2: Safari (Mais Fácil)

1. **Abra o Safari**

2. **Na barra de endereços, digite:**
   ```
   vnc://192.168.68.118:5902
   ```
   Ou via Tailscale:
   ```
   vnc://100.78.16.90:5902
   ```

3. **Pressione Enter**

4. **O Safari abrirá automaticamente o Screen Sharing**

5. **Digite a senha e conecte**

---

## 🎯 Método 3: Terminal

1. **Abra o Terminal** (⌘ + Espaço → Terminal)

2. **Execute:**
   ```bash
   open vnc://192.168.68.118:5902
   ```
   Ou via Tailscale:
   ```bash
   open vnc://100.78.16.90:5902
   ```

3. **O Screen Sharing abrirá automaticamente**

---

## 🎯 Método 4: RealVNC Viewer (App Dedicado)

Se preferir um app dedicado:

1. **Baixe RealVNC Viewer** da App Store (gratuito)

2. **Abra o app**

3. **Clique em "+" para adicionar conexão**

4. **Configure:**
   - **VNC Server**: `192.168.68.118:5902`
   - **Name**: Ubuntu Lenovo
   - Clique em "OK"

5. **Clique duas vezes** na conexão criada

6. **Digite a senha** e conecte

---

## 📋 Endereços de Conexão

### Rede Local (mesma WiFi):
- **IP**: `192.168.68.118`
- **Porta**: `5902`
- **Endereço completo**: `192.168.68.118:5902`

### Via Tailscale (de qualquer lugar):
- **IP**: `100.78.16.90`
- **Porta**: `5902`
- **Endereço completo**: `100.78.16.90:5902`

---

## 🔐 Senha

Use a senha que você configurou com o comando `vncpasswd` no Ubuntu.

---

## 🆘 Troubleshooting

### "Não foi possível conectar"

**No Ubuntu, verifique se o VNC está rodando:**
```bash
vncserver -list
```

**Se não estiver, inicie:**
```bash
vncserver :2 -geometry 1920x1080 -depth 24
```

### "Conexão recusada"

**Verifique o firewall no Ubuntu:**
```bash
sudo ufw status
sudo ufw allow 5902/tcp
```

### "Senha incorreta"

**Redefina a senha no Ubuntu:**
```bash
vncpasswd
```

Depois reinicie o VNC:
```bash
vncserver -kill :2
vncserver :2 -geometry 1920x1080 -depth 24
```

---

## 💡 Dica Rápida

**Maneira mais fácil:**
1. Abra o **Spotlight** (⌘ + Espaço)
2. Digite: **Screen Sharing**
3. Digite: **192.168.68.118:5902**
4. Conecte!

---

## 🎉 Pronto!

Agora você tem acesso completo ao seu Ubuntu remotamente pelo MacBook!
