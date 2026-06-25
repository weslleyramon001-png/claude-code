# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Identidade do Usuário

- **Sempre chamar de Ramon** — nunca Weslley ou outro nome
- Nome completo: Weslley Ramon Cavalcanti da Silva
- Email: weslleyramon001@gmail.com
- GitHub: weslleyramon001-png
- Estilo: comunicação direta e objetiva, gosta de aprender fazendo
- **Idioma: sempre responder em português do Brasil**

---

## Estado do Ambiente (25/06/2026)

| Máquina | Status | IP Tailscale | Usuário SSH |
|---|---|---|---|
| Dell (Ramon) | ✅ Tailscale OK | `100.82.120.121` | SSH pendente |
| Samsung GalaxyBook | ✅ SSH + Tailscale OK | `100.124.202.29` | `wesll` (alias `ssh samsung`) |
| Samsung Lyvian | ⬜ Setup parcial | — | `lyvia` |
| Vsap (container Claude) | ✅ Tailscale OK | `100.114.215.37` | — (reiniciar Tailscale a cada sessão; SSH servidor não aplicável) |

**Chave SSH pública (container → notebooks):**
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDARoAUlYSMUERft2wtEYGuAYk6zOh/zJncy3M9lMVW5 claude-code-samsung
```

**Para reiniciar Tailscale no container:**
```bash
tailscaled --state=/tmp/tailscale-state --tun=userspace-networking &
sleep 4 && tailscale up
```

---

## Ritual de Início de Sessão

Ao começar uma nova sessão, o JARBAS deve:

1. Reiniciar Tailscale no container (comando acima)
2. Testar conectividade: `ssh samsung` (Samsung GalaxyBook)
3. Ler memória do Drive: buscar "JARBAS - Memória de Sessão" mais recente
4. Retomar pelo que ficou pendente

---

## Cérebro do JARBAS

Repositório principal: `weslleyramon001-png/claude-code`

Este repositório tem duas partes:

1. **`jarbas-backend/`** — Backend FastAPI do JARBAS (Just A Rather Brilliant Autonomous System), assistente de IA pessoal do Ramon, construído sobre a API Anthropic com ferramentas, memória, voz e navegador.
2. **`plugins/`** — Coleção de plugins Claude Code (slash commands, agentes, hooks e skills) para estender as capacidades do Claude Code em qualquer projeto.

Os arquivos raiz (`README.md`, `.github/`, `.devcontainer/`) fazem parte do upstream `anthropics/claude-code` do qual este fork é derivado.

---

### Contexto de Negócios

#### Pony-Digital

Marca/negócio digital de Ramon. Handle: `@w.ramon`.

| Item | Detalhe |
|---|---|
| Plataforma de vendas | Kiwify |
| Email marketing | MailerLite (funil de 7 emails — conteúdo pronto, falta configurar) |
| Instagram | `@w.ramon` |
| Vault Obsidian | Pasta "Pony Digital" no Google Drive |

**Produtos digitais criados (prontos para vender):**

| Produto | Status |
|---|---|
| Eletrônica de Ouro | ✅ Pronto — upload pendente no Kiwify |
| Tráfego Pago para Iniciantes | ✅ Pronto |
| Instagram que Vende | ✅ Pronto |
| Finanças Pessoais do Zero | ✅ Pronto |
| Copywriting que Converte | ✅ Pronto |

#### Servlink Telecom

Empresa de telecom (ISP) em Recife/PE onde Ramon trabalha.

| Item | Detalhe |
|---|---|
| Servidor IXC | `https://ixc.servlinktelecom.com.br` |
| CNPJ | `12.284.049/0001-00` |
| Instagram | `@servlinktelecom` |
| MCP integrado | ✅ IXC Servlink MCP (`server.py`) |
| Acesso Adapta ONE | Via browser (sem API direta) |

**Ferramentas MCP disponíveis no IXC:**
clientes, contratos, faturas, radius/PPPoE, tickets/OS, consulta genérica

> Token de acesso IXC: salvo no Google Drive (não commitar no repositório)

---

### Serviços e Ferramentas Conectados

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
| Adapta ONE | Browser (sem API) | ⬜ Acesso manual |

**Ferramentas instaladas no PC (Dell):**

| Categoria | Ferramentas |
|---|---|
| Desenvolvimento | PowerShell 7, VS Code, Git, Node.js, Python 3.13, GitHub Desktop |
| Vídeo | DaVinci Resolve, CapCut, FFmpeg, OBS Studio, Audacity, VLC, yt-dlp |
| Armazenamento | OneDrive, Google Drive Desktop (5TB) |
| IA | Claude Code CLI, Claude Chrome, Claude VS Code, ChatGPT Desktop |

---

### JARBAS — Status de Produção

**JARBAS está live e deployado no Railway.**

