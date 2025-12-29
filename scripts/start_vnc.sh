#!/bin/bash

echo "=== Iniciando VNC Server para Acesso Remoto ==="

# Parar qualquer instância anterior
pkill x11vnc 2>/dev/null

# Criar diretório VNC se não existir
mkdir -p ~/.vnc

# Definir senha VNC (você pode mudar depois)
echo "Configurando senha VNC..."
x11vnc -storepasswd vnc123 ~/.vnc/passwd 2>/dev/null

# Iniciar x11vnc compartilhando a sessão atual
echo "Iniciando x11vnc..."
x11vnc -display :0 \
       -auth guess \
       -forever \
       -noxdamage \
       -repeat \
       -rfbauth ~/.vnc/passwd \
       -rfbport 5900 \
       -shared \
       -bg \
       -o ~/.vnc/x11vnc.log

sleep 2

if pgrep -x "x11vnc" > /dev/null; then
    echo ""
    echo "=== VNC Server Iniciado com Sucesso! ==="
    echo ""
    echo "Para conectar do MacBook:"
    echo "1. Abra 'Finder' → 'Ir' → 'Conectar ao Servidor' (⌘+K)"
    echo "2. Digite: vnc://192.168.68.118:5900"
    echo "3. Ou via Tailscale: vnc://100.78.16.90:5900"
    echo "4. Senha: vnc123"
    echo ""
    echo "Para parar o VNC: pkill x11vnc"
else
    echo ""
    echo "ERRO: VNC não iniciou. Verifique os logs em ~/.vnc/x11vnc.log"
fi
