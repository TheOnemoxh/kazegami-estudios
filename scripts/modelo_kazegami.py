# -*- coding: utf-8 -*-
"""
modelo_kazegami.py
==================
FUENTE ÚNICA DE VERDAD NUMÉRICA del proyecto KAZEGAMI RESTAURANTE.

Todo número que aparezca en los estudios (demanda, oferta, capacidad, recetas,
costos de insumos, equipos y tecnología) sale de este módulo. Si cambias un
supuesto aquí, vuelve a correr:

    python scripts/analizar_encuesta.py      # regenera gráficas + datos/*.md

y actualiza los .md que citen la cifra (busca la cifra vieja con grep).

Convenciones
------------
* Moneda: pesos colombianos (COP) de octubre de 2026, IVA/impoconsumo incluido
  cuando se trata de precios de venta. Proyecciones a precios constantes 2026.
* Año base: 2026. Horizonte de proyección: 2027-2031.
* Portafolio: SOLO los 3 platos más frecuentados de la encuesta
  (Rollos de sushi, Ramen y Tempura).
"""
from __future__ import annotations

import glob
import os
from dataclasses import dataclass

import numpy as np
import pandas as pd

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# 0. Utilidades
# ---------------------------------------------------------------------------

def cop(x: float, dec: int = 0) -> str:
    """Formato colombiano: $1.234.567"""
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "—"
    s = f"{x:,.{dec}f}"
    s = s.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"${s}"


def num(x: float, dec: int = 0) -> str:
    s = f"{x:,.{dec}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def pct(x: float, dec: int = 1) -> str:
    return num(100 * x, dec) + " %"


def ruta_excel() -> str:
    files = glob.glob(os.path.join(RAIZ, "ResultadosEncuesta", "*.xlsx"))
    if not files:
        raise FileNotFoundError("No se encontró el Excel en ResultadosEncuesta/")
    return files[0]


def cargar_encuesta() -> pd.DataFrame:
    return pd.read_excel(ruta_excel(), sheet_name="Respuestas de formulario 1")


# ---------------------------------------------------------------------------
# 1. Parámetros que salen DIRECTAMENTE de la encuesta (n = 106)
# ---------------------------------------------------------------------------
PLATOS_TOP3 = ["Rollos de sushi", "Ramen", "Tempura"]

FREQ_MAP = {  # ocasiones de consumo de sushi/ramen por año
    "Más de una vez por semana": 78,   # 1,5 veces/semana
    "Una vez por semana": 52,
    "Una o dos veces al mes": 18,      # 1,5 veces/mes
    "Unas pocas veces al año": 4,
    "Casi nunca": 1,
    "Nunca lo he probado": 0,
}


def separar_multiple(serie: pd.Series) -> pd.Series:
    """Separa respuestas de selección múltiple de Google Forms.
    Ojo: la opción 'Aún no sé, quisiera ver el menú' contiene una coma."""
    protegidas = {
        "Aún no sé, quisiera ver el menú": "Aún no sé / quisiera ver el menú",
        "Zona Norte (Manzanillo, Los Morros, Serena del Mar)": "Zona Norte (Manzanillo / Los Morros / Serena del Mar)",
        "Recomendaciones de hoteles, guías turísticos y/o anfitriones": "Recomendaciones de hoteles / guías turísticos y/o anfitriones",
    }
    out = []
    for v in serie.dropna().astype(str):
        for k, r in protegidas.items():
            v = v.replace(k, r)
        out.extend([p.strip() for p in v.split(", ") if p.strip()])
    return pd.Series(out)


def parametros_encuesta(df: pd.DataFrame | None = None) -> dict:
    df = cargar_encuesta() if df is None else df
    c = list(df.columns)
    p = {}
    p["n"] = len(df)
    acept = df[c[2]].value_counts()
    p["aceptacion"] = (acept.get("Si, consumo comida japonesa o mariscos", 0)
                       + acept.get("No los he probado, pero estaría dispuesto a probarlos", 0)) / len(df)
    # Frecuencia
    fr = df[c[4]].dropna().map(FREQ_MAP)
    p["frecuencia_anual"] = fr.mean()
    p["n_frecuencia"] = fr.notna().sum()
    # Platos
    platos = separar_multiple(df[c[6]]).value_counts()
    p["platos_conteo"] = platos
    reales = platos.drop(labels=["Aún no sé / quisiera ver el menú"], errors="ignore")
    top3 = reales[PLATOS_TOP3]
    p["menciones_top3"] = int(top3.sum())
    p["menciones_platos"] = int(reales.sum())
    p["share_top3"] = top3.sum() / reales.sum()
    p["mix"] = (top3 / top3.sum()).to_dict()
    # Disposición de pago cena completa
    wtp = df[c[21]].dropna()
    p["n_wtp"] = len(wtp)
    p["wtp_60k_mas"] = (~wtp.str.startswith("Menos de $60.000")).mean()
    # Probabilidad de visita
    pv = df[c[28]].dropna()
    p["prob_visita_alta"] = pv.isin(["Probable", "Muy probable"]).mean()
    p["n_prob"] = len(pv)
    # Concepto
    con = df[c[20]].dropna()
    p["concepto_atractivo"] = con.isin(["Atractivo", "Muy atractivo"]).mean()
    return p


# ---------------------------------------------------------------------------
# 2. Supuestos de fuentes secundarias y del equipo (documentados en 99_bibliografia)
# ---------------------------------------------------------------------------
# Fuentes citadas: ver datos/FUENTES_Y_VERIFICACION.md (cada valor tiene su URL y fecha de consulta).
SUP = {
    # ---- Fuentes secundarias VERIFICADAS ----
    "pob_2024": 1_010_408,            # DANE, proyecciones post-COVID (Cartagena Cómo Vamos)
    "pob_2025": 1_011_520,            # DANE (El Universal, 13-ago-2025; Telencuestas con base DANE)
    "pob_2026": 1_010_995,            # DANE (El Universal, 13-ago-2025)
    "pob_2033": 998_638,              # DANE (El Universal, 13-ago-2025)
    "adultos_2025": 719_615,          # DANE 2025: población de 18 años y más (Telencuestas con base DANE)
    "turistas_ext_2024": 855_744,     # Migración Colombia vía El Universal (16-mar-2026)
    "turistas_ext_2025": 866_264,     # idem (+1,22 %)
    "smmlv_2026": 1_750_905,          # Decreto 1469 de 2025
    "aux_transporte_2026": 249_095,
    "pct_estratos_3a6": 0.30,         # Cartagena Cómo Vamos: viviendas estratos 3 (21 %), 4 (3 %), 5 (4 %), 6 (2 %) – El Universal, 08-sep-2020
    "pct_turismo_gastronomia": 0.113, # Corpoturismo 2025: 11,3 % viaja por gastronomía
    "crec_restaurantes_2024": 0.02,   # ACODRES (Portafolio, 23-feb-2025)
    "oferentes_2026": 37,             # Tripadvisor: 37 restaurantes en la categoría "japonesa" de Cartagena (consulta oct-2026)
    "oferentes_ramen": 7,             # Tripadvisor: 7 restaurantes de Cartagena con ramen (consulta oct-2026)
    "salmon_kg_sipsa": 56_463,        # SIPSA-DANE (referencia; no se usa salmón)
    # ---- ESTIMACIONES del equipo basadas en investigación (no hay dato público exacto) ----
    "pct_turistas_japonesa": 0.10,    # se aproxima con el 11,3 % que viaja por gastronomía (Corpoturismo)
    "platos_por_ocasion": 1.0,        # un plato fuerte del Top 3 por ocasión de consumo
    "platos_dia_oferente": 50,        # no hay datos públicos de ventas de la competencia (requiere observación de campo)
    "dias_oferente": 340,             # locales que abren casi todo el año (cierres por festivos/mantenimiento)
    "crec_oferta": 0.02,              # = crecimiento de establecimientos de restaurantes 2024 (ACODRES)
}
SUP["pct_adultos"] = SUP["adultos_2025"] / SUP["pob_2025"]   # 71,1 % (DANE)

