# CLAUDE.md

Este arquivo guia o JARBAS (Claude Code) ao trabalhar neste repositório.

---

# 🧠 Cérebro do JARBAS

Repositório principal: `weslleyramon001-png/claude-code`

---

## 👤 Identidade do Usuário

- **Sempre chamar de Ramon** — nunca Weslley ou outro nome
- Nome completo: Weslley Ramon Cavalcanti da Silva
- Email: weslleyramon001@gmail.com
- GitHub: weslleyramon001-png
- Estilo: comunicação direta e objetiva, gosta de aprender fazendo
- **Idioma: sempre responder em português do Brasil**

---

## 🖥️ Ambiente & Infraestrutura

| Máquina | Status | IP Tailscale | Usuário SSH |
|---|---|---|---|
| Dell (Ramon) | ✅ Tailscale OK | `100.82.120.121` | SSH pendente |
| Samsung GalaxyBook | ✅ SSH + Tailscale OK | `100.124.202.29` | `wesll` (alias `ssh samsung`) |
| Samsung Lyvian | ⬜ Setup parcial | — | `lyvia` |
| Vsap (container Claude) | ✅ Tailscale OK | `100.114.215.37` | — (reiniciar Tailscale a cada sessão) |

**Chave SSH pública (container → notebooks):**
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDARoAUlYSMUERft2wtEYGuAYk6zOh/zJncy3M9lMVW5 claude-code-samsung
```

**Reiniciar Tailscale no container:**
```bash
tailscaled --state=/tmp/tailscale-state --tun=userspace-networking &
sleep 4 && tailscale up
```

---

## 🔁 Ritual de Início de Sessão

Ao começar uma nova sessão, o JARBAS deve:

1. Reiniciar Tailscale no container (comando acima)
2. Testar conectividade: `ssh samsung` (Samsung GalaxyBook)
3. Ler memória do Drive: buscar arquivo mais recente em `99 - Sessões` do Cérebro do JARBAS
4. Retomar pelo que ficou pendente

---

## 💼 Negócios

### Pony-Digital

Marca/negócio digital de Ramon. Handle: `@w.ramon`.

| Item | Detalhe |
|---|---|
| Plataforma de vendas | Kiwify |
| Email marketing | MailerLite (funil de 7 emails — conteúdo pronto, falta configurar) |
| Instagram | `@w.ramon` |
| Vault Obsidian | Pasta "Pony Digital" no Google Drive |

**Produtos digitais prontos para vender:**

| Produto | Status |
|---|---|
| Eletrônica de Ouro | ✅ Pronto — upload pendente no Kiwify |
| Tráfego Pago para Iniciantes | ✅ Pronto |
| Instagram que Vende | ✅ Pronto |
| Finanças Pessoais do Zero | ✅ Pronto |
| Copywriting que Converte | ✅ Pronto |

### Servlink Telecom

Empresa de telecom (ISP) em Recife/PE onde Ramon trabalha.

| Item | Detalhe |
|---|---|
| Servidor IXC | `https://ixc.servlinktelecom.com.br` |
| CNPJ | `12.284.049/0001-00` |
| Instagram | `@servlinktelecom` |
| MCP integrado | ✅ IXC Servlink MCP (`server.py`) |
| Acesso Adapta ONE | Via browser (sem API direta) |

**Ferramentas MCP disponíveis no IXC:** clientes, contratos, faturas, radius/PPPoE, tickets/OS, consulta genérica

> Token de acesso IXC: salvo no Google Drive (`🔐 Chaves e Tokens - JARBAS.md`) — **nunca commitar no repositório**

---

## 🔌 Serviços e Ferramentas Conectados

| Serviço | Acesso | Status |
|---|---|---|
| Google Drive (5TB) | MCP | ✅ Conectado |
| Gmail | MCP | ✅ Conectado |
| Google Calendar | MCP | ✅ Conectado |
| Slack | MCP | ✅ Conectado |
| Canva | MCP | ✅ Conectado |
| Chrome | Extensão + MCP Playwright | ✅ Conectado |
| VS Code | Extensão Claude | ✅ Conectado |
| IXC Servlink | MCP (`server.py`) | ✅ Conectado |
| Railway | MCP (`mcp-servers/railway/server.py`) | ✅ Configurado — requer `RAILWAY_API_TOKEN` |
| MailerLite | MCP (`mcp-servers/mailerlite/server.py`) | ✅ Configurado — requer `MAILERLITE_API_KEY` |
| ElevenLabs | MCP (`mcp-servers/elevenlabs/server.py`) | ✅ Configurado — requer `ELEVENLABS_API_KEY` |
| Obsidian | MCP (`mcp-servers/obsidian/server.py`) | ⚠️ Requer plugin "Local REST API" no Dell — via Tailscale (`OBSIDIAN_HOST`, `OBSIDIAN_TOKEN`) |
| Adapta ONE | Browser (sem API) | ⬜ Acesso manual |

**Ferramentas instaladas no Dell:**

