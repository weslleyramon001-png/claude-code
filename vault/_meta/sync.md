# Sync com Google Drive — Configuração

## Opção 1: Pasta do Google Drive (mais simples)

1. Instale o **Google Drive para Desktop**
2. Clone o repositório dentro da pasta do Google Drive:
   ```bash
   cd ~/Google\ Drive/Meu\ Drive/
   git clone https://github.com/weslleyramon001-png/claude-code.git ixc-vault
   ```
3. Abra o Obsidian e aponte para `ixc-vault/vault/` como vault
4. O Google Drive sincroniza automaticamente qualquer mudança

## Opção 2: rclone (avançado, qualquer OS)

```bash
# Instalar rclone
curl https://rclone.org/install.sh | sudo bash

# Configurar Google Drive
rclone config

# Sincronizar vault para o Drive
rclone sync /home/user/claude-code/vault gdrive:IXC-Vault

# Automatizar com cron (a cada 30 min)
*/30 * * * * rclone sync /home/user/claude-code/vault gdrive:IXC-Vault
```

## Opção 3: GitHub como nuvem (já funciona)

O vault já está no repositório git. Para manter sincronizado:

```bash
# Puxar atualizações feitas pelo Claude
git pull origin main

# Ver o que mudou
git log --oneline -10
```

## Obsidian: apontar para o vault

1. Abra o Obsidian
2. **Abrir pasta como vault**
3. Selecione: `caminho/para/claude-code/vault`
4. Pronto — todas as notas aparecem organizadas

## Plugins Obsidian recomendados

- **Dataview** — consultas dinâmicas nas notas
- **Git** — visualizar histórico de mudanças
- **Calendar** — visualizar notas por data
- **Kanban** — acompanhar pendências dos módulos
