# Guia de Setup — Notebook da Lyvian
**Para ter exatamente o mesmo ambiente do Dell do Weslley**  
Data de referência: 25/06/2026

---

## Entendendo Como Funciona

Esta sessão roda em **dois modos diferentes**:

| Modo | Como acessar | MCP Servers | Plugins |
|---|---|---|---|
| **Claude Code na Web** (este aqui) | claude.ai/code | Gmail, Drive, Calendar, Slack, Canva, Figma, etc. — tudo automático pela plataforma | Skills e comandos do repositório |
| **Claude Code CLI** (terminal local) | Instalar o CLI + configurar manualmente | Precisa configurar cada MCP server | Plugins do repositório |

**A maioria dos poderes desta sessão vem do claude.ai/code** — basta logar com a mesma conta Google/Anthropic em qualquer máquina e tudo aparece igual.

---

## PASSO 1 — Acesso Imediato (5 minutos)

### No Samsung da Lyvian, abrir o navegador:

1. Ir para: **https://claude.ai/code**
2. Fazer login com a conta: `weslleyramon001@gmail.com`
3. Conectar o repositório: `weslleyramon001-png/claude-code`
4. Pronto — todos os MCP servers (Gmail, Google Drive, Calendar, Slack, Canva, Figma, Gamma, Lovable, GitHub, etc.) estarão disponíveis automaticamente

Isso já dá **100% dos poderes desta sessão** sem instalar nada.

---

## PASSO 2 — Claude Code CLI Local (Terminal nativo)

Para rodar no terminal do Samsung sem precisar do navegador:

### Windows (PowerShell como Administrador):
```powershell
# Instalar Node.js (se não tiver)
winget install OpenJS.NodeJS.LTS

# Instalar Claude Code CLI
npm install -g @anthropic-ai/claude-code

# Verificar instalação
claude --version
```

### Login:
```bash
claude
# Na primeira vez abre o navegador para autenticar com a conta Anthropic
# Usar: weslleyramon001@gmail.com
```

---

## PASSO 3 — Clonar o Repositório

```bash
# No terminal do Samsung:
git clone https://github.com/weslleyramon001-png/claude-code.git
cd claude-code

# Mudar para o branch de trabalho
git checkout jarbas/modest-fermi-neb57t

# Abrir Claude Code dentro do projeto
claude
```

Agora o Claude Code local terá acesso a todos os plugins do repositório:
- `/commit-push-pr`
- `/code-review`
- `/feature-dev`
- `/hookify`
- E todos os outros em `plugins/`

---

## PASSO 4 — MCP Servers no CLI Local

Os MCP servers no CLI local precisam ser configurados manualmente. Criar o arquivo:

**Windows:** `C:\Users\<nome-usuario>\.claude\claude_desktop_config.json`  
**Linux/Mac:** `~/.claude/claude_desktop_config.json`

### Configuração base (GitHub já vem via token):
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "SEU_TOKEN_GITHUB_AQUI"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:\\Users\\Lyvian\\Documents"]
    }
  }
}
```

### Para os outros servidores (Gmail, Drive, Calendar, Slack, etc.):
Esses servidores no **claude.ai/code** são gerenciados pela Anthropic automaticamente.  
No CLI local, cada um precisa de setup OAuth próprio — é mais complexo.  
**Recomendação: usar o claude.ai/code no navegador para tarefas que precisam desses serviços.**

---

## PASSO 5 — Tailscale (Rede com o Dell do Weslley)

Para o Samsung da Lyvian acessar o Dell (IP `100.82.120.121`) e o JARBAS local:

### Windows:
1. Baixar: https://tailscale.com/download/windows
2. Instalar e abrir
3. Fazer login com a mesma conta Google: `weslleyramon001@gmail.com`
4. Aceitar o convite da rede (Weslley precisa aprovar no painel Tailscale)

### Verificar conexão:
```bash
# Após instalar Tailscale, deve pingar o Dell:
ping 100.82.120.121
```

---

## PASSO 6 — JARBAS (Interface Local)

O JARBAS roda na nuvem (Railway) — não precisa instalar nada para usar.  
Basta abrir o arquivo de interface no navegador:

1. Weslley copia o arquivo `D:\jarbas.html` para um pen drive ou envia via WhatsApp/Drive
2. No Samsung: salvar em qualquer lugar, ex: `C:\Users\Lyvian\Desktop\jarbas.html`
3. Abrir com Edge ou Chrome
4. URL da API já está configurada no HTML apontando para Railway

Ou acessar direto: **https://claude-code-production-62f5.up.railway.app**

---

## PASSO 7 — Git Configurado

```bash
git config --global user.name "Weslley Ramon"
git config --global user.email "weslleyramon001@gmail.com"
```

---

## PASSO 8 — VS Code (opcional, mas recomendado)

```bash
# Instalar VS Code
winget install Microsoft.VisualStudioCode

# Extensão Claude Code no VS Code
# Abrir VS Code → Extensions → buscar "Claude Code" → Instalar
```

---

## Resumo — Checklist para o Samsung Lyvian

- [ ] Abrir claude.ai/code e logar com weslleyramon001@gmail.com
- [ ] Conectar repositório weslleyramon001-png/claude-code
- [ ] Selecionar branch `jarbas/modest-fermi-neb57t`
- [ ] Testar: pedir para ler este arquivo SETUP_LYVIAN.md
- [ ] (Opcional) Instalar Node.js + `npm install -g @anthropic-ai/claude-code`
- [ ] (Opcional) `git clone` do repositório no terminal local
- [ ] (Opcional) Instalar Tailscale e entrar na rede do Weslley
- [ ] (Opcional) Copiar `jarbas.html` para o desktop
- [ ] (Opcional) Instalar VS Code + extensão Claude Code

---

## O Que Fica Igual Automaticamente (sem configurar nada)

Ao logar no claude.ai/code com a mesma conta:
- Modelo: `claude-sonnet-4-6`
- MCP Servers: Gmail, Google Drive, Google Calendar, Slack, GitHub, Canva, Figma, Gamma, Lovable, Kiwi, AWS Marketplace, Supermetrics, Alpic, Autodesk
- Histórico de contexto da sessão (via SESSAO_WESLLEY.md no repositório)
- Todos os plugins em `plugins/`
- Todas as skills e comandos slash
- Acesso ao JARBAS backend no Railway

---

## Chaves de API (para CLI local ou `.env` do JARBAS)

Se for rodar o JARBAS localmente no Samsung, precisará de:

| Variável | Onde obter |
|---|---|
| `ANTHROPIC_API_KEY` | console.anthropic.com → API Keys |
| `ELEVENLABS_API_KEY` | elevenlabs.io → Profile → API Keys (⚠️ renovar — atual expirada) |
| `TAVILY_API_KEY` | app.tavily.com |
| `ACCESS_TOKEN` | Qualquer senha forte (você define) |

---

## Contato de Suporte

- Repositório: https://github.com/weslleyramon001-png/claude-code
- Claude Code docs: https://code.claude.com/docs
- Para retomar esta sessão: abrir claude.ai/code → repositório → ler SESSAO_WESLLEY.md
