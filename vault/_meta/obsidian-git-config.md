---
tipo: configuracao
titulo: Obsidian Git — Configuração Recomendada
tags: [obsidian, git, configuracao]
---

# Obsidian Git — Configuração Recomendada

> Valores ideais para sincronizar o vault da Lyvian automaticamente.

## Configurações do plugin

```json
{
  "commitMessage": "vault: {{hostname}} - {{date}}",
  "autoCommitMessage": "vault: atualização automática {{date}}",
  "commitDateFormat": "YYYY-MM-DD HH:mm:ss",
  "autoSaveInterval": 0,
  "autoPushInterval": 10,
  "autoPullInterval": 5,
  "autoPullOnBoot": true,
  "disablePush": false,
  "pullBeforePush": true,
  "disablePopups": false,
  "listChangedFilesInMessageBody": false,
  "showStatusBar": true,
  "updateSubmodules": false,
  "syncMethod": "merge",
  "customMessageOnAutoBackup": false,
  "autoBackupAfterFileChange": false,
  "treeStructure": false,
  "refreshSourceControl": true,
  "basePath": "",
  "showedMobileNotice": true,
  "differentiateMainBranchCommits": false,
  "changedFilesInStatusBar": false
}
```

## Como aplicar manualmente

1. No Obsidian, vá em `Configurações` → `Obsidian Git`
2. Configure cada campo conforme a tabela abaixo:

| Campo | Valor |
|---|---|
| Auto pull interval | `5` minutos |
| Auto push interval | `10` minutos |
| Pull on startup | ✅ |
| Pull before push | ✅ |
| Show status bar | ✅ |
| Sync method | `merge` |

## Atalhos úteis

| Atalho | Ação |
|---|---|
| `Ctrl+P` → `Git: Pull` | Buscar atualizações agora |
| `Ctrl+P` → `Git: Push` | Enviar notas agora |
| `Ctrl+P` → `Git: Commit all` | Salvar tudo com mensagem |

→ [[sync]]
→ [[CEREBRO-LYVIAN]]
