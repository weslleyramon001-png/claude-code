# JARBAS — Status do Projeto

**Branch GitHub:** `claude/great-ramanujan-dsjpac`
**Arquivos:** `jarbas-ui/index.html` + `jarbas-backend/`

## O que está 100% pronto
- [x] Interface holográfica roxa — rings magenta/índigo/violeta/cyan
- [x] Backend Python (FastAPI) — chat, WebSocket streaming, memória, voz
- [x] Sistema de memória longo prazo (SQLite)
- [x] Ferramentas: data/hora BR, calculadora, pesquisa web, clima
- [x] ElevenLabs TTS async em PT-BR
- [x] Perfil completo de Weslley (`weslley_profile.md`)
- [x] Personalidade calibrada — leal, direto, estratégico
- [x] Dockerfile + railway.toml — deploy com um clique
- [x] .env.example com todas as variáveis documentadas

## Status das Keys (17/06/2026 → sessão atual)
- [x] API Key Anthropic — CONFIGURADA (US$ 5 de crédito)
- [ ] API Key ElevenLabs — pendente (conta existe, precisa da key)
- [ ] Deploy Railway — pendente

## Como ativar localmente
```bash
cd jarbas-backend
cp .env.example .env
# preenche as keys no .env
bash run_local.sh
```

## Como fazer deploy no Railway
```bash
railway login
railway init
railway up
```
Depois cola a URL gerada no Settings do jarbas-ui/index.html