ESCENARIOS = {  # crecimiento anual del consumo per cápita de los 3 platos (todas con fuente)
    "Pesimista": 0.0202,  # Raddar: crecimiento del gasto total de los hogares, dic-2024 (Portafolio)
    "Base": 0.036,        # Raddar: crecimiento del gasto en comidas fuera del hogar, dic-2024 (Portafolio)
    "Optimista": 0.095,   # Sushi Master: piezas vendidas 438.898 (2024) → 480.397 (2025), +9,5 % (Valora Analitik)
}
ANIOS = [2027, 2028, 2029, 2030, 2031]


def tasa_poblacion() -> float:
    return (SUP["pob_2033"] / SUP["pob_2026"]) ** (1 / 7) - 1


def tasa_turismo() -> float:
    return SUP["turistas_ext_2025"] / SUP["turistas_ext_2024"] - 1


# ---------------------------------------------------------------------------
# 3. DEMANDA
# ---------------------------------------------------------------------------

def embudo_demanda(p: dict, poblacion: float, turistas: float) -> dict:
    adultos = poblacion * SUP["pct_adultos"]
    cap_pago = adultos * SUP["pct_estratos_3a6"]
    con_wtp = cap_pago * p["wtp_60k_mas"]
    ocasiones = con_wtp * p["frecuencia_anual"]
    platos_res = ocasiones * p["share_top3"] * SUP["platos_por_ocasion"]
    tur_jap = turistas * SUP["pct_turistas_japonesa"]
    platos_tur = tur_jap * p["share_top3"] * SUP["platos_por_ocasion"]
    return dict(poblacion=poblacion, adultos=adultos, cap_pago=cap_pago, con_wtp=con_wtp,
                ocasiones=ocasiones, platos_res=platos_res, turistas=turistas,
                tur_jap=tur_jap, platos_tur=platos_tur, total=platos_res + platos_tur)


def demanda_actual(p: dict) -> dict:
    tur_2026 = SUP["turistas_ext_2025"] * (1 + tasa_turismo())
    return embudo_demanda(p, SUP["pob_2026"], tur_2026)


def demanda_historica(p: dict) -> pd.DataFrame:
    tur_2026 = SUP["turistas_ext_2025"] * (1 + tasa_turismo())
    filas = []
    for anio, pob, tur in [(2024, SUP["pob_2024"], SUP["turistas_ext_2024"]),
                           (2025, SUP["pob_2025"], SUP["turistas_ext_2025"]),
                           (2026, SUP["pob_2026"], tur_2026)]:
        e = embudo_demanda(p, pob, tur)
        filas.append(dict(Año=anio, Población=pob, Turistas=tur,
                          Residentes=e["platos_res"], Turismo=e["platos_tur"], Total=e["total"]))
    return pd.DataFrame(filas)


def proyeccion_demanda(p: dict) -> pd.DataFrame:
    d0 = demanda_actual(p)
    rp, rt = tasa_poblacion(), tasa_turismo()
    filas = []
    for esc, g in ESCENARIOS.items():
        for i, anio in enumerate([2026] + ANIOS):
            res = d0["platos_res"] * ((1 + rp) * (1 + g)) ** i
            tur = d0["platos_tur"] * ((1 + rt) * (1 + g)) ** i
            filas.append(dict(Escenario=esc, Año=anio, Residentes=res, Turismo=tur, Total=res + tur))
    return pd.DataFrame(filas)


def demanda_base_por_plato(p: dict) -> pd.DataFrame:
    d = proyeccion_demanda(p)
    d = d[d.Escenario == "Base"].copy()
    for plato in PLATOS_TOP3:
        d[plato] = d["Total"] * p["mix"][plato]
    return d[["Año"] + PLATOS_TOP3 + ["Total"]].reset_index(drop=True)


# ---------------------------------------------------------------------------
# 4. OFERTA y BALANCE
# ---------------------------------------------------------------------------

def oferta_actual() -> float:
    return SUP["oferentes_2026"] * SUP["platos_dia_oferente"] * SUP["dias_oferente"]


def proyeccion_oferta() -> pd.DataFrame:
    o0 = oferta_actual()
    filas = []
    for i, anio in enumerate([2026] + ANIOS):
        oferentes = SUP["oferentes_2026"] * (1 + SUP["crec_oferta"]) ** i
        filas.append(dict(Año=anio, Oferentes=oferentes, Oferta=o0 * (1 + SUP["crec_oferta"]) ** i))
    return pd.DataFrame(filas)


def balance(p: dict) -> pd.DataFrame:
    d = proyeccion_demanda(p)
    o = proyeccion_oferta().set_index("Año")["Oferta"]
    piv = d.pivot(index="Año", columns="Escenario", values="Total")[list(ESCENARIOS)]
    b = pd.DataFrame({"Oferta": o})
    for esc in ESCENARIOS:
        b[f"Demanda {esc}"] = piv[esc]
        b[f"DI {esc}"] = piv[esc] - o
    cap = capacidad()
    b["Kazegami"] = cap.set_index("Año")["Platos utilizados"]
    b["Cuota DI base"] = b["Kazegami"] / b["DI Base"]
    b["Cuota mercado base"] = b["Kazegami"] / b["Demanda Base"]
    return b.reset_index()


# ---------------------------------------------------------------------------
# 5. TAMAÑO: capacidad diseñada, instalada y utilizada
# ---------------------------------------------------------------------------
CAP = {
    "mesas": 12, "puestos_mesa": 4, "puestos_barra": 8,
    "rot_almuerzo": 1.5, "rot_cena": 2.0,
    "platos_por_comensal": 1.2,
    "dias_anio": 312,  # 6 días/semana (lunes cerrado) × 52
    "factor_instalada": 0.80,
    "utilizacion": {2027: 0.50, 2028: 0.58, 2029: 0.66, 2030: 0.73, 2031: 0.80},
}


def puestos() -> int:
    return CAP["mesas"] * CAP["puestos_mesa"] + CAP["puestos_barra"]


