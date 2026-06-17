#!/bin/bash
# connect-tailscale.sh — Conecta Claude à rede Tailscale do Ramon
# Uso: bash connect-tailscale.sh TS_AUTH_KEY="tskey-auth-xxxxx"

set -e

echo "╔══════════════════════════════════════════╗"
echo "║  Claude → Tailscale → Máquinas do Ramon  ║"
echo "╚══════════════════════════════════════════╝"

# Verifica se a key foi passada como variável de ambiente
if [ -z "$TS_AUTH_KEY" ]; then
    echo ""
    echo "❌ Auth key não encontrada."
    echo "   Uso: TS_AUTH_KEY='tskey-auth-xxxx' bash connect-tailscale.sh"
    echo ""
    echo "   Para gerar a key:"
    echo "   → Acesse: https://login.tailscale.com/admin/settings/keys"
    echo "   → Generate auth key → Reusable: ON → Expiry: 90 days"
    exit 1
fi

# Instala Tailscale se necessário
if ! command -v tailscale &>/dev/null; then
    echo "📦 Instalando Tailscale..."
    curl -fsSL https://tailscale.com/install.sh | sh -q
fi

# Inicia o daemon
tailscaled --tun=userspace-networking --state=/tmp/tailscaled.state &>/tmp/tailscaled.log &
sleep 3

# Conecta à rede
echo "🔗 Conectando ao Tailscale..."
tailscale up --authkey="$TS_AUTH_KEY" --hostname="claude-session" --accept-routes 2>/dev/null
sleep 2

# Mostra IP e máquinas disponíveis
echo ""
echo "✅ Conectado! IP desta sessão: $(tailscale ip -4 2>/dev/null || echo 'obtendo...')"
echo ""
echo "📡 Máquinas disponíveis na sua rede:"
tailscale status 2>/dev/null || echo "   (aguardando sincronização...)"
echo ""
echo "Para conectar via SSH em uma máquina:"
echo "  ssh -i .ssh/claude_key usuario@IP-DA-MAQUINA"
