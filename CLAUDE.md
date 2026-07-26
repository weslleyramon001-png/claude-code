# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Repository Overview

This repository has three distinct parts:

1. **`jarbas-backend/`** — A FastAPI Python backend for JARBAS ("Just A Rather Brilliant Autonomous System"), a personal AI assistant for Weslley Ramon built on the Anthropic API with tools, memory, voice, and browser capabilities.
2. **`jarbas-ui/`** — A standalone single-file PWA frontend for JARBAS. Self-contained `index.html` with embedded CSS/JS, connects to the backend via WebSocket for streaming responses.
3. **`plugins/`** — A collection of Claude Code plugins (custom slash commands, agents, hooks, and skills) for extending Claude Code's capabilities in any project.

The root-level files (`README.md`, `.github/`, `.devcontainer/`) are part of the upstream `anthropics/claude-code` repository that this fork is based on.

---

## JARBAS — Production Status

**JARBAS is live and deployed on Railway.**

| Item | Value |
|---|---|
| Production URL | `https://claude-code-production-62f5.up.railway.app` |
| Railway project | `lively-youthfulness` |
| Local interface | `D:\jarbas.html` (Edge on Dell) |
| Local backend (SSD) | `E:\JARBAS\app\main_local.py` (FastAPI porta 8001, Ollama llama3.2:3b) |
| Railway paid plan | ✅ Upgrade realizado (era trial até 18/07/2026) |
| Tailscale (Dell) | `100.82.120.121` |
| ACCESS_TOKEN | `EsbIv-dM0BlmannuhcGED0-zg5WVAdu8nKzdXN2rX0g` |
| N8N | `https://n8n-production-fea4.up.railway.app` |

### Active Features (as of 26/07/2026)

| Feature | Status |
|---|---|
| Chat (Claude `claude-sonnet-4-6`) | ✅ Online |
| Voice — ElevenLabs Daniel (`onwK4e9ZLuTAKqWW03F9`) | ⚠️ Chave precisa renovação (erro 401) |
| Hook Stop de voz (pt-BR-AntonioNeural) | ✅ Reativado (sessão 21/07) |
| Botão Toggle TTS (🔊/🔇) | ✅ Online (commit 670cce1) |
| Parar voz com Escape / fone Play/Pause | ✅ Online (commit 290273b) |
| JARVIS animation (4 rings + waveform) | ✅ Online |
| Persistent memory (SQLite) | ✅ Online |
| Web search (Tavily) | ✅ Online |
| Financial module (movements + balance) | ✅ Online |
| Reminders (CRUD) | ✅ Online |
| Bearer Token auth (`ACCESS_TOKEN`) | ✅ Configured on Railway |
| Push notifications | ✅ Ready |
| PWA (installable on mobile) | ✅ Ready |
| SpaceDesk (espelhamento Dell → Samsung TV) | ✅ Configurado (sessão 21/07) |

### Pending Tasks (atualizado 26/07/2026)