| Item | Valor |
|---|---|
| URL de Produção | `https://claude-code-production-62f5.up.railway.app` |
| Projeto Railway | `lively-youthfulness` |
| Interface local | `D:\jarbas.html` (Edge no Dell) |
| Trial Railway expira | **18/07/2026** — fazer upgrade para pago (~R$25/mês) antes desta data |
| Tailscale (Dell) | `100.82.120.121` |

#### Funcionalidades Ativas (22/06/2026)

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

#### Pendências

| Prioridade | Tarefa |
|---|---|
| 🔴 URGENTE | Renovar chave ElevenLabs → atualizar `ELEVENLABS_API_KEY` no Railway |
| 🔴 URGENTE | Configurar SSH no Dell: instalar OpenSSH, adicionar chave pública em `C:\ProgramData\ssh\administrators_authorized_keys` |
| 🟡 Antes de 18/07 | Fazer upgrade do trial Railway para plano pago |
| 🟡 | Configurar Tailscale do Samsung para iniciar automaticamente no boot |
| ⬜ | Clonar voz JARVIS (Paul Bettany) no ElevenLabs |
| ⬜ | MailerLite — configurar funil de 7 emails (conteúdo já escrito) |
| ⬜ | Kiwify — publicar os 5 produtos digitais da Pony-Digital |
| ⬜ | Finalizar setup Samsung Lyvian (Obsidian, extensão Chrome, MCPs locais) |

> Para renovar chave ElevenLabs: `elevenlabs.io` → avatar → Profile → API Keys → deletar chave antiga → Create API Key → colar no Railway Variables → confirmar `ELEVENLABS_VOICE_ID=onwK4e9ZLuTAKqWW03F9`.

> SSH no Dell (PowerShell como Admin):
> ```powershell
> Start-Service sshd; Set-Service -Name sshd -StartupType 'Automatic'
> $key = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIDARoAUlYSMUERft2wtEYGuAYk6zOh/zJncy3M9lMVW5 claude-code-samsung"
> Add-Content -Path "C:\ProgramData\ssh\administrators_authorized_keys" -Value $key
> icacls "C:\ProgramData\ssh\administrators_authorized_keys" /inheritance:r /grant "Administradores:F" /grant "SYSTEM:F"
> ```

---

### JARBAS Backend

#### Rodando Localmente

```bash
cd jarbas-backend
cp .env.example .env      # Preencher no mínimo ANTHROPIC_API_KEY
pip install -r requirements.txt
playwright install chromium   # Necessário para ferramentas de screenshot/browse
python main.py
```

Servidor inicia em `http://localhost:8000`. Verificar com:
```bash
curl http://localhost:8000/health
```

Modo dev com auto-reload:
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
| `ACCESS_TOKEN` | Não | Auth Bearer para todos os endpoints (aberto se não definido) |
| `DB_PATH` | Não | Caminho SQLite (padrão: `jarbas_memory.db`; usar `/data/jarbas_memory.db` no Railway) |
| `MAX_TOKENS` | Não | Padrão: 2048 |
| `HISTORY_LIMIT` | Não | Mensagens mantidas no contexto; padrão: 20 |

#### Arquitetura

**Módulos:**

- `main.py` — App FastAPI, todos os endpoints HTTP/WebSocket e o loop agêntico `run_agent()`
- `config.py` — Classe `Config` singleton que lê todas as env vars via `python-dotenv`
- `memory.py` — SQLite via `sqlite3` puro. Inicializa todas as tabelas na importação. Gerencia: mensagens, sessões, user_facts, movements (financeiro), reminders
- `personality.py` — System prompt e persona do JARBAS. `get_system_prompt(user_facts)` injeta fatos persistidos do usuário no prompt base em runtime
- `tools.py` — Todas as ferramentas do agente como funções async + `format_tools_for_claude()` (retorna schema de tools Claude) + dispatcher `process_tool_call()`
- `voice.py` — ElevenLabs TTS via `httpx`; retorna `bytes` ou `None`
- `browser.py` — Playwright Chromium headless; `take_screenshot()` retorna `{"base64": str, "url": str}` ou `{"error": str}`; `browse_and_read()` retorna texto da página

**Loop agêntico (`run_agent` em `main.py:110`):**

O loop roda até 10 iterações para tratar tool calls encadeadas:
1. Salvar mensagem do usuário → extrair/persistir fatos (regex em `memory.py`)
2. Carregar últimas N mensagens do SQLite como histórico
3. Construir system prompt com fatos do usuário injetados
4. Chamar Claude (`claude-sonnet-4-6`, definido em `config.py:CLAUDE_MODEL`)
5. Se `stop_reason == "tool_use"`: despachar ferramentas, anexar resultados como turno `user`, repetir
6. Na resposta de texto: salvar no DB e retornar

WebSocket (`/ws/{session_id}`) usa modo streaming — tokens enviados como frames JSON `{"type": "token", "content": "..."}`; REST `/chat` usa não-streaming.

