# CLAUDE.md

Este arquivo fornece orientações ao Claude Code (claude.ai/code) ao trabalhar com o código deste repositório.

---

## Visão Geral do Repositório

Este repositório tem três partes distintas:

1. **`jarbas-backend/`** — Backend FastAPI para o JARBAS ("Just A Rather Brilliant Autonomous System"), assistente de IA pessoal do Weslley Ramon, construído sobre a API Anthropic com ferramentas, memória, voz e capacidade de browser.
2. **`jarbas-ui/`** — Frontend PWA do JARBAS: um único `index.html` com animação JARVIS, chat via WebSocket e service worker para suporte offline e instalação como app.
3. **`plugins/`** — Coleção de plugins do Claude Code (slash commands, agentes, hooks e skills) para estender as capacidades do Claude Code em qualquer projeto.

Os arquivos na raiz (`README.md`, `.github/`, `.devcontainer/`, `scripts/`, `examples/`) fazem parte do repositório upstream `anthropics/claude-code` no qual este fork é baseado.

---

## JARBAS — Status de Produção

**O JARBAS está em produção no Railway.**

| Item | Valor |
|---|---|
| URL de produção | `https://claude-code-production-62f5.up.railway.app` |
| Projeto Railway | `lively-youthfulness` |
| Interface local | `jarbas-ui/index.html` (abrir no browser, configurar a URL do backend nas configurações) |
| Trial Railway expira | **18/07/2026** — fazer upgrade para o plano pago (~R$25/mês) antes desta data |
| Tailscale (Dell) | `100.82.120.121` |

### Funcionalidades Ativas (em 24/06/2026)

| Funcionalidade | Status |
|---|---|
| Chat (Claude `claude-sonnet-4-6`) | ✅ Online |
| Voz — ElevenLabs Daniel (`onwK4e9ZLuTAKqWW03F9`) | ⚠️ Chave precisa de renovação (erro 401) |
| Animação JARVIS (4 anéis + waveform) | ✅ Online |
| Memória persistente (SQLite) | ✅ Online |
| Busca web (Tavily) | ✅ Online |
| Módulo financeiro (movimentos + saldo) | ✅ Online |
| Lembretes (CRUD) | ✅ Online |
| Autenticação Bearer Token (`ACCESS_TOKEN`) | ✅ Configurado no Railway |
| Notificações push | ✅ Pronto |
| PWA (instalável no celular) | ✅ Pronto |
| Clima (Open-Meteo) | ✅ Online (sem chave de API) |
| Info do sistema (psutil) | ✅ Online |
| Leitura/escrita/listagem de arquivos | ✅ Online |
| Gerenciamento explícito de memória | ✅ Online |
| Gerador de conteúdo de marketing | ✅ Online |

### Tarefas Pendentes

| Prioridade | Tarefa |
|---|---|
| 🔴 URGENTE | Renovar chave ElevenLabs → atualizar `ELEVENLABS_API_KEY` no Railway |
| 🟡 Antes de 18/07 | Fazer upgrade do trial Railway para plano pago |
| ⬜ | Tailscale nos outros notebooks (Samsung Lyvian etc.) |
| ⬜ | Clonar voz JARVIS (Paul Bettany) no ElevenLabs |
| ⬜ | MailerLite — configurar funil de 7 emails (conteúdo já escrito) |
| ⬜ | Kiwify — publicar pacote de planilhas (produto pronto, falta fazer upload) |

> Para renovar a chave ElevenLabs: `elevenlabs.io` → avatar → Profile → API Keys → deletar a chave antiga → Create API Key → colar nas Variables do Railway → confirmar `ELEVENLABS_VOICE_ID=onwK4e9ZLuTAKqWW03F9`.

---

## Backend JARBAS

### Rodando Localmente

```bash
cd jarbas-backend
cp .env.example .env      # Preencha pelo menos ANTHROPIC_API_KEY
pip install -r requirements.txt
playwright install chromium   # Necessário para as ferramentas de screenshot/browse
python main.py
```

O servidor inicia em `http://localhost:8000`. Verifique com:
```bash
curl http://localhost:8000/health
```

Modo de desenvolvimento com auto-reload:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Consulte `jarbas-backend/SETUP.md` para o guia completo de configuração e deploy no Railway.

### Variáveis de Ambiente