def capacidad() -> pd.DataFrame:
    rot = CAP["rot_almuerzo"] + CAP["rot_cena"]
    com_dia_dis = puestos() * rot
    platos_dia_dis = com_dia_dis * CAP["platos_por_comensal"]
    dis = platos_dia_dis * CAP["dias_anio"]
    ins = dis * CAP["factor_instalada"]
    filas = []
    for anio, u in CAP["utilizacion"].items():
        uti = ins * u
        filas.append({"Año": anio, "Platos diseñados": dis, "Platos instalados": ins,
                      "% utilización": u, "Platos utilizados": uti,
                      "Platos/día": uti / CAP["dias_anio"],
                      "Comensales/día": uti / CAP["dias_anio"] / CAP["platos_por_comensal"],
                      "Rotación efectiva": uti / CAP["dias_anio"] / CAP["platos_por_comensal"] / puestos()})
    return pd.DataFrame(filas)


def unidades_por_plato(p: dict) -> pd.DataFrame:
    cap = capacidad()
    out = cap[["Año", "Platos utilizados"]].copy()
    for plato in PLATOS_TOP3:
        out[plato] = out["Platos utilizados"] * p["mix"][plato]
    return out


# ---------------------------------------------------------------------------
# 6. RECETAS ESTÁNDAR (por porción) — formato Punto 6
# ---------------------------------------------------------------------------
@dataclass
class Insumo:
    nombre: str
    cantidad: float   # por porción, en la unidad de compra (kg, L, und)
    unidad: str       # unidad de compra
    precio: float     # COP por unidad de compra (precio verificado; ver fuente)
    proveedor: str
    origen: str       # Caribe / Bolívar / Importado / Nacional
    fuente: str = ""  # fuente del precio
    tipo: str = "Costo (materia prima directa)"


# Precios mayoristas SIPSA-DANE en Cartagena (Bazurto), 26-oct-2026, salvo que se indique otra fuente.
F_SIPSA_CTG = "SIPSA-DANE, Cartagena (Bazurto), 26-oct-2026 (vía Agronegocios)"
F_SIPSA_NAL = "SIPSA-DANE, promedio nacional, 26-oct-2026 (vía Agronegocios)"
F_SIPSA_CAR = "SIPSA-DANE, región Caribe, 26-oct-2026 (vía Agronegocios)"
F_GGM = "Global Gourmet Market Colombia, consulta 24-oct-2026"
REND_FILETE = 0.46  # rendimiento en filete de referencia (Mancera, 2024: 46,15 % en cachama); se asume similar para pargo

RECETAS: dict[str, list[Insumo]] = {
    "Rollos de sushi": [  # 1 rollo = 8 piezas (≈ 260 g)
        Insumo("Arroz japonés para sushi (bulto Botan 50 lb)", 0.120, "kg", 370_000 / 22.68, "Importador de insumos japoneses", "Importado", F_GGM + ": $370.000 / 50 lb"),
        Insumo("Vinagre de arroz (Kenko 750 ml)", 0.015, "L", 18_000 / 0.75, "Importador de insumos japoneses", "Importado", F_GGM + ": $18.000 / 750 ml"),
        Insumo("Azúcar refinada (sazón del shari)", 0.005, "kg", 3_820, "Mayorista de Bazurto", "Nacional", F_SIPSA_CTG),
        Insumo("Sal (sazón del shari)", 0.002, "kg", 1_100, "Mayorista de Bazurto", "Nacional", F_SIPSA_CTG),
        Insumo("Alga nori (paquete de 100 hojas)", 1, "und", 98_000 / 100, "Importador de insumos japoneses", "Importado", F_GGM + ": $98.000 / 100 hojas"),
        Insumo(f"Pargo rojo entero fresco (pesca artesanal; 45 g de filete, rinde {int(REND_FILETE*100)} %)", 0.045 / REND_FILETE, "kg", 21_000, "Pescadores artesanales – Mercado de Bazurto", "Caribe", F_SIPSA_CTG),
        Insumo("Langostino 16-20", 0.025, "kg", 62_445, "Pescadería mayorista", "Nacional", F_SIPSA_NAL),
        Insumo("Aguacate papelillo", 0.030, "kg", 11_083, "Agricultores de Bolívar (Bazurto)", "Bolívar", F_SIPSA_CTG),
        Insumo("Pepino cohombro", 0.020, "kg", 2_367, "Agricultores de Bolívar (Bazurto)", "Bolívar", F_SIPSA_CTG),
        Insumo("Mango de azúcar (toque caribeño)", 0.015, "kg", 2_400, "Agricultores de Bolívar (Bazurto)", "Bolívar", F_SIPSA_CTG),
        Insumo("Queso crema (Alpina 380 g)", 0.020, "kg", 13_000 / 0.38, "Distribuidor de lácteos", "Nacional", "Mercasur, consulta 24-oct-2026: $13.000 / 380 g"),
        Insumo("Ajonjolí descortezado", 0.003, "kg", 12_000 / 0.25, "Importador de insumos japoneses", "Nacional", F_GGM + ": $12.000 / 250 g"),
        Insumo("Salsa de soya (Sakura 20 L)", 0.015, "L", 294_000 / 20, "Importador de insumos japoneses", "Importado", F_GGM + ": $294.000 / 20 L"),
        Insumo("Wasabi en polvo (Waner 1 kg)", 0.002, "kg", 115_000, "Importador de insumos japoneses", "Importado", F_GGM + ": $115.000 / kg"),
        Insumo("Jengibre encurtido – gari (340 g)", 0.010, "kg", 15_000 / 0.34, "Importador de insumos japoneses", "Importado", F_GGM + ": $15.000 / 340 g"),
        Insumo("Mayonesa (base de la salsa spicy de la casa)", 0.010, "kg", 18_490, "Mayorista de Bazurto", "Nacional", F_SIPSA_CTG),
    ],
    "Ramen": [  # 1 bowl ≈ 650 ml
        Insumo("Fideo de trigo estilo chuka (Best Choice 400 g)", 0.120, "kg", 15_500 / 0.4, "Importador de insumos japoneses", "Importado", F_GGM + ": $15.500 / 400 g"),
        Insumo("Espinazo de cerdo (caldo)", 0.150, "kg", 12_750, "Expendio de carnes – Bazurto", "Bolívar", F_SIPSA_CAR),
        Insumo("Rabadillas de pollo (caldo)", 0.100, "kg", 6_500, "Avícola regional", "Bolívar", F_SIPSA_NAL),
        Insumo("Tocino de barriga de cerdo (chashu)", 0.060, "kg", 18_170, "Expendio de carnes – Bazurto", "Bolívar", F_SIPSA_NAL),
        Insumo("Huevo rojo A (ajitama)", 1, "und", 494, "Avícola regional", "Bolívar", F_SIPSA_CTG),
        Insumo("Miso (Hikari 1 kg)", 0.020, "kg", 40_000, "Importador de insumos japoneses", "Importado", F_GGM + ": $40.000 / kg"),
        Insumo("Salsa de soya (Sakura 20 L)", 0.020, "L", 294_000 / 20, "Importador de insumos japoneses", "Importado", F_GGM + ": $294.000 / 20 L"),
        Insumo("Mirin (Kikkoman 375 ml)", 0.010, "L", 43_000 / 0.375, "Importador de insumos japoneses", "Importado", F_GGM + ": $43.000 / 375 ml"),
        Insumo("Alga nori (½ hoja)", 0.5, "und", 98_000 / 100, "Importador de insumos japoneses", "Importado", F_GGM + ": $98.000 / 100 hojas"),
        Insumo("Cebollín chino", 0.010, "kg", 6_333, "Agricultores de Bolívar (Bazurto)", "Bolívar", F_SIPSA_CTG),
        Insumo("Repollo blanco salteado", 0.030, "kg", 2_077, "Agricultores de Bolívar (Bazurto)", "Bolívar", F_SIPSA_CTG),
        Insumo("Ajo", 0.008, "kg", 5_858, "Agricultores de Bolívar (Bazurto)", "Bolívar", F_SIPSA_CTG),
        Insumo("Aceite de ajonjolí (Kuki 1.650 ml)", 0.005, "L", 138_500 / 1.65, "Importador de insumos japoneses", "Importado", F_GGM + ": $138.500 / 1.650 ml"),
    ],
    "Tempura": [  # porción mixta: 5 langostinos + vegetales
        Insumo("Langostino 16-20", 0.120, "kg", 62_445, "Pescadería mayorista", "Nacional", F_SIPSA_NAL),
        Insumo("Berenjena", 0.035, "kg", 1_333, "Agricultores de Bolívar (Bazurto)", "Bolívar", F_SIPSA_CTG),
        Insumo("Ahuyama", 0.035, "kg", 1_667, "Agricultores de Bolívar (Bazurto)", "Bolívar", F_SIPSA_CTG),
        Insumo("Cebolla cabezona blanca", 0.030, "kg", 2_408, "Agricultores de Bolívar (Bazurto)", "Bolívar", F_SIPSA_CTG),
        Insumo("Harina para tempura (Best Choice 1 kg)", 0.050, "kg", 23_000, "Importador de insumos japoneses", "Importado", F_GGM + ": $23.000 / kg"),
        Insumo("Fécula de maíz", 0.015, "kg", 37_153, "Mayorista de Bazurto", "Nacional", F_SIPSA_CTG),
        Insumo("Huevo rojo A (½ unidad)", 0.5, "und", 494, "Avícola regional", "Bolívar", F_SIPSA_CTG),
        Insumo("Aceite vegetal para freír (consumo + reposición)", 0.060, "kg", 9_792, "Mayorista de Bazurto", "Nacional", F_SIPSA_CTG),
        Insumo("Alga kombu (dashi para tentsuyu)", 0.002, "kg", 16_000 / 0.1, "Importador de insumos japoneses", "Importado", F_GGM + ": $16.000 / 100 g"),
        Insumo("Salsa de soya (Sakura 20 L)", 0.010, "L", 294_000 / 20, "Importador de insumos japoneses", "Importado", F_GGM + ": $294.000 / 20 L"),
        Insumo("Mirin (Kikkoman 375 ml)", 0.010, "L", 43_000 / 0.375, "Importador de insumos japoneses", "Importado", F_GGM + ": $43.000 / 375 ml"),
        Insumo("Rábano rojo rallado (en lugar de daikon)", 0.020, "kg", 6_333, "Agricultores de Bolívar (Bazurto)", "Bolívar", F_SIPSA_CTG),
    ],
}

