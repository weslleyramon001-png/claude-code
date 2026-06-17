# Ativar JARBAS — Guia Rápido (quando chegar em casa)

> Tempo estimado: 10 minutos | Você faz, eu configuro o resto

---

## O que você precisa trazer

| # | O quê | Onde pegar |
|---|-------|-----------|
| 1 | API Key Anthropic | console.anthropic.com → API Keys |
| 2 | API Key ElevenLabs | elevenlabs.io → Profile → API Keys |
| 3 | Login Railway | railway.app → Login with GitHub |

---

## PASSO 1 — Anthropic (5 min)

1. Acessa **console.anthropic.com**
2. Cria conta ou faz login
3. Vai em **API Keys → Create Key**
4. Dá um nome: `JARBAS`
5. Copia a key: `sk-ant-api03-xxxxx`
6. Vai em **Billing → Add Credits → $10** (mínimo para ativar)
7. Me manda a key aqui no chat

---

## PASSO 2 — ElevenLabs (2 min)

1. Acessa **elevenlabs.io** (você já tem conta)
2. Clica no seu perfil → **Profile**
3. Copia a API Key
4. Me manda aqui no chat

---

## PASSO 3 — Railway (3 min)

1. Acessa **railway.app**
2. Clica **Login → Login with GitHub**
3. Autoriza o acesso
4. Me fala quando estiver logado — eu faço o resto

---

## O que EU faço depois

```
1. Crio o projeto no Railway via CLI
2. Configuro todas as variáveis de ambiente (.env)
3. Faço o deploy do JARBAS automaticamente
4. Railway gera URL pública (ex: jarbas.up.railway.app)
5. Conecto o frontend à URL
6. Testo chat + voz + memória
7. JARBAS online 24/7
```

---

## Enquanto isso — Tailscale (opcional, mas recomendado)

Se quiser que eu também acesse seu computador:

1. Baixa **tailscale.com/download/windows**
2. Instala → Login com Google
3. Acessa **login.tailscale.com/admin/settings/keys**
4. Generate auth key → Reusable ON → 90 days
5. Me manda a key

---

*Pode dormir tranquilo — quando chegar, é só me mandar as keys.*
