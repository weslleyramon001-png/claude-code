# CLAUDE.md — Contexto Permanente: Projeto Pony-Digital

> Este arquivo é carregado automaticamente em toda sessão do Claude Code.
> Última atualização: 2026-06-16 (atualizado 19:34)

---

## 👤 Identidade do Usuário

- **Nome:** Weslley Ramon
- **Email:** weslleyramon001@gmail.com
- **Projeto principal:** Pony-Digital (empreendedorismo digital com IA)

---

## 🧠 O que é o Pony-Digital

"Segundo cérebro" dedicado a vendas digitais, empreendedorismo, mindset e aplicação de tecnologia/IA aos negócios.

**Pilares:** Empreendedorismo Digital + Mindset/Disciplina + Tecnologia/IA

O vault do Obsidian está organizado no Google Drive em:
`Meu Drive > Cérebro Pony-Digital`

---

## 📁 Estrutura do Vault (Obsidian)

```
01-Identidade-Marca/       → posicionamento, bio, persona, branding
02-Produtos-e-Afiliacoes/  → Hotmart, Kiwify, Monetizze, Braip
03-Funil-Vendas/           → landing, email, recuperação, pós-venda
04-Conteudo-Instagram/     → calendário, templates, hashtags
05-Mindset-Disciplina/     → hábitos, foco, mente de riqueza
06-Tecnologia-IA/          → ferramentas, automação, IA no negócio
07-Metricas-e-Resultados/  → KPIs, receita, aprendizados
08-Aprendizados-Diarios/   → daily notes
09-Templates/              → modelos de notas reutilizáveis
Produtos-Digitais/Planilhas/ → planilhas .xlsx prontas para venda
```

---

## 📦 Produto Digital em Andamento: Pack de Planilhas

**Status:** Planilhas criadas e documentadas no Drive (15/06/2026)

| # | Arquivo | Categoria | Preço sugerido |
|---|---------|-----------|----------------|
| 01 | Controle de Hábitos | Produtividade | R$ 47 |
| 02 | Planner Semanal | Produtividade | R$ 47 |
| 03 | Reserva de Emergência | Financeiro | R$ 47 |
| 04 | Controle de Gastos | Financeiro | R$ 47 |
| 05 | Orçamento Mensal | Financeiro | R$ 57 |
| 06 | Simulador de Juros | Financeiro | R$ 57 |
| 07 | Controle de Metas | Produtividade | R$ 57 |
| 08 | Precificação | Negócios | R$ 67 |
| 10 | Fluxo de Caixa | Financeiro | R$ 67 |
| 11 | DRE Simplificado | Financeiro | R$ 77 |
| 12 | Carteira de Ações | Investimentos | R$ 77 |
| 13 | Controle de Estoque | Negócios | R$ 77 |
| 16 | ISP Gestão Pro | Negócios | R$ 97 |

**Localização no Drive:** `Cérebro Pony-Digital > Produtos-Digitais > Planilhas`
**Notas Obsidian:** `02-Produtos-e-Afiliacoes/Planilhas/` (arquivos .md individuais)

---

## ✅ Demandas Concluídas

- [x] Estrutura do vault Obsidian criada (30/05/2026)
- [x] MOC Principal (`00-MOC-Principal.md`) criado
- [x] Identidade, Posicionamento, Bio, Persona, Storytelling definidos
- [x] Calendário editorial (30 dias Instagram) criado
- [x] Stack de ferramentas (grátis → pago → escala) definido
- [x] 13 planilhas .xlsx criadas e enviadas ao Drive (15/06/2026)
- [x] Notas .md documentando cada planilha criadas no Obsidian (15/06/2026)
- [x] CLAUDE.md criado e commitado no GitHub (16/06/2026)
- [x] Rede_Neutra_ONU_Tracker.xlsx (V9) finalizado — dark theme + gráficos com fundo escuro + textos brancos (16/06/2026)

---

## 🔄 Demandas em Andamento / Próximos Passos

- [ ] Listar produtos REAIS para promover em cada plataforma (Hotmart, Kiwify, Monetizze, Braip)
- [ ] Criar banco de Hooks Virais para Instagram
- [ ] Criar Templates de Reels e Carrossel (com referências visuais)
- [ ] Preencher Métricas com números reais conforme aparecem
- [ ] Configurar funil de vendas (landing page + sequência de 7 emails)
- [ ] Publicar pack de planilhas em alguma plataforma

---

## 🛠️ Ferramentas e Integrações Conectadas