PRECIO_VENTA = {"Rollos de sushi": 40_000, "Ramen": 38_000, "Tempura": 38_000}  # COP, impoconsumo 8 % incluido
IMPOCONSUMO = 0.08

# Precios reales de la competencia (para el método de precios)
COMPETENCIA_PRECIOS = {
    "Rollos de sushi": ("Masaki Sushi Wok (Rappi): 12 rollos completos entre $40.000 y $57.000; promedio $49.550", 49_550),
    "Ramen": ("Dame Ramen, Bocagrande (menú web): 9 ramen entre $35.000 y $69.000; promedio $45.667", 45_667),
    "Tempura": ("Masaki Sushi Wok (Rappi): tempura mixta de vegetales $25.000 (sin langostino)", 25_000),
}

# Activos específicos de cada línea (para la fila de depreciación del formato Punto 6)
ACTIVOS_PLATO = {
    "Rollos de sushi": [("Vitrina refrigerada curva para sushi (Makfrio)", 1, 5_136_000),
                        ("Arrocera industrial a gas 10 L (Pallomaro)", 2, 2_052_750),
                        ("Cuchillo yanagiba 270 mm Sekiryu", 2, 441_200),
                        ("Cuchillo sashimi 240 mm", 2, 150_000)],
    "Ramen": [("Quemador de piso para caldos + marmita 60 L", 1, 2_800_000),
              ("Ollas de acero inoxidable 60 L", 3, 650_000)],
    "Tempura": [("Freidora industrial a gas 20 L, 2 canastas (Exhibir Equipos)", 1, 5_089_000)],
}
VIDA_UTIL_ANIOS = 10  # maquinaria y equipo / muebles (Decreto 1625/2016 art. 1.2.1.18.4 – tasa 10 %)

# Costos o gastos de servicio asignados a cada línea (mensual, año 2027) – ESTIMACIÓN del equipo
SERVICIOS_PLATO = {
    "Rollos de sushi": [("Gas natural (arroceras)", 1, 180_000), ("Energía de la vitrina refrigerada", 1, 220_000),
                        ("Palillos, servilletas y desechables de barra", 1, 260_000)],
    "Ramen": [("Gas natural (caldo 10–12 h diarias)", 1, 520_000), ("Agua para caldos y lavado", 1, 90_000),
              ("Servilletas y cucharas de servicio", 1, 120_000)],
    "Tempura": [("Gas natural (freidora)", 1, 260_000), ("Disposición de aceite usado (gestor autorizado)", 1, 60_000),
                ("Papel absorbente y servilletas", 1, 100_000)],
}


def costo_receta(plato: str) -> float:
    return sum(i.cantidad * i.precio for i in RECETAS[plato])


