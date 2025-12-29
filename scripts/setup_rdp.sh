#!/bin/bash

echo "=== Configurando RDP (xrdp) no Ubuntu para acesso nativo do macOS ==="

# Instalar xrdp
echo "Instalando xrdp..."
sudo apt update
sudo apt install -y xrdp

# Adicionar usuário xrdp ao grupo ssl-cert
sudo adduser xrdp ssl-cert

# Configurar ambiente desktop
echo "Configurando ambiente desktop..."
if ! dpkg -l | grep -q xfce4; then
    echo "Instalando XFCE4 (leve e eficiente)..."
    sudo apt install -y xfce4 xfce4-goodies
fi

# Configurar xrdp para usar XFCE
echo ". /usr/share/xfce4/xinitrc" > ~/.xsession

# Configurar xrdp para permitir conexões
sudo sed -i 's/port=3389/port=3389/g' /etc/xrdp/xrdp.ini
sudo sed -i 's/max_bpp=32/max_bpp=128/g' /etc/xrdp/xrdp.ini
sudo sed -i 's/xserverbpp=24/xserverbpp=128/g' /etc/xrdp/xrdp.ini

# Reiniciar serviço xrdp
sudo systemctl restart xrdp
sudo systemctl enable xrdp

echo ""
echo "=== Configuração RDP concluída! ==="
echo ""
echo "Para conectar do MacBook via RDP (nativo):"
echo "1. Abra o app 'Conexão de Área de Trabalho Remota' (Microsoft Remote Desktop)"
echo "2. Adicione novo PC com:"
echo "   - IP Tailscale: 100.78.16.90"
echo "   - OU IP local: 192.168.68.118"
echo "3. Use seu usuário e senha do Ubuntu"
echo ""
echo "Vantagens do RDP:"
echo "- Nativo no macOS"
echo "- Melhor performance que VNC"
echo "- Suporte a áudio redirecionado"
echo "- Compartilhamento de clipboard"
