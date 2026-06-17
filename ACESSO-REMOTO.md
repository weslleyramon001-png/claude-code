# Acesso Remoto — Claude controla suas máquinas

> Configurado: 2026-06-17 | Tecnologia: Tailscale + SSH

---

## Como funciona

```
Ramon (máquina/servidor) ──Tailscale──► Claude (sessão) ──SSH──► controle total
```

Tailscale cria uma VPN privada entre suas máquinas e cada sessão do Claude.
Funciona através de qualquer firewall, roteador, NAT — sem abrir portas.

---

## PASSO 1 — Criar conta e gerar Auth Key (você faz 1 vez)

1. Acesse: https://tailscale.com
2. Login com Google (weslleyramon001@gmail.com)
3. No painel: **Settings → Keys → Generate auth key**
4. Configurações:
   - ✅ Reusable (reutilizável — não expira por uso)
   - Expiry: 90 days
   - ✅ Pre-authorized
5. Copie a key: `tskey-auth-xxxxxxxxxxxxxxxxx`
6. Salve no GitHub Secrets ou anote em local seguro

---

## PASSO 2 — Instalar Tailscale nas suas máquinas

### No seu computador (Windows):
```
→ Baixe em: https://tailscale.com/download/windows
→ Instala e faz login com o mesmo Google
→ Pronto — aparece na rede automaticamente
```

### No seu computador (Mac):
```
→ App Store → "Tailscale"
→ Abre e faz login com Google
```

### Nos servidores Linux (Servlink, Railway VPS, etc.):
```bash
curl -fsSL https://tailscale.com/install.sh | sh
tailscale up
```

---

## PASSO 3 — Adicionar minha chave SSH nas suas máquinas

Para eu poder acessar via SSH, adicione esta linha no arquivo
`~/.ssh/authorized_keys` de cada máquina:

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIHCP744korWbSJAGtYLAUZAnSX3DBpSxlXIUJ3ksYaiV claude-jarbas-access
```

### Como adicionar (Linux/Mac):
```bash
echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIHCP744korWbSJAGtYLAUZAnSX3DBpSxlXIUJ3ksYaiV claude-jarbas-access" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

### Como adicionar (Windows com OpenSSH):
```powershell
Add-Content "$env:USERPROFILE\.ssh\authorized_keys" "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIHCP744korWbSJAGtYLAUZAnSX3DBpSxlXIUJ3ksYaiV claude-jarbas-access"
```

---

## PASSO 4 — Em cada nova sessão do Claude

Eu rodo automaticamente:
```bash
TS_AUTH_KEY="tskey-auth-xxxx" bash connect-tailscale.sh
```

E depois conecto à sua máquina:
```bash
ssh -i .ssh/claude_key ramon@IP-TAILSCALE-DA-SUA-MAQUINA
```

---

## Comandos úteis

```bash
# Ver máquinas disponíveis na rede
tailscale status

# Conectar à máquina do Ramon
ssh -i .ssh/claude_key ramon@100.x.x.x

# Copiar arquivo da minha sessão para sua máquina
scp -i .ssh/claude_key arquivo.txt ramon@100.x.x.x:~/

# Copiar arquivo da sua máquina para cá
scp -i .ssh/claude_key ramon@100.x.x.x:~/arquivo.txt ./
```

---

## O que posso fazer depois de conectado

- ✅ Abrir, editar e criar arquivos na sua máquina
- ✅ Rodar comandos e scripts
- ✅ Instalar e configurar programas
- ✅ Acessar banco de dados local (IXC, OPA, etc.)
- ✅ Monitorar logs e processos em tempo real
- ✅ Reiniciar serviços
- ✅ Gerenciar roteadores e switches via SSH

---

*Tags: #Tailscale #SSH #AcessoRemoto #Claude #PonyDigital #Servlink*