def tabla_punto6(p: dict, plato: str, anio: int = 2027) -> tuple[pd.DataFrame, dict]:
    """Construye la tabla con las columnas exactas del modelo de Punto6EstudioTecnicoImg:
    Insumo | Cantidad por mes | Proveedor (precio, calidad, postventa) | Precio | Total |
    Identificación del elemento | Total final"""
    unid = unidades_por_plato(p).set_index("Año").loc[anio, plato] / 12
    filas = []
    for i in RECETAS[plato]:
        qmes = i.cantidad * unid
        total = qmes * i.precio
        filas.append({"Insumo": i.nombre, "Cantidad por mes": qmes, "Unidad": i.unidad,
                      "Proveedor": i.proveedor, "Precio": i.precio, "Total": total,
                      "Identificación": "Costo", "Total final": total})
    activos_total = 0
    for nombre, q, precio in ACTIVOS_PLATO[plato]:
        filas.append({"Insumo": nombre, "Cantidad por mes": q, "Unidad": "und",
                      "Proveedor": "Proveedor de equipos de cocina", "Precio": precio, "Total": q * precio,
                      "Identificación": "Activo", "Total final": np.nan})
        activos_total += q * precio
    for nombre, q, precio in SERVICIOS_PLATO[plato]:
        filas.append({"Insumo": nombre, "Cantidad por mes": q, "Unidad": "servicio",
                      "Proveedor": "Empresa de servicios / proveedor local", "Precio": precio, "Total": q * precio,
                      "Identificación": "Costo o gasto", "Total final": q * precio})
    dep = activos_total / (VIDA_UTIL_ANIOS * 12)
    filas.append({"Insumo": "Gasto de depreciación de activos de la línea", "Cantidad por mes": 1,
                  "Unidad": "mes", "Proveedor": f"{cop(activos_total)} ÷ ({VIDA_UTIL_ANIOS} × 12)",
                  "Precio": dep, "Total": dep, "Identificación": "Gasto (depreciación)", "Total final": dep})
    df = pd.DataFrame(filas)
    total_final = df["Total final"].sum()
    mp = df.loc[df["Identificación"] == "Costo", "Total final"].sum()
    resumen = dict(unidades_mes=unid, total_final=total_final, costo_unitario=total_final / unid,
                   mp_mes=mp, mp_unitario=mp / unid, activos=activos_total, depreciacion=dep,
                   precio=PRECIO_VENTA[plato], precio_sin_imp=PRECIO_VENTA[plato] / (1 + IMPOCONSUMO))
    resumen["food_cost"] = resumen["mp_unitario"] / resumen["precio_sin_imp"]
    resumen["margen_contrib"] = resumen["precio_sin_imp"] - resumen["costo_unitario"]
    return df, resumen


def consolidado_insumos(p: dict) -> pd.DataFrame:
    u = unidades_por_plato(p)
    filas = []
    for _, r in u.iterrows():
        fila = {"Año": int(r["Año"])}
        tot = 0
        for plato in PLATOS_TOP3:
            c = r[plato] * costo_receta(plato)
            fila[plato] = c
            tot += c
        fila["Total anual"] = tot
        fila["Promedio mensual"] = tot / 12
        filas.append(fila)
    return pd.DataFrame(filas)


def consumo_insumos_clave(p: dict, anio: int = 2027) -> pd.DataFrame:
    """Kg/L/und anuales por insumo, sumando los 3 platos (para disponibilidad)."""
    u = unidades_por_plato(p).set_index("Año").loc[anio]
    agg = {}
    for plato in PLATOS_TOP3:
        for i in RECETAS[plato]:
            k = (i.nombre.split(" (")[0], i.unidad, i.origen)
            agg[k] = agg.get(k, 0) + i.cantidad * u[plato]
    df = pd.DataFrame([{"Insumo": k[0], "Unidad": k[1], "Origen": k[2], "Cantidad anual": v}
                       for k, v in agg.items()])
    return df.sort_values(["Origen", "Cantidad anual"], ascending=[True, False])


# ---------------------------------------------------------------------------
# 7. EQUIPOS, MOBILIARIO, ADECUACIÓN Y TECNOLOGÍA (CAPEX) + OPEX
# ---------------------------------------------------------------------------
V = "Verificado"
E = "Estimado"
EQUIPOS = [  # (ítem, cantidad, precio unitario, área, vida útil años, estado, fuente)
    ("Ultracongelador / abatidor −40 °C, 5 bandejas (TechGelato TG25BCF)", 1, 15_990_000, "Refrigeración", 10, V, "Makfrio / America Food Solutions, oct-2026"),
    ("Nevera vertical industrial 2 puertas acero inoxidable (TG1400R2A)", 2, 10_190_000, "Refrigeración", 10, V, "America Food Solutions, oct-2026"),
    ("Mesa refrigerada de preparación 1,50 m", 2, 7_704_000, "Refrigeración", 10, V, "Makfrio, oct-2026"),
    ("Congelador horizontal ≈ 500 L", 1, 3_900_000, "Refrigeración", 10, E, "Sin precio público consultable; requiere cotización"),
    ("Vitrina refrigerada curva para sushi", 1, 5_136_000, "Barra", 10, V, "Makfrio, oct-2026"),
    ("Fabricador de hielo 65 kg", 1, 4_990_000, "Barra", 10, V, "Makfrio, oct-2026"),
    ("Nevera exhibidora de bebidas 2 puertas 1.100 L", 1, 12_800_000, "Barra", 10, V, "FrigoMaster, oct-2026"),
    ("Arrocera industrial a gas 10 L", 2, 2_052_750, "Cocina", 10, V, "Pallomaro, oct-2026"),
    ("Estufa industrial de piso 36\", 6 puestos (ETP-36)", 1, 3_940_923, "Cocina", 10, V, "Pallomaro, oct-2026"),
    ("Quemador de piso para caldos + marmita 60 L", 1, 2_800_000, "Cocina", 10, E, "Sin precio público consultable; requiere cotización"),
    ("Freidora industrial a gas 20 L, 2 canastas", 1, 5_089_000, "Cocina", 10, V, "Exhibir Equipos, oct-2026"),
    ("Campana extractora en acero inoxidable (3 módulos de 1 m)", 3, 850_000, "Cocina", 10, V, "SMR Industriales, oct-2026"),
    ("Extractor centrífugo y ductería para la campana", 1, 6_000_000, "Cocina", 10, E, "Sin precio público consultable; requiere cotización"),
    ("Trampa de grasas en acero inoxidable", 1, 2_500_000, "Cocina", 10, E, "Sin precio público consultable; requiere cotización"),
    ("Mesas de trabajo en acero inoxidable (MAINOX2)", 4, 2_535_000, "Cocina", 10, V, "Exhibir Equipos, oct-2026"),
    ("Pozuelo triple de lavado en acero inoxidable", 1, 3_200_000, "Cocina", 10, E, "Sin precio público consultable; requiere cotización"),
    ("Ollas de acero inoxidable 60 L", 3, 650_000, "Cocina", 10, E, "Sin precio público consultable; requiere cotización"),
    ("Balanzas digitales de precisión", 2, 350_000, "Control de calidad", 10, E, "Estimación del equipo"),
    ("Termómetros de punzón y data loggers de temperatura", 4, 180_000, "Control de calidad", 10, E, "Estimación del equipo"),
    ("Cuchillo yanagiba 270 mm Sekiryu", 2, 441_200, "Barra", 10, V, "Global Gourmet Market, oct-2026"),
    ("Cuchillo sashimi 240 mm", 2, 150_000, "Barra", 10, V, "Global Gourmet Market, oct-2026"),
    ("Utensilios menores (makisu, bandejas GN, coladores, tablas)", 1, 3_500_000, "Cocina", 10, E, "Estimación del equipo"),
    ("Vajilla japonesa (platos, bowls de ramen, palillos reutilizables)", 1, 9_000_000, "Sala", 10, E, "Estimación del equipo"),
    ("Planta eléctrica diésel 18-20 kVA cabinada (respaldo de cadena de frío)", 1, 53_300_000, "Respaldo", 10, V, "Maquitec de Colombia, oct-2026"),
]

