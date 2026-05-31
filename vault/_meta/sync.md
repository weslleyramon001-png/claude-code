---
tipo: guia
titulo: Configuração de Sync — Windows + Obsidian Git
tags: [sync, obsidian, windows, git]
---

# Sync Automático — Windows + Obsidian Git

> Este guia conecta o Obsidian ao repositório GitHub onde a Lyvian salva tudo.
> Toda vez que a Lyvian atualizar o vault, o Obsidian no seu PC reflete automaticamente.

---

## Passo 1 — Instalar o Git no Windows

1. Acesse: https://git-scm.com/download/win
2. Baixe e instale o **Git for Windows**
3. Durante a instalação, deixe todas as opções padrão
4. Confirme que funcionou abrindo o **PowerShell** e digitando:
   ```powershell
   git --version
   ```

---

## Passo 2 — Clonar o repositório

Abra o **PowerShell** e execute:

```powershell
# Navegue até onde quer salvar (ex: Documentos)
cd "$env:USERPROFILE\Documents"

# Clone o repositório
git clone https://github.com/weslleyramon001-png/claude-code.git lyvian-vault

# Entre na pasta
cd lyvian-vault
```

> A pasta `lyvian-vault\vault` será o seu vault no Obsidian.

---

## Passo 3 — Abrir o vault no Obsidian

1. Abra o **Obsidian**
2. Clique em **"Abrir pasta como cofre"** (Open folder as vault)
3. Navegue até: `Documentos\lyvian-vault\vault`
4. Clique em **Selecionar pasta**
5. O Obsidian abrirá o cérebro da Lyvian

---

## Passo 4 — Instalar o plugin Obsidian Git

Dentro do Obsidian:

1. `Configurações` (ícone de engrenagem) → `Plugins de comunidade`
2. Clique em **"Ativar plugins de comunidade"**
3. Clique em **"Procurar"**
4. Busque por: `Obsidian Git`
5. Clique em **Instalar** → **Ativar**

---

## Passo 5 — Configurar o Obsidian Git

Ainda em `Configurações` → `Obsidian Git`:

| Configuração | Valor recomendado |
|---|---|
| Auto pull interval (minutes) | `5` |
| Pull updates on startup | ✅ Ativado |
| Auto push | ✅ Ativado |
| Auto push interval (minutes) | `10` |
| Commit message | `vault: atualização automática {{date}}` |
| Pull before push | ✅ Ativado |

---

## Passo 6 — Autenticar com o GitHub

Na primeira vez que o plugin tentar sincronizar, o Windows pedirá login:

1. Uma janela do browser vai abrir
2. Faça login na sua conta GitHub
3. Autorize o acesso
4. Pronto — autenticação salva

---

## Como funciona depois de configurado

```
Lyvian aprende algo novo
  ↓
Salva no vault (commit + push para GitHub)
  ↓
A cada 5 minutos, Obsidian Git faz pull automático
  ↓
Sua nota aparece no Obsidian no seu PC
  ↓
Google Drive (se configurado) sincroniza o arquivo
```

---

## Sincronizar manualmente (qualquer hora)

Dentro do Obsidian, pressione `Ctrl + P` e digite:
- `Obsidian Git: Pull` — busca atualizações agora
- `Obsidian Git: Push` — envia suas notas agora

---

## Relacionamentos

→ [[CEREBRO-LYVIAN]]
→ [[_meta/credenciais]]
