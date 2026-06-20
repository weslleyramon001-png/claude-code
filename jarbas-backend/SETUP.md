# JARBAS Backend — Guia de Configuração

**JARBAS** = Just A Rather Brilliant Autonomous System  
Backend do seu assistente de IA pessoal. Precisa de chaves de API para funcionar.

---

## Pré-requisitos

- Python 3.11+
- Conta na Anthropic (obrigatório) → https://console.anthropic.com/
- Conta na ElevenLabs (opcional, para voz) → https://elevenlabs.io/
- Conta na Tavily (opcional, para busca web) → https://tavily.com/

---

## Passo 1 — Clonar o repositório e entrar na pasta

```bash
git clone https://github.com/weslleyramon001-png/claude-code.git
cd claude-code/jarbas-backend
```

---

## Passo 2 — Configurar as chaves de API

Copie o arquivo de exemplo e edite com suas chaves:

```bash
cp .env.example .env
```

Abra o `.env` e preencha:

| Variável | Onde obter | Obrigatório? |
|----------|-----------|--------------|
| `ANTHROPIC_API_KEY` | https://console.anthropic.com/ → API Keys | SIM |
| `ELEVENLABS_API_KEY` | https://elevenlabs.io/ → Profile → API Key | Não (voz desativada) |
| `ELEVENLABS_VOICE_ID` | https://elevenlabs.io/voice-library | Não (usa Adam por padrão) |
| `TAVILY_API_KEY` | https://tavily.com/ → Dashboard | Não (busca web desativada) |
| `SECRET_KEY` | Gere com `python -c "import secrets; print(secrets.token_hex(32))"` | Recomendado em produção |

### Como obter a chave Anthropic (passo a passo):
1. Acesse https://console.anthropic.com/
2. Crie uma conta (ou faça login)
3. No menu lateral, clique em **"API Keys"**
4. Clique em **"Create Key"**
5. Copie a chave (começa com `sk-ant-...`)
6. Cole em `ANTHROPIC_API_KEY=` no seu `.env`

---

## Passo 3 — Instalar dependências

```bash
pip install -r requirements.txt
```

Se preferir usar um ambiente virtual (recomendado):

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

---

## Passo 4 — Rodar localmente

```bash
python main.py
```

O servidor inicia em `http://localhost:8000`

Verifique se está funcionando:

```bash
curl http://localhost:8000/health
```

Resposta esperada:
```json
{"status": "ok", "version": "1.0.0", "jarbas": "online"}
```

---

## Passo 5 — Fazer deploy no Railway

### 5.1 Criar conta no Railway
1. Acesse https://railway.app/
2. Clique em **"Start a New Project"**
3. Faça login com sua conta GitHub

### 5.2 Criar novo projeto
1. Clique em **"New Project"**
2. Selecione **"Deploy from GitHub repo"**
3. Selecione o repositório `weslleyramon001-png/claude-code`
4. Railway vai detectar o `Dockerfile` automaticamente

### 5.3 Configurar variáveis de ambiente no Railway
1. No painel do projeto, clique na sua aplicação
2. Vá em **"Variables"**
3. Adicione cada variável do seu `.env`:
   - `ANTHROPIC_API_KEY` = sua chave
   - `ELEVENLABS_API_KEY` = sua chave (se tiver)
   - `TAVILY_API_KEY` = sua chave (se tiver)
   - `SECRET_KEY` = string aleatória longa
   - `DB_PATH` = `/data/jarbas_memory.db`

### 5.4 Adicionar volume persistente (para o banco de dados)
1. No painel do projeto, clique em **"+ New"** → **"Volume"**
2. Monte em `/data`
3. Isso garante que a memória do JARBAS persista entre restarts

### 5.5 Fazer deploy
1. Clique em **"Deploy"**
2. Aguarde o build (geralmente 2-3 minutos)
3. Railway vai mostrar a URL pública: `https://seu-projeto.up.railway.app`

### 5.6 Verificar o deploy
```bash
curl https://seu-projeto.up.railway.app/health
```

---

## Passo 6 — Conectar o Frontend

1. Abra o arquivo `../jarbas-ui/index.html` no seu navegador
2. Clique no ícone de configurações (canto superior direito)
3. Em **"Backend URL"**, coloque a URL do Railway:
   ```
   wss://seu-projeto.up.railway.app/ws/default
   ```
4. Clique em **"Salvar"**

Para testar localmente, use:
```
ws://localhost:8000/ws/default
```

---

## Passo 7 — Testar com curl

### Enviar uma mensagem:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Olá JARBAS, como você está?", "session_id": "teste"}'
```

### Ver histórico:
```bash
curl "http://localhost:8000/history?session_id=teste"
```

### Limpar histórico:
```bash
curl -X POST http://localhost:8000/clear \
  -H "Content-Type: application/json" \
  -d '{"session_id": "teste"}'
```

### Testar voz (salva como audio.mp3):
```bash
curl -X POST http://localhost:8000/voice \
  -H "Content-Type: application/json" \
  -d '{"text": "JARBAS online e pronto para servir, Weslley."}' \
  --output audio.mp3
```

### Health check:
```bash
curl http://localhost:8000/health
```

---

## Solução de Problemas

| Erro | Causa provável | Solução |
|------|----------------|---------|
| `503` em `/chat` | `ANTHROPIC_API_KEY` ausente | Adicione a chave no `.env` |
| `401 Unauthorized` | Chave da API inválida | Verifique se a chave está correta |
| `Connection refused` | Servidor não está rodando | Execute `python main.py` |
| Voz retorna `503` | `ELEVENLABS_API_KEY` ausente | Adicione a chave ou ignore |
| Busca web indisponível | `TAVILY_API_KEY` ausente | Adicione a chave ou ignore |

---

## Estrutura dos arquivos

```
jarbas-backend/
├── main.py          ← Servidor FastAPI (endpoints + WebSocket)
├── config.py        ← Configurações e variáveis de ambiente
├── memory.py        ← Memória SQLite (histórico + fatos do usuário)
├── personality.py   ← Personalidade e system prompt do JARBAS
├── tools.py         ← Ferramentas do agente (busca, cálculo, etc.)
├── voice.py         ← Síntese de voz ElevenLabs
├── requirements.txt ← Dependências Python
├── Dockerfile       ← Para deploy em containers
├── railway.toml     ← Configuração Railway
├── .env.example     ← Template de configuração (copie para .env)
└── SETUP.md         ← Este arquivo
```
