# -*- coding: utf-8 -*-
"""
analizar_encuesta.py
====================
Procesa el 100 % de la encuesta (106 respuestas × 31 columnas) y genera:

  * datos/RESUMEN_ENCUESTA.md      → tablas de frecuencia, porcentajes y cruces
  * datos/MODELO_PROYECCIONES.md   → demanda, oferta, balance, capacidad y costos (desde modelo_kazegami.py)
  * assets/graficas/*.png          → gráficas a 300 DPI (encuesta + proyecciones + costos)

Uso (desde la raíz del repositorio):
    python scripts/analizar_encuesta.py
"""
from __future__ import annotations

import os
import sys
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd
import seaborn as sns

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import modelo_kazegami as M  # noqa: E402

RAIZ = M.RAIZ
GRAF = os.path.join(RAIZ, "assets", "graficas")
DATOS = os.path.join(RAIZ, "datos")
os.makedirs(GRAF, exist_ok=True)
os.makedirs(DATOS, exist_ok=True)

# ---------------------------------------------------------------------------
# Estilo visual uniforme
# ---------------------------------------------------------------------------
AZUL = "#2a78d6"       # serie principal
NARANJA = "#eb6834"    # resaltado (Top 3 / Kazegami)
AQUA = "#1baf7a"
AMARILLO = "#eda100"
GRIS = "#b8b6ae"       # "otros" / contexto
TINTA = "#2b2b2b"
TINTA2 = "#52514e"
REJILLA = "#e6e4df"
SECUENCIAL = ["#d6e6f8", "#a9c9ef", "#6fa3e3", "#2a78d6", "#1b4f91"]
PLATO_COLOR = {"Rollos de sushi": AZUL, "Ramen": NARANJA, "Tempura": AQUA}

plt.rcParams.update({
    "font.family": ["Liberation Sans", "DejaVu Sans"],
    "font.size": 10.5,
    "axes.edgecolor": REJILLA,
    "axes.labelcolor": TINTA2,
    "axes.titlesize": 13,
    "axes.titleweight": "bold",
    "axes.titlecolor": TINTA,
    "axes.titlelocation": "left",
    "xtick.color": TINTA2,
    "ytick.color": TINTA2,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": False,
    "figure.dpi": 100,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.facecolor": "white",
    "text.parse_math": False,
})

FUENTE_ENC = "Fuente: Encuesta de mercado Kazegami (n = 106), octubre de 2026. Elaboración propia."
FUENTE_MOD = "Fuente: Elaboración propia con base en la encuesta (n = 106), DANE, Migración Colombia y supuestos del equipo."

GRAFICAS: list[tuple[str, str]] = []  # (archivo, título) para el índice


def guardar(fig, nombre: str, titulo: str, fuente: str = FUENTE_ENC):
    # La fuente se escribe como pie de figura en el documento (Markdown), no dentro de la imagen.
    fig.tight_layout()
    ruta = os.path.join(GRAF, nombre)
    fig.savefig(ruta)
    plt.close(fig)
    GRAFICAS.append((nombre, titulo))


def envolver(t: str, n: int = 32) -> str:
    return "\n".join(textwrap.wrap(str(t), n))


def barras_h(conteos: pd.Series, total: int, titulo: str, nombre: str, resaltar=None,
             subtitulo: str | None = None, ancho=7.5, color=AZUL, ordenar=True, wrap=34):
    s = conteos.sort_values(ascending=True) if ordenar else conteos.iloc[::-1]
    alto = max(2.4, 0.42 * len(s) + 1.2)
    fig, ax = plt.subplots(figsize=(ancho, alto))
    colores = [NARANJA if (resaltar and k in resaltar) else color for k in s.index]
    ax.barh([envolver(k, wrap) for k in s.index], s.values, color=colores, height=0.62)
    mx = s.max()
    for i, v in enumerate(s.values):
        ax.text(v + mx * 0.01, i, f"{int(v)}  ({v / total * 100:.1f} %)", va="center", fontsize=9, color=TINTA)
    ax.set_xlim(0, mx * 1.28)
    ax.xaxis.set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.set_title(titulo, pad=22 if subtitulo else 10)
    if subtitulo:
        ax.text(0, 1.02, subtitulo, transform=ax.transAxes, fontsize=9, color=TINTA2)
    guardar(fig, nombre, titulo)


def barras_v(conteos: pd.Series, total: int, titulo: str, nombre: str, resaltar=None, subtitulo=None,
             ancho=7.5, alto=4.2, wrap=14, color=AZUL):
    fig, ax = plt.subplots(figsize=(ancho, alto))
    colores = [NARANJA if (resaltar and k in resaltar) else color for k in conteos.index]
    x = np.arange(len(conteos))
    ax.bar(x, conteos.values, color=colores, width=0.62)
    for i, v in enumerate(conteos.values):
        ax.text(i, v + conteos.max() * 0.015, f"{int(v)}\n{v / total * 100:.1f} %", ha="center", va="bottom",
                fontsize=9, color=TINTA)
    ax.set_xticks(x, [envolver(k, wrap) for k in conteos.index], fontsize=8.5)
    ax.set_ylim(0, conteos.max() * 1.25)
    ax.yaxis.set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="x", length=0)
    ax.set_title(titulo, pad=22 if subtitulo else 10)
    if subtitulo:
        ax.text(0, 1.02, subtitulo, transform=ax.transAxes, fontsize=9, color=TINTA2)
    guardar(fig, nombre, titulo)


# ---------------------------------------------------------------------------
# Tablas markdown
# ---------------------------------------------------------------------------

