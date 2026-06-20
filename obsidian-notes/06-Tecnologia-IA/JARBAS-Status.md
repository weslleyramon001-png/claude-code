# JARBAS — Status do Projeto

> Última atualização: 2026-06-17
> Tags: #jarbas #ia #backend #python #railway

---

## O que é o JARBAS

**Just A Rather Brilliant Autonomous System** — assistente de IA pessoal do Weslley Ramon.

Inspirado no JARVIS do Homem de Ferro. Interface holográfica roxa/violeta/magenta. Backend Python com memória persistente, voz e ferramentas integradas.

**Criação:** Weslley Ramon + Claude (parceria — Weslley é o criador, Claude é a implementação)

---

## Arquitetura

```
jarbas-ui/
  index.html        → Interface holográfica roxa (PWA)
  manifest.json     → Instalar como app no celular
  sw.js             → Service Worker (funciona offline)

jarbas-backend/
  main.py           → FastAPI — endpoints + WebSocket streaming
  memory.py         → SQLite — memória de curto e longo prazo
  personality.py    → Personalidade JARBAS calibrada para Weslley
  tools.py          → 5 ferramentas: data/hora, calculadora, web, clima, arquivo
  voice.py          → ElevenLabs TTS em PT-BR
  config.py         → Variáveis de ambiente
  weslley_profile.md → Perfil completo de Weslley
  Dockerfile        → Container pronto
  railway.toml      → Deploy Railway com 1 clique
  setup.sh          → Script interativo de ativação
  .env.example      → Template de chaves
  SETUP.md          → Guia completo passo a passo
```

---

## Endpoints da API

| Método | Endpoint | Função |
|--------|----------|--------|
| GET | `/health` | Status do sistema |
| POST | `/chat` | Enviar mensagem |
| WS | `/ws/{session_id}` | Chat em tempo real (streaming) |
| GET | `/history/{session_id}` | Histórico da sessão |
| POST | `/clear/{session_id}` | Limpar histórico |
| POST | `/fact` | Salvar fato na memória longa |
| POST | `/voice` | Gerar áudio (ElevenLabs) |

---

## Ferramentas do Agente

1. **`get_current_datetime`** — data/hora atual em PT-BR (fuso Brasília)
2. **`calculate`** — calculadora matemática segura (sem eval direto)
3. **`web_search`** — pesquisa web via Tavily API (opcional)
4. **`get_weather`** — clima atual (placeholder — activar com API)
5. **`create_file_content`** — gerar conteúdo estruturado (planilhas, posts, etc.)

---

## Memória Persistente (SQLite)

3 tabelas:
- **`messages`** — histórico de conversas por sessão
- **`user_facts`** — fatos de longo prazo (extraídos automaticamente das conversas)
- **`sessions`** — metadata das sessões

Auto-extração: JARBAS detecta informações importantes na conversa e salva automaticamente como fatos.

---

## Interface (PWA)

- Tema holográfico roxa/violeta/magenta
- 4 rings orbitais animados: magenta, índigo, violeta, cyan
- Core pulsante "J" com gradiente
- Chat com streaming (typewriter effect)
- Playback de voz
- Configurações: URL do backend, session ID, toggle de voz
- **PWA** — pode ser instalado como app no celular (Android + iOS)

---

## O que falta (precisa das keys do Weslley)

- [ ] `ANTHROPIC_API_KEY` → console.anthropic.com → API Keys
- [ ] `ELEVENLABS_API_KEY` → elevenlabs.io → Profile → API Keys
- [ ] Conta no Railway → railway.app → Login with GitHub
- [ ] (Opcional) `TAVILY_API_KEY` → tavily.com → pesquisa web

---

## Como Ativar (sequência 08h)

```bash
# 1. Entrar na pasta do backend
cd jarbas-backend

# 2. Rodar o setup interativo (pede as keys e testa)
bash setup.sh

# 3. Deploy no Railway
railway login
railway init
railway up

# 4. Copiar a URL pública do Railway
# 5. Abrir jarbas-ui/index.html → Settings → colar URL
```

---

## Custo estimado mensal

| Serviço | Plano | Custo |
|---------|-------|-------|
| Anthropic API | Pay-per-use | ~$10-20/mês |
| ElevenLabs | Free (10k chars) ou Starter ($5) | $0-5/mês |
| Railway | Hobby ($5 crédito grátis) | $0-5/mês |
| Tavily | Free (1000 req/mês) | $0 |
| **Total** | | **~$10-25/mês** |

---

## Links

- **GitHub:** `weslleyramon001-png/claude-code` branch `claude/great-ramanujan-dsjpac`
- **SETUP.md:** instruções completas dentro de `jarbas-backend/SETUP.md`
