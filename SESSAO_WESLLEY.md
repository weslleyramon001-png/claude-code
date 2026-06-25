# Sessão Claude Code — Weslley Ramon
**Data:** 25/06/2026  
**Usuário:** weslleyramon001@gmail.com  
**Repositório:** weslleyramon001-png/claude-code  
**Branch de trabalho:** `jarbas/modest-fermi-neb57t`

---

## Modelo de IA

- **Modelo:** `claude-sonnet-4-6`
- **Empresa:** Anthropic
- **Cutoff de conhecimento:** Agosto 2025
- **Contexto:** Comprimido automaticamente quando fica longo — trabalho continua sem interrupção

---

## Ambiente de Execução

- **Tipo:** Container remoto na nuvem (ephemeral — some após inatividade)
- **Sistema:** Linux 6.18.5
- **Diretório de trabalho:** `/home/user/claude-code`
- **Repositório clonado fresh** a cada sessão nova
- **Tudo que vale a pena PRECISA ser commitado e pushado para persistir**
- **Chromium pré-instalado** (Playwright headless — sem janela visual)
- **Proxy HTTPS** configurado para saída de rede

---

## O Que Consigo Fazer

### Terminal & Sistema
- Rodar qualquer comando Bash no container
- Ler, criar, editar arquivos
- Git completo (commit, push, pull, branch, merge)
- Instalar pacotes (pip, npm, apt)
- Rodar servidores locais
- Playwright headless (navegar, clicar, fazer scraping, tirar screenshot de páginas)

### GitHub
- Ver PRs, issues, commits
- Criar PRs (como draft automaticamente após push)
- Comentar em issues/PRs
- Fazer push de código
- Criar branches, arquivos, releases
- Assinar PRs para receber eventos em tempo real (CI, reviews, comentários)

### Ferramentas MCP Disponíveis (Servidores Conectados)

| Servidor | O que faz |
|---|---|
| **GitHub** | CRUD completo: PRs, issues, commits, branches, releases, CI |
| **Gmail** | Ler, buscar, criar rascunhos, etiquetar emails |
| **Google Calendar** | Criar, editar, listar eventos; sugerir horários |
| **Google Drive** | Ler, criar, buscar, baixar, copiar arquivos |
| **Slack** | Enviar, ler, buscar mensagens; criar canais; reagir |
| **Canva** | Criar, editar, exportar designs |
| **Figma** | Ler/criar designs, componentes, design systems |
| **Gamma** | Criar apresentações e documentos com IA |
| **Lovable** | Criar apps full-stack com IA (TypeScript + Supabase) |
| **AWS Marketplace** | Pesquisar soluções na AWS Marketplace |
| **Supermetrics** | Analytics de marketing (150+ fontes: Google Ads, Meta, etc.) |
| **Kiwi.com** | Buscar voos |
| **Autodesk** | Buscar documentação de produtos Autodesk |
| **Alpic** | Deploys, logs, analytics de projetos |

### Skills (Comandos Slash) Disponíveis

| Skill | O que faz |
|---|---|
| `/commit-push-pr` | Commit + push + abre PR automaticamente |
| `/code-review` | Revisa PR com múltiplos agentes e score de confiança |
| `/security-review` | Revisão de segurança das mudanças pendentes |
| `/simplify` | Refatora código para simplicidade |
| `/run` | Roda o app do projeto e observa comportamento |
| `/verify` | Verifica se uma mudança funciona de verdade |
| `/review` | Revisa um PR do GitHub |
| `/init` | Cria CLAUDE.md com documentação do projeto |
| `/update-config` | Configura hooks, permissões, variáveis em settings.json |
| `/keybindings-help` | Customiza atalhos de teclado |
| `/loop` | Roda um comando em intervalo recorrente |
| `/claude-api` | Referência da API Anthropic/Claude |
| `/session-start-hook` | Cria hook de startup para o projeto |

### Agentes Especializados

| Agente | Para que serve |
|---|---|
| `Explore` | Busca rápida no código (arquivos, símbolos, padrões) |
| `Plan` | Planeja implementação de features complexas |
| `claude-code-guide` | Responde dúvidas sobre Claude Code, SDK, API |
| `general-purpose` | Pesquisa multi-step, tarefas complexas |
| `statusline-setup` | Configura status line do Claude Code |

