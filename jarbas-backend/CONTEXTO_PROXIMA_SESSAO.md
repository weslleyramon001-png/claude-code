# Contexto para Próxima Sessão — JARBAS + IXC + OPA Suite

**Data:** 03/07/2026  
**Prioridade:** Continuar acesso IXC e implementar ferramentas permanentes

---

## 1. ACESSO IXC — O QUE FOI DESCOBERTO

### Credenciais
- **URL admin:** `https://ixc.servlinktelecom.com.br/adm.php`
- **Login web:** `ramon@servlink.com.br` / `8768238888Ll@`
- **2FA:** Sim — código enviado para `weslleyramon001@gmail.com` (remetente: `noreply@ixcsoft.com.br`)
- **Basic Auth API:** `NTc6MTM2YTRiZGMwNDY4MDA3ZDhlYTA3Mzg5YjQxMTcyOWI4Y2M2ZGY0NGNlZmRkNWMyYTRhYjBhYmVkZDQyMzJkMQ==`

### Problema da API REST (webservice/v1)
- **POST funciona** (criação de registros)
- **GET com body = 404** — nginx do servidor IXC descarta o body em requisições GET antes de chegar ao PHP
- **Fix:** SSH no servidor → ajustar nginx para passar body em GET
- **Alternativa funcionando:** Playwright navegando a interface web `adm.php`

### O que o Playwright conseguiu fazer
- Login completo com 2FA via Playwright ✅
- Acessou painel admin `adm.php` ✅
- Navegou Provedor → Clientes Fibra (ONU): **5.916 ONUs total** ✅
- Viu coluna "ONU rede neutra" na listagem ✅
- Menu tem: **Rede Neutra - Client** e **Clientes Fibra (ONU)**

### TAREFA PENDENTE — Alta prioridade
O usuário quer:
1. **Quantidade de ONUs online por VLAN da rede neutra**
2. Para isso: logar no IXC → Provedor → Rede Neutra - Client → ver lista por VLAN

### Como fazer na próxima sessão
```python
# Fluxo de login Playwright (testado e funcionando):
# 1. Acessa /app/login
# 2. Preenche #email → Enter
# 3. Preenche #password → Enter  
# 4. Se "sessão ativa": clica vg-button com "Enter"
# 5. Se "Two-Factor": preenche input visível com código do email → Enter
# 6. Navega: Provedor → Rede Neutra - Client
# OBS: token 2FA expira rápido — pegar do Gmail MCP (noreply@ixcsoft.com.br)
```

### Ferramentas Playwright disponíveis
- Chromium em `/opt/pw-browsers/chromium`
- Remover proxy: `os.environ.pop('HTTPS_PROXY', None)` etc.
- Args obrigatórios: `--no-sandbox --disable-dev-shm-usage --ignore-certificate-errors`

---

## 2. IMPLEMENTAÇÃO PERMANENTE — O QUE FAZER

### A. Adicionar ferramentas IXC ao JARBAS (`jarbas-backend/tools.py`)
Ferramentas a criar (usando Playwright + httpx):
- `ixc_clientes_fibra_onu` — lista ONUs com filtros
- `ixc_rede_neutra_por_vlan` — conta ONUs por VLAN da rede neutra
- `ixc_login_playwright` — função de login reutilizável

### B. Salvar credenciais IXC como variável Railway
Adicionar ao Railway:
- `IXC_LOGIN_EMAIL=ramon@servlink.com.br`
- `IXC_LOGIN_PASSWORD=8768238888Ll@`
- `IXC_BASIC_AUTH=NTc6MTM2YTRiZGMwNDY4MDA3ZDhlYTA3Mzg5YjQxMTcyOWI4Y2M2ZGY0NGNlZmRkNWMyYTRhYjBhYmVkZDQyMzJkMQ==`
- `IXC_BASE_URL=https://ixc.servlinktelecom.com.br`

### C. Problema do 2FA
- O IXC pede 2FA a cada nova sessão de navegador
- Solução: marcar dispositivo como "confiável por 30 dias" durante o login Playwright
  - Há um checkbox "Trust this browser for 30 days" na tela de 2FA
  - Se marcado, sessões subsequentes do mesmo browser storage não pedem 2FA
- Implementar: salvar browser state (cookies + localStorage) em arquivo persistente

---

## 3. OPA SUITE — STATUS

### Documentação salva no Google Drive
- **Pasta:** `opa-suite` (ID: `1ig2ucmbPMVascIjIhORwtwRmnsq3Q7iI`)
- **Arquivo:** `api-opa-suite.md` (ID: `1AQwybHyI5DHznUfQnf6hqOU8vcqQPFBJ`)
- **Pasta pai:** ID `1enQJ-luY1ydW8Hejz047P-SqQ1GUnWtA`

### O que está documentado (19 endpoints):
- Atendimentos (CRUD + filtros)
- Canais, Templates, Cliente, Contatos, Etiqueta, Departamentos

### Seções PENDENTES (não documentadas ainda):
- Mensagens, Usuário, Notificação, Motivos, Períodos
- Usuário precisa colar o conteúdo dessas seções quando disponível

### Autenticação OPA Suite
```
Base URL: https://meudominio.com.br/api/v1/
Authorization: Bearer MEUTOKEN
```
- No caso da Servlink: usar o token da conta OPA Suite deles
- Integração principal: WhatsApp via dialog360

---

## 4. PRÓXIMOS PASSOS (em ordem de prioridade)

1. **[AGORA]** Logar IXC com novo 2FA → Provedor → Rede Neutra - Client → contar ONUs por VLAN
2. **[HOJE]** Implementar `ixc_rede_neutra_por_vlan` no JARBAS com browser state persistente
3. **[HOJE]** Marcar dispositivo Playwright como "confiável 30 dias" para evitar 2FA futuro
4. **[SEMANA]** Documentar seções pendentes OPA Suite (pedir ao usuário)
5. **[SEMANA]** Corrigir nginx IXC para GET+body funcionar (precisa SSH no servidor)

---

## 5. ESTRUTURA DO PROJETO

```
jarbas-backend/
├── main.py          # FastAPI + WebSocket + run_agent()
├── config.py        # Config singleton, CLAUDE_MODEL="claude-sonnet-4-6"
├── memory.py        # SQLite: messages, user_facts, movements, reminders
├── personality.py   # System prompt JARBAS, get_system_prompt(user_facts)
├── tools.py         # Ferramentas do agente (adicionar ixc_* aqui)
├── voice.py         # ElevenLabs TTS
└── browser.py       # Playwright: take_screenshot(), browse_and_read()
```

**Deploy:** Railway — `https://claude-code-production-62f5.up.railway.app`  
**Branch de trabalho:** `claude/greeting-qjbwba`

---

## 6. COMO INICIAR A PRÓXIMA SESSÃO

```
Contexto: Arquivo CONTEXTO_PROXIMA_SESSAO.md no repo.
Tarefa imediata: Logar no IXC (usar Playwright com 2FA do Gmail MCP),
navegar Provedor → Rede Neutra - Client, extrair contagem de ONUs online por VLAN.
Em seguida: implementar ferramentas IXC permanentes no jarbas-backend/tools.py.
```