def md_tabla(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    lineas = ["| " + " | ".join(str(c) for c in cols) + " |",
              "|" + "|".join([":---" if i == 0 else "---:" for i in range(len(cols))]) + "|"]
    for _, r in df.iterrows():
        lineas.append("| " + " | ".join(str(v) for v in r.values) + " |")
    return "\n".join(lineas)


def tabla_frecuencia(serie: pd.Series, total: int, multiple=False, orden=None) -> pd.DataFrame:
    if multiple:
        vc = M.separar_multiple(serie).value_counts()
    else:
        vc = serie.dropna().astype(str).value_counts()
    if orden:
        vc = vc.reindex([o for o in orden if o in vc.index] + [i for i in vc.index if i not in orden])
    sin = serie.isna().sum()
    df = pd.DataFrame({"Respuesta": vc.index, "Frecuencia absoluta": vc.values,
                       "% sobre 106": [M.num(v / total * 100, 1) + " %" for v in vc.values]})
    if not multiple:
        acum = (vc.cumsum() / total * 100).values
        df["% acumulado"] = [M.num(a, 1) + " %" for a in acum]
    if sin:
        fila = {"Respuesta": "Sin respuesta", "Frecuencia absoluta": sin, "% sobre 106": M.num(sin / total * 100, 1) + " %"}
        if not multiple:
            fila["% acumulado"] = "100,0 %"
        df = pd.concat([df, pd.DataFrame([fila])], ignore_index=True)
    return df


# ---------------------------------------------------------------------------
# PROGRAMA PRINCIPAL
# ---------------------------------------------------------------------------

def main():
    df = M.cargar_encuesta()
    N = len(df)
    C = list(df.columns)
    p = M.parametros_encuesta(df)
    assert N == 106 and len(C) == 31, f"Se esperaban 106×31 y llegaron {N}×{len(C)}"

    ORD_FREQ = ["Más de una vez por semana", "Una vez por semana", "Una o dos veces al mes",
                "Unas pocas veces al año", "Casi nunca", "Nunca lo he probado"]
    ORD_GASTO = ["Menos de $60.000 COP (< $15 USD aprox.)", "$60.000 a $100.000 COP ($15 - $25 USD aprox.)",
                 "$100.000 a $150.000 COP ($25 - $40 USD aprox.)", "$150.000 a $250.000 COP ($40 - $60 USD aprox.)",
                 "Más de $250.000 COP (> $60 USD aprox.)"]
    ORD_LIK = ["Nada importante", "Poco importante", "Normal", "Importante", "Muy importante"]
    ORD_ATR = ["Nada atractivo", "Poco atractivo", "Normal", "Atractivo", "Muy atractivo"]
    ORD_PROB = ["Nada probable", "Poco probable", "Quizás", "Probable", "Muy probable"]
    ORD_EJEC = ["Hasta $20.000 COP (< $5 USD aprox.)", "$20.000 - $30.000 COP ($5 - $10 USD aprox.)",
                "$30.000 - $40.000 COP ($10 - $15 USD aprox.)", "Más de $40.000 (> $15 USD aprox.)", "No me interesa"]
    ORD_EDAD = ["18 - 25 años", "26 - 35 años", "36 - 45 años", "46 - 60 años", "Más de 60 años"]

    def corto(s):
        return (s.replace(" COP", "").replace(" aprox.", "").replace("($15 - $25 USD)", "")
                .replace("($25 - $40 USD)", "").replace("($40 - $60 USD)", "").replace("(< $15 USD)", "")
                .replace("(> $60 USD)", "").strip())

    # ---------------- Gráficas de la encuesta ----------------
    vc = df[C[2]].value_counts()
    barras_h(vc, N, "Aceptación de la comida japonesa y los mariscos", "g01_aceptacion.png",
             resaltar=["Si, consumo comida japonesa o mariscos", "No los he probado, pero estaría dispuesto a probarlos"],
             subtitulo=f"El {p['aceptacion'] * 100:.1f} % consume o está dispuesto a probar")
    vc = df[C[3]].value_counts()
    barras_h(vc, N, "Perfil del encuestado según residencia", "g02_residencia.png")
    vc = df[C[29]].value_counts().reindex(ORD_EDAD).fillna(0)
    barras_v(vc, N, "Rango de edad de los encuestados", "g03_edades.png",
             subtitulo="Muestra concentrada en adultos jóvenes (18 a 25 años)")
    vc = df[C[4]].value_counts().reindex(ORD_FREQ).fillna(0)
    barras_h(vc, N, "Frecuencia de consumo de sushi o ramen", "g04_frecuencia.png", ordenar=False,
             subtitulo=f"Frecuencia promedio ponderada: {p['frecuencia_anual']:.1f} ocasiones por persona al año")
    vc = df[C[5]].value_counts()
    barras_h(vc, N, "Ocasión de consumo más frecuente", "g05_ocasion.png",
             resaltar=["Salida con amigos(as)", "Cena en pareja"])
    platos = p["platos_conteo"]
    barras_h(platos, N, "Platos más frecuentados (selección múltiple)", "g06_platos_top3.png",
             resaltar=M.PLATOS_TOP3,
             subtitulo="En naranja, el Top 3 que define el portafolio técnico de Kazegami")
    vc = df[C[7]].value_counts()
    barras_h(vc, N, "Condiciones médicas o preferencias alimentarias", "g07_restricciones.png")
    vc = df[C[8]].value_counts()
    barras_h(vc, N, "Tipo de restaurante que eligen con más frecuencia", "g08_tipo_restaurante.png",
             resaltar=["Comida japonesa y/o asiática"])
    vc = df[C[9]].value_counts().reindex(ORD_GASTO).dropna()
    vc.index = [corto(i) for i in vc.index]
    barras_v(vc, N, "Gasto por persona en la última salida a comer", "g09_gasto_historico.png")
    zonas = M.separar_multiple(df[C[10]]).value_counts()
    barras_h(zonas, N, "Zonas de Cartagena donde han comido cocina japonesa/asiática", "g10_zonas_consumo.png",
             resaltar=["Centro Histórico", "Manga", "Bocagrande"], subtitulo="Selección múltiple")
    dis = M.separar_multiple(df[C[11]]).value_counts()
    barras_h(dis, N, "Lo que menos gusta de los restaurantes de este tipo en Cartagena", "g11_disgustos.png",
             resaltar=["Precios altos", "Porciones pequeñas"], subtitulo="Selección múltiple: debilidades de la competencia")

    # Atributos (Likert apilada 100 %)
    atr_cols = C[12:20]
    nombres = [c.split("[")[1].rstrip("]") for c in atr_cols]
    tabla_lik = pd.DataFrame({n: df[c].value_counts().reindex(ORD_LIK).fillna(0) for n, c in zip(nombres, atr_cols)}).T
    tabla_lik_pct = tabla_lik.div(tabla_lik.sum(axis=1), axis=0) * 100
    orden_atr = (tabla_lik_pct["Muy importante"] + tabla_lik_pct["Importante"]).sort_values().index
    tabla_lik_pct = tabla_lik_pct.loc[orden_atr]
    fig, ax = plt.subplots(figsize=(8.5, 4.6))
    izq = np.zeros(len(tabla_lik_pct))
    for j, cat in enumerate(ORD_LIK):
        vals = tabla_lik_pct[cat].values
        ax.barh([envolver(i, 30) for i in tabla_lik_pct.index], vals, left=izq, color=SECUENCIAL[j],
                edgecolor="white", linewidth=1.5, label=cat, height=0.66)
        for k, v in enumerate(vals):
            if v >= 7:
                ax.text(izq[k] + v / 2, k, f"{v:.0f} %", ha="center", va="center", fontsize=8,
                        color="white" if j >= 3 else TINTA)
        izq += vals
    ax.set_xlim(0, 100)
    ax.xaxis.set_major_formatter(mtick.PercentFormatter())
    ax.legend(ncol=5, loc="upper left", bbox_to_anchor=(0, 1.13), frameon=False, fontsize=8.5)
    ax.set_title("Importancia de los atributos al elegir restaurante", pad=34)
    ax.tick_params(axis="y", length=0)
    guardar(fig, "g12_importancia_atributos.png", "Importancia de los atributos al elegir restaurante")

    vc = df[C[20]].value_counts().reindex(ORD_ATR).fillna(0)
    barras_v(vc, N, "¿Qué tan atractivo es el concepto Kazegami?", "g13_atractivo_concepto.png",
             resaltar=["Atractivo", "Muy atractivo"],
             subtitulo=f"{p['concepto_atractivo'] * 100:.1f} % lo califica como atractivo o muy atractivo (de quienes respondieron)")
    vc = df[C[21]].value_counts().reindex(ORD_GASTO).dropna()
    vc.index = [corto(i) for i in vc.index]
    barras_v(vc, N, "Disposición de pago por una cena completa en Kazegami", "g14_disposicion_pago.png",
             resaltar=["$60.000 a $100.000"], subtitulo="Rango modal: $60.000 a $100.000 por persona")
    vc = df[C[22]].value_counts().reindex(ORD_EJEC).dropna()
    vc.index = [corto(i).replace("(< $5 USD)", "").replace("($5 - $10 USD)", "").replace("($10 - $15 USD)", "")
                .replace("(> $15 USD)", "").strip() for i in vc.index]
    barras_v(vc, N, "Precio dispuesto a pagar por un menú ejecutivo", "g15_menu_ejecutivo.png",
             resaltar=["$20.000 - $30.000"])
    vc = df[C[23]].value_counts()
    barras_h(vc, N, "Interés en una experiencia Omakase", "g16_omakase_interes.png")
    vc = df[C[24]].value_counts()
    vc.index = [corto(i).replace("(< $25 USD)", "").replace("($25 - $45 USD)", "").replace("($45 - $65 USD)", "").strip()
                for i in vc.index]
    barras_h(vc, N, "Precio por persona para un Omakase de 60-90 minutos", "g17_omakase_precio.png")
    vc = df[C[25]].value_counts()
    barras_h(vc, N, "Zona preferida para ubicar Kazegami", "g18_zona_preferida.png",
             resaltar=["Centro Histórico", "Manga"])
    can = M.separar_multiple(df[C[26]]).value_counts()
    barras_h(can, N, "Dónde buscan recomendaciones de restaurantes", "g19_canales_busqueda.png",
             resaltar=["Instagram o TikTok", "Recomendaciones de amigos y familiares", "Google Maps"],
             subtitulo="Selección múltiple")
    vc = df[C[27]].value_counts()
    barras_h(vc, N, "Medio preferido para reservar una mesa", "g20_reserva.png", resaltar=["Por WhatsApp"])
    vc = df[C[28]].value_counts().reindex(ORD_PROB).fillna(0)
    barras_v(vc, N, "Probabilidad de visitar Kazegami en la zona elegida", "g21_probabilidad_visita.png",
             resaltar=["Probable", "Muy probable"],
             subtitulo=f"{p['prob_visita_alta'] * 100:.1f} % lo visitaría probablemente o muy probablemente")

    # Cruce 1: frecuencia × disposición de pago (mapa de calor)
    ct = pd.crosstab(df[C[4]], df[C[21]]).reindex(index=ORD_FREQ, columns=ORD_GASTO).fillna(0)
    ct.columns = [corto(c) for c in ct.columns]
    fig, ax = plt.subplots(figsize=(8.6, 4.4))
    sns.heatmap(ct, annot=True, fmt=".0f", cmap=sns.light_palette(AZUL, as_cmap=True), cbar=False,
                linewidths=1.5, linecolor="white", ax=ax, annot_kws={"fontsize": 10})
    ax.set_xlabel("Disposición de pago por cena en Kazegami")
    ax.set_ylabel("")
    ax.set_xticklabels([envolver(t.get_text(), 12) for t in ax.get_xticklabels()], rotation=0, fontsize=8.5)
    ax.set_title("Cruce: frecuencia de consumo × disposición de pago")
    guardar(fig, "g22_cruce_frecuencia_pago.png", "Cruce: frecuencia de consumo × disposición de pago")

    # Cruce 2: ocasión × probabilidad de visita (100 %)
    ct2 = pd.crosstab(df[C[5]], df[C[28]]).reindex(columns=ORD_PROB).fillna(0)
    ct2 = ct2.loc[ct2.sum(axis=1).sort_values().index]
    ct2p = ct2.div(ct2.sum(axis=1), axis=0) * 100
    fig, ax = plt.subplots(figsize=(8.5, 3.9))
    izq = np.zeros(len(ct2p))
    pal = ["#e8b4a0", "#f2d0c2", "#d9d7d0", "#6fa3e3", "#1b4f91"]
    for j, cat in enumerate(ORD_PROB):
        v = ct2p[cat].values
        ax.barh([f"{envolver(i, 26)}  (n={int(ct2.loc[i].sum())})" for i in ct2p.index], v, left=izq,
                color=pal[j], edgecolor="white", linewidth=1.5, label=cat, height=0.66)
        for k, x in enumerate(v):
            if x >= 9:
                ax.text(izq[k] + x / 2, k, f"{x:.0f} %", ha="center", va="center", fontsize=8,
                        color="white" if j >= 3 else TINTA)
        izq += v
    ax.set_xlim(0, 100)
    ax.xaxis.set_major_formatter(mtick.PercentFormatter())
    ax.legend(ncol=5, loc="upper left", bbox_to_anchor=(0, 1.15), frameon=False, fontsize=8.5)
    ax.set_title("Cruce: ocasión de consumo × probabilidad de visita", pad=34)
    ax.tick_params(axis="y", length=0)
    guardar(fig, "g23_cruce_ocasion_visita.png", "Cruce: ocasión de consumo × probabilidad de visita")

    # Cruce 3: Top 3 de platos según frecuencia (consumidores frecuentes vs ocasionales)
    grupos = {"Frecuentes (≥ 1-2 veces/mes)": ORD_FREQ[:3], "Ocasionales (pocas veces/año)": [ORD_FREQ[3]],
              "Casi nunca / nunca": ORD_FREQ[4:]}
    filas = []
    for g, vals in grupos.items():
        sub = df[df[C[4]].isin(vals)]
        cnt = M.separar_multiple(sub[C[6]]).value_counts()
        filas.append({"Grupo": g, "n": len(sub), **{pl: cnt.get(pl, 0) / max(len(sub), 1) * 100 for pl in M.PLATOS_TOP3}})
    cruce3 = pd.DataFrame(filas)
    fig, ax = plt.subplots(figsize=(8.2, 4.0))
    x = np.arange(len(cruce3))
    w = 0.26
    for j, pl in enumerate(M.PLATOS_TOP3):
        ax.bar(x + (j - 1) * w, cruce3[pl], width=w - 0.02, color=PLATO_COLOR[pl], label=pl)
        for k, v in enumerate(cruce3[pl]):
            ax.text(x[k] + (j - 1) * w, v + 1, f"{v:.0f} %", ha="center", fontsize=8, color=TINTA)
    ax.set_xticks(x, [f"{g}\n(n={n})" for g, n in zip(cruce3.Grupo, cruce3.n)], fontsize=8.5)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax.set_ylim(0, max(cruce3[M.PLATOS_TOP3].max()) * 1.2)
    ax.legend(frameon=False, ncol=3, loc="upper left", bbox_to_anchor=(0, 1.12), fontsize=9)
    ax.set_title("Cruce: preferencia del Top 3 según frecuencia de consumo", pad=28)
    ax.grid(axis="y", color=REJILLA)
    ax.set_axisbelow(True)
    guardar(fig, "g24_cruce_top3_frecuencia.png", "Cruce: preferencia del Top 3 según frecuencia de consumo")

    # ---------------- Gráficas del modelo ----------------
    hist = M.demanda_historica(p)
    proy = M.proyeccion_demanda(p)
    fig, ax = plt.subplots(figsize=(8.4, 4.4))
    ax.plot(hist["Año"], hist["Total"] / 1000, color=TINTA2, lw=2, marker="o", ms=6, label="Histórico estimado 2024-2026")
    estilos = {"Pesimista": (GRIS, "--"), "Base": (AZUL, "-"), "Optimista": (AQUA, "--")}
    for esc, (col, ls) in estilos.items():
        s = proy[proy.Escenario == esc]
        ax.plot(s["Año"], s["Total"] / 1000, color=col, lw=2.2 if esc == "Base" else 1.8, ls=ls, marker="o", ms=5, label=f"Escenario {esc.lower()}")
        ax.text(2031.12, s["Total"].iloc[-1] / 1000, f"{M.num(s['Total'].iloc[-1] / 1000, 0)} mil", va="center", fontsize=8.5, color=TINTA)
    ax.set_xlim(2023.7, 2031.9)
    ax.set_ylabel("Miles de platos al año")
    ax.grid(axis="y", color=REJILLA)
    ax.legend(frameon=False, fontsize=8.5, loc="upper left")
    ax.set_title("Demanda de los 3 platos en Cartagena: histórico y proyección 2027-2031")
    guardar(fig, "g25_proyeccion_demanda_escenarios.png", "Proyección de la demanda 2027-2031 por escenario", FUENTE_MOD)

    dpp = M.demanda_base_por_plato(p)
    dpp = dpp[dpp.Año >= 2027]
    fig, ax = plt.subplots(figsize=(8.2, 4.4))
    base = np.zeros(len(dpp))
    for pl in M.PLATOS_TOP3:
        v = dpp[pl].values / 1000
        ax.bar(dpp["Año"], v, bottom=base, color=PLATO_COLOR[pl], width=0.62, label=pl, edgecolor="white", linewidth=1.5)
        for k, x in enumerate(v):
            ax.text(dpp["Año"].iloc[k], base[k] + x / 2, f"{x:.0f}", ha="center", va="center", fontsize=8.5, color="white")
        base += v
    for k, t in enumerate(base):
        ax.text(dpp["Año"].iloc[k], t + 10, f"{t:.0f} mil", ha="center", fontsize=9, color=TINTA, fontweight="bold")
    ax.set_ylim(0, base.max() * 1.15)
    ax.set_ylabel("Miles de platos al año")
    ax.legend(frameon=False, ncol=3, loc="upper left", bbox_to_anchor=(0, 1.12))
    ax.set_title("Proyección de la demanda (escenario base) por plato", pad=28)
    guardar(fig, "g26_proyeccion_demanda_platos.png", "Proyección de la demanda por plato 2027-2031", FUENTE_MOD)

    of = M.proyeccion_oferta()
    fig, ax = plt.subplots(figsize=(8.2, 4.2))
    cols = [GRIS] + [AZUL] * 5
    ax.bar(of["Año"], of["Oferta"] / 1000, color=cols, width=0.62)
    for a, o, n in zip(of["Año"], of["Oferta"], of["Oferentes"]):
        ax.text(a, o / 1000 + 8, f"{o / 1000:.0f} mil\n({n:.0f} locales)", ha="center", fontsize=8.5, color=TINTA)
    ax.set_ylim(0, of["Oferta"].max() / 1000 * 1.2)
    ax.set_ylabel("Miles de platos al año")
    ax.set_title("Proyección de la oferta de sushi, ramen y tempura en Cartagena")
    guardar(fig, "g27_proyeccion_oferta.png", "Proyección de la oferta 2027-2031", FUENTE_MOD)

    bal = M.balance(p)
    fig, ax = plt.subplots(figsize=(8.4, 4.5))
    ax.plot(bal["Año"], bal["Demanda Base"] / 1000, color=AZUL, lw=2.4, marker="o", label="Demanda (base)")
    ax.plot(bal["Año"], bal["Oferta"] / 1000, color=TINTA2, lw=2.2, marker="s", label="Oferta")
    ax.fill_between(bal["Año"], bal["Oferta"] / 1000, bal["Demanda Base"] / 1000, color=NARANJA, alpha=0.18,
                    label="Demanda insatisfecha")
    for a, d, o in zip(bal["Año"], bal["Demanda Base"], bal["Oferta"]):
        ax.text(a, (d + o) / 2000, f"{(d - o) / 1000:.0f} mil", ha="center", va="center", fontsize=8.5, color="#a8441b")
    ax.set_ylim(600, bal["Demanda Base"].max() / 1000 * 1.08)
    ax.set_ylabel("Miles de platos al año")
    ax.grid(axis="y", color=REJILLA)
    ax.legend(frameon=False, fontsize=9, loc="upper left")
    ax.set_title("Balance oferta vs. demanda y demanda insatisfecha (2026-2031)")
    guardar(fig, "g28_oferta_vs_demanda.png", "Comparativa oferta vs. demanda", FUENTE_MOD)

    cap = M.capacidad()
    fig, ax = plt.subplots(figsize=(8.2, 4.3))
    x = np.arange(len(cap))
    w = 0.27
    ax.bar(x - w, cap["Platos diseñados"] / 1000, w - 0.02, color=SECUENCIAL[1], label="Capacidad diseñada")
    ax.bar(x, cap["Platos instalados"] / 1000, w - 0.02, color=SECUENCIAL[3], label="Capacidad instalada (80 %)")
    ax.bar(x + w, cap["Platos utilizados"] / 1000, w - 0.02, color=NARANJA, label="Capacidad utilizada")
    for k, (u, pu) in enumerate(zip(cap["Platos utilizados"], cap["% utilización"])):
        ax.text(x[k] + w, u / 1000 + 1, f"{M.num(u / 1000, 1)}\n({pu * 100:.0f} %)", ha="center", fontsize=8, color=TINTA)
    ax.set_xticks(x, cap["Año"].astype(str))
    ax.set_ylabel("Miles de platos al año")
    ax.set_ylim(0, cap["Platos diseñados"].max() / 1000 * 1.22)
    ax.legend(frameon=False, ncol=3, fontsize=8.5, loc="upper left", bbox_to_anchor=(0, 1.12))
    ax.set_title("Capacidad diseñada, instalada y utilizada de Kazegami", pad=28)
    guardar(fig, "g29_capacidad_instalada.png", "Capacidad diseñada, instalada y utilizada", FUENTE_MOD)

    up = M.unidades_por_plato(p)
    fig, ax = plt.subplots(figsize=(8.2, 4.3))
    base = np.zeros(len(up))
    for pl in M.PLATOS_TOP3:
        v = up[pl].values
        ax.bar(up["Año"], v, bottom=base, color=PLATO_COLOR[pl], width=0.62, label=pl, edgecolor="white", linewidth=1.5)
        for k, xx in enumerate(v):
            ax.text(up["Año"].iloc[k], base[k] + xx / 2, M.num(xx), ha="center", va="center", fontsize=8, color="white")
        base += v
    for k, t in enumerate(base):
        ax.text(up["Año"].iloc[k], t + 600, M.num(t), ha="center", fontsize=9, fontweight="bold", color=TINTA)
    ax.set_ylim(0, base.max() * 1.15)
    ax.set_ylabel("Platos servidos al año")
    ax.legend(frameon=False, ncol=3, loc="upper left", bbox_to_anchor=(0, 1.12))
    ax.set_title("Platos que servirá Kazegami por año (capacidad utilizada)", pad=28)
    guardar(fig, "g30_unidades_kazegami.png", "Platos servidos por Kazegami 2027-2031", FUENTE_MOD)

    loc = M.matriz_localizacion()
    tot = {z: loc[f"{z} pond."].sum() for z in M.ZONAS}
    s = pd.Series(tot).sort_values()
    fig, ax = plt.subplots(figsize=(7.6, 3.0))
    ax.barh(s.index, s.values, color=[NARANJA if v == s.max() else AZUL for v in s.values], height=0.6)
    for i, v in enumerate(s.values):
        ax.text(v + 0.05, i, M.num(v, 2), va="center", fontsize=10, color=TINTA)
    ax.set_xlim(0, 10)
    ax.set_xlabel("Calificación ponderada (sobre 10)")
    ax.tick_params(axis="y", length=0)
    ax.set_title("Microlocalización: método de ponderación de factores")
    guardar(fig, "g31_localizacion_ponderacion.png", "Resultado de la microlocalización", FUENTE_MOD)

    rc = M.resumen_costos(p)
    capex = pd.Series({
        "Maquinaria y equipos de cocina, refrigeración y barra": rc["equipos"],
        "Adecuación del local": rc["adecuacion"],
        "Mobiliario": rc["mobiliario"],
        "Inventario inicial de insumos (1 mes)": rc["inventario_inicial"],
        "Tecnología (hardware)": rc["tecnologia_hw"],
        "Software y plataformas (año 1)": rc["software_anual"],
    }).sort_values()
    total = capex.sum()
    fig, ax = plt.subplots(figsize=(8.4, 3.8))
    ax.barh([envolver(i, 34) for i in capex.index], capex.values / 1e6, color=AZUL, height=0.62)
    for i, v in enumerate(capex.values):
        ax.text(v / 1e6 + 2, i, f"{M.cop(v / 1e6, 1)} M  ({v / total * 100:.1f} %)", va="center", fontsize=9, color=TINTA)
    ax.set_xlim(0, capex.max() / 1e6 * 1.45)
    ax.xaxis.set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.set_title(f"Distribución de la inversión técnica (total {M.cop(total / 1e6, 1)} millones)")
    guardar(fig, "g32_distribucion_capex.png", "Distribución de costos técnicos (inversión)", FUENTE_MOD)

    opex = pd.Series({
        "Nómina con prestaciones": rc["nomina_mensual"],
        "Insumos de los 3 platos (2027)": rc["insumos_anual_2027"] / 12,
        **{k: v for k, v in M.OPEX_MENSUAL},
        "Software y plataformas": rc["software_anual"] / 12,
        "Depreciación": rc["dep_mensual"],
    }).sort_values()
    tot_op = opex.sum()
    fig, ax = plt.subplots(figsize=(8.4, 5.2))
    ax.barh([envolver(i, 38) for i in opex.index], opex.values / 1e6, color=[NARANJA if "Insumos" in i else AZUL for i in opex.index], height=0.62)
    for i, v in enumerate(opex.values):
        ax.text(v / 1e6 + 0.4, i, f"{M.cop(v / 1e6, 1)} M ({v / tot_op * 100:.1f} %)", va="center", fontsize=8.5, color=TINTA)
    ax.set_xlim(0, opex.max() / 1e6 * 1.4)
    ax.xaxis.set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.set_title(f"Costos de operación mensuales 2027 (total {M.cop(tot_op / 1e6, 1)} millones)")
    guardar(fig, "g33_distribucion_opex.png", "Distribución de costos de operación mensuales", FUENTE_MOD)

    # Costo unitario vs precio
    filas = []
    for pl in M.PLATOS_TOP3:
        _, r = M.tabla_punto6(p, pl)
        filas.append(dict(Plato=pl, MP=r["mp_unitario"], CIF=r["costo_unitario"] - r["mp_unitario"],
                          Margen=r["precio_sin_imp"] - r["costo_unitario"], Imp=r["precio"] - r["precio_sin_imp"], Precio=r["precio"]))
    cu = pd.DataFrame(filas)
    fig, ax = plt.subplots(figsize=(8.2, 4.3))
    base = np.zeros(len(cu))
    partes = [("MP", "Materia prima directa", SECUENCIAL[4]), ("CIF", "Servicios y depreciación de la línea", SECUENCIAL[2]),
              ("Margen", "Margen de contribución", NARANJA), ("Imp", "Impoconsumo (8 %)", GRIS)]
    for col, lab, colr in partes:
        v = cu[col].values / 1000
        ax.bar(cu["Plato"], v, bottom=base, color=colr, width=0.55, label=lab, edgecolor="white", linewidth=1.5)
        for k, xx in enumerate(v):
            if xx > 1.8:
                ax.text(k, base[k] + xx / 2, f"${xx:.1f} mil", ha="center", va="center", fontsize=8.5,
                        color="white" if col in ("MP", "Margen") else TINTA)
        base += v
    for k, t in enumerate(cu["Precio"]):
        ax.text(k, t / 1000 + 0.8, f"Precio {M.cop(t)}", ha="center", fontsize=9, fontweight="bold", color=TINTA)
    ax.set_ylim(0, cu["Precio"].max() / 1000 * 1.2)
    ax.set_ylabel("Miles de COP por plato")
    ax.legend(frameon=False, ncol=2, fontsize=8.5, loc="upper left", bbox_to_anchor=(0, 1.17))
    ax.set_title("Estructura del precio de venta por plato", pad=38)
    guardar(fig, "g34_estructura_precio.png", "Estructura de costo unitario y precio por plato", FUENTE_MOD)

    ins = M.consolidado_insumos(p)
    fig, ax = plt.subplots(figsize=(8.2, 4.2))
    base = np.zeros(len(ins))
    for pl in M.PLATOS_TOP3:
        v = ins[pl].values / 1e6
        ax.bar(ins["Año"], v, bottom=base, color=PLATO_COLOR[pl], width=0.62, label=pl, edgecolor="white", linewidth=1.5)
        for k, xx in enumerate(v):
            ax.text(ins["Año"].iloc[k], base[k] + xx / 2, f"{xx:.0f}", ha="center", va="center", fontsize=8.5, color="white")
        base += v
    for k, t in enumerate(base):
        ax.text(ins["Año"].iloc[k], t + 8, f"{M.cop(t, 0)} M", ha="center", fontsize=9, fontweight="bold", color=TINTA)
    ax.set_ylim(0, base.max() * 1.15)
    ax.set_ylabel("Millones de COP al año")
    ax.legend(frameon=False, ncol=3, loc="upper left", bbox_to_anchor=(0, 1.12))
    ax.set_title("Costo anual de insumos por plato (precios constantes 2026)", pad=28)
    guardar(fig, "g35_costo_insumos_anual.png", "Costo anual de insumos 2027-2031", FUENTE_MOD)

    # Origen de la materia prima (participación en el costo)
    up27 = M.unidades_por_plato(p).set_index("Año").loc[2027]
    org = {}
    for pl in M.PLATOS_TOP3:
        for i in M.RECETAS[pl]:
            org[i.origen] = org.get(i.origen, 0) + i.cantidad * i.precio * up27[pl]
    org = pd.Series(org).sort_values()
    etq = {"Caribe": "Pesca artesanal del Caribe", "Bolívar": "Agro y proteínas de Bolívar",
           "Importado": "Insumos japoneses importados", "Nacional": "Otros insumos nacionales"}
    fig, ax = plt.subplots(figsize=(7.8, 2.9))
    ax.barh([etq[i] for i in org.index], org.values / org.sum() * 100,
            color=[AQUA if i in ("Caribe", "Bolívar") else GRIS if i == "Nacional" else AZUL for i in org.index], height=0.6)
    for i, v in enumerate(org.values):
        ax.text(v / org.sum() * 100 + 0.8, i, f"{v / org.sum() * 100:.1f} %", va="center", fontsize=9.5, color=TINTA)
    ax.set_xlim(0, 60)
    ax.xaxis.set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    loc_share = (org.get("Caribe", 0) + org.get("Bolívar", 0)) / org.sum() * 100
    ax.set_title(f"Origen de la materia prima: {loc_share:.0f} % del costo es local (Caribe + Bolívar)")
    guardar(fig, "g36_origen_insumos.png", "Origen de la materia prima de los 3 platos", FUENTE_MOD)

    # ---------------- RESUMEN_ENCUESTA.md ----------------
    out = ["# RESUMEN ESTADÍSTICO DE LA ENCUESTA — KAZEGAMI RESTAURANTE", "",
           "> Archivo generado automáticamente por `scripts/analizar_encuesta.py`. **No editar a mano**: si cambia el Excel, vuelve a correr el script.",
           "",
           f"- **Instrumento:** Encuesta de mercado – Restaurante Kazegami (Cartagena), Google Forms.",
           f"- **Respuestas válidas:** {N} (todas aceptaron participar). **Columnas:** {len(C)}.",
           f"- **Periodo de recolección:** {pd.to_datetime(df[C[0]]).min():%d/%m/%Y %H:%M} a {pd.to_datetime(df[C[0]]).max():%d/%m/%Y %H:%M}.",
           "- **Muestreo:** no probabilístico por conveniencia (difusión digital). Los porcentajes se calculan sobre 106 salvo que se indique.",
           "- **Preguntas de selección múltiple:** la suma de menciones supera 106; el % indica la proporción de encuestados que eligió la opción.",
           "",
           "## Indicadores clave", "",
           md_tabla(pd.DataFrame([
               ["Aceptación (consume o probaría comida japonesa/mariscos)", M.pct(p["aceptacion"])],
               ["Concepto atractivo o muy atractivo (n = 105)", M.pct(p["concepto_atractivo"])],
               ["Visitaría probablemente o muy probablemente (n = 104)", M.pct(p["prob_visita_alta"])],
               ["Disposición de pago ≥ $60.000 por cena (n = 104)", M.pct(p["wtp_60k_mas"])],
               ["Frecuencia promedio ponderada (ocasiones/persona/año)", M.num(p["frecuencia_anual"], 2)],
               ["Menciones de platos (sin 'Aún no sé')", str(p["menciones_platos"])],
               ["Menciones del Top 3 (sushi + ramen + tempura)", f"{p['menciones_top3']} ({M.pct(p['share_top3'])})"],
               ["Mezcla del Top 3: Rollos de sushi / Ramen / Tempura",
                " / ".join(M.pct(p["mix"][k]) for k in M.PLATOS_TOP3)],
           ], columns=["Indicador", "Valor"])), "",
           "### Top 3 de platos (regla de negocio del proyecto)", "",
           md_tabla(pd.DataFrame([[i + 1, pl, int(p["platos_conteo"][pl]), M.num(p["platos_conteo"][pl] / N * 100, 1) + " %",
                                   M.pct(p["mix"][pl])] for i, pl in enumerate(M.PLATOS_TOP3)],
                                 columns=["Puesto", "Plato", "Menciones", "% de encuestados", "Peso dentro del Top 3"])), "",
           "> Ponderación de frecuencia usada: más de una vez por semana = 78/año; una vez por semana = 52; una o dos veces al mes = 18; unas pocas veces al año = 4; casi nunca = 1; nunca = 0.",
           "", "## Tablas de frecuencia por pregunta", ""]
    multiples = {6, 10, 11, 26}
    ordenes = {4: ORD_FREQ, 9: ORD_GASTO, 21: ORD_GASTO, 22: ORD_EJEC, 20: ORD_ATR, 28: ORD_PROB, 29: ORD_EDAD}
    for i, col in enumerate(C):
        if i == 0:
            continue
        titulo = col.strip()
        out.append(f"### P{i}. {titulo}")
        out.append("")
        if i == 30:
            abiertas = df[col].dropna().astype(str)
            out.append(f"Pregunta abierta opcional: {len(abiertas)} respuestas de 106. Respuestas textuales:")
            out.append("")
            for a in abiertas:
                out.append(f"- {a.strip()}")
            out.append("")
            continue
        if 12 <= i <= 19:
            orden = ORD_LIK[::-1]
        else:
            orden = ordenes.get(i)
        t = tabla_frecuencia(df[col], N, multiple=i in multiples, orden=orden)
        out.append(md_tabla(t))
        out.append("")
    out += ["## Matriz de importancia de atributos (%)", "",
            md_tabla(tabla_lik.loc[orden_atr[::-1]].astype(int).reset_index().rename(columns={"index": "Atributo"})), "",
            "## Cruces de variables", "",
            "### Cruce 1. Frecuencia de consumo × disposición de pago por cena", "",
            md_tabla(ct.astype(int).reset_index().rename(columns={C[4]: "Frecuencia"})), "",
            "### Cruce 2. Ocasión de consumo × probabilidad de visita", "",
            md_tabla(ct2.astype(int).reset_index().rename(columns={C[5]: "Ocasión"})), "",
            "### Cruce 3. % que menciona cada plato del Top 3 según frecuencia de consumo", "",
            md_tabla(cruce3.assign(**{pl: cruce3[pl].map(lambda v: M.num(v, 1) + " %") for pl in M.PLATOS_TOP3})), "",
            "### Cruce 4. Zona preferida para Kazegami × rango de edad", "",
            md_tabla(pd.crosstab(df[C[25]], df[C[29]]).reset_index().rename(columns={C[25]: "Zona preferida"})), "",
            "## Índice de gráficas generadas", "",
            md_tabla(pd.DataFrame([(f"`assets/graficas/{a}`", t) for a, t in GRAFICAS], columns=["Archivo", "Contenido"])), ""]
    with open(os.path.join(DATOS, "RESUMEN_ENCUESTA.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(out))

    # ---------------- MODELO_PROYECCIONES.md ----------------
    d0 = M.demanda_actual(p)
    mo = ["# MODELO DE PROYECCIONES Y COSTOS — KAZEGAMI", "",
          "> Generado por `scripts/analizar_encuesta.py` a partir de `scripts/modelo_kazegami.py` (fuente única de verdad numérica).", "",
          "## Demanda actual 2026 (embudo)", "",
          md_tabla(pd.DataFrame([
              ["Población de Cartagena 2026 (DANE)", M.num(d0["poblacion"])],
              ["Adultos de 18 años y más (72 %)", M.num(d0["adultos"])],
              ["Con capacidad de pago, estratos 3 a 6 (30 %)", M.num(d0["cap_pago"])],
              [f"Dispuestos a pagar ≥ $60.000 por cena ({M.pct(p['wtp_60k_mas'])})", M.num(d0["con_wtp"])],
              [f"Ocasiones de consumo al año (× {M.num(p['frecuencia_anual'], 2)})", M.num(d0["ocasiones"])],
              [f"Platos del Top 3 consumidos por residentes (× {M.pct(p['share_top3'])})", M.num(d0["platos_res"])],
              ["Turistas extranjeros 2026 (proyectado +1,22 %)", M.num(d0["turistas"])],
              ["Turistas que consumen cocina japonesa (10 %)", M.num(d0["tur_jap"])],
              ["Platos del Top 3 consumidos por turistas", M.num(d0["platos_tur"])],
              ["**Demanda actual total 2026 (platos/año)**", f"**{M.num(d0['total'])}**"],
          ], columns=["Paso", "Valor"])), "",
          "## Proyección de la demanda por escenario", "",
          md_tabla(proy.pivot(index="Año", columns="Escenario", values="Total")[list(M.ESCENARIOS)].round(0).astype(int)
                   .map(M.num).reset_index()), "",
          "## Demanda base por plato", "",
          md_tabla(M.demanda_base_por_plato(p).round(0).astype(int).map(M.num).assign(Año=lambda d: d["Año"].str.replace(".", "", regex=False))), "",
          "## Oferta y balance", "",
          md_tabla(bal[["Año", "Oferta", "Demanda Base", "DI Base", "Kazegami"]].fillna(0).round(0).astype(int)
                   .map(M.num).assign(Año=lambda d: d["Año"].str.replace(".", "", regex=False))), "",
          "## Capacidad", "",
          md_tabla(cap.round(2)), "",
          "## Costos resumen", "",
          md_tabla(pd.DataFrame([(k, M.cop(v)) for k, v in rc.items()], columns=["Concepto", "Valor"])), "",
          ]
    with open(os.path.join(DATOS, "MODELO_PROYECCIONES.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(mo))

    M.escribir_fuentes(os.path.join(DATOS, "FUENTES_Y_VERIFICACION.md"))
    print(f"OK · {len(GRAFICAS)} gráficas en assets/graficas · RESUMEN_ENCUESTA.md, MODELO_PROYECCIONES.md y FUENTES_Y_VERIFICACION.md en datos/")


if __name__ == "__main__":
    main()
