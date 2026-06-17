#!/bin/bash
# dev-setup.sh — Prepara o ambiente de desenvolvimento completo
# Uso: bash dev-setup.sh

set -e

echo "╔══════════════════════════════════════════╗"
echo "║  Pony-Digital / Servlink — Dev Setup     ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# 1. Node.js
if ! command -v node &>/dev/null; then
  echo "📦 Instalando Node.js 22..."
  curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
  apt-get install -y nodejs
else
  echo "✅ Node.js $(node --version)"
fi

# 2. Python
if ! command -v python3 &>/dev/null; then
  echo "📦 Instalando Python 3..."
  apt-get install -y python3 python3-pip
else
  echo "✅ Python $(python3 --version)"
fi

# 3. Playwright (para Claude ver e testar apps)
echo ""
echo "🎭 Instalando Playwright MCP..."
npx @playwright/mcp@latest --version 2>/dev/null || true
npx playwright install chromium --with-deps -q
echo "✅ Playwright pronto"

# 4. Dependências do JARBAS
echo ""
echo "🤖 Instalando dependências do JARBAS..."
if [ -f "jarbas-backend/requirements.txt" ]; then
  pip install -r jarbas-backend/requirements.txt -q
  echo "✅ JARBAS backend pronto"
fi

# 5. Git config básico
echo ""
echo "⚙️  Verificando Git..."
git config --global init.defaultBranch main 2>/dev/null || true
echo "✅ Git OK"

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║  ✅ Setup completo!                      ║"
echo "║                                          ║"
echo "║  Próximo passo:                          ║"
echo "║  → bash jarbas-backend/run_local.sh      ║"
echo "╚══════════════════════════════════════════╝"

# 6. Display virtual para controle de apps
bash start-desktop.sh
