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
| Railway trial expires | **18/07/2026** — upgrade to paid (~R$25/mês) before this date |
| Tailscale (Dell) | `100.82.120.121` |

### Active Features (as of 26/06/2026)

| Feature | Status |
|---|---|
| Chat (Claude `claude-sonnet-4-6`) | ✅ Online |
| Voice — ElevenLabs Daniel (`onwK4e9ZLuTAKqWW03F9`) | ⚠️ Key needs renewal (401 error) |
| JARVIS animation (4 rings + waveform) | ✅ Online |
| Persistent memory (SQLite) | ✅ Online |
| Web search (Tavily) | ✅ Online |
| Financial module (movements + balance) | ✅ Online |
| Reminders (CRUD) | ✅ Online |
| Bearer Token auth (`ACCESS_TOKEN`) | ✅ Configured on Railway |
| Push notifications | ✅ Ready |
| PWA (installable on mobile) | ✅ Ready |

### Pending Tasks

| Priority | Task |
|---|---|
| 🔴 URGENT | Renew ElevenLabs API key → update `ELEVENLABS_API_KEY` on Railway |
| 🟡 Before 18/07 | Upgrade Railway trial to paid plan |
| ⬜ | Tailscale on other notebooks (Samsung Lyvian etc.) |
| ⬜ | Clone JARVIS voice (Paul Bettany) on ElevenLabs |
| ⬜ | MailerLite — set up 7-email funnel (content already written) |
| ⬜ | Kiwify — publish spreadsheet pack (product ready, just needs upload) |

> To renew ElevenLabs key: `elevenlabs.io` → avatar → Profile → API Keys → delete old key → Create API Key → paste in Railway Variables → confirm `ELEVENLABS_VOICE_ID=onwK4e9ZLuTAKqWW03F9`.

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
- **JARBAS persona** is defined in `personality.py`. It addresses the user as "Ramon" or "chefe". It knows about Ramon's businesses: **Pony-Digital** (digital products, Instagram marketing, spreadsheet packs on Kiwify/Hotmart) and **Servlink** (internet service provider).
