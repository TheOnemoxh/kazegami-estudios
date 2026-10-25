# -*- coding: utf-8 -*-
"""
compilar_word.py
================
Une los .md de cada estudio con Pandoc, aplica la plantilla académica y deja listos:

    entregables_word/Taller_1_Estudio_de_Mercado_Kazegami.docx
    entregables_word/Taller_2_Estudio_Tecnico_Kazegami.docx

Después del paso de Pandoc, python-docx:
  * inserta la tabla de contenido después de la portada (se actualiza al abrir en Word),
  * da formato a todas las tablas (bordes, encabezado con color institucional suave,
    filas alternas, fuente 8-9 pt, encabezado repetido en cada página),
  * centra las imágenes y achica las notas de "Fuente".
Al final verifica que cada .docx exista, pese lo esperado y contenga todas las tablas e imágenes.

Uso:
    python scripts/compilar_word.py            # compila los dos
    python scripts/compilar_word.py --pdf      # además exporta PDF con LibreOffice (opcional)
"""
from __future__ import annotations

import glob
import os
import re
import shutil
import subprocess
import sys
import zipfile

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLANTILLA = os.path.join(RAIZ, "assets", "plantillas", "plantilla_unicartagena.docx")
SALIDA = os.path.join(RAIZ, "entregables_word")

DOCUMENTOS = [
    ("01_estudio_mercado", "Taller_1_Estudio_de_Mercado_Kazegami.docx", "Taller No. 1 - Estudio de Mercados - Kazegami Restaurante"),
    ("02_estudio_tecnico", "Taller_2_Estudio_Tecnico_Kazegami.docx", "Taller No. 2 - Estudio Técnico - Kazegami Restaurante"),
]

CABECERA_FONDO = "D6E6F8"   # azul institucional suave
CABECERA_TEXTO = RGBColor(0x1F, 0x3A, 0x68)
BANDA = "F5F7FB"
BORDE = "9FB3CF"


# ---------------------------------------------------------------------------
def pandoc(carpeta: str, salida: str, titulo: str):
    archivos = sorted(glob.glob(os.path.join(RAIZ, carpeta, "*.md")))
    if not archivos:
        raise SystemExit(f"No hay .md en {carpeta}")
    cmd = ["pandoc", *archivos, "-f", "markdown+pipe_tables+raw_attribute+fenced_divs-tex_math_dollars-tex_math_single_backslash",
           "-t", "docx", "--reference-doc", PLANTILLA, "--resource-path", RAIZ,
           "--metadata", f"title-meta={titulo}", "-o", salida]
    subprocess.run(cmd, check=True, cwd=RAIZ)
    return archivos


def _sombrear(celda, color):
    tcPr = celda._tc.get_or_add_tcPr()
    for s in tcPr.findall(qn("w:shd")):
        tcPr.remove(s)
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), color)
    tcPr.append(shd)


def _bordes(tabla):
    tblPr = tabla._tbl.tblPr
    for b in tblPr.findall(qn("w:tblBorders")):
        tblPr.remove(b)
    borders = OxmlElement("w:tblBorders")
    for lado in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{lado}")
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), "4")
        e.set(qn("w:space"), "0")
        e.set(qn("w:color"), BORDE)
        borders.append(e)
    tblPr.append(borders)
    # ancho 100 %
    for w in tblPr.findall(qn("w:tblW")):
        tblPr.remove(w)
    tblW = OxmlElement("w:tblW")
    tblW.set(qn("w:w"), "5000")
    tblW.set(qn("w:type"), "pct")
    tblPr.append(tblW)
    # márgenes de celda
    mar = OxmlElement("w:tblCellMar")
    for lado, v in (("top", "30"), ("bottom", "30"), ("left", "70"), ("right", "70")):
        e = OxmlElement(f"w:{lado}")
        e.set(qn("w:w"), v)
        e.set(qn("w:type"), "dxa")
        mar.append(e)
    tblPr.append(mar)


def formatear_tablas(doc):
    for t in doc.tables:
        ncol = len(t.columns)
        tam = Pt(8) if ncol >= 7 else Pt(8.5) if ncol >= 5 else Pt(9)
        _bordes(t)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        for i, fila in enumerate(t.rows):
            if i == 0:
                trPr = fila._tr.get_or_add_trPr()
                h = OxmlElement("w:tblHeader")
                h.set(qn("w:val"), "true")
                trPr.append(h)
            no_partir = OxmlElement("w:cantSplit")
            fila._tr.get_or_add_trPr().append(no_partir)
            for celda in fila.cells:
                if i == 0:
                    _sombrear(celda, CABECERA_FONDO)
                elif i % 2 == 0:
                    _sombrear(celda, BANDA)
                for p in celda.paragraphs:
                    p.paragraph_format.space_after = Pt(0)
                    p.paragraph_format.space_before = Pt(0)
                    p.paragraph_format.line_spacing = 1.0
                    for r in p.runs:
                        r.font.size = tam
                        if i == 0:
                            r.font.bold = True
                            r.font.color.rgb = CABECERA_TEXTO