| Variável | Obrigatória | Descrição |
|---|---|---|
| `ANTHROPIC_API_KEY` | Sim | Necessária para todas as chamadas ao Claude |
| `ELEVENLABS_API_KEY` | Não | Habilita o endpoint `/voice` de TTS |
| `ELEVENLABS_VOICE_ID` | Não | Padrão: `onwK4e9ZLuTAKqWW03F9` (Daniel) |
| `TAVILY_API_KEY` | Não | Habilita a ferramenta `web_search` |
| `ACCESS_TOKEN` | Não | Auth Bearer para todos os endpoints (acesso aberto se não definido) |
| `SECRET_KEY` | Não | Chave secreta do app (gerar com `python -c "import secrets; print(secrets.token_hex(32))"`) |
| `ALLOWED_ORIGINS` | Não | Origens CORS separadas por vírgula, ou `*` (padrão: `*`) |
| `DB_PATH` | Não | Caminho do SQLite (padrão: `jarbas_memory.db`; use `/data/jarbas_memory.db` no Railway) |
| `MAX_TOKENS` | Não | Padrão: 4096 |
| `HISTORY_LIMIT` | Não | Mensagens mantidas no contexto; padrão: 30 |
| `HOST` | Não | Endereço de bind (padrão: `0.0.0.0`) |
| `PORT` | Não | Porta (padrão: `8000`) |

### Arquitetura

**Módulos:**

- `main.py` — App FastAPI, todos os endpoints HTTP/WebSocket e o loop agentic `run_agent()`
- `config.py` — Classe `Config` singleton que lê todas as variáveis de ambiente via `python-dotenv`
- `memory.py` — SQLite via `sqlite3` puro. Auto-inicializa todas as tabelas na importação. Gerencia: messages, sessions, user_facts, movements (financeiro), reminders
- `personality.py` — System prompt e persona do JARBAS. `get_system_prompt(user_facts)` injeta os fatos persistidos na prompt base em tempo de execução
- `tools.py` — Todas as ferramentas do agente como funções async + `format_tools_for_claude()` (retorna o schema de tools do Claude) + dispatcher `process_tool_call()`
- `voice.py` — TTS ElevenLabs via `httpx`; retorna `bytes` ou `None`
- `browser.py` — Playwright headless Chromium; `take_screenshot()` retorna `{"base64": str, "url": str}` ou `{"error": str}`; `browse_and_read()` retorna o texto da página
- `SETUP.md` — Guia completo de configuração local e deploy no Railway

**O loop agentic (`run_agent` em `main.py:110`):**

O loop executa até 10 iterações para tratar chamadas encadeadas de ferramentas:
1. Salva mensagem do usuário → extrai e persiste fatos (regex em `memory.py`)
2. Carrega as últimas N mensagens do SQLite como histórico de conversa
3. Constrói o system prompt com os fatos do usuário injetados
4. Chama o Claude (`claude-sonnet-4-6`, definido em `config.py:CLAUDE_MODEL`)
5. Se `stop_reason == "tool_use"`: despacha ferramentas, adiciona resultados como turno `user`, repete
6. Na resposta de texto: salva no banco e retorna

O WebSocket (`/ws/{session_id}`) usa modo streaming — tokens são enviados como frames JSON:
```
{"type": "token",      "content": "..."}               — um por token recebido em streaming
{"type": "screenshot", "url": "...", "base64": "..."}  — resultado de screenshot do browser
{"type": "done",       "full_response": "...", "tool_calls": [...]}
{"type": "error",      "message": "..."}
```
O endpoint REST `/chat` usa modo sem streaming.

**Design de memória:**
A tabela `user_facts` armazena fatos de longo prazo de duas formas:
1. **Auto-extração**: padrões regex em `memory.py` detectam nome, localização, metas e negócios a partir das mensagens em português
2. **Salvamento explícito**: a ferramenta `save_memory` permite ao Claude salvar fatos por categoria (`identity`, `business`, `goals`, `preferences`, `finance`, `projects`, etc.)

Os fatos são reinjetados no system prompt a cada chamada, dando ao JARBAS memória persistente entre sessões sem RAG. Use as ferramentas `list_memories` e `delete_memory` para gerenciar os fatos armazenados.

**Módulo financeiro:**
A tabela `movements` registra entradas e saídas. As ferramentas `add_movement`, `list_movements`, `get_balance` expõem isso ao Claude. Os endpoints REST `/finance/balance` e `/finance/movements` também expõem diretamente.

