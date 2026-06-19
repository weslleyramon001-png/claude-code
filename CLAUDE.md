# CLAUDE.md — Contexto do Projeto Weslley Ramon
> Leia este arquivo PRIMEIRO em toda sessão. Ele contém o estado atual de todos os projetos.

---

## QUEM É O USUÁRIO
- **Nome**: Weslley Ramon
- **Email**: weslleyramon001@gmail.com
- **Localização**: Brasil
- **Ferramentas**: Claude Code CLI (Windows, VS Code terminal), Claude Web (claude.ai/code)
- **SSD Móvel**: 30TB — vault Obsidian em `E:\CEREBRO` (letra pode variar)

---

## PROJETOS ATIVOS

### 1. REDE NEUTRA (planilha Excel)
**Arquivo atual**: `Rede_Neutra_V14_dash.xlsx`
**Status**: V14 entregue — gráficos embutidos no Dashboard, aguardando confirmação visual

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
- Fundo gráficos: XML post-processing via zipfile — detectar namespace: `ns = 'c:' if '<c:chartSpace' in xml else ''`
- `<spPr>` DEVE ser o ÚLTIMO filho de `</plotArea>` — inserir ANTES do fechamento
- Remover `<style val="10"/>` que sobrescreve cores customizadas

**Abas da planilha (V14)**:
1. `📊 Dashboard` — KPIs gerais + tabela resumo + 4 gráficos embutidos (linhas 28-59)
2. `🔵 VIRTUAL NET` — dados CTO/ONU
3. `🟢 INEDITTUS FI`
4. `🟡 POPNET`
5. `🔴 RSNET`
6. `🟣 WORLD CONNEC`
7. `📈 Relatório` — consolidado automático

**Posição dos gráficos no Dashboard (V14)**:
```python
add_bar("CTOs por Operadora",  3, 2,28, 8,43,"60A5FA")   # top-left
add_bar("ONUs por Operadora",  4, 9,28,15,43,"10B981")   # top-right
add_bar("Receita (R$)",        5, 2,44, 8,59,"FBBF24")   # bottom-left
add_pie("Distribuição ONUs %", 4, 9,44,15,59)            # bottom-right
```

**Pendências**:
- [ ] Confirmar fundo dark dos gráficos na V14
- [ ] Validar todas as formulas automáticas
- [ ] Upload Google Drive
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

### 4. CÉREBRO OBSIDIAN (vault SSD 30TB)
**Status**: Script criado, aguardando execução no SSD local
**Script**: `criar_cerebro_ssd.py` — gera vault completo
**Destino**: `E:\CEREBRO` (confirmar letra do SSD antes de rodar)
**O que cria**:
- Pastas organizadas: 001_PROJETOS, 002_CLIENTES, 003_MARKETING, etc.
- Notas `.md` interligadas com `[[wikilinks]]`
- Canvas visual `🗺️ Mapa Neural.canvas` — mapa do cérebro
- Config Obsidian pré-configurada (tema dark, accent `#60A5FA`)
- Graph View com cores por tipo de nó

**Como executar (no Claude Code local do VS Code)**:
```
"cria o vault Obsidian no meu SSD — rode o script criar_cerebro_ssd.py"
```
Ou manualmente:
1. Salvar `criar_cerebro_ssd.py` em qualquer pasta
2. Ajustar `SSD_PATH` para a letra correta do SSD
3. `python criar_cerebro_ssd.py`
4. Abrir Obsidian → Open folder as vault → selecionar `E:\CEREBRO`

**Pendências**:
- [ ] Confirmar letra do SSD (E:, F:, G:?)
- [ ] Executar script no PC local
- [ ] Instalar tema AnuPpuccin no Obsidian
- [ ] Instalar plugin Dataview e Canvas no Obsidian
- [ ] Adicionar mais nós à rede (clientes, automações)

---

### 5. CLAUDE CODE CLI (local)
**Status**: Instalado no Windows (VS Code terminal)
**Login**: Claude Pro — weslleyramon001@gmail.com
**Caminho**: `~\OneDrive\Documentos\GitHub\claude-code`
**Como abrir**: No terminal do VS Code, digitar `claude`
**Vantagem sobre web**: Acesso direto ao SSD e arquivos locais, sem latência
**Importante**: Não colar código de autenticação no chat — só no terminal

---

## REGRAS GERAIS QUE O WESLLEY DEFINIU
1. **Sempre tema Power BI dark** — nunca fundo branco em planilhas
2. **Tudo automático** — formulas dinâmicas, não valores fixos
3. **Gráficos alinhados** — TwoCellAnchor, nunca sobrepostos
4. **Salvar contexto aqui** — atualizar este CLAUDE.md quando houver progresso
5. **Não perguntar o que já foi decidido** — consultar este arquivo primeiro
6. **Usar Claude local (VS Code) para tarefas com arquivos** — evitar web para criação de arquivos locais

---

## HISTÓRICO DE VERSÕES (Rede Neutra)
| Versão | O que mudou |
|--------|-------------|
| V9 | Original enviada pelo usuário |
| V10 | Correção de dados (RSNET, Virtual Net, Popnet) |
| V11 | Fórmulas automáticas adicionadas (gráficos sobrepostos) |
| V12 | Gráficos movidos para aba separada, tema dark tentado |
| V13 | Tema dark correto (#0B1929), XML patch nos gráficos, TwoCellAnchor |
| V14 | Gráficos embutidos no Dashboard (linhas 28-59), sem aba Gráficos separada |

---

## COMO ATUALIZAR ESTE ARQUIVO
Após cada sessão produtiva, atualizar:
1. Status dos projetos (o que foi feito)
2. Pendências (o que falta)
3. Versão atual dos arquivos
4. Qualquer decisão nova de design/cor/estrutura

**Último update**: 2026-06-19 — V14 entregue + Cérebro Obsidian criado (script pronto para SSD)