| Priority | Task |
|---|---|
| 🔴 URGENTE | Renovar chave ElevenLabs → `ELEVENLABS_API_KEY` no Railway (erro 401) |
| 🟡 | Corrigir MAX_TOKENS Railway (atualmente 2048 — muito curto, deve ser 4096) |
| 🟡 | Adicionar data atual no system prompt do JARBAS |
| 🟡 | Corrigir nick do JARBAS para chamar o usuário de "Major" (atualmente "chefe") |
| 🟡 | Upload ebooks Pony-Digital no Kiwify (4 PDFs em `D:\Documentos\`) |
| ⬜ | Workana: selecionar 3 habilidades principais no perfil |
| ⬜ | Workana: upload de foto de perfil (manual) |
| ⬜ | Workana: aguardar aprovação (até 15 dias) ou pagar R$59,90 p/ aprovação em 24h |
| ⬜ | N8N — DM Instagram wl.solucion: configurar webhook (App ID: 2270042597068200) |
| ⬜ | Tailscale nos outros notebooks (Samsung Lyvian etc.) |
| ⬜ | Clone voz JARVIS (Paul Bettany) no ElevenLabs |
| ⬜ | MailerLite — funil 7 emails (conteúdo já escrito) |
| ⬜ | Publicar Pack Planilhas Pony-Digital no Kiwify (produto pronto, falta upload) |

> Para renovar chave ElevenLabs: `elevenlabs.io` → avatar → Profile → API Keys → delete chave antiga → Create API Key → colar em Railway Variables → confirmar `ELEVENLABS_VOICE_ID=onwK4e9ZLuTAKqWW03F9`.

---

## JARBAS — Regra de Consulta à Documentação

**INSTRUÇÃO PERMANENTE — COMBINADO COM O MAJOR (registrado 25/07/2026)**

O JARBAS deve INTERCALAR conhecimento próprio + documentação oficial — não apenas para responder perguntas, mas principalmente para EXECUTAR.

**Regra:**
1. Se já sei de cabeça com certeza → executo direto.
2. Se tenho dúvida sobre parâmetro, configuração ou funcionalidade → consulto o link da documentação ANTES de executar.
3. Se a funcionalidade é nova (pós ago/2025) → consulto sempre.

Isso vale para: configurar MCP, criar/editar hooks, usar Agent SDK, montar workflows e sub-agentes, ajustar settings e permissões, qualquer execução técnica no Claude Code.

**Referência:** Documento com 150+ links da documentação oficial:
- ID Drive: `1QaOFEXC3PynFYqvDZGRglbKrQNhczC83ahefrr-At9M` (pasta "01 - JARBAS Produção")
- URL base: `https://code.claude.com/docs/pt/`

---

## JARBAS — Negócios de Ramon

### wl.solucion
- Site: `https://wl-solucion.vercel.app`
- Instagram: `@wl.solucion`
- Produtos no Kiwify:

| Produto | Preço | Checkout |
|---|---|---|
| Arsenal IA — 70 Prompts | R$47 | `pay.kiwify.com.br/UAUfzqU` |
| Primeiros Passos no Digital | R$27 | `pay.kiwify.com.br/SXYIuha` |
| Clube WL-Solución | R$47/mês | `pay.kiwify.com.br/p2dk5ES` |
| Mentalidade de Empreendedor | R$27 | `pay.kiwify.com.br/uFSDRrX` |
| Tráfego e Vendas Online | R$47 | `pay.kiwify.com.br/VKKt5mB` |
| Renda Passiva com Infoprodutos | R$47 | `pay.kiwify.com.br/JNTNz3n` |
| ISP Gestão Pro | R$97 | `pay.kiwify.com.br/mgBpE6H` |
| Liberdade Financeira Digital | R$97 | `pay.kiwify.com.br/TPS1eam` |

### Pony-Digital
- 13 planilhas prontas → publicar no Kiwify por R$97 (pendente)

### Servlink (ISP)
- Ramon trabalha lá como Gestor de TI e Infraestrutura (jan/2022 - atual)
- Token IXC: `57:136a4bdc0468007d8ea07389b411729b8cc6df44cefdd5c2a4ab0abedd4232d1`
- Servidor IXC: `https://ixc.servlinktelecom.com.br`

### Workana (nova frente — freelance)
- Perfil criado em 21/07/2026
- Função: Scripting & Automations
- Foco: Chatbot WhatsApp + N8N + IA (projetos R$2.500–R$7.000)
- Portfólio principal: JARBAS (FastAPI + Claude + ElevenLabs + Railway)
- Experiência Ramon: 10+ anos TI (técnico/supervisor SP + gestão ISP)
- Meta: renda extra para complementar salário atual de R$2.600/mês

---

## JARBAS — Cérebro no Google Drive

Pasta raiz: `1Vc_ORmy3FS5jh01-EVZrtTQv5Dt27w_4` ("Cérebro Lyvian-IA Claude")

| Subpasta | ID Drive |
|---|---|
| 01 - JARBAS Produção | `1C-UKbe_-C38ZmktdSgoFsy9Bqhztvk7h` |
| 02 - Credenciais e Tokens | `1Eh1vyyjfRumVd6OomVx1xnIzJyufu-W8` |
| 03 - wl.solucion | `1zuhBuTghAmHpl499aVUC2Oeu77qH9aTv` |
| 04 - Pony-Digital | `1vHs893Wig2a8KpG8Forl5fq4Qy9OkiM2` |
| 05 - Redes Sociais | `1wwox4az5zppmmA1jfKGYyxHgtrlGcIuW` |
| 06 - Infraestrutura | `1lLPKHEawbC3x72-vO8q-peYFOKDcpNHE` |
| 07 - Pendências | `1mrxPzxvLvC6Z2ictbn64-McyB3d-Gbv0` |

**Documentos-chave na pasta "01 - JARBAS Produção":**
- `1QaOFEXC3PynFYqvDZGRglbKrQNhczC83ahefrr-At9M` — 150+ links documentação Claude Code
- `1YQFcWl9k4o0G5wg9aPl-8zdEP7pD4P0XLU9GbSiE6-Q` — Regra de Consulta à Documentação (25/07/2026)
- `1A00M_PHfbfMBJ78kIgfMlkOWp9J8GESE57a9pYPSFZ0` — Sessão 19/07 (voz interrompível + toggle TTS)

**Arquivos locais importantes no Dell:**
| O que | Caminho |
|---|---|
| Backend local | `C:\jarbas\jarbas-backend\` |
| Interface web | `C:\jarbas\jarbas-backend\static\ui\index.html` |
| Extensão mic toggle | `C:\Users\WESLLEY RAMON\jarbas-ext\` |
| AHK fone YYK-520 | `C:\Users\WESLLEY RAMON\jarbas-ext\jarbas-fone.ahk` |
| Launch script | `C:\Users\WESLLEY RAMON\jarbas-ext\launch-jarbas.ps1` |
| Agente local | `C:\Users\WESLLEY RAMON\JARBAS\agente_local.py` |
| Python voz local | `C:\Users\WESLLEY RAMON\JARBAS\jarbas_voz.py` |

**REGRA PERMANENTE:** Sempre atualizar o Drive ao fim de cada sessão. É o backup center do JARBAS.

---

## JARBAS Backend

### Running Locally

```bash
cd jarbas-backend
cp .env.example .env      # Fill in at minimum ANTHROPIC_API_KEY
pip install -r requirements.txt
playwright install chromium   # Required for screenshot/browse tools
python main.py
```

Server starts at `http://localhost:8000`. Verify with:
```bash
curl http://localhost:8000/health
```

Alternative dev mode with auto-reload:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Environment Variables

| Variable | Required | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | Yes | Powers all Claude calls |
| `ELEVENLABS_API_KEY` | No | Enables `/voice` TTS endpoint |
| `ELEVENLABS_VOICE_ID` | No | Default: `onwK4e9ZLuTAKqWW03F9` (Daniel, British JARVIS-style) |
| `TAVILY_API_KEY` | No | Enables `web_search` tool (1000 free searches/month) |
| `ACCESS_TOKEN` | No | Bearer auth for all endpoints (open if unset) |
| `ALLOWED_ORIGINS` | No | Comma-separated CORS origins; default `*` |
| `DB_PATH` | No | SQLite path (default: `jarbas_memory.db`; use `/data/jarbas_memory.db` on Railway) |
| `SECRET_KEY` | No | Session secret; change in production |
| `MAX_TOKENS` | No | Default: **4096** |
| `HISTORY_LIMIT` | No | Messages kept in context; default: **30** |
| `HOST` | No | Bind host; default `0.0.0.0` |
| `PORT` | No | Bind port; default `8000` |

### Architecture

**Module breakdown:**

- `main.py` — FastAPI app, all HTTP/WebSocket endpoints, and the `run_agent()` agentic loop
- `config.py` — Single `Config` class (singleton `config`) that reads all env vars via `python-dotenv`. `CLAUDE_MODEL = "claude-sonnet-4-6"` is hardcoded here.
- `memory.py` — SQLite via raw `sqlite3`. Auto-initialises all tables on import. Manages: `messages`, `sessions`, `user_facts`, `movements` (financial), `reminders`
- `personality.py` — JARBAS system prompt and persona. `get_system_prompt(user_facts)` injects persisted user facts into the base prompt at runtime. Contains context about Ramon's businesses (Pony-Digital, Servlink).
- `tools.py` — All agent tools as async functions + `format_tools_for_claude()` (returns Claude tools schema) + `process_tool_call()` dispatcher
- `voice.py` — ElevenLabs TTS via `httpx`; returns `bytes` or `None`
- `browser.py` — Playwright headless Chromium; `take_screenshot()` returns `{"base64": str, "url": str}` or `{"error": str}`; `browse_and_read()` returns page text

**The agentic loop (`run_agent` in `main.py:110`):**

The loop runs up to 10 iterations to handle chained tool calls:
1. Save user message → extract/persist facts from it (regex-based in `memory.py`)
2. Load last N messages from SQLite as conversation history
3. Build system prompt with injected user facts
4. Call Claude (`claude-sonnet-4-6`, defined in `config.py:CLAUDE_MODEL`)
5. If `stop_reason == "tool_use"`: dispatch tools, append results as a `user` turn, repeat
6. On text response: save to DB and return

WebSocket (`/ws/{session_id}`) uses streaming mode — tokens are pushed as `{"type": "token", "content": "..."}` JSON frames; REST `/chat` uses non-streaming.

**Memory design:**
`user_facts` table stores long-term facts extracted from user messages via regex patterns (Portuguese name/location/goal/business patterns in `memory.py:_EXTRACTION_PATTERNS`). These are re-injected into the system prompt on every call. Claude can also manage memories explicitly via the `save_memory`, `list_memories`, and `delete_memory` tools.

**Financial module:**
The `movements` table tracks income/expenses. Tools `add_movement`, `list_movements`, `get_balance` expose this to Claude. REST endpoints `/finance/balance` and `/finance/movements` also expose it directly.

### Agent Tools Reference

All tools are registered in `tools.py:format_tools_for_claude()` and dispatched in `process_tool_call()`.

| Tool | Description |
|---|---|
| `get_current_datetime` | Current date/time in Brasília timezone |
| `calculate` | Safe eval of math expressions (sqrt, log, trig, etc.) |
| `web_search` | Tavily-powered web search — requires `TAVILY_API_KEY` |
| `get_weather` | Real-time weather via Open-Meteo + geocoding (no key needed) |
| `create_file_content` | Generates a formatted file block for download/copy |
| `generate_pony_digital_content` | Marketing content (hooks, captions, emails, CTAs, headlines) for Pony-Digital |
| `add_movement` | Record a financial entrada/saida |
| `list_movements` | Show financial history + balance |
| `get_balance` | Show current totals (entradas, saídas, saldo) |
| `create_reminder` | Create a new reminder |
| `list_reminders` | List pending (or all) reminders |
| `complete_reminder` | Mark a reminder as done by ID |
| `save_memory` | Explicitly save a user fact by category |
| `list_memories` | List all saved user facts with IDs |
| `delete_memory` | Delete a user fact by ID |
| `take_screenshot` | Playwright screenshot of any URL; returns vision image block to Claude |
| `browse_and_read` | Playwright text extraction from any URL |
| `system_info` | CPU/RAM/disk/uptime from `psutil` |
| `run_command` | Execute shell commands on the server (up to 30s timeout) |
| `list_files` | List directory contents |
| `read_file` | Read file contents from server |
| `write_file` | Create or overwrite a file on the server |

**Adding a new tool:** add the async function to `tools.py`, register its schema in `format_tools_for_claude()`, and add a dispatch branch in `process_tool_call()`.

**Screenshot results** flow back to Claude as vision (`image` content blocks), not plain text — the only place in the app where response content is non-text.

### Deployment (Railway)

The `Dockerfile` in `jarbas-backend/` builds a `python:3.11-slim` image with Playwright Chromium dependencies. `railway.toml` configures the Railway deployment:
- Builder: Dockerfile
- Start command: `uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}`
- Health check: `/health` (300s timeout)
- Restart policy: on_failure (max 3 retries)

Mount a volume at `/data` and set `DB_PATH=/data/jarbas_memory.db` for persistent memory across deploys.

### API Endpoints Summary

| Method | Path | Auth | Description |
|---|---|---|---|
| GET | `/health` | No | Health check + service status |
| GET | `/status` | No | Full service status dashboard (checks Anthropic, ElevenLabs, Tavily, DB) |
| POST | `/chat` | Yes | Send message, get response (REST, non-streaming) |
| GET | `/history` | Yes | Conversation history for a session |
| POST | `/clear` | Yes | Clear session history |
| POST | `/voice` | Yes | Text-to-speech (ElevenLabs) → audio/mpeg |
| GET | `/export/{session_id}` | No | Export history as JSON or TXT |
| GET | `/finance/balance` | Yes | Financial balance summary |
| GET | `/finance/movements` | Yes | Financial movement history |
| GET | `/reminders` | Yes | List reminders |
| POST | `/reminders` | Yes | Create reminder |
| PATCH | `/reminders/{id}/complete` | Yes | Mark reminder complete |
| WS | `/ws/{session_id}` | Token param | Streaming WebSocket |

WebSocket auth: pass `?token=<ACCESS_TOKEN>` as a query param (Bearer headers aren't standard for WS).

---

## JARBAS Frontend (jarbas-ui/)

A standalone single-file PWA that is the primary web interface for JARBAS.

```
jarbas-ui/
├── index.html       # 2000+ line self-contained app (CSS + JS embedded)
├── manifest.json    # PWA manifest (name, icons, theme #A855F7, pt-BR)
├── sw.js            # Service worker — network-first caching for offline fallback
└── icons/
    ├── icon-192.png
    └── icon-512.png
```

**Key characteristics:**
- Dark purple theme (`--bg: #09050F`, `--primary: #A855F7`) with JARVIS-style animated rings
- Connects to backend via WebSocket (`/ws/{session_id}`) for token streaming
- Falls back to REST `/chat` if WebSocket fails
- Sends Bearer token via `Authorization` header (REST) or `?token=` query param (WS)
- Markdown rendering for assistant responses (code blocks, bold, etc.)
- Screenshot events from the backend (`{"type": "screenshot", ...}`) are displayed inline
- PWA-installable on iOS/Android; service worker uses network-first with cache fallback

**To serve locally:** open `jarbas-ui/index.html` directly in a browser — no build step needed. Point the backend URL at `http://localhost:8000` or the Railway production URL.

**Voice flow:** the UI calls `POST /voice` with the assistant's response text, then plays the returned `audio/mpeg` via the Web Audio API.

---

## Claude Code Plugins

Located in `plugins/`, each plugin follows this structure:

```
plugin-name/
├── .claude-plugin/plugin.json   # Plugin metadata
├── commands/                    # Slash commands (*.md)
├── agents/                      # Specialized subagents (*.md)
├── skills/                      # Auto-invoked skills (SKILL.md)
├── hooks/                       # Event handlers
└── README.md
```

### Available Plugins

| Plugin | What it does |
|---|---|
| `agent-sdk-dev` | `/new-sdk-app` command + validators for Claude Agent SDK projects |
| `claude-opus-4-5-migration` | Migrates model strings and beta headers to Opus 4.5 |
| `code-review` | `/code-review` — multi-agent PR review with confidence scoring |
| `commit-commands` | `/commit`, `/commit-push-pr`, `/clean_gone` — git workflow automation |
| `explanatory-output-style` | SessionStart hook that adds educational context |
| `feature-dev` | `/feature-dev` — 7-phase guided feature development workflow |
| `frontend-design` | Auto-invoked skill for production-grade frontend design guidance |
| `hookify` | `/hookify` — creates custom hooks from conversation analysis |
| `learning-output-style` | SessionStart hook that encourages meaningful code contributions |
| `plugin-dev` | `/plugin-dev:create-plugin` — 8-phase guided plugin creation |
| `pr-review-toolkit` | `/pr-review-toolkit:review-pr` — specialized PR review agents |
| `ralph-wiggum` | `/ralph-loop` — iterative autonomous loops with stop-hook interception |
| `security-guidance` | PreToolUse hook that warns on 9 security patterns |

All plugins are registered in `.claude-plugin/marketplace.json` at the repo root.

### GitHub Actions

Multiple workflows live in `.github/workflows/`:

| Workflow | Trigger | Purpose |
|---|---|---|
| `claude.yml` | `@claude` mentions in issues/PRs | Runs Claude Code via `anthropics/claude-code-action@v1` with Workload Identity Federation (no static key) |
| `claude-issue-triage.yml` | Issue events | Auto-labels new issues |
| `claude-dedupe-issues.yml` | Issue events | Detects and flags duplicate issues |
| `auto-close-duplicates.yml` | Issue events | Closes confirmed duplicates |
| `issue-lifecycle-comment.yml` | Issue events | Posts lifecycle comments |
| `issue-opened-dispatch.yml` | Issue opened | Dispatches to downstream workflows |
| `backfill-duplicate-comments.yml` | Manual | Backfills duplicate comments |
| `lock-closed-issues.yml` | Schedule | Locks old closed issues |
| `log-issue-events.yml` | Issue events | Audit logging |
| `non-write-users-check.yml` | PR events | Validates contributor permissions |
| `remove-autoclose-label.yml` | Issue events | Removes autoclose labels on activity |
| `sweep.yml` | Schedule | Repo maintenance sweep |

The `claude.yml` action uses Workload Identity Federation — configure `ANTHROPIC_FEDERATION_RULE_ID`, `ANTHROPIC_ORGANIZATION_ID`, `ANTHROPIC_SERVICE_ACCOUNT_ID`, and `ANTHROPIC_WORKSPACE_ID` as repository variables (not secrets).

---

## Key Conventions

- **Language:** All JARBAS user-facing text is in Brazilian Portuguese. Code, comments, and docstrings in `jarbas-backend/` are also in Portuguese. Plugin code is in English.
- **Claude model:** `claude-sonnet-4-6` (hardcoded in `config.py:CLAUDE_MODEL`). To update, change it there.
- **No test suite** exists for `jarbas-backend/`. Validate manually with `curl` against the running server.
- **SQLite connections** are opened and closed per-call (not pooled). WAL mode is enabled.
- **Tool additions:** Add the async function to `tools.py`, register its schema in `format_tools_for_claude()`, and add a dispatch branch in `process_tool_call()`.
- **Screenshot results** flow back to Claude as vision (`image` content blocks), not plain text — this is the only place the response content is non-text.
- **Memory system has two layers:** automatic regex extraction from messages (`auto_extract_and_save` in `memory.py`) + explicit tool calls (`save_memory`, `list_memories`, `delete_memory`). Both write to the same `user_facts` table and are injected into every system prompt.
- The `weslley_profile.md` file in `jarbas-backend/` is context documentation for JARBAS's persona/tools but is **not loaded at runtime**; facts are stored in SQLite instead.
- **JARBAS persona** is defined in `personality.py`. It addresses the user as "Ramon" or "Major" (pending fix — currently "chefe" in code). It knows about Ramon's businesses: **wl.solucion** (produtos digitais IA/automação), **Pony-Digital** (marketing, planilhas no Kiwify), and **Servlink** (ISP — Ramon works there as IT Manager, does not own it).
- **N8N API Key** expires 08/08/2026 — renew at the Railway n8n instance.