### Ferramentas do Agente (lista completa)

| Ferramenta | Descrição |
|---|---|
| `get_current_datetime` | Data e hora atual no fuso de Brasília |
| `calculate` | Cálculo matemático seguro (operações básicas, sqrt, log, trig, pi, e) |
| `web_search` | Busca web via Tavily (requer `TAVILY_API_KEY`) |
| `get_weather` | Clima em tempo real via Open-Meteo (sem chave) |
| `create_file_content` | Gera conteúdo formatado como arquivo para download/cópia |
| `generate_pony_digital_content` | Conteúdo de marketing: hook, caption, email, cta, headline |
| `system_info` | CPU, RAM, disco, uptime via psutil |
| `run_command` | Executa comandos shell no servidor |
| `list_files` | Lista conteúdo de diretório |
| `read_file` | Lê conteúdo de arquivo |
| `write_file` | Cria ou sobrescreve um arquivo |
| `add_movement` | Registra movimento financeiro (entrada/saida) |
| `list_movements` | Lista movimentos financeiros com resumo de saldo |
| `get_balance` | Mostra total de entradas, saídas e saldo líquido |
| `create_reminder` | Cria um lembrete com prazo opcional |
| `list_reminders` | Lista lembretes pendentes (ou todos) |
| `complete_reminder` | Marca lembrete como concluído por ID |
| `save_memory` | Salva explicitamente um fato na memória persistente |
| `list_memories` | Lista todas as memórias salvas por categoria |
| `delete_memory` | Apaga uma memória por ID |
| `take_screenshot` | Screenshot do browser headless de qualquer URL |
| `browse_and_read` | Extração de texto via browser headless de uma URL |

**Para adicionar uma nova ferramenta:** adicione a função async em `tools.py`, registre seu schema em `format_tools_for_claude()` e adicione um branch de dispatch em `process_tool_call()`.

### Deploy (Railway)

O `Dockerfile` em `jarbas-backend/` constrói uma imagem `python:3.11-slim` com as dependências do Playwright Chromium. O `railway.toml` configura o deploy no Railway. Monte um volume em `/data` e defina `DB_PATH=/data/jarbas_memory.db` para memória persistente entre restarts.

### Resumo dos Endpoints da API

| Método | Caminho | Auth | Descrição |
|---|---|---|---|
| GET | `/health` | Nenhuma | Health check + status dos serviços |
| GET | `/status` | Nenhuma | Dashboard completo (verifica Anthropic/ElevenLabs/Tavily/DB) |
| POST | `/chat` | Bearer | Envia mensagem, recebe resposta (REST, sem streaming) |
| GET | `/history` | Bearer | Histórico de conversa de uma sessão |
| POST | `/clear` | Bearer | Limpa histórico da sessão |
| POST | `/voice` | Bearer | Texto para fala (ElevenLabs), retorna `audio/mpeg` |
| GET | `/export/{session_id}` | Nenhuma | Exporta histórico em JSON ou TXT (`?format=txt`) |
| GET | `/finance/balance` | Bearer | Resumo do saldo financeiro |
| GET | `/finance/movements` | Bearer | Histórico de movimentos financeiros (`?limit=20&category=`) |
| GET | `/reminders` | Bearer | Lista lembretes (`?include_completed=false`) |
| POST | `/reminders` | Bearer | Cria lembrete |
| PATCH | `/reminders/{id}/complete` | Bearer | Marca lembrete como concluído |
| WS | `/ws/{session_id}` | `?token=` | WebSocket com streaming |

---

## Frontend JARBAS

Localizado em `jarbas-ui/`, é um frontend PWA auto-contido:

```
jarbas-ui/
├── index.html      # App single-file: animação JARVIS + chat WebSocket
├── manifest.json   # Manifesto PWA (tema roxo escuro, pt-BR)
├── sw.js           # Service worker para cache offline
└── icons/          # Ícones do app (192×192, 512×512)
```

**Detalhes de design:**
- `index.html` único — todo CSS e JS inline, sem etapa de build
- Tema roxo escuro (`#09050F` background, `#A855F7` primário)
- Animação JARVIS com 4 anéis e waveform de áudio
- Conecta ao backend via WebSocket (`wss://...` em produção, `ws://localhost:8000` localmente)
- URL do backend e token Bearer configuráveis pelo painel de configurações no app
- Instalável como PWA no celular (Android/iOS)
- Service worker com estratégia network-first; cache de fallback para `index.html` e `manifest.json`