| Categoria | Ferramentas |
|---|---|
| Desenvolvimento | PowerShell 7, VS Code, Git, Node.js, Python 3.13, GitHub Desktop |
| Vídeo | DaVinci Resolve, CapCut, FFmpeg, OBS Studio, Audacity, VLC, yt-dlp |
| Armazenamento | OneDrive, Google Drive Desktop (5TB) |
| IA | Claude Code CLI, Claude Chrome, Claude VS Code, ChatGPT Desktop |

---

## 🤖 JARBAS — Sistema

**JARBAS** (Just A Rather Brilliant Autonomous System) é o assistente de IA pessoal do Ramon, construído sobre a API Anthropic com ferramentas, memória, voz e navegador.

Este repositório tem duas partes:

1. **`jarbas-backend/`** — Backend FastAPI deployado no Railway
2. **`plugins/`** — Plugins Claude Code (slash commands, agentes, hooks, skills)

### Status de Produção

**JARBAS está live no Railway.**

| Item | Valor |
|---|---|
| URL de Produção | `https://claude-code-production-62f5.up.railway.app` |
| Projeto Railway | `lively-youthfulness` |
| Interface local | `D:\jarbas.html` (Edge no Dell) |
| Trial Railway expira | **18/07/2026** — fazer upgrade antes desta data (~R$25/mês) |

**Funcionalidades ativas:**

| Funcionalidade | Status |
|---|---|
| Chat (Claude `claude-sonnet-4-6`) | ✅ Online |
| Voz — ElevenLabs Daniel (`onwK4e9ZLuTAKqWW03F9`) | ⚠️ Chave precisa renovação (erro 401) |
| Animação JARVIS (4 rings + waveform) | ✅ Online |
| Memória persistente (SQLite) | ✅ Online |
| Pesquisa web (Tavily) | ✅ Online |
| Módulo financeiro (movimentos + saldo) | ✅ Online |
| Lembretes (CRUD) | ✅ Online |
| Auth Bearer Token (`ACCESS_TOKEN`) | ✅ Configurado no Railway |
| Notificações Push | ✅ Pronto |
| PWA (instalável no celular) | ✅ Pronto |

### Pendências

| Prioridade | Tarefa |
|---|---|
| 🔴 URGENTE | Renovar chave ElevenLabs → atualizar `ELEVENLABS_API_KEY` no Railway |
| 🔴 URGENTE | Configurar SSH no Dell: instalar OpenSSH + adicionar chave pública |
| 🟡 Antes de 18/07 | Fazer upgrade do trial Railway para plano pago |
| 🟡 | Configurar Tailscale do Samsung GalaxyBook para iniciar no boot |
| ⬜ | Clonar voz JARVIS (Paul Bettany) no ElevenLabs |
| ⬜ | MailerLite — configurar funil de 7 emails (conteúdo já escrito) |
| ⬜ | Kiwify — publicar os 5 produtos digitais da Pony-Digital |
| ⬜ | Finalizar setup Samsung Lyvian (Obsidian, extensão Chrome, MCPs locais) |

> **Renovar ElevenLabs:** `elevenlabs.io` → avatar → Profile → API Keys → deletar chave antiga → Create API Key → colar em Railway Variables → confirmar `ELEVENLABS_VOICE_ID=onwK4e9ZLuTAKqWW03F9`

> **SSH no Dell** (PowerShell como Admin):
> ```powershell
> Start-Service sshd; Set-Service -Name sshd -StartupType 'Automatic'
> $key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDARoAUlYSMUERft2wtEYGuAYk6zOh/zJncy3M9lMVW5 claude-code-samsung"
> Add-Content -Path "C:\ProgramData\ssh\administrators_authorized_keys" -Value $key
> icacls "C:\ProgramData\ssh\administrators_authorized_keys" /inheritance:r /grant "Administradores:F" /grant "SYSTEM:F"
> ```

### Backend

#### Rodando Localmente

```bash
cd jarbas-backend
cp .env.example .env      # Preencher no mínimo ANTHROPIC_API_KEY
pip install -r requirements.txt
playwright install chromium
python main.py
```

Servidor em `http://localhost:8000`. Verificar:
```bash
curl http://localhost:8000/health
```

Modo dev:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### Variáveis de Ambiente

| Variável | Obrigatório | Descrição |
|---|---|---|
| `ANTHROPIC_API_KEY` | Sim | Alimenta todas as chamadas Claude |
| `ELEVENLABS_API_KEY` | Não | Habilita endpoint `/voice` TTS |
| `ELEVENLABS_VOICE_ID` | Não | Padrão: `onwK4e9ZLuTAKqWW03F9` (Daniel) |
| `TAVILY_API_KEY` | Não | Habilita ferramenta `web_search` |
| `ACCESS_TOKEN` | Não | Auth Bearer (aberto se não definido) |
| `DB_PATH` | Não | Caminho SQLite (usar `/data/jarbas_memory.db` no Railway) |
| `MAX_TOKENS` | Não | Padrão: 2048 |
| `HISTORY_LIMIT` | Não | Mensagens no contexto; padrão: 20 |

