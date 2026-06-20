#!/usr/bin/env bash
# JARBAS — Script de ativação rápida
# Uso: bash setup.sh

set -e

GREEN='\033[0;32m'
PURPLE='\033[0;35m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${PURPLE}"
echo "  ╔══════════════════════════════════════╗"
echo "  ║  JARBAS — Setup de Ativação          ║"
echo "  ║  Just A Rather Brilliant Auto System ║"
echo "  ╚══════════════════════════════════════╝"
echo -e "${NC}"

# ── Verificar se .env existe ───────────────────────────────────────────────
if [ ! -f ".env" ]; then
  echo -e "${YELLOW}[1/4] Criando .env a partir do template...${NC}"
  cp .env.example .env
  echo -e "${GREEN}    .env criado.${NC}"
else
  echo -e "${GREEN}[1/4] .env já existe. Pulando criação.${NC}"
fi

# ── Coletar as keys ────────────────────────────────────────────────────────
echo ""
echo -e "${YELLOW}[2/4] Configurar chaves de API${NC}"
echo "    (pressione Enter para manter o valor atual)"
echo ""

# Anthropic
current=$(grep "ANTHROPIC_API_KEY" .env | cut -d= -f2)
echo -n "    Anthropic API Key [${current:0:20}...]: "
read -r input
if [ -n "$input" ]; then
  sed -i "s|ANTHROPIC_API_KEY=.*|ANTHROPIC_API_KEY=$input|" .env
  echo -e "${GREEN}    Anthropic key salva.${NC}"
fi

# ElevenLabs
current=$(grep "ELEVENLABS_API_KEY" .env | cut -d= -f2)
echo -n "    ElevenLabs API Key [${current:0:20}...]: "
read -r input
if [ -n "$input" ]; then
  sed -i "s|ELEVENLABS_API_KEY=.*|ELEVENLABS_API_KEY=$input|" .env
  echo -e "${GREEN}    ElevenLabs key salva.${NC}"
fi

# Tavily (opcional)
current=$(grep "TAVILY_API_KEY" .env | cut -d= -f2)
echo -n "    Tavily API Key (opcional, Enter para pular) [${current:0:15}...]: "
read -r input
if [ -n "$input" ]; then
  sed -i "s|TAVILY_API_KEY=.*|TAVILY_API_KEY=$input|" .env
  echo -e "${GREEN}    Tavily key salva.${NC}"
fi

# ── Instalar dependências ──────────────────────────────────────────────────
echo ""
echo -e "${YELLOW}[3/4] Instalando dependências Python...${NC}"
pip install -r requirements.txt --quiet
echo -e "${GREEN}    Dependências instaladas.${NC}"

# ── Testar o servidor ──────────────────────────────────────────────────────
echo ""
echo -e "${YELLOW}[4/4] Testando servidor...${NC}"
echo -e "    Iniciando JARBAS em background por 3 segundos..."

uvicorn main:app --host 0.0.0.0 --port 8000 &
SERVER_PID=$!
sleep 3

if curl -s http://localhost:8000/health > /dev/null 2>&1; then
  echo -e "${GREEN}    Servidor OK — JARBAS está online!${NC}"
  HEALTH=$(curl -s http://localhost:8000/health)
  echo "    $HEALTH"
else
  echo -e "${YELLOW}    Servidor ainda iniciando (normal na primeira vez).${NC}"
fi

kill $SERVER_PID 2>/dev/null || true

echo ""
echo -e "${PURPLE}══════════════════════════════════════════${NC}"
echo -e "${GREEN}  JARBAS configurado! Para rodar:${NC}"
echo ""
echo "  LOCAL:     uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
echo "  RAILWAY:   railway up"
echo ""
echo -e "${PURPLE}══════════════════════════════════════════${NC}"
echo ""