MOBILIARIO_TEC = [  # (ítem, cantidad, precio unitario, categoría, vida útil, estado, fuente)
    ("Adecuación del local (obra civil, pisos, baños, redes de gas y eléctricas)", 1, 85_000_000, "Adecuación", 5, E, "Estimación del equipo; requiere presupuesto de obra"),
    ("Barra de sushi en madera para 8 comensales", 1, 12_000_000, "Mobiliario", 10, E, "Estimación del equipo"),
    ("Mesas de madera para 4 personas", 12, 650_000, "Mobiliario", 10, E, "Estimación del equipo"),
    ("Sillas de comedor", 48, 280_000, "Mobiliario", 10, E, "Estimación del equipo"),
    ("Bancos altos de barra", 8, 350_000, "Mobiliario", 10, E, "Estimación del equipo"),
    ("Aire acondicionado minisplit 24.000 BTU", 4, 4_067_900, "Adecuación", 10, V, "Falabella Colombia, oct-2026"),
    ("Iluminación y decoración de inspiración japonesa", 1, 15_000_000, "Adecuación", 5, E, "Estimación del equipo"),
    ("Aviso exterior y señalización", 1, 4_500_000, "Adecuación", 5, E, "Estimación del equipo"),
    ("Sistema de sonido ambiental", 1, 2_800_000, "Mobiliario", 10, E, "Estimación del equipo"),
    ("Computador administrativo", 1, 3_200_000, "Tecnología", 5, E, "Estimación del equipo"),
    ("Tablets comanderas para meseros", 3, 1_100_000, "Tecnología", 5, E, "Estimación del equipo"),
    ("Impresoras térmicas de comandas y facturas", 3, 650_000, "Tecnología", 5, E, "Estimación del equipo"),
    ("Cajón monedero y lector de código", 1, 550_000, "Tecnología", 5, E, "Estimación del equipo"),
    ("Red WiFi y router empresarial", 1, 900_000, "Tecnología", 5, E, "Estimación del equipo"),
    ("UPS para POS y red", 1, 1_200_000, "Tecnología", 5, E, "Estimación del equipo"),
    ("Kit de cámaras de seguridad (4 cámaras + grabador)", 1, 2_200_000, "Tecnología", 5, E, "Estimación del equipo"),
]

SOFTWARE_ANUAL = [  # (servicio, costo anual) – gasto, no activo. ESTIMACIÓN (los planes se cotizan con el proveedor)
    ("Software POS para restaurantes con facturación electrónica DIAN (licencia anual)", 2_400_000),
    ("Plataforma de reservas en línea + WhatsApp Business API (anual)", 1_800_000),
    ("Módulo de inventarios y recetas estándar (anual)", 1_200_000),
    ("Dominio, página web y correo corporativo (anual)", 900_000),
]

NOMINA = [  # (cargo, cantidad, salario base mensual, fuente)
    ("Chef ejecutivo / sushiman principal", 1, 1_947_429, "Indeed Colombia: salario promedio de chef, act. 02-oct-2026"),
    ("Sushiman auxiliar (barra)", 1, 1_750_905, "SMMLV 2026 (el promedio de Indeed para cocinero, $1.341.350, es inferior al mínimo legal)"),
    ("Cocinero de línea caliente (ramen y tempura)", 2, 1_750_905, "SMMLV 2026 (Indeed cocinero/a: $1.341.350 < mínimo legal)"),
    ("Auxiliar de cocina y steward", 2, 1_750_905, "SMMLV 2026"),
    ("Meseros", 4, 1_750_905, "SMMLV 2026 (Indeed mesero/a: $1.524.922 < mínimo legal)"),
    ("Anfitrión(a) y cajero(a)", 1, 1_750_905, "SMMLV 2026"),
    ("Administrador(a)", 1, 3_501_810, "Estimación: 2 SMMLV (sin dato público verificable para Cartagena)"),
]
FACTOR_PRESTACIONAL = 1.38  # Aleluya (2026): ≈ 38 % con exoneración de salud, SENA e ICBF (art. 114-1 E.T., personas jurídicas)

TARIFA_ENERGIA_KWH = 1_033.32 * 1.20   # Afinia sep-2026 ($1.033,32/kWh, El Universal) + 20 % contribución de usuarios comerciales (Ley 142 de 1994)
CONSUMO_KWH_MES = 2_600                # ESTIMACIÓN del equipo según potencia de equipos de refrigeración, aire acondicionado e iluminación
ARRIENDO_M2_MANGA = 75_295             # Fincaraíz, mediana de 20 locales en arriendo en Manga, consulta 24-oct-2026
AREA_LOCAL_M2 = 200

OPEX_MENSUAL = [  # (concepto, valor mensual)
    ("Arriendo del local (200 m² × $75.295/m², mediana Manga)", AREA_LOCAL_M2 * ARRIENDO_M2_MANGA),
    ("Energía eléctrica (Afinia: 2.600 kWh × $1.240/kWh)", round(CONSUMO_KWH_MES * TARIFA_ENERGIA_KWH, -3)),
    ("Agua y alcantarillado (Aguas de Cartagena)", 650_000),
    ("Gas natural (Gases del Caribe)", 1_100_000),
    ("Internet y telefonía", 250_000),
    ("Marketing digital y pauta en redes (presupuesto del equipo)", 2_500_000),
    ("Aseo, fumigación y control de plagas", 450_000),
    ("Mantenimiento de equipos", 600_000),
    ("Seguros (todo riesgo y responsabilidad civil)", 550_000),
    ("Derechos de autor por música (Sayco–Acinpro / OSA)", 120_000),
]


def tabla_capex(lista) -> pd.DataFrame:
    df = pd.DataFrame(lista, columns=["Ítem", "Cantidad", "Precio unitario", "Categoría", "Vida útil (años)", "Estado", "Fuente"])
    df["Total"] = df["Cantidad"] * df["Precio unitario"]
    df["Depreciación mensual"] = df["Total"] / (df["Vida útil (años)"] * 12)
    return df


def nomina_mensual() -> pd.DataFrame:
    df = pd.DataFrame(NOMINA, columns=["Cargo", "Cantidad", "Salario base", "Fuente"])
    aux = df["Salario base"].apply(lambda s: SUP["aux_transporte_2026"] if s <= 2 * SUP["smmlv_2026"] else 0)
    df["Costo total mensual"] = df["Cantidad"] * (df["Salario base"] * FACTOR_PRESTACIONAL + aux)
    return df


def resumen_costos(p: dict) -> dict:
    eq = tabla_capex(EQUIPOS)
    mob = tabla_capex(MOBILIARIO_TEC)
    soft = sum(v for _, v in SOFTWARE_ANUAL)
    ins = consolidado_insumos(p)
    ins27 = ins.loc[ins.Año == 2027, "Total anual"].iloc[0]
    nom = nomina_mensual()["Costo total mensual"].sum()
    opex = sum(v for _, v in OPEX_MENSUAL)
    capital_trabajo_insumos = ins27 / 12  # 1 mes de inventario
    return dict(
        equipos=eq["Total"].sum(),
        mobiliario=mob.loc[mob["Categoría"].isin(["Mobiliario"]), "Total"].sum(),
        adecuacion=mob.loc[mob["Categoría"].isin(["Adecuación"]), "Total"].sum(),
        tecnologia_hw=mob.loc[mob["Categoría"] == "Tecnología", "Total"].sum(),
        software_anual=soft,
        insumos_anual_2027=ins27,
        inventario_inicial=capital_trabajo_insumos,
        nomina_mensual=nom,
        opex_mensual=opex,
        dep_mensual=eq["Depreciación mensual"].sum() + mob["Depreciación mensual"].sum(),
    )


