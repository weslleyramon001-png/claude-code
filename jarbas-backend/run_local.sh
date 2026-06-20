#!/bin/bash
# JARBAS — Ativação local (sem Railway)
# Uso: bash run_local.sh

set -e

echo "╔══════════════════════════════════╗"
echo "║     JARBAS — Modo Local          ║"
echo "╚══════════════════════════════════╝"

# Verifica se .env existe
if [ ! -f .env ]; then
    echo ""
    echo "⚠️  Arquivo .env não encontrado."
    echo "   Copiando .env.example → .env ..."
    cp .env.example .env
    echo ""
    echo "👉 Abra o arquivo .env e preencha ao menos ANTHROPIC_API_KEY"
    echo "   Depois rode este script novamente."
    exit 1
fi

# Verifica se ANTHROPIC_API_KEY está configurada
source .env
if [ -z "$ANTHROPIC_API_KEY" ] || [ "$ANTHROPIC_API_KEY" = "sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" ]; then
    echo ""
    echo "❌ ANTHROPIC_API_KEY não configurada no .env"
    echo "   Obtenha em: https://console.anthropic.com/"
    exit 1
fi

# Instala dependências se necessário
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📦 Instalando dependências..."
    pip install -r requirements.txt -q
fi

echo ""
echo "✅ Configuração OK. Iniciando JARBAS..."
echo "   Backend: http://localhost:8000"
echo "   Docs:    http://localhost:8000/docs"
echo ""
echo "   Para usar a interface, abra jarbas-ui/index.html no browser."
echo "   No painel de Settings, coloque: http://localhost:8000"
echo ""
echo "   Pressione Ctrl+C para encerrar."
echo ""

python main.py
