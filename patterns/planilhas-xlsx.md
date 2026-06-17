# Padrões: Planilhas .xlsx com openpyxl

## Erros que JÁ ACONTECERAM — nunca repetir

### ❌ ERRO 1: String injection no XML de gráficos
**Sintoma:** Excel abre com "PASTA DE TRABALHO REPARADA", gráficos somem
**Causa:** Injeção de XML via string mantém `xmlns="..."` (default namespace) — Excel exige `c:` prefix
**Solução:** SEMPRE usar `xml.etree.ElementTree` com `ET.register_namespace("c", C_NS)` + `ET.fromstring()` + `ET.tostring()`

### ❌ ERRO 2: `<c:txPr>` sem `<a:p>` filho
**Sintoma:** Mesmo erro — PASTA REPARADA
**Causa:** `CT_TextBody` no schema OOXML exige `bodyPr(1) + lstStyle(0..1) + p(1..n)` — o `<a:p>` é OBRIGATÓRIO
**Solução:** Sempre incluir a estrutura completa (ver mk_txPr abaixo)

### ❌ ERRO 3: `<c:txPr>` depois de `<c:crossAx>` nos eixos
**Sintoma:** PASTA REPARADA
**Causa:** Schema OOXML para catAx/valAx: `txPr` deve vir ANTES de `crossAx`
**Solução:** `insert_before(ax, f"{C_}crossAx", mk_txPr(...))`

### ❌ ERRO 4: `ws["A1"].value = x` em célula mesclada
**Sintoma:** `AttributeError: 'MergedCell' object attribute 'value' is read-only`
**Causa:** Após `merge_cells()`, só a célula top-left é editável mas pelo método `.cell()`
**Solução:** SEMPRE `ws.cell(row=r, column=c).value = x` após qualquer merge

### ❌ ERRO 5: `DataLabel` em vez de `DataLabelList`
**Sintoma:** `TypeError: PieChart.dLbls should be DataLabelList not DataLabel`
**Solução:** `from openpyxl.chart.label import DataLabelList; dl = DataLabelList(); dl.showPercent = True; ch.dLbls = dl`

---

## Código correto — copiar sempre

### mk_txPr() — estrutura válida
```python
C_NS = "http://schemas.openxmlformats.org/drawingml/2006/chart"
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
C_ = f"{{{C_NS}}}"; A_ = f"{{{A_NS}}}"

def mk_txPr(fill_hex, bold=False):
    txPr = ET.Element(f"{C_}txPr")
    ET.SubElement(txPr, f"{A_}bodyPr")           # obrigatório
    ET.SubElement(txPr, f"{A_}lstStyle")
    p = ET.SubElement(txPr, f"{A_}p")            # OBRIGATÓRIO — sem isso Excel repara
    pPr = ET.SubElement(p, f"{A_}pPr")
    defRPr = ET.SubElement(pPr, f"{A_}defRPr")
    if bold: defRPr.set("b", "1")
    sf = ET.SubElement(ET.SubElement(defRPr, f"{A_}solidFill"), f"{A_}srgbClr")
    sf.set("val", fill_hex)
    ET.SubElement(defRPr, f"{A_}latin").set("typeface", "Calibri")
    return txPr
```

### patch_chart_xml() — função completa e testada
```python
def patch_chart_xml(data: bytes) -> bytes:
    ns_map = {}
    for event, elem in ET.iterparse(io.BytesIO(data), events=["start-ns"]):
        ns_map[elem[0]] = elem[1]
    for prefix, uri in ns_map.items():
        try: ET.register_namespace(prefix, uri)
        except: pass
    ET.register_namespace("c", C_NS); ET.register_namespace("a", A_NS)
    
    tree = ET.fromstring(data)
    chart_el = tree.find(f"{C_}chart")

    tree.append(mk_spPr("0A1628", "10B981"))           # chartSpace bg — APÓS </chart>

    if chart_el is not None:
        pa = chart_el.find(f"{C_}plotArea")
        if pa is not None:
            pa.append(mk_spPr("060E1C", "059669"))     # plotArea bg — no final
            for ax in pa.findall(f"{C_}catAx"):
                insert_before(ax, f"{C_}crossAx", mk_txPr("F0F9FF"))  # ANTES crossAx
            for ax in pa.findall(f"{C_}valAx"):
                insert_before(ax, f"{C_}crossAx", mk_txPr("F0F9FF"))

        title_el = chart_el.find(f"{C_}title")
        if title_el is not None:
            title_el.append(mk_txPr("10B981", bold=True))

        legend = chart_el.find(f"{C_}legend")
        if legend is not None:
            legend.append(mk_spPr("0C1A2E", "10B981"))
            legend.append(mk_txPr("F0F9FF"))

    for dLbls in tree.iter(f"{C_}dLbls"):
        dLbls.append(mk_txPr("F0F9FF"))

    return ET.tostring(tree, encoding="unicode").encode("utf-8")
```

### insert_before() helper
```python
def insert_before(parent, tag, new_elem):
    for i, child in enumerate(list(parent)):
        if child.tag == tag:
            parent.insert(i, new_elem); return
    parent.append(new_elem)
```

---

## Grid System KPI (padrão visual testado)

```python
CARDS = [(2,5),(7,10),(12,15),(17,20)]  # 4 cards, 4 cols cada, gap de 2
# Col widths: [2,12,12,12,12, 2,12,12,12,12, 2,12,12,12,12, 2,12,12,12,12, 2]
# Total: 21 colunas visíveis

def kpi_card(ws, ci, rl, rv, label, value, bg=BG_CARD, lc=GRAY, vc=EMERALD, vs=28, ac=EMERALD):
    cs, ce = CARDS[ci]
    ws.merge_cells(f"{L(cs)}{rl}:{L(ce)}{rl}")
    c = ws.cell(row=rl, column=cs)   # .cell() — nunca ws["A1"] após merge
    c.value = label; c.font = fn(lc,9,True); c.fill = F(bg); c.alignment = CA
    c.border = Bdr(left=(ac,"medium"), right=(ac,"medium"), top=(ac,"medium"))
    ws.merge_cells(f"{L(cs)}{rv}:{L(ce)}{rv}")
    c = ws.cell(row=rv, column=cs)
    c.value = value; c.font = Font(name="Calibri", size=vs, bold=True, color=vc)
    c.fill = F(bg); c.alignment = CA
    c.border = Bdr(left=(ac,"medium"), right=(ac,"medium"), bottom=(ac,"medium"))
```

---

## Paleta oficial (dark navy/emeralda)
```
BG="060E1C"  BG_CARD="0C1A2E"  BG_CARD2="111F36"  BG_HDR="071525"
EMERALD="10B981"  EM_L="34D399"  EM_DIM="052E16"
GOLD="F59E0B"  RED="F87171"  BLUE_L="93C5FD"  GRAY="94A3B8"  WHITE="F0F9FF"
chartSpace fill="0A1628"  plotArea fill="060E1C"  legend fill="0C1A2E"
```