# ---------------------------------------------------------------------------
# 8. LOCALIZACIÓN: método cualitativo por puntos
# ---------------------------------------------------------------------------
# Arriendo: mediana $/m² en Fincaraíz (consulta 24-oct-2026). Votos: encuesta. Calificaciones cuantitativas
# normalizadas min-max a escala 1-10; las cualitativas son juicio del equipo (se indica en la tabla).
ARRIENDO_M2 = {"Centro Histórico": 110_000, "Manga": 75_295, "Bocagrande": 130_000, "Getsemaní": 83_333}
VOTOS_ZONA = {"Centro Histórico": 33, "Manga": 17, "Bocagrande": 10, "Getsemaní": 8}


def _minmax(d: dict, invertir: bool = False) -> dict:
    lo, hi = min(d.values()), max(d.values())
    out = {}
    for k, v in d.items():
        x = (v - lo) / (hi - lo)
        out[k] = round(1 + 9 * ((1 - x) if invertir else x), 2)
    return out


FACTORES_LOC = [  # (factor, peso, {zona: calificación 1-10}, justificación)
    ("Preferencia de los encuestados", 0.25, _minmax(VOTOS_ZONA),
     "Cuantitativa: votos de la encuesta 33 / 17 / 10 / 8, normalizados 1-10"),
    ("Costo de arriendo por m²", 0.20, _minmax(ARRIENDO_M2, invertir=True),
     "Cuantitativa: mediana Fincaraíz $110.000 / $75.295 / $130.000 / $83.333 por m² (menor = mejor)"),
    ("Flujo de turistas y ejecutivos", 0.15,
     {"Centro Histórico": 10, "Manga": 5, "Bocagrande": 9, "Getsemaní": 8},
     "Cualitativa (equipo): cercanía a hoteles, centro de convenciones y oficinas"),
    ("Cercanía a proveedores (Bazurto, Mercado del Mar)", 0.10,
     {"Centro Histórico": 7, "Manga": 9, "Bocagrande": 6, "Getsemaní": 8},
     "Cualitativa (equipo): menor tiempo de traslado del pescado fresco"),
    ("Accesibilidad y parqueadero", 0.10,
     {"Centro Histórico": 4, "Manga": 8, "Bocagrande": 7, "Getsemaní": 5},
     "Cualitativa (equipo): vías, parqueo y acceso para proveedores"),
    ("Saturación de la competencia (menor = mejor)", 0.10,
     {"Centro Histórico": 4, "Manga": 6, "Bocagrande": 4, "Getsemaní": 6},
     "Cualitativa (equipo): restaurantes japoneses/nikkei identificados en cada zona"),
    ("Restricciones normativas para adecuar cocina (PEMP / POT)", 0.10,
     {"Centro Histórico": 4, "Manga": 8, "Bocagrande": 7, "Getsemaní": 5},
     "Cualitativa (equipo): Centro y Getsemaní son zona patrimonial; limita extracción de humos y obras"),
]
ZONAS = ["Centro Histórico", "Manga", "Bocagrande", "Getsemaní"]


def matriz_localizacion() -> pd.DataFrame:
    filas = []
    for f, w, cal, just in FACTORES_LOC:
        fila = {"Factor": f, "Peso": w}
        for z in ZONAS:
            fila[f"{z} cal."] = cal[z]
            fila[f"{z} pond."] = cal[z] * w
        filas.append(fila)
    return pd.DataFrame(filas)


if __name__ == "__main__":
    p = parametros_encuesta()
    print({k: v for k, v in p.items() if k != "platos_conteo"})
    print(demanda_actual(p))
    print(demanda_historica(p))
    print(proyeccion_demanda(p).pivot(index="Año", columns="Escenario", values="Total"))
    print(proyeccion_oferta())
    print(balance(p).round(3).to_string())
    print(capacidad().round(2).to_string())
    print(unidades_por_plato(p).round(0).to_string())
    for pl in PLATOS_TOP3:
        df, r = tabla_punto6(p, pl)
        print(pl, {k: round(v, 3) for k, v in r.items()}, "receta", round(costo_receta(pl)))
    print(consolidado_insumos(p).round(0).to_string())
    print({k: round(v) for k, v in resumen_costos(p).items()})
    m = matriz_localizacion()
    print(m[[c for c in m.columns if "pond" in c]].sum())