#### Arquitetura

**Módulos:**

- `main.py` — App FastAPI, endpoints HTTP/WebSocket e loop agêntico `run_agent()`
- `config.py` — Classe `Config` singleton, lê env vars via `python-dotenv`
- `memory.py` — SQLite puro. Gerencia: mensagens, sessões, user_facts, movements, reminders
- `personality.py` — System prompt do JARBAS. `get_system_prompt(user_facts)` injeta fatos persistidos
- `tools.py` — Ferramentas do agente + `format_tools_for_claude()` + dispatcher `process_tool_call()`
- `voice.py` — ElevenLabs TTS via `httpx`
- `browser.py` — Playwright Chromium headless; screenshot e leitura de páginas

**Loop agêntico (`run_agent` em `main.py:110`):** roda até 10 iterações para tool calls encadeadas.

**Design de memória:** tabela `user_facts` com fatos extraídos via regex, re-injetados no system prompt a cada chamada.

**Módulo financeiro:** tabela `movements`, ferramentas `add_movement`, `list_movements`, `get_balance`, endpoints REST `/finance/balance` e `/finance/movements`.

#### Deploy (Railway)

`Dockerfile` em `jarbas-backend/` constrói imagem `python:3.11-slim` com Playwright Chromium. Montar volume em `/data` e definir `DB_PATH=/data/jarbas_memory.db` para memória persistente.

#### Endpoints da API

| Método | Caminho | Descrição |
|---|---|---|
| GET | `/health` | Health check (sem auth) |
| GET | `/status` | Dashboard de status |
| POST | `/chat` | Enviar mensagem (REST, não-streaming) |
| GET | `/history` | Histórico de conversa |
| POST | `/clear` | Limpar histórico de sessão |
| POST | `/voice` | Text-to-speech (ElevenLabs) |
| GET | `/export/{session_id}` | Exportar histórico como JSON ou TXT |
| GET | `/finance/balance` | Saldo financeiro |
| GET | `/finance/movements` | Histórico de movimentos |
| GET | `/reminders` | Listar lembretes |
| POST | `/reminders` | Criar lembrete |
| PATCH | `/reminders/{id}/complete` | Marcar lembrete como concluído |
| WS | `/ws/{session_id}` | WebSocket streaming |

---

## 🧩 Claude Code Plugins

Localizados em `plugins/`. Estrutura padrão:

```
plugin-name/
├── .claude-plugin/plugin.json
├── commands/
├── agents/
├── skills/
├── hooks/
└── README.md
```

**Plugins disponíveis:**

| Plugin | O que faz |
|---|---|
| `agent-sdk-dev` | Comando `/new-sdk-app` + validadores para projetos Claude Agent SDK |
| `claude-opus-4-5-migration` | Migra strings de modelo e beta headers para Opus 4.5 |
| `code-review` | `/code-review` — revisão de PR multi-agente com pontuação de confiança |
| `commit-commands` | `/commit`, `/commit-push-pr`, `/clean_gone` — automação de workflow git |
| `explanatory-output-style` | Hook SessionStart que adiciona contexto educacional |
| `feature-dev` | `/feature-dev` — workflow guiado de feature em 7 fases |
| `frontend-design` | Skill auto-invocada para orientação de design frontend |
| `hookify` | `/hookify` — cria hooks customizados a partir da conversa |
| `learning-output-style` | Hook SessionStart que incentiva contribuições significativas |
| `plugin-dev` | `/plugin-dev:create-plugin` — criação guiada de plugin em 8 fases |
| `pr-review-toolkit` | `/pr-review-toolkit:review-pr` — agentes de revisão de PR |
| `ralph-wiggum` | `/ralph-loop` — loops autônomos com interceptação de stop-hook |
| `security-guidance` | Hook PreToolUse que avisa sobre 9 padrões de segurança |

**GitHub Actions:** `.github/workflows/claude.yml` responde a menções `@claude` em issues/PRs via `anthropics/claude-code-action@v1`.

---

## 📐 Convenções do Projeto

- **Idioma:** Todo texto do JARBAS ao usuário em português do Brasil. Código/comentários em `jarbas-backend/` em português. Plugins em inglês.
- **Modelo Claude:** `claude-sonnet-4-6` (definido em `config.py:CLAUDE_MODEL`).
- **Sem testes automatizados** no `jarbas-backend/`. Validar com `curl`.
- **Conexões SQLite** abertas e fechadas por chamada. Modo WAL habilitado.
- **Adição de ferramentas:** função async em `tools.py` → schema em `format_tools_for_claude()` → branch em `process_tool_call()`.
- **Screenshots** retornam ao Claude como blocos de conteúdo `image`, não texto.
- O arquivo `weslley_profile.md` em `jarbas-backend/` é documentação de contexto — não carregado em runtime.