---

## Permissões e Restrições

### O que posso fazer sem pedir confirmação
- Ler/editar/criar arquivos locais
- Rodar testes e linters
- Fazer buscas no código
- Usar a maioria das ferramentas de leitura

### O que peço confirmação antes de fazer
- `git push` (afeta repositório compartilhado)
- Deletar arquivos ou branches
- `git reset --hard` ou comandos destrutivos
- Criar PRs (faço automaticamente como draft após push)
- Postar comentários no GitHub
- Enviar mensagens pelo Slack/Gmail
- Qualquer ação irreversível ou visível para outros

### Restrições de repositório nesta sessão
- Só posso interagir com: `weslleyramon001-png/claude-code`
- Para outros repositórios: preciso verificar com `list_repos`

---

## Memória Desta Sessão

### Sobre Weslley Ramon
- Email: weslleyramon001@gmail.com
- Esposa: Lyvian (tem um Samsung — "Samsung Lyvian")
- Dell com Tailscale: IP `100.82.120.121`
- Projeto principal: **JARBAS** — assistente pessoal IA em produção no Railway

### JARBAS (Status 25/06/2026)
- **URL produção:** `https://claude-code-production-62f5.up.railway.app`
- **Railway project:** `lively-youthfulness`
- **Trial expira:** 18/07/2026 (upgradar para pago ~R$25/mês antes disso)
- **Interface local:** `D:\jarbas.html` (Edge no Dell)
- **Modelo:** `claude-sonnet-4-6` (definido em `config.py`)

| Feature | Status |
|---|---|
| Chat Claude | ✅ Online |
| Voice ElevenLabs Daniel (`onwK4e9ZLuTAKqWW03F9`) | ⚠️ Chave expirada (401) |
| Animação JARVIS | ✅ Online |
| Memória SQLite | ✅ Online |
| Web search Tavily | ✅ Online |
| Financeiro | ✅ Online |
| Lembretes | ✅ Online |
| Auth Bearer Token | ✅ Configurado no Railway |
| Push notifications | ✅ Pronto |
| PWA mobile | ✅ Pronto |

### Pendências JARBAS
- 🔴 **URGENTE:** Renovar chave ElevenLabs → `ELEVENLABS_API_KEY` no Railway
  - Como: elevenlabs.io → avatar → Profile → API Keys → deletar antiga → Create → colar no Railway
- 🟡 Antes 18/07: Upgrade Railway trial para plano pago
- ⬜ Tailscale nos outros notebooks (Samsung Lyvian etc.)
- ⬜ Clonar voz JARVIS (Paul Bettany) no ElevenLabs
- ⬜ MailerLite — funil de 7 emails (conteúdo pronto, falta configurar)
- ⬜ Kiwify — publicar pacote de planilhas (produto pronto, falta upload)

---

## Como Retomar Esta Sessão em Outro Notebook

1. Abra claude.ai/code (ou o app Claude Code)
2. Conecte ao repositório `weslleyramon001-png/claude-code`
3. Leia este arquivo: `SESSAO_WESLLEY.md`
4. Branch de trabalho: `jarbas/modest-fermi-neb57t`
5. Me diga: "Weslley, leia o SESSAO_WESLLEY.md e me ajude a configurar o notebook da Lyvian"

---

## Estrutura do Repositório

```
claude-code/
├── jarbas-backend/          # FastAPI — backend do JARBAS (produção no Railway)
│   ├── main.py              # App FastAPI + loop agêntico
│   ├── config.py            # Variáveis de ambiente (CLAUDE_MODEL aqui)
│   ├── memory.py            # SQLite — memória, finanças, lembretes
│   ├── personality.py       # System prompt do JARBAS
│   ├── tools.py             # Ferramentas do agente
│   ├── voice.py             # ElevenLabs TTS
│   ├── browser.py           # Playwright headless
│   ├── Dockerfile           # Build para Railway
│   └── railway.toml         # Config Railway
├── plugins/                 # Plugins Claude Code
│   ├── agent-sdk-dev/
│   ├── code-review/
│   ├── commit-commands/
│   ├── feature-dev/
│   └── ...
├── CLAUDE.md                # Instruções principais do projeto
└── SESSAO_WESLLEY.md        # Este arquivo
```
