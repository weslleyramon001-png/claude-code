# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Repository Overview

This repository has two distinct parts:

1. **`jarbas-backend/`** — A FastAPI Python backend for JARBAS ("Just A Rather Brilliant Autonomous System"), a personal AI assistant for Weslley Ramon built on the Anthropic API with tools, memory, voice, and browser capabilities.
2. **`plugins/`** — A collection of Claude Code plugins (custom slash commands, agents, hooks, and skills) for extending Claude Code's capabilities in any project.

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

### Active Features (as of 22/06/2026)

| Feature | Status |
|---|---|
| Chat (Claude `claude-sonnet-4-6`) | ✅ Online |
| Voice — ElevenLabs Daniel (`onwK4e9ZLuTAKqWW03F9`) | ✅ Key renewed 26/06/2026 |
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
| 🟡 Before 18/07 | Upgrade Railway trial to paid plan |
| ⬜ | Dell G7 — finish remaining apps (DaVinci, Chrome extensions) |
| ⬜ | Dell G7 — add `MAILERLITE_API_KEY` env var (after MailerLite onboarding) |
| ⬜ | Tailscale on Samsung Lyvian |
| ⬜ | Clone JARVIS voice (Paul Bettany) on ElevenLabs |
| ⬜ | MailerLite — set up 7-email funnel (content already written) |
| ⬜ | Kiwify — publish spreadsheet pack (product ready, just needs upload) |

> To renew ElevenLabs key: `elevenlabs.io` → avatar → Profile → API Keys → delete old key → Create API Key → paste in Railway Variables → confirm `ELEVENLABS_VOICE_ID=onwK4e9ZLuTAKqWW03F9`.

---

## Machines & Infrastructure

### Machine Inventory

| Machine | Model | IP Tailscale | Status | User |
|---|---|---|---|---|
| Dell G7 | i7 \| 8GB RAM \| GTX 1050 Ti 4GB \| Win 11 | `100.82.120.121` | ✅ Core setup done (26/06/2026) | weslley ramon |
| Vsap (W-RAMON) | i7-10870H \| 32GB RAM \| NVMe 1TB \| Win 11 Pro | work network | ✅ Fully configured | wesll |
| Samsung GalaxyBook | Galaxy Book 2 360 | `100.124.202.29` | ✅ SSH + Tailscale OK | wesll |
| Samsung Lyvian | Galaxy Book 3 360 | — | ⬜ Pending setup | lyvia |
| Vsap container | Claude Code remote | `100.114.215.37` | ✅ Active (restart Tailscale each session) | — |

### Vsap (W-RAMON) — Reference Environment (fully configured 03/06/2026)

| Tool | Version |
|---|---|
| Node.js / npm | 24.16.0 / 11.13.0 |
| pnpm | 11.5.1 |
| Git | 2.54.0 |
| VS Code | 1.121.0 |
| Python | 3.13.13 |
| PowerShell | 7.6.2 |
| Vercel CLI | 54.7.1 |
| DaVinci Resolve | 21 |
| Obsidian | 1.12.7 |
| VLC | 3.0.23 |
| Chrome MCP | ✅ working |
| Extensão Claude in Chrome | ⬜ confirm |

### Dell G7 — Setup Checklist (execute in order)

**Dell is the home machine / local AI workstation** — GTX 1050 Ti 4GB for ComfyUI / Stable Diffusion.

#### 1. SSH ✅ DONE (26/06/2026)
- OpenSSH Server installed and set to auto-start
- Windows Firewall rule created for port 22
- Container public key authorized in `C:\ProgramData\ssh\administrators_authorized_keys`
- SSH user: `weslley ramon` (note the space — use quotes)
- From container: `ssh -o ProxyCommand="tailscale --socket=/tmp/tailscale.sock nc %h %p" "weslley ramon@100.82.120.121"`

#### 2. GPU & AI Core
- [x] NVIDIA App already installed (detected via winget)
- [ ] ComfyUI at `D:\ComfyUI`

#### 3. Development Tools ✅ ALL DONE (26/06/2026)
- [x] Node.js v24.18.0 + npm 11.16.0
- [x] pnpm (installed via `npm i -g pnpm`)
- [x] Git 2.54.0
- [x] VS Code
- [x] Python 3.13.14
- [x] Vercel CLI (installed via `npm i -g vercel`)
- [ ] Windows Terminal — install from Microsoft Store
- [ ] PowerShell 7 — `winget install Microsoft.PowerShell`

#### 4. Apps
- [ ] DaVinci Resolve 21 — manual download: `blackmagicdesign.com/products/davinciresolve`
- [x] Obsidian — installed
- [ ] VLC — `winget install VideoLAN.VLC`
- [ ] Chrome MCP extension — install from Chrome Web Store
- [ ] Extensão Claude in Chrome — install from Chrome Web Store

#### 5. Obsidian — Local REST API Plugin ✅ DONE (26/06/2026)
- Plugin installed and enabled
- Token saved as `OBSIDIAN_TOKEN` machine env var
- `OBSIDIAN_HOST=http://localhost:27123` set

