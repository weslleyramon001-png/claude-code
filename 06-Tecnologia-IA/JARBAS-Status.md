# JARBAS — Status do Projeto

> Última atualização: 2026-06-17 (sessão noturna — sem Weslley)
> Branch GitHub: `claude/great-ramanujan-dsjpac`

---

## O que é o JARBAS

Assistente de IA pessoal do Weslley Ramon — conectado ao Pony-Digital.
Interface holográfica roxa + backend Python com memória, voz e ferramentas de agente.

**Arquivos principais:**
- `jarbas-ui/index.html` — interface completa (PWA pronta)
- `jarbas-backend/main.py` — FastAPI + WebSocket + memória SQLite
- `jarbas-backend/tools.py` — 5 ferramentas do agente
- `jarbas-backend/voice.py` — ElevenLabs TTS async
- `jarbas-backend/weslley_profile.md` — contexto pessoal do Weslley

---

## ✅ 100% Pronto (sem precisar de keys)

- [x] Interface holográfica roxa — rings magenta/índigo/violeta/cyan
- [x] Backend FastAPI com WebSocket streaming
- [x] Sistema de memória (SQLite — mensagens + fatos + sessões)
- [x] 5 ferramentas: data/hora BR, calculadora, pesquisa web (Tavily), clima, agenda
- [x] ElevenLabs TTS async em PT-BR
- [x] Perfil completo do Weslley (`weslley_profile.md`)
- [x] Personalidade JARBAS calibrada — leal, direto, estratégico
- [x] Dockerfile + railway.toml — deploy Railway com 1 clique
- [x] `.env.example` — template com comentários
- [x] **PWA** — `manifest.json` + `sw.js` + meta tags iOS/Android
  - JARBAS pode ser instalado como app no celular
  - Funciona offline (cache de assets)
  - Ícone na tela inicial (precisa criar os PNGs: icon-192.png e icon-512.png)
- [x] **`setup.sh`** — script interativo de ativação
  - Cria o `.env` a partir do template
  - Pede as keys uma por uma
  - Instala dependências
  - Testa o servidor automaticamente

---

## ⏳ Aguardando Weslley (às 8h)

| Item | O que precisa |
|------|--------------|
| API Key Anthropic | `console.anthropic.com` → API Keys → criar + $10 crédito |
| API Key ElevenLabs | `elevenlabs.io` → Profile → API Keys (já tem conta) |
| Conta Railway | `railway.app` → Login with GitHub |
| API Key Tavily | `tavily.com` → opcional, para pesquisa web real |

---

## Passos para ativar às 8h (estimativa: 15 min)

```bash
# 1. Dentro de jarbas-backend/
bash setup.sh
# → vai pedir as keys e instalar tudo

# 2. Deploy no Railway
railway login
railway init
railway up
# → Railway gera uma URL pública (ex: jarbas-backend.up.railway.app)

# 3. Abrir jarbas-ui/index.html
# → Settings panel → colar a URL do Railway

# 4. PRONTO — testar chat, voz e memória
```

---

## PWA — Instalar no Celular

Depois de subir no Railway:
1. Abrir `index.html` no celular (servindo via Railway ou localmente)
2. Chrome/Safari → "Adicionar à tela inicial"
3. JARBAS aparece como app nativo no celular

> **Falta:** criar os ícones `jarbas-ui/icons/icon-192.png` e `icon-512.png`
> (pode usar Canva ou gerar com script Python — faremos às 8h)

---

## Próximas integrações (pós-ativação)

- [ ] Google Drive automático — JARBAS cria notas Obsidian
- [ ] Planilhas automáticas — JARBAS gera .xlsx sob demanda
- [ ] WhatsApp integration (via Evolution API ou Twilio)
- [ ] Relatório diário automático por email

---

*Tags: #JARBAS #IA #Tecnologia #Pony-Digital*
