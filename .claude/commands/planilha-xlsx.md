# Skill: /planilha-xlsx

Você é especialista em criar planilhas .xlsx profissionais com tema escuro usando openpyxl + XML patch.

## Contexto do Projeto
- Usuário: Weslley Ramon — Pony-Digital / Servlink ISP
- Scripts base: `Script/Rede_Neutra_ONU_Tracker_build.py` e `Script/xlsx_chart_patch.py`
- Paleta obrigatória: dark navy/emeralda (ver abaixo)
- Entrega sempre via `SendUserFile` após gerar em `/tmp/`

## Paleta de Cores (NUNCA alterar sem instrução explícita)
```
BG="060E1C"        # fundo geral
BG_CARD="0C1A2E"   # cards KPI
BG_CARD2="111F36"  # cards alternados
BG_HDR="071525"    # header/seção
EMERALD="10B981"   # cor principal
EM_L="34D399"      # emeralda clara
EM_DIM="052E16"    # emeralda escura (header tabela)
GOLD="F59E0B"      # destaque/receita
RED="F87171"       # alerta/inadimplência
BLUE_L="93C5FD"    # ONUs/conectividade
GRAY="94A3B8"      # texto secundário
WHITE="F0F9FF"     # texto principal tabela
```

## Grid System KPI (4 cards por linha)
```python
CARDS = [(2,5),(7,10),(12,15),(17,20)]  # (col_start, col_end) 1-indexed
# Larguras: [2,12,12,12,12, 2,12,12,12,12, 2,12,12,12,12, 2,12,12,12,12, 2]
# Sempre usar ws.cell(row, col) após merge_cells — NUNCA ws["A1"] em célula mesclada
```

## Regras Críticas de XML Patch (NUNCA violar)
1. Usar `xml.etree.ElementTree` (ET) com `ET.register_namespace("c", C_NS)` — NUNCA string injection
2. `c:txPr` exige `<a:bodyPr> + <a:lstStyle> + <a:p>` (CT_TextBody — `a:p` é OBRIGATÓRIO)
3. `txPr` nos eixos vai ANTES de `<c:crossAx>` via `insert_before()`
4. `spPr` no chartSpace vai DEPOIS de `</c:chart>` via `tree.append()`
5. Sempre re-serializar com ET para preservar prefixo `c:` — sem isso Excel "repara" o arquivo

## mk_txPr() correto
```python
def mk_txPr(fill_hex, bold=False):
    txPr = ET.Element(f"{C_}txPr")
    ET.SubElement(txPr, f"{A_}bodyPr")
    ET.SubElement(txPr, f"{A_}lstStyle")
    p = ET.SubElement(txPr, f"{A_}p")        # OBRIGATÓRIO
    pPr = ET.SubElement(p, f"{A_}pPr")
    defRPr = ET.SubElement(pPr, f"{A_}defRPr")
    if bold: defRPr.set("b", "1")
    sf = ET.SubElement(ET.SubElement(defRPr, f"{A_}solidFill"), f"{A_}srgbClr")
    sf.set("val", fill_hex)
    ET.SubElement(defRPr, f"{A_}latin").set("typeface", "Calibri")
    return txPr
```

## Posições de Inserção XML
- `chartSpace spPr` → `tree.append(mk_spPr(...))` após `</c:chart>`
- `plotArea spPr` → `pa.append(mk_spPr(...))` no final
- `catAx/valAx txPr` → `insert_before(ax, f"{C_}crossAx", mk_txPr(...))`
- `title txPr` → `title_el.append(mk_txPr(...))`
- `legend spPr+txPr` → `legend.append(...)`
- `dLbls txPr` → `dLbls.append(mk_txPr(...))`

## Ao receber uma tarefa de planilha
1. Verificar se existe script base em `Script/` para reutilizar
2. Gerar em `/tmp/arquivo.xlsx`
3. Aplicar patch XML de gráficos se houver gráficos
4. Entregar via `SendUserFile`
5. Commitar script atualizado no repo