#### 6. Environment Variables — Status
| Variable | Status |
|---|---|
| `RAILWAY_API_TOKEN` | ✅ Set (`d914290f-fd5e-46d0-9baf-9bfacc75c10d`) |
| `ELEVENLABS_API_KEY` | ✅ Set (renewed 26/06/2026) |
| `OBSIDIAN_HOST` | ✅ Set (`http://localhost:27123`) |
| `OBSIDIAN_TOKEN` | ✅ Set |
| `MAILERLITE_API_KEY` | ⬜ Pending — get from MailerLite → Integrations → API after onboarding |

To add MailerLite key when ready (PowerShell as Admin):
```powershell
[System.Environment]::SetEnvironmentVariable("MAILERLITE_API_KEY", "SEU_TOKEN", "Machine")
```
Or via remote SSH from container:
```bash
ssh -o ProxyCommand="tailscale --socket=/tmp/tailscale.sock nc %h %p" "weslley ramon@100.82.120.121" "powershell -Command \"[System.Environment]::SetEnvironmentVariable('MAILERLITE_API_KEY', 'KEY_AQUI', 'Machine')\""
```

#### 7. Future / Optional
- [ ] Upgrade hardware — 32GB RAM + 1TB NVMe
- [ ] Thunderbolt — verify if Dell G7 supports eGPU
- [ ] MCP Kiwify — create webhook receiver in JARBAS backend (no public API)
- [ ] MCP Instagram — Meta for Developers app + Graph API + `mcp-servers/instagram/server.py`

### Samsung GalaxyBook — Pending
- [ ] Configure Tailscale to auto-start on boot:
```bash
sudo systemctl enable tailscaled
sudo systemctl start tailscaled
```

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
| `ELEVENLABS_VOICE_ID` | No | Default: `onwK4e9ZLuTAKqWW03F9` (Daniel) |
| `TAVILY_API_KEY` | No | Enables `web_search` tool |
| `ACCESS_TOKEN` | No | Bearer auth for all endpoints (open if unset) |
| `DB_PATH` | No | SQLite path (default: `jarbas_memory.db`; use `/data/jarbas_memory.db` on Railway) |
| `MAX_TOKENS` | No | Default: 2048 |
| `HISTORY_LIMIT` | No | Messages kept in context; default: 20 |

### Architecture

**Module breakdown:**

- `main.py` — FastAPI app, all HTTP/WebSocket endpoints, and the `run_agent()` agentic loop
- `config.py` — Single `Config` class (singleton `config`) that reads all env vars via `python-dotenv`
- `memory.py` — SQLite via raw `sqlite3`. Auto-initialises all tables on import. Manages: messages, sessions, user_facts, movements (financial), reminders
- `personality.py` — JARBAS system prompt and persona. `get_system_prompt(user_facts)` injects persisted user facts into the base prompt at runtime
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
`user_facts` table stores long-term facts extracted from user messages via regex patterns (Portuguese name/location/goal/business patterns). These are re-injected into the system prompt on every call, giving JARBAS persistent memory across sessions without RAG.

**Financial module:**  
The `movements` table tracks income/expenses. Tools `add_movement`, `list_movements`, `get_balance` expose this to Claude. REST endpoints `/finance/balance` and `/finance/movements` also expose it directly.

### Deployment (Railway)

The `Dockerfile` in `jarbas-backend/` builds a `python:3.11-slim` image with Playwright Chromium dependencies. `railway.toml` configures the Railway deployment. Mount a volume at `/data` and set `DB_PATH=/data/jarbas_memory.db` for persistent memory.

### API Endpoints Summary

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Health check (no auth) |
| GET | `/status` | Full service status dashboard (no auth) |
| POST | `/chat` | Send message, get response (REST, non-streaming) |
| GET | `/history` | Conversation history for a session |
| POST | `/clear` | Clear session history |
| POST | `/voice` | Text-to-speech (ElevenLabs) |
| GET | `/export/{session_id}` | Export history as JSON or TXT |
| GET | `/finance/balance` | Financial balance summary |
| GET | `/finance/movements` | Financial movement history |
| GET | `/reminders` | List reminders |
| POST | `/reminders` | Create reminder |
| PATCH | `/reminders/{id}/complete` | Mark reminder complete |
| WS | `/ws/{session_id}` | Streaming WebSocket |

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

### GitHub Actions

`.github/workflows/claude.yml` — Responds to `@claude` mentions in issues/PRs using `anthropics/claude-code-action@v1` with Workload Identity Federation (no static API key stored).

---

## Key Conventions

- **Language:** All JARBAS user-facing text is in Brazilian Portuguese. Code, comments, and docstrings in `jarbas-backend/` are also in Portuguese. Plugin code is in English.
- **Claude model:** `claude-sonnet-4-6` (set in `config.py`). When updating, change `CLAUDE_MODEL` there.
- **No test suite** exists for `jarbas-backend/`. Validate manually with `curl` against the running server.
- **SQLite connections** are opened and closed per-call (not pooled). WAL mode is enabled.
- **Tool additions:** Add the async function to `tools.py`, register its schema in `format_tools_for_claude()`, and add a dispatch branch in `process_tool_call()`.
- **Screenshot results** flow back to Claude as vision (`image` content blocks), not plain text — this is the only place the response content is non-text.
- The `weslley_profile.md` file in `jarbas-backend/` is context documentation for JARBAS's persona/tools but is not loaded at runtime; facts are stored in SQLite instead.