# ---------------------------------------------------------------------------
# 9. ARCHIVO DE FUENTES Y VERIFICACIÓN (datos/FUENTES_Y_VERIFICACION.md)
# ---------------------------------------------------------------------------
FUENTES_GENERALES = [  # (dato, valor, estado, fuente con URL)
    ("Encuesta de mercado (todas las cifras de la encuesta)", "n = 106, 31 columnas", "Verificado", "ResultadosEncuesta/*.xlsx (datos primarios del equipo)"),
    ("Población de Cartagena 2024 / 2025 / 2026 / 2033", "1.010.408 / 1.011.520 / 1.010.995 / 998.638", "Verificado", "DANE vía El Universal (13-ago-2025): https://www.eluniversal.com.co/cartagena/2025/08/13/poblacion-de-cartagena-se-reducira-estas-son-las-proyecciones-del-dane/"),
    ("Población de 18 años y más (2025)", "719.615 (71,1 %)", "Verificado", "DANE vía Telencuestas: https://telencuestas.com/censos-de-poblacion/colombia/2025/bolivar/cartagena-de-indias"),
    ("Viviendas en estratos 3 a 6", "30 % (21 + 3 + 4 + 2)", "Verificado", "Cartagena Cómo Vamos vía El Universal (08-sep-2020): https://www.eluniversal.com.co/cartagena/2020/09/08/69-de-las-viviendas-en-cartagena-pertenece-a-estratos-1-y-ii/"),
    ("Turistas extranjeros 2024 / 2025", "855.744 / 866.264", "Verificado", "Migración Colombia vía El Universal (16-mar-2026): https://www.eluniversal.com.co/economica/2026/03/16/los-cinco-paises-que-mas-turistas-le-generaron-a-cartagena-durante-2025/"),
    ("Turistas que viajan por gastronomía", "11,3 %", "Verificado", "Corpoturismo vía El Universal (26-dic-2025)"),
    ("Turistas extranjeros que consumen cocina japonesa", "10 %", "Estimación", "Aproximado al 11,3 % anterior; no existe dato específico"),
    ("Ocupación hotelera 1.er trimestre 2025", "70,5 %", "Verificado", "Cartagena Cómo Vamos: https://cartagenacomovamos.org/turismo-en-cartagena-primer-trimestre-2025/"),
    ("Salario mínimo 2026 y auxilio de transporte", "$1.750.905 y $249.095", "Verificado", "Decreto 1469 de 2025; Portafolio"),
    ("Restaurantes japoneses en Cartagena", "37 (7 con ramen)", "Verificado", "Tripadvisor (24-oct-2026): https://www.tripadvisor.com/Restaurants-g297476-c27-Cartagena_Cartagena_District_Bolivar_Department.html"),
    ("Platos del Top 3 vendidos por competidor al día", "50", "Estimación", "Sin datos públicos de ventas; requiere observación de campo"),
    ("Crecimiento de establecimientos de restaurantes 2024", "2 %", "Verificado", "ACODRES vía Portafolio (23-feb-2025)"),
    ("Crecimiento del gasto: total hogares / comidas fuera del hogar (dic-2024)", "2,02 % / 3,6 %", "Verificado", "Raddar vía Portafolio: https://www.portafolio.co/economia/finanzas/en-que-gastaron-mas-los-hogares-colombianos-en-el-2024-622923"),
    ("Crecimiento Sushi Master 2024 → 2025 (piezas)", "438.898 → 480.397 (+9,5 %)", "Verificado", "Valora Analitik (04-dic-2025): https://www.valoraanalitik.com/?p=532819"),
    ("Precios de rollos (Masaki Sushi Wok)", "$40.000-$57.000 (prom. $49.550)", "Verificado", "Rappi: https://www.rappi.com.co/restaurantes/900039514-masaki-sushi-wok"),
    ("Precios de ramen (Dame Ramen)", "$35.000-$69.000 (prom. $45.667)", "Verificado", "https://dameramen.com/menu/"),
    ("Tempura de vegetales (Masaki)", "$25.000", "Verificado", "Rappi (ídem)"),
    ("Food cost de restaurantes rentables", "28 %-35 %", "Verificado", "Gordon Food Service (Rivers, s.f.): https://gfs.com/es-us/?p=5384"),
    ("Rendimiento en filete del pescado", "46 %", "Estimación", "Mancera (2024): 46,15 % en cachama; se asume similar para pargo"),
    ("Arriendo de locales ($/m² mediana): Manga / Centro / Bocagrande / Getsemaní", "$75.295 / $110.000 / $130.000 / $83.333", "Verificado", "Fincaraíz (24-oct-2026): https://www.fincaraiz.com.co/arriendo/locales/manga/cartagena"),
    ("Tarifa de energía Afinia", "$1.033,32/kWh (+20 % contribución comercial)", "Verificado", "El Universal (11-sep-2026); Ley 142 de 1994"),
    ("Consumo de energía del local", "2.600 kWh/mes", "Estimación", "Cálculo del equipo según equipos instalados"),
    ("Factor prestacional", "1,38", "Verificado", "Aleluya (2026): https://aleluya.com/blog/nomina/costo-de-un-empleado-en-colombia-2026/"),
    ("Salario de chef (promedio Colombia)", "$1.947.429", "Verificado", "Indeed Colombia (02-oct-2026)"),
    ("Salario del administrador", "2 SMMLV", "Estimación", "Sin dato público verificable para Cartagena"),
    ("Capacidad: puestos, rotación, utilización, platos por comensal", "56 / 3,5 / 50-80 % / 1,2", "Estimación", "Parámetros de diseño del equipo"),
    ("Calificaciones cualitativas de la microlocalización", "1-10", "Estimación", "Juicio del equipo (flujo turístico, proveedores, acceso, competencia, normativa)"),
    ("Precios de venta de Kazegami", "$40.000 / $38.000 / $38.000", "Decisión", "Método mixto: costo + food cost 28-35 % + precio de la competencia + disposición de pago"),
]


def escribir_fuentes(ruta: str) -> None:
    def tabla(cab, filas):
        out = ["| " + " | ".join(cab) + " |", "|" + "|".join([":---"] * len(cab)) + "|"]
        out += ["| " + " | ".join(str(x) for x in f) + " |" for f in filas]
        return "\n".join(out)

    eq = tabla_capex(EQUIPOS)
    mob = tabla_capex(MOBILIARIO_TEC)
    insumos = []
    vistos = set()
    for pl in PLATOS_TOP3:
        for i in RECETAS[pl]:
            if i.nombre in vistos:
                continue
            vistos.add(i.nombre)
            insumos.append((i.nombre, f"{cop(i.precio)}/{i.unidad}", "Verificado", i.fuente))
    n_v = sum(1 for f in FUENTES_GENERALES if f[2] == "Verificado") + len(insumos) + (eq["Estado"] == "Verificado").sum() + (mob["Estado"] == "Verificado").sum()
    n_e = sum(1 for f in FUENTES_GENERALES if f[2] == "Estimación") + (eq["Estado"] == "Estimado").sum() + (mob["Estado"] == "Estimado").sum()
    txt = [
        "# FUENTES Y VERIFICACIÓN DE LOS DATOS — KAZEGAMI",
        "",
        "> Generado por `scripts/analizar_encuesta.py` desde `scripts/modelo_kazegami.py`. Consultas realizadas el 24 de octubre de 2026.",
        "> **Verificado** = dato tomado de una fuente pública citada. **Estimación** = no existe dato público; valor razonado por el equipo con base en la investigación. **Decisión** = definición del proyecto.",
        "",
        f"**Resumen:** {n_v} datos verificados y {n_e} estimaciones.",
        "",
        "## 1. Mercado, demanda, oferta y operación",
        "",
        tabla(["Dato", "Valor", "Estado", "Fuente"], FUENTES_GENERALES),
        "",
        "## 2. Precios de insumos (recetas estándar)",
        "",
        tabla(["Insumo", "Precio", "Estado", "Fuente"], insumos),
        "",
        "## 3. Maquinaria y equipos",
        "",
        tabla(["Equipo", "Precio unitario", "Estado", "Fuente"], [(r["Ítem"], cop(r["Precio unitario"]), r["Estado"], r["Fuente"]) for _, r in eq.iterrows()]),
        "",
        "## 4. Mobiliario, adecuación y tecnología",
        "",
        tabla(["Ítem", "Precio unitario", "Estado", "Fuente"], [(r["Ítem"], cop(r["Precio unitario"]), r["Estado"], r["Fuente"]) for _, r in mob.iterrows()]),
        "",
        "## 5. Nómina",
        "",
        tabla(["Cargo", "Salario base", "Fuente"], [(c, cop(sv), f) for c, _, sv, f in NOMINA]),
        "",
        "## 6. Qué falta para que todo sea dato real (trabajo de campo)",
        "",
        "- Cotizar en tienda los equipos marcados como **Estimado** (congelador, quemador de caldos, extractor, trampa de grasa, pozuelo, ollas, utensilios, vajilla, mobiliario y tecnología).",
        "- Pedir presupuesto de obra para la adecuación del local.",
        "- Observar en 2 o 3 competidores cuántos platos venden en una hora pico, para reemplazar la estimación de 50 platos diarios.",
        "- Confirmar en Bazurto el rendimiento real del pargo al filetearlo.",
        "- Cotizar el software POS (Siigo, Alegra o Loggro) y la plataforma de reservas.",
    ]
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("\n".join(txt) + "\n")
