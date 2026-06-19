# CLAUDE.md — Contexto do Projeto Weslley Ramon
> Leia este arquivo PRIMEIRO em toda sessão. Ele contém o estado atual de todos os projetos.

---

## QUEM É O USUÁRIO
- **Nome**: Weslley Ramon
- **Email**: weslleyramon001@gmail.com
- **Localização**: Brasil
- **Ferramentas**: Claude Code CLI (Windows, VS Code terminal), Claude Web (claude.ai/code)

---

## PROJETOS ATIVOS

### 1. REDE NEUTRA (planilha Excel)
**Arquivo atual**: `Rede_Neutra_V13_dark.xlsx`
**Status**: Em desenvolvimento — V13 entregue, aguardando aprovação visual

**Operadoras (5 total)**:
| Operadora | CTOs | ONUs | Receita | Inadimp |
|-----------|------|------|---------|---------|
| 🔵 VIRTUAL NET | 3 | 8 | R$ 720,00 | 0% |
| 🟢 INEDITTUS FI | 3 | 8 | R$ 499,50 | 0% |
| 🟡 POPNET | 4 | 8 | R$ 360,00 | 25% |
| 🔴 RSNET | 1 | 3 | R$ 267,00 | 0% |
| 🟣 WORLD CONNEC | 2 | 6 | R$ 449,50 | 20% |

**Tema Power BI (padrão documentado — SEMPRE usar estas cores)**:
- Fundo geral: `#0B1929`
- Cards escuro: `#112236`
- Cards médio: `#162E48`
- Header linha: `#0D2137`
- Borda/accent: `#1E3A5F`
- Texto branco: `#FFFFFF`
- Texto slate: `#94A3B8`
- Verde: `#10B981`
- Amarelo: `#FBBF24`
- Vermelho: `#F87171`
- Azul: `#60A5FA`
- Roxo: `#A78BFA`

**Regras técnicas da planilha**:
- Formulas automáticas: `=COUNTA(B11:B200)` para CTOs, `=SUM(K11:K200)` para ONUs
- Cross-sheet: `='🔵 VIRTUAL NET'!B7` etc.
- Gráficos: TwoCellAnchor (`from openpyxl.drawing.spreadsheet_drawing import TwoCellAnchor, AnchorMarker`)
- Fundo gráficos: XML post-processing via zipfile (sem prefixo `c:` no namespace!)
- Script de build: `/tmp/build_v13.py` (temporário — recriar se necessário)

**Abas da planilha**:
1. `📊 Dashboard` — KPIs gerais + tabela resumo
2. `🔵 VIRTUAL NET` — dados CTO/ONU
3. `🟢 INEDITTUS FI`
4. `🟡 POPNET`
5. `🔴 RSNET`
6. `🟣 WORLD CONNEC`
7. `📊 Gráficos` — 4 gráficos alinhados (2×2), fundo escuro
8. `📈 Relatório` — consolidado automático

**Pendências**:
- [ ] Confirmar se fundo dos gráficos ficou azul escuro (V13 enviada)
- [ ] Validar todas as formulas automáticas
- [ ] Publicar no Kiwify como parte do Pack de Planilhas

---

### 2. PACK DE PLANILHAS (produto Kiwify)
**Status**: ~14 planilhas criadas, todas com tema Power BI dark
**Scripts base**: `D:\Planilhas-Produtos\_dark_base.py` (local no PC do usuário)
**Documentação**: `Pack-Planilhas-Financeiras.md` no Google Drive
**Pendências**:
- [ ] Publicar produto no Kiwify
- [ ] Configurar funil de 7 emails no MailerLite

---

### 3. JARBAS (assistente de IA)
**Status**: Online em produção no Railway
**Stack**: FastAPI + WebSocket + SQLite (backend), Railway (hospedagem)
**Funcionalidades**: Chat, memória, acesso ao Drive/Obsidian
**Plano Railway**: Trial → migrar para pago
**Pendências**:
- [ ] Clonar voz do JARVIS (Iron Man) para o JARBAS
- [ ] Migrar Railway para plano pago

---

### 4. CLAUDE CODE CLI (local)
**Status**: Instalado no Windows (VS Code terminal)
**Login**: Claude Pro — autenticar via `/login` dentro do Claude Code
**Como abrir**: No terminal do VS Code, digitar `claude`
**Importante**: Não colar código de autenticação no chat — só no terminal

---

## REGRAS GERAIS QUE O WESLLEY DEFINIU
1. **Sempre tema Power BI dark** — nunca fundo branco em planilhas
2. **Tudo automático** — formulas dinâmicas, não valores fixos
3. **Gráficos alinhados** — TwoCellAnchor, nunca sobrepostos
4. **Salvar contexto aqui** — atualizar este CLAUDE.md quando houver progresso
5. **Não perguntar o que já foi decidido** — consultar este arquivo primeiro

---

## HISTÓRICO DE VERSÕES (Rede Neutra)
| Versão | O que mudou |
|--------|-------------|
| V9 | Original enviada pelo usuário |
| V10 | Correção de dados (RSNET, Virtual Net, Popnet) |
| V11 | Fórmulas automáticas adicionadas (gráficos sobrepostos) |
| V12 | Gráficos movidos para aba separada, tema dark tentado |
| V13 | Tema dark correto (#0B1929), XML patch nos gráficos, TwoCellAnchor |

---

## COMO ATUALIZAR ESTE ARQUIVO
Após cada sessão produtiva, atualizar:
1. Status dos projetos (o que foi feito)
2. Pendências (o que falta)
3. Versão atual dos arquivos
4. Qualquer decisão nova de design/cor/estrutura

**Último update**: 2026-06-19 — V13 da Rede Neutra entregue com XML dark patch