Para usar: abra `jarbas-ui/index.html` no browser, clique no ícone de configurações e informe a URL WebSocket do backend e o token de acesso.

---

## Plugins do Claude Code

Localizados em `plugins/`, cada plugin segue esta estrutura:

```
plugin-name/
├── .claude-plugin/plugin.json   # Metadados do plugin
├── commands/                    # Slash commands (*.md)
├── agents/                      # Subagentes especializados (*.md)
├── skills/                      # Skills auto-invocadas (SKILL.md)
├── hooks/                       # Handlers de eventos
└── README.md
```

### Plugins Disponíveis

| Plugin | O que faz |
|---|---|
| `agent-sdk-dev` | Comando `/new-sdk-app` + validadores para projetos com Claude Agent SDK |
| `claude-opus-4-5-migration` | Migra strings de modelo e headers beta para o Opus 4.5 |
| `code-review` | `/code-review` — revisão de PR multi-agente com pontuação de confiança |
| `commit-commands` | `/commit`, `/commit-push-pr`, `/clean_gone` — automação de workflow git |
| `explanatory-output-style` | Hook SessionStart que adiciona contexto educacional |
| `feature-dev` | `/feature-dev` — workflow guiado de desenvolvimento de features em 7 fases |
| `frontend-design` | Skill auto-invocada para orientações de design frontend profissional |
| `hookify` | `/hookify` — cria hooks customizados a partir da análise da conversa |
| `learning-output-style` | Hook SessionStart que incentiva contribuições de código com significado |
| `plugin-dev` | `/plugin-dev:create-plugin` — criação guiada de plugins em 8 fases |
| `pr-review-toolkit` | `/pr-review-toolkit:review-pr` — agentes especializados em revisão de PR |
| `ralph-wiggum` | `/ralph-loop` — loops autônomos iterativos com intercepção por stop-hook |
| `security-guidance` | Hook PreToolUse que avisa sobre 9 padrões de segurança |

### GitHub Actions

`.github/workflows/` contém vários workflows automatizados:

| Workflow | Finalidade |
|---|---|
| `claude.yml` | Responde a menções `@claude` em issues/PRs via `anthropics/claude-code-action@v1` |
| `claude-issue-triage.yml` | Triagem automática de novas issues com labels |
| `claude-dedupe-issues.yml` | Detecta e marca issues duplicadas |
| `auto-close-duplicates.yml` | Fecha automaticamente issues confirmadas como duplicatas |
| `issue-lifecycle-comment.yml` | Posta comentários de ciclo de vida em issues |
| `lock-closed-issues.yml` | Trava issues após fechamento |
| `sweep.yml` | Varredura periódica de issues obsoletas |
| Outros | `log-issue-events.yml`, `non-write-users-check.yml`, etc. |

Todos os workflows com Claude usam Workload Identity Federation (nenhuma API key estática armazenada).

---

## Convenções Importantes

- **Idioma:** Todo texto voltado ao usuário no JARBAS está em português brasileiro. Código, comentários e docstrings em `jarbas-backend/` também são em português. Código de plugins fica em inglês.
- **Modelo Claude:** `claude-sonnet-4-6` (definido em `config.py:CLAUDE_MODEL`). Para atualizar, altere `CLAUDE_MODEL` nesse arquivo.
- **Sem suite de testes** para `jarbas-backend/`. Valide manualmente com `curl` contra o servidor em execução.
- **Conexões SQLite** são abertas e fechadas por chamada (sem pool). Modo WAL habilitado.
- **Resultados de screenshot** voltam ao Claude como blocos de visão (`image` content blocks), não texto plano — é o único lugar onde o conteúdo da resposta não é texto.
- O arquivo `weslley_profile.md` em `jarbas-backend/` é documentação de contexto da persona/ferramentas do JARBAS, mas não é carregado em runtime; os fatos ficam armazenados no SQLite.
- **CORS:** Padrão permite todas as origens (`*`). Restrinja via variável de ambiente `ALLOWED_ORIGINS` em produção.
- **Auth:** Token Bearer verificado via variável `ACCESS_TOKEN`. Auth do WebSocket usa query param `?token=`.
