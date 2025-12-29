#!/bin/bash

echo "=== Configurando VNC no Ubuntu para acesso remoto completo ==="

# Instalar servidor VNC
echo "Instalando servidor VNC..."
sudo apt update
sudo apt install -y tigervnc-standalone-server tigervnc-xorg-extension

# Instalar ambiente desktop (se não tiver)
echo "Verificando ambiente desktop..."
if ! dpkg -l | grep -q ubuntu-desktop; then
    echo "Instalando Ubuntu Desktop (mínimo)..."
    sudo apt install -y ubuntu-desktop-minimal
fi

# Configurar VNC
echo "Configurando VNC..."
mkdir -p ~/.vnc

# Criar script de inicialização
cat > ~/.vnc/xstartup << 'EOF'
#!/bin/bash
xrdb $HOME/.Xresources
startxfce4 &
EOF

chmod +x ~/.vnc/xstartup

# Definir senha VNC
echo "Definindo senha VNC (será solicitada):"
vncpasswd

echo ""
echo "=== Configuração VNC concluída! ==="
echo ""
echo "Para iniciar o VNC server:"
echo "vncserver :1 -geometry 1920x1080 -depth 24"
echo ""
echo "Para parar o VNC server:"
echo "vncserver -kill :1"
echo ""
echo "Para conectar do MacBook via VNC:"
echo "1. Use o IP do Tailscale: 100.78.16.90:5901"
echo "2. Ou use o IP local: 192.168.68.118:5901"
echo "3. Use um cliente VNC como:"
echo "   - RealVNC Viewer"
echo "   - Chrome Remote Desktop"
echo "   - Ou o app 'Screen Sharing' nativo do macOS"
