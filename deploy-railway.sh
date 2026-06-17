#!/bin/bash
# deploy-railway.sh — Deploy automático do JARBAS no Railway
# Uso: RAILWAY_TOKEN="xxx" ANTHROPIC_KEY="sk-ant-xxx" ELEVENLABS_KEY="xxx" bash deploy-railway.sh

set -e

echo "╔══════════════════════════════════════════╗"
echo "║       JARBAS → Railway Deploy            ║"
echo "╚══════════════════════════════════════════╝"

# Verifica variáveis obrigatórias
if [ -z "$RAILWAY_TOKEN" ] || [ -z "$ANTHROPIC_KEY" ]; then
    echo "❌ Variáveis necessárias:"
    echo "   RAILWAY_TOKEN — token do Railway (railway.app → Account Settings → Tokens)"
    echo "   ANTHROPIC_KEY — sk-ant-api03-xxxxx"
    echo "   ELEVENLABS_KEY — (opcional, para voz)"
    echo ""
    echo "Uso: RAILWAY_TOKEN='xxx' ANTHROPIC_KEY='yyy' bash deploy-railway.sh"
    exit 1
fi

# Autenticar no Railway
echo "🔗 Autenticando no Railway..."
export RAILWAY_TOKEN="$RAILWAY_TOKEN"

# Entrar na pasta do backend
cd jarbas-backend

# Criar projeto se não existir
echo "🚀 Iniciando deploy..."
railway up --detach

echo ""
echo "⏳ Aguardando deploy (pode levar 2-3 minutos)..."
sleep 30

# Pegar URL do projeto
RAILWAY_URL=$(railway domain 2>/dev/null || echo "")

if [ -n "$RAILWAY_URL" ]; then
    echo ""
    echo "✅ JARBAS no ar!"
    echo "   URL: https://$RAILWAY_URL"
    echo ""
    echo "Próximo passo: abra jarbas-ui/index.html"
    echo "Settings → Backend URL → cole: wss://$RAILWAY_URL/ws/default"
else
    echo "✅ Deploy enviado! Verifique em: railway.app/dashboard"
fi

cd ..
