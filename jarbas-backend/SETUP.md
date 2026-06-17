# JARBAS — Guia de Setup Completo

## 1. Configurar as chaves (.env)

Copie o arquivo de exemplo e preencha:
```bash
cp .env.example .env
```

Edite `.env` com suas chaves:
- `ANTHROPIC_API_KEY` → console.anthropic.com → API Keys
- `ELEVENLABS_API_KEY` → elevenlabs.io → Profile → API Keys
- `AGENT_NAME` → o nome que escolher (JARBAS, SCOFIELD, etc.)

## 2. Rodar localmente (teste)

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Acessa: http://localhost:8000/health

## 3. Deploy no Railway

1. Acessa railway.app → New Project → Deploy from GitHub
2. Seleciona o repo `weslleyramon001-png/claude-code`
3. Define o Root Directory como `jarbas-backend`
4. Adiciona as variáveis de ambiente (mesmo conteúdo do .env)
5. Railway gera uma URL pública automaticamente

## 4. Conectar o frontend

No arquivo `jarbas-ui/index.html`, troque:
```js
const BACKEND_URL = "http://localhost:8000"  // local
// ou
const BACKEND_URL = "https://SEU-APP.railway.app"  // produção
```

## 5. Endpoints disponíveis

| Endpoint | Método | Função |
|---|---|---|
| `/health` | GET | Status do sistema |
| `/chat` | POST | Enviar mensagem |
| `/ws/{session_id}` | WebSocket | Chat em tempo real (streaming) |
| `/history/{session_id}` | GET | Histórico da sessão |
| `/clear/{session_id}` | POST | Limpar histórico |
| `/fact` | POST | Salvar fato na memória longa |
| `/voice/{text}` | GET | Gerar áudio (ElevenLabs) |

## 6. Trocar o nome do agente

Mude `AGENT_NAME` no `.env` para qualquer nome que escolher.
O sistema usa em toda a personalidade e respostas automaticamente.