def formatear_parrafos(doc):
    for p in doc.paragraphs:
        if p._p.xpath(".//w:drawing"):
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.keep_with_next = True
        texto = p.text.strip()
        if texto.startswith("Fuente:"):
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(8)
            for r in p.runs:
                r.font.size = Pt(8)
                r.font.color.rgb = RGBColor(0x52, 0x51, 0x4E)


def insertar_indice(doc):
    """Inserta 'Contenido' + campo TOC justo después del primer salto de página (fin de la portada)."""
    destino = None
    for p in doc.paragraphs:
        if p._p.xpath('.//w:br[@w:type="page"]'):
            destino = p
            break
    if destino is None:
        return
    titulo = OxmlElement("w:p")
    pPr = OxmlElement("w:pPr")
    ps = OxmlElement("w:pStyle")
    ps.set(qn("w:val"), "TOCHeading")
    pPr.append(ps)
    titulo.append(pPr)
    r = OxmlElement("w:r")
    t = OxmlElement("w:t")
    t.text = "Contenido"
    r.append(t)
    titulo.append(r)

    campo = OxmlElement("w:p")
    for tipo, instr in (("begin", None), (None, 'TOC \\o "1-2" \\h \\z \\u'), ("separate", None), ("text", None), ("end", None)):
        run = OxmlElement("w:r")
        if tipo == "text":
            tt = OxmlElement("w:t")
            tt.text = "Haga clic derecho → Actualizar campo para ver la tabla de contenido."
            run.append(tt)
        elif tipo:
            fc = OxmlElement("w:fldChar")
            fc.set(qn("w:fldCharType"), tipo)
            if tipo == "begin":
                fc.set(qn("w:dirty"), "true")
            run.append(fc)
        else:
            it = OxmlElement("w:instrText")
            it.set(qn("xml:space"), "preserve")
            it.text = instr
            run.append(it)
        campo.append(run)

    salto = OxmlElement("w:p")
    rr = OxmlElement("w:r")
    br = OxmlElement("w:br")
    br.set(qn("w:type"), "page")
    rr.append(br)
    salto.append(rr)

    destino._p.addnext(salto)
    destino._p.addnext(campo)
    destino._p.addnext(titulo)

    # Que Word actualice los campos al abrir
    settings = doc.settings.element
    uf = OxmlElement("w:updateFields")
    uf.set(qn("w:val"), "true")
    settings.append(uf)


def verificar(ruta, archivos_md):
    md = "\n".join(open(a, encoding="utf-8").read() for a in archivos_md)
    tablas_esp = len(re.findall(r"^Table: ", md, flags=re.M))
    imgs_esp = len(re.findall(r"!\[[^\]]*\]\(([^)]+)\)", md))
    doc = Document(ruta)
    with zipfile.ZipFile(ruta) as z:
        imgs = [n for n in z.namelist() if n.startswith("word/media/")]
    peso = os.path.getsize(ruta) / 1024
    tablas = len(doc.tables)
    ok = os.path.exists(ruta) and peso > 100 and tablas >= tablas_esp and len(imgs) >= len(set(re.findall(r"!\[[^\]]*\]\(([^)]+)\)", md)))
    print(f"  · {os.path.basename(ruta)}: {peso:,.0f} KB · tablas {tablas}/{tablas_esp} · imágenes únicas {len(imgs)} (referencias {imgs_esp}) · {'OK' if ok else 'REVISAR'}")
    if "Estudio_Tecnico" in ruta:
        texto = "\n".join(c.text for t in doc.tables for c in t.rows[0].cells)
        p6 = sum(1 for t in doc.tables if "Identificación del elemento" in " ".join(c.text for c in t.rows[0].cells))
        print(f"    tablas con formato Punto 6 (columna 'Identificación del elemento'): {p6}")
        ok = ok and p6 >= 3
    return ok


def main():
    if not shutil.which("pandoc"):
        raise SystemExit("Falta Pandoc: https://pandoc.org/installing.html")
    if not os.path.exists(PLANTILLA):
        subprocess.run([sys.executable, os.path.join(RAIZ, "scripts", "generar_plantilla_word.py")], check=True)
    os.makedirs(SALIDA, exist_ok=True)
    todo_ok = True
    for carpeta, nombre, titulo in DOCUMENTOS:
        ruta = os.path.join(SALIDA, nombre)
        archivos = pandoc(carpeta, ruta, titulo)
        doc = Document(ruta)
        insertar_indice(doc)
        formatear_tablas(doc)
        formatear_parrafos(doc)
        doc.core_properties.title = titulo
        doc.core_properties.author = "Angulo, Molina, Cañas, Vergara, Rodriguez"
        doc.save(ruta)
        print(f"Compilado {nombre} ({len(archivos)} archivos .md)")
        todo_ok &= verificar(ruta, archivos)
        if "--pdf" in sys.argv and shutil.which("soffice"):
            subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", SALIDA, ruta],
                           check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("VERIFICACIÓN:", "TODO OK" if todo_ok else "HAY ALGO QUE REVISAR")


if __name__ == "__main__":
    main()
