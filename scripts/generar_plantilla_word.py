# -*- coding: utf-8 -*-
"""
generar_plantilla_word.py
=========================
Crea assets/plantillas/plantilla_unicartagena.docx: la plantilla de estilos (reference-doc)
que Pandoc usa para dar formato académico a los dos estudios.

  * Carta (21,59 × 27,94 cm), márgenes de 2,5 cm
  * Fuente Arial 11, interlineado 1,15, títulos en azul institucional
  * Estilos de portada: Portada, PortadaTitulo, PortadaSub (se usan con ::: {custom-style="..."})
  * Títulos de tabla y figura, pie de página con número de página

Uso: python scripts/generar_plantilla_word.py
"""
from __future__ import annotations

import os
import subprocess

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SALIDA = os.path.join(RAIZ, "assets", "plantillas", "plantilla_unicartagena.docx")

AZUL = RGBColor(0x1F, 0x3A, 0x68)       # azul institucional
AZUL_MEDIO = RGBColor(0x2A, 0x78, 0xD6)
GRIS = RGBColor(0x52, 0x51, 0x4E)
FUENTE = "Arial"


def fijar_fuente(style, nombre=FUENTE, tam=None, negrita=None, cursiva=None, color=None):
    f = style.font
    f.name = nombre
    rpr = style.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for att in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(att), nombre)
    for att in ("w:asciiTheme", "w:hAnsiTheme", "w:cstheme", "w:eastAsiaTheme"):
        if rfonts.get(qn(att)) is not None:
            del rfonts.attrib[qn(att)]
    if tam:
        f.size = Pt(tam)
    if negrita is not None:
        f.bold = negrita
    if cursiva is not None:
        f.italic = cursiva
    if color is not None:
        f.color.rgb = color


def estilo(doc, nombre, tipo=WD_STYLE_TYPE.PARAGRAPH):
    try:
        return doc.styles[nombre]
    except KeyError:
        return doc.styles.add_style(nombre, tipo)


def campo_pagina(parrafo):
    run = parrafo.add_run()
    for tag, txt in (("begin", None), (None, "PAGE"), ("end", None)):
        if tag:
            el = OxmlElement("w:fldChar")
            el.set(qn("w:fldCharType"), tag)
        else:
            el = OxmlElement("w:instrText")
            el.set(qn("xml:space"), "preserve")
            el.text = txt
        run._r.append(el)


def main():
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    base = SALIDA + ".base.docx"
    with open(base, "wb") as f:
        subprocess.run(["pandoc", "--print-default-data-file", "reference.docx"], stdout=f, check=True)
    doc = Document(base)

    # Página
    for s in doc.sections:
        s.page_width, s.page_height = Cm(21.59), Cm(27.94)
        s.top_margin = s.bottom_margin = Cm(2.5)
        s.left_margin = s.right_margin = Cm(2.5)
        s.footer_distance = Cm(1.2)
        s.header_distance = Cm(1.2)
        pie = s.footer.paragraphs[0] if s.footer.paragraphs else s.footer.add_paragraph()
        pie.text = ""
        pie.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r = pie.add_run("Kazegami Restaurante · Seminario Taller Creación de Empresas · Universidad de Cartagena    ")
        r.font.size = Pt(8)
        r.font.color.rgb = GRIS
        campo_pagina(pie)

    # Texto
    for nombre in ("Normal", "Body Text", "First Paragraph", "Compact"):
        st = estilo(doc, nombre)
        fijar_fuente(st, tam=11, color=RGBColor(0x1F, 0x1F, 0x1F))
        pf = st.paragraph_format
        pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
        pf.line_spacing = 1.15
        if nombre != "Compact":
            pf.space_after = Pt(6)
            pf.space_before = Pt(0)
            pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # Títulos
    for nivel, tam, antes in ((1, 16, 18), (2, 13, 14), (3, 11.5, 10)):
        st = estilo(doc, f"Heading {nivel}")
        fijar_fuente(st, tam=tam, negrita=True, color=AZUL if nivel < 3 else AZUL_MEDIO)
        st.paragraph_format.space_before = Pt(antes)
        st.paragraph_format.space_after = Pt(6)
        st.paragraph_format.keep_with_next = True
        if nivel == 1:
            pPr = st.element.get_or_add_pPr()
            bdr = OxmlElement("w:pBdr")
            bot = OxmlElement("w:bottom")
            for k, v in (("w:val", "single"), ("w:sz", "8"), ("w:space", "4"), ("w:color", "2A78D6")):
                bot.set(qn(k), v)
            bdr.append(bot)
            pPr.append(bdr)
    st = estilo(doc, "Title")
    fijar_fuente(st, tam=20, negrita=True, color=AZUL)

    # Leyendas
    st = estilo(doc, "Table Caption")
    fijar_fuente(st, tam=9.5, negrita=True, cursiva=False, color=AZUL)
    st.paragraph_format.space_before = Pt(10)
    st.paragraph_format.space_after = Pt(4)
    st.paragraph_format.keep_with_next = True
    st.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    st = estilo(doc, "Image Caption")
    fijar_fuente(st, tam=9.5, negrita=True, cursiva=False, color=AZUL)
    st.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    st.paragraph_format.space_after = Pt(2)
    st = estilo(doc, "Captioned Figure")
    st.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    st.paragraph_format.keep_with_next = True

    # Portada
    for nombre, tam, neg, col, espacio in (("Portada", 13, True, AZUL, 10), ("PortadaTitulo", 22, True, AZUL, 16),
                                           ("PortadaSub", 11, False, GRIS, 8)):
        st = estilo(doc, nombre)
        st.base_style = doc.styles["Normal"]
        fijar_fuente(st, tam=tam, negrita=neg, color=col)
        st.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
        st.paragraph_format.space_after = Pt(espacio)
        st.paragraph_format.space_before = Pt(0)
    st = estilo(doc, "TOC Heading")
    fijar_fuente(st, tam=16, negrita=True, color=AZUL)

    # Hipervínculos
    try:
        st = doc.styles["Hyperlink"]
        st.font.color.rgb = AZUL_MEDIO
    except KeyError:
        pass

    doc.save(SALIDA)
    os.remove(base)
    print("OK ·", os.path.relpath(SALIDA, RAIZ))


if __name__ == "__main__":
    main()