- **Google Drive** — vault principal do Obsidian + planilhas
- **Google Calendar** — agenda e planejamento
- **Gmail** — comunicações
- **Slack** — comunicação e histórico de demandas
- **Canva** — criação de conteúdo visual
- **GitHub** (`weslleyramon001-png/claude-code`) — repositório de trabalho
- **Obsidian** — segundo cérebro / sistema de notas

---

## 🧭 Como Retomar uma Sessão

Ao iniciar uma nova sessão, o Claude deve:

1. Ler este arquivo (`CLAUDE.md`) — feito automaticamente
2. Verificar arquivos recentes no Drive se houver dúvida sobre progresso
3. Perguntar ao Weslley se há novas prioridades antes de continuar

---

## ⚠️ Regras Importantes

- Sempre commitar e fazer push de qualquer arquivo criado para o GitHub
- Sempre salvar cópias importantes no Google Drive também
- Nunca deixar trabalho apenas no container local da sessão
- Atualizar este CLAUDE.md sempre que uma demanda for concluída ou iniciada

---

## 🧪 Conhecimento Técnico Acumulado — Planilhas xlsx com Gráficos

### Projeto: Rede_Neutra_ONU_Tracker (openpyxl + XML patch)
**Scripts:** `Script/Rede_Neutra_ONU_Tracker_build.py` e `Script/xlsx_chart_patch.py`

#### Regras para patch de XML de gráficos em arquivos .xlsx

O xlsx é um zip. Os gráficos ficam em `xl/charts/chart*.xml`. Para colorir fundo e texto
dos gráficos sem suporte nativo do openpyxl, é necessário pós-processar o XML via `zipfile`.

**NUNCA usar `xml.etree.ElementTree` com string-based injection.** O formato final
deve usar `c:` prefix (`xmlns:c="..."`), não default namespace (`xmlns="..."`).
Usar `ET.register_namespace("c", C_NS)` + `ET.fromstring()` + `ET.tostring()` garante isso.

**Erros fatais que causam "PASTA DE TRABALHO REPARADA" no Excel:**

| Erro | Causa | Correção |
|------|-------|----------|
| String patch sem namespace `c:` | Excel exige `c:` prefix em chart XML | Usar ET (re-serializa com `c:`) |
| `<c:txPr>` sem `<a:p>` filho | `CT_TextBody` exige `bodyPr + lstStyle + p(1..n)` | Sempre incluir `<a:p><a:pPr>...</a:pPr></a:p>` |
| `<c:txPr>` fora de ordem em `catAx`/`valAx` | Schema OOXML: `txPr` deve vir **antes** de `<c:crossAx>` | `insert_before(ax, f"{C_}crossAx", mk_txPr(...))` |
| `<c:txPr>` antes de `<c:tx>` em `title` | Schema: `tx → spPr → txPr` | `title_el.append(mk_txPr(...))` |

**Estrutura correta de `mk_txPr()`:**
```python
def mk_txPr(fill_hex, bold=False):
    txPr = ET.Element(f"{C_}txPr")
    ET.SubElement(txPr, f"{A_}bodyPr")           # obrigatório
    ET.SubElement(txPr, f"{A_}lstStyle")          # opcional mas recomendado
    p = ET.SubElement(txPr, f"{A_}p")            # OBRIGATÓRIO (CT_TextBody)
    pPr = ET.SubElement(p, f"{A_}pPr")
    defRPr = ET.SubElement(pPr, f"{A_}defRPr")
    if bold: defRPr.set("b", "1")
    sf = ET.SubElement(ET.SubElement(defRPr, f"{A_}solidFill"), f"{A_}srgbClr")
    sf.set("val", fill_hex)
    ET.SubElement(defRPr, f"{A_}latin").set("typeface", "Calibri")
    return txPr
```

**Posições corretas de inserção (via ET API):**
- `chartSpace spPr` → `tree.append(mk_spPr(...))` — depois de `</chart>`
- `plotArea spPr` → `pa.append(mk_spPr(...))` — no final de plotArea
- `catAx/valAx txPr` → `insert_before(ax, f"{C_}crossAx", mk_txPr(...))` — antes de crossAx
- `title txPr` → `title_el.append(mk_txPr(...))` — depois de `</tx>`
- `legend spPr+txPr` → `legend.append(...)` — no final
- `dLbls txPr` → `dLbls.append(mk_txPr(...))` — no final

**Paleta de cores usada (dark navy/emeralda):**
```
BG="060E1C"  BG_CARD="0C1A2E"  BG_HDR="071525"
EMERALD="10B981"  GOLD="F59E0B"  RED="F87171"  BLUE_L="93C5FD"
chartSpace fill="0A1628"  plotArea fill="060E1C"  legend fill="0C1A2E"
```
