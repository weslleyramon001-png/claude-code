"""
Patch correto: c:txPr exige a:bodyPr + a:lstStyle + a:p (obrigatório por CT_TextBody)
"""
import zipfile, io, os
import xml.etree.ElementTree as ET

C_NS = "http://schemas.openxmlformats.org/drawingml/2006/chart"
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
C_ = f"{{{C_NS}}}"; A_ = f"{{{A_NS}}}"

def mk_spPr(fill_hex, ln_hex):
    sp = ET.Element(f"{C_}spPr")
    sf = ET.SubElement(ET.SubElement(sp, f"{A_}solidFill"), f"{A_}srgbClr"); sf.set("val", fill_hex)
    ln = ET.SubElement(sp, f"{A_}ln")
    lf = ET.SubElement(ET.SubElement(ln, f"{A_}solidFill"), f"{A_}srgbClr"); lf.set("val", ln_hex)
    return sp

def mk_txPr(fill_hex, bold=False):
    """CT_TextBody: bodyPr(1) + lstStyle(0..1) + p(1..n) — all required"""
    txPr = ET.Element(f"{C_}txPr")
    # 1. bodyPr — required
    ET.SubElement(txPr, f"{A_}bodyPr")
    # 2. lstStyle — optional but common
    ET.SubElement(txPr, f"{A_}lstStyle")
    # 3. at least one a:p — REQUIRED (CT_TextBody constraint)
    p = ET.SubElement(txPr, f"{A_}p")
    pPr = ET.SubElement(p, f"{A_}pPr")
    defRPr = ET.SubElement(pPr, f"{A_}defRPr")
    if bold: defRPr.set("b", "1")
    sf = ET.SubElement(ET.SubElement(defRPr, f"{A_}solidFill"), f"{A_}srgbClr")
    sf.set("val", fill_hex)
    lat = ET.SubElement(defRPr, f"{A_}latin"); lat.set("typeface", "Calibri")
    return txPr

def insert_before(parent, tag, new_elem):
    for i, child in enumerate(list(parent)):
        if child.tag == tag:
            parent.insert(i, new_elem); return
    parent.append(new_elem)

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

    # 1. chartSpace spPr → append at end (after </chart>)
    tree.append(mk_spPr("0A1628", "10B981"))

    if chart_el is not None:
        pa = chart_el.find(f"{C_}plotArea")
        if pa is not None:
            # 2. plotArea spPr → append at end
            pa.append(mk_spPr("060E1C", "059669"))
            # 3. catAx txPr → before <crossAx>
            for ax in pa.findall(f"{C_}catAx"):
                insert_before(ax, f"{C_}crossAx", mk_txPr("F0F9FF"))
            # 4. valAx txPr → before <crossAx>
            for ax in pa.findall(f"{C_}valAx"):
                insert_before(ax, f"{C_}crossAx", mk_txPr("F0F9FF"))

        # 5. title txPr → append (after </tx>)
        title_el = chart_el.find(f"{C_}title")
        if title_el is not None:
            title_el.append(mk_txPr("10B981", bold=True))

        # 6. legend spPr + txPr → append
        legend = chart_el.find(f"{C_}legend")
        if legend is not None:
            legend.append(mk_spPr("0C1A2E", "10B981"))
            legend.append(mk_txPr("F0F9FF"))

    # 7. dLbls txPr → append
    for dLbls in tree.iter(f"{C_}dLbls"):
        dLbls.append(mk_txPr("F0F9FF"))

    return ET.tostring(tree, encoding="unicode").encode("utf-8")

IN  = "/tmp/Rede_Neutra_V8_raw.xlsx"
OUT = "/tmp/Rede_Neutra_V9.xlsx"

with zipfile.ZipFile(IN,"r") as zin:
    with zipfile.ZipFile(OUT,"w",zipfile.ZIP_DEFLATED) as zout:
        for name in zin.namelist():
            data = zin.read(name)
            if name.startswith("xl/charts/chart") and name.endswith(".xml"):
                try:
                    data = patch_chart_xml(data)
                    print(f"patched {name}")
                except Exception as e:
                    print(f"[warn] {name}: {e}")
            zout.writestr(name, data)

# Print the txPr from chart1 to verify a:p is present
with zipfile.ZipFile(OUT) as z:
    c = z.read("xl/charts/chart1.xml").decode()
    import re
    m = re.search(r'<c:txPr>.*?</c:txPr>', c, re.DOTALL)
    print("\nFirst txPr in chart1:")
    print(m.group() if m else "NOT FOUND")

print(f"\nSize: {os.path.getsize(OUT):,} bytes")