**Design de memória:**
Tabela `user_facts` armazena fatos de longo prazo extraídos das mensagens via regex (padrões em português de nome/local/objetivo/negócio). Re-injetados no system prompt a cada chamada, dando memória persistente entre sessões sem RAG.

**Módulo financeiro:**
Tabela `movements` rastreia receitas/despesas. Ferramentas `add_movement`, `list_movements`, `get_balance` expõem isso ao Claude. Endpoints REST `/finance/balance` e `/finance/movements` também expõem diretamente.

#### Deploy (Railway)

O `Dockerfile` em `jarbas-backend/` constrói imagem `python:3.11-slim` com dependências Playwright Chromium. `railway.toml` configura o deploy Railway. Montar volume em `/data` e definir `DB_PATH=/data/jarbas_memory.db` para memória persistente.

#### Endpoints da API

| Método | Caminho | Descrição |
|---|---|---|
| GET | `/health` | Health check (sem auth) |
| GET | `/status` | Dashboard de status completo (sem auth) |
| POST | `/chat` | Enviar mensagem, receber resposta (REST, não-streaming) |
| GET | `/history` | Histórico de conversa de uma sessão |
| POST | `/clear` | Limpar histórico de sessão |
| POST | `/voice` | Text-to-speech (ElevenLabs) |
| GET | `/export/{session_id}` | Exportar histórico como JSON ou TXT |
| GET | `/finance/balance` | Resumo do saldo financeiro |
| GET | `/finance/movements` | Histórico de movimentos financeiros |
| GET | `/reminders` | Listar lembretes |
| POST | `/reminders` | Criar lembrete |
| PATCH | `/reminders/{id}/complete` | Marcar lembrete como concluído |
| WS | `/ws/{session_id}` | WebSocket streaming |

---

### Claude Code Plugins

Localizados em `plugins/`, cada plugin segue esta estrutura:

```
plugin-name/
├── .claude-plugin/plugin.json   # Metadados do plugin
├── commands/                    # Slash commands (*.md)
├── agents/                      # Subagentes especializados (*.md)
├── skills/                      # Skills auto-invocadas (SKILL.md)
├── hooks/                       # Event handlers
└── README.md
```

#### Plugins Disponíveis

| Plugin | O que faz |
|---|---|
| `agent-sdk-dev` | Comando `/new-sdk-app` + validadores para projetos Claude Agent SDK |
| `claude-opus-4-5-migration` | Migra strings de modelo e beta headers para Opus 4.5 |
| `code-review` | `/code-review` — revisão de PR multi-agente com pontuação de confiança |
| `commit-commands` | `/commit`, `/commit-push-pr`, `/clean_gone` — automação de workflow git |
| `explanatory-output-style` | Hook SessionStart que adiciona contexto educacional |
| `feature-dev` | `/feature-dev` — workflow guiado de desenvolvimento de feature em 7 fases |
| `frontend-design` | Skill auto-invocada para orientação de design frontend em produção |
| `hookify` | `/hookify` — cria hooks customizados a partir de análise da conversa |
| `learning-output-style` | Hook SessionStart que incentiva contribuições de código significativas |
| `plugin-dev` | `/plugin-dev:create-plugin` — criação guiada de plugin em 8 fases |
| `pr-review-toolkit` | `/pr-review-toolkit:review-pr` — agentes especializados em revisão de PR |
| `ralph-wiggum` | `/ralph-loop` — loops autônomos iterativos com interceptação de stop-hook |
| `security-guidance` | Hook PreToolUse que avisa sobre 9 padrões de segurança |

#### GitHub Actions

`.github/workflows/claude.yml` — Responde a menções `@claude` em issues/PRs usando `anthropics/claude-code-action@v1` com Workload Identity Federation (sem API key estática armazenada).

---

### Convenções do Projeto

- **Idioma:** Todo texto do JARBAS voltado ao usuário é em português do Brasil. Código, comentários e docstrings em `jarbas-backend/` também em português. Código de plugins em inglês.
- **Modelo Claude:** `claude-sonnet-4-6` (definido em `config.py`). Para atualizar, alterar `CLAUDE_MODEL` lá.
- **Sem suite de testes** para `jarbas-backend/`. Validar manualmente com `curl` contra o servidor em execução.
- **Conexões SQLite** abertas e fechadas por chamada (não pooled). Modo WAL habilitado.
- **Adição de ferramentas:** Adicionar função async em `tools.py`, registrar schema em `format_tools_for_claude()`, e adicionar branch de dispatch em `process_tool_call()`.
- **Resultados de screenshot** retornam ao Claude como visão (blocos de conteúdo `image`), não texto plano — este é o único lugar onde o conteúdo da resposta não é texto.
- O arquivo `weslley_profile.md` em `jarbas-backend/` é documentação de contexto para a persona/ferramentas do JARBAS mas não é carregado em runtime; fatos são armazenados no SQLite.
