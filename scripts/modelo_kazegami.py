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
SUP = {
    # Fuentes secundarias verificadas
    "pob_2024": 1_010_408,            # DANE, proyecciones post-COVID (citado por Cartagena Cómo Vamos)
    "pob_2025": 1_011_520,            # DANE (El Universal, 13-ago-2025)
    "pob_2026": 1_010_995,            # DANE (El Universal, 13-ago-2025)
    "pob_2033": 998_638,              # DANE (El Universal, 13-ago-2025)
    "turistas_ext_2024": 855_744,     # Migración Colombia vía El Universal (16-mar-2026)
    "turistas_ext_2025": 866_264,     # idem (+1,22 %)
    "smmlv_2026": 1_750_905,          # Decreto 1469 de 2025
    "aux_transporte_2026": 249_095,
    "salmon_kg_sipsa": 56_463,        # SIPSA-DANE, filete de salmón congelado, oct-2026 (referencia)
    "crec_restaurantes_2024": 0.02,   # ACODRES (Portafolio, 23-feb-2025)
    # Supuestos del equipo (explícitos y modificables)
    "pct_adultos": 0.72,              # población de 18 años y más (estructura por edad DANE, aprox.)
    "pct_estratos_3a6": 0.30,         # población con capacidad de pago (estratos 3 a 6) – supuesto
    "pct_turistas_japonesa": 0.10,    # % de turistas extranjeros que consumen cocina japonesa en su estadía
    "platos_por_ocasion": 1.0,        # plato fuerte por ocasión de consumo
    "oferentes_2026": 45,             # establecimientos que venden sushi/ramen/tempura (relevamiento Tripadvisor/Wanderlog/Google Maps)
    "platos_dia_oferente": 50,        # platos/día de los 3 productos por establecimiento (promedio)
    "dias_oferente": 340,             # días de operación al año de la competencia
    "crec_oferta": 0.02,              # crecimiento anual de la oferta (ACODRES 2024)
}

ESCENARIOS = {  # crecimiento anual del consumo per cápita de los 3 platos
    "Pesimista": 0.01,
    "Base": 0.03,
    "Optimista": 0.05,
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
    precio: float     # COP por unidad de compra
    proveedor: str
    origen: str       # Caribe / Bolívar / Importado / Nacional
    tipo: str = "Costo (materia prima directa)"


RECETAS: dict[str, list[Insumo]] = {
    "Rollos de sushi": [  # 1 rollo = 8 piezas (≈ 260 g)
        Insumo("Arroz japonés de grano corto", 0.120, "kg", 22_000, "Importador de insumos japoneses (Bogotá/Barranquilla)", "Importado"),
        Insumo("Vinagre de arroz", 0.015, "L", 28_000, "Importador de insumos japoneses", "Importado"),
        Insumo("Azúcar y sal (sazón del shari)", 0.007, "kg", 4_500, "Distribuidor mayorista local", "Nacional"),
        Insumo("Alga nori (lámina)", 1, "und", 1_700, "Importador de insumos japoneses", "Importado"),
        Insumo("Atún aleta amarilla fresco (pesca artesanal)", 0.045, "kg", 48_000, "Pescadores artesanales – Mercado de Bazurto / Mercado del Mar", "Caribe"),
        Insumo("Langostino del Caribe (pelado)", 0.025, "kg", 55_000, "Pescadería del Mercado del Mar", "Caribe"),
        Insumo("Aguacate (Montes de María)", 0.030, "kg", 9_000, "Agricultores de Bolívar", "Bolívar"),
        Insumo("Pepino", 0.020, "kg", 4_000, "Agricultores de Bolívar", "Bolívar"),
        Insumo("Mango de azúcar (toque caribeño)", 0.015, "kg", 6_000, "Agricultores de Bolívar", "Bolívar"),
        Insumo("Queso crema", 0.020, "kg", 26_000, "Distribuidor de lácteos", "Nacional"),
        Insumo("Ajonjolí tostado", 0.003, "kg", 30_000, "Distribuidor mayorista local", "Nacional"),
        Insumo("Salsa de soya", 0.015, "L", 25_000, "Importador de insumos japoneses", "Importado"),
        Insumo("Wasabi en pasta", 0.003, "kg", 150_000, "Importador de insumos japoneses", "Importado"),
        Insumo("Jengibre encurtido (gari)", 0.010, "kg", 45_000, "Importador de insumos japoneses", "Importado"),
        Insumo("Salsas de la casa (anguila / spicy mayo)", 0.010, "L", 30_000, "Elaboración propia (insumos nacionales)", "Nacional"),
    ],
    "Ramen": [  # 1 bowl ≈ 650 ml
        Insumo("Fideo ramen (alcalino)", 0.120, "kg", 26_000, "Importador de insumos japoneses", "Importado"),
        Insumo("Huesos de cerdo y pollo para caldo", 0.250, "kg", 9_000, "Expendio de carnes – Bazurto", "Bolívar"),
        Insumo("Panceta de cerdo (chashu)", 0.060, "kg", 32_000, "Expendio de carnes – Bazurto", "Bolívar"),
        Insumo("Huevo (ajitama)", 1, "und", 650, "Avícola regional", "Bolívar"),
        Insumo("Miso", 0.020, "kg", 40_000, "Importador de insumos japoneses", "Importado"),
        Insumo("Salsa de soya", 0.020, "L", 25_000, "Importador de insumos japoneses", "Importado"),
        Insumo("Mirin", 0.010, "L", 38_000, "Importador de insumos japoneses", "Importado"),
        Insumo("Alga nori (½ lámina)", 0.5, "und", 1_700, "Importador de insumos japoneses", "Importado"),
        Insumo("Cebollín", 0.010, "kg", 8_000, "Agricultores de Bolívar", "Bolívar"),
        Insumo("Brotes de soya / maíz tierno", 0.030, "kg", 10_000, "Agricultores de Bolívar", "Bolívar"),
        Insumo("Ajo y jengibre frescos", 0.010, "kg", 12_000, "Agricultores de Bolívar", "Bolívar"),
        Insumo("Aceite de ajonjolí", 0.005, "L", 60_000, "Importador de insumos japoneses", "Importado"),
    ],
    "Tempura": [  # porción mixta: 5 langostinos + vegetales
        Insumo("Langostino del Caribe (con cola)", 0.120, "kg", 55_000, "Pescadería del Mercado del Mar", "Caribe"),
        Insumo("Vegetales (berenjena, ahuyama, batata, cebolla)", 0.100, "kg", 5_000, "Agricultores de Bolívar", "Bolívar"),
        Insumo("Harina para tempura", 0.050, "kg", 22_000, "Importador de insumos japoneses", "Importado"),
        Insumo("Fécula de maíz", 0.015, "kg", 10_000, "Distribuidor mayorista local", "Nacional"),
        Insumo("Huevo (½ unidad)", 0.5, "und", 650, "Avícola regional", "Bolívar"),
        Insumo("Aceite vegetal para freír (consumo + reposición)", 0.060, "L", 12_000, "Distribuidor mayorista local", "Nacional"),
        Insumo("Dashi en polvo (salsa tentsuyu)", 0.003, "kg", 120_000, "Importador de insumos japoneses", "Importado"),
        Insumo("Salsa de soya", 0.010, "L", 25_000, "Importador de insumos japoneses", "Importado"),
        Insumo("Mirin", 0.010, "L", 38_000, "Importador de insumos japoneses", "Importado"),
        Insumo("Rábano / daikon rallado", 0.020, "kg", 8_000, "Agricultores de Bolívar", "Bolívar"),
    ],
}

PRECIO_VENTA = {"Rollos de sushi": 40_000, "Ramen": 38_000, "Tempura": 34_000}  # COP, impoconsumo 8 % incluido
IMPOCONSUMO = 0.08

# Activos específicos de cada línea (para la fila de depreciación del formato Punto 6)
ACTIVOS_PLATO = {
    "Rollos de sushi": [("Vitrina refrigerada de barra (neta) 1,5 m", 1, 7_500_000),
                        ("Arrocera industrial a gas 10 L", 2, 1_900_000),
                        ("Set de cuchillos japoneses (yanagiba, deba, usuba)", 2, 1_800_000),
                        ("Esterillas makisu y utensilios de barra", 1, 900_000)],
    "Ramen": [("Quemador de piso para caldos + marmita 60 L", 1, 2_800_000),
              ("Ollas de acero inoxidable 60 L", 3, 650_000),
              ("Bowls de cerámica para ramen", 60, 38_000)],
    "Tempura": [("Freidora industrial a gas doble cuba 2×20 L", 1, 5_200_000),
                ("Utensilios de fritura (canastas, rejillas, termómetro)", 1, 650_000)],
}
VIDA_UTIL_ANIOS = 10  # maquinaria y equipo / muebles (Decreto 1625/2016 art. 1.2.1.18.4 – tasa 10 %)

# Costos o gastos de servicio asignados a cada línea (mensual, año 2027)
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
EQUIPOS = [  # (ítem, cantidad, precio unitario, área, vida útil años)
    ("Ultracongelador / abatidor de temperatura (−40 °C) para pescado crudo", 1, 28_000_000, "Refrigeración", 10),
    ("Nevera vertical industrial 2 puertas acero inoxidable", 2, 9_800_000, "Refrigeración", 10),
    ("Mesa refrigerada de preparación con bandejas GN", 2, 8_500_000, "Refrigeración", 10),
    ("Congelador horizontal 500 L", 1, 3_900_000, "Refrigeración", 10),
    ("Vitrina refrigerada de barra de sushi (neta) 1,5 m", 1, 7_500_000, "Barra", 10),
    ("Fabricador de hielo 150 kg/día", 1, 6_800_000, "Barra", 10),
    ("Nevera exhibidora de bebidas", 1, 4_200_000, "Barra", 10),
    ("Arrocera industrial a gas 10 L", 2, 1_900_000, "Cocina", 10),
    ("Estufa industrial 6 puestos con horno", 1, 6_500_000, "Cocina", 10),
    ("Quemador de piso para caldos + marmita 60 L", 1, 2_800_000, "Cocina", 10),
    ("Freidora industrial a gas doble cuba 2×20 L", 1, 5_200_000, "Cocina", 10),
    ("Campana extractora en acero inoxidable 3 m con motor", 1, 14_000_000, "Cocina", 10),
    ("Trampa de grasas en acero inoxidable", 1, 2_500_000, "Cocina", 10),
    ("Mesas de trabajo en acero inoxidable", 4, 1_300_000, "Cocina", 10),
    ("Pozuelo triple de lavado en acero inoxidable", 1, 3_200_000, "Cocina", 10),
    ("Ollas de acero inoxidable 60 L", 3, 650_000, "Cocina", 10),
    ("Balanzas digitales de precisión", 2, 350_000, "Control de calidad", 10),
    ("Termómetros de punzón y data loggers de temperatura", 4, 180_000, "Control de calidad", 10),
    ("Set de cuchillos japoneses (yanagiba, deba, usuba)", 2, 1_800_000, "Barra", 10),
    ("Utensilios menores (makisu, bandejas GN, coladores, tablas)", 1, 3_500_000, "Cocina", 10),
    ("Vajilla japonesa (platos, bowls de ramen, palillos reutilizables)", 1, 9_000_000, "Sala", 10),
    ("Planta eléctrica diésel 20 kVA (respaldo de cadena de frío)", 1, 32_000_000, "Respaldo", 10),
]

MOBILIARIO_TEC = [  # (ítem, cantidad, precio unitario, categoría, vida útil)
    ("Adecuación del local (obra civil, pisos, baños, redes de gas y eléctricas)", 1, 85_000_000, "Adecuación", 5),
    ("Barra de sushi en madera para 8 comensales", 1, 12_000_000, "Mobiliario", 10),
    ("Mesas de madera para 4 personas", 12, 650_000, "Mobiliario", 10),
    ("Sillas de comedor", 48, 280_000, "Mobiliario", 10),
    ("Bancos altos de barra", 8, 350_000, "Mobiliario", 10),
    ("Aire acondicionado tipo minisplit 24.000 BTU", 4, 4_500_000, "Adecuación", 10),
    ("Iluminación y decoración de inspiración japonesa", 1, 15_000_000, "Adecuación", 5),
    ("Aviso exterior y señalización", 1, 4_500_000, "Adecuación", 5),
    ("Sistema de sonido ambiental", 1, 2_800_000, "Mobiliario", 10),
    ("Computador administrativo", 1, 3_200_000, "Tecnología", 5),
    ("Tablets comanderas para meseros", 3, 1_100_000, "Tecnología", 5),
    ("Impresoras térmicas de comandas y facturas", 3, 650_000, "Tecnología", 5),
    ("Cajón monedero y lector de código", 1, 550_000, "Tecnología", 5),
    ("Red WiFi y router empresarial", 1, 900_000, "Tecnología", 5),
    ("UPS para POS y red", 1, 1_200_000, "Tecnología", 5),
    ("Kit de cámaras de seguridad (4 cámaras + grabador)", 1, 2_200_000, "Tecnología", 5),
]

SOFTWARE_ANUAL = [  # (servicio, costo anual) – gasto, no activo
    ("Software POS para restaurantes con facturación electrónica DIAN (licencia anual)", 2_400_000),
    ("Plataforma de reservas en línea + WhatsApp Business API (anual)", 1_800_000),
    ("Módulo de inventarios y recetas estándar (anual)", 1_200_000),
    ("Dominio, página web y correo corporativo (anual)", 900_000),
]

NOMINA = [  # (cargo, cantidad, salario base mensual)
    ("Chef ejecutivo / sushiman principal", 1, 4_500_000),
    ("Sushiman auxiliar (barra)", 1, 2_600_000),
    ("Cocinero de línea caliente (ramen y tempura)", 2, 2_200_000),
    ("Auxiliar de cocina y steward", 2, 1_750_905),
    ("Meseros", 4, 1_750_905),
    ("Anfitrión(a) y cajero(a)", 1, 1_900_000),
    ("Administrador(a)", 1, 3_800_000),
]
FACTOR_PRESTACIONAL = 1.52  # seguridad social, parafiscales y prestaciones sociales

OPEX_MENSUAL = [  # (concepto, valor mensual)
    ("Arriendo del local (≈ 200 m² en Manga)", 11_000_000),
    ("Energía eléctrica (Afinia)", 3_200_000),
    ("Agua y alcantarillado (Aguas de Cartagena)", 650_000),
    ("Gas natural (Gases del Caribe)", 1_100_000),
    ("Internet y telefonía", 250_000),
    ("Marketing digital y pauta en redes", 2_500_000),
    ("Aseo, fumigación y control de plagas", 450_000),
    ("Mantenimiento de equipos", 600_000),
    ("Seguros (todo riesgo y responsabilidad civil)", 550_000),
    ("Derechos de autor por música (Sayco–Acinpro / OSA)", 120_000),
]


def tabla_capex(lista) -> pd.DataFrame:
    df = pd.DataFrame(lista, columns=["Ítem", "Cantidad", "Precio unitario", "Categoría", "Vida útil (años)"])
    df["Total"] = df["Cantidad"] * df["Precio unitario"]
    df["Depreciación mensual"] = df["Total"] / (df["Vida útil (años)"] * 12)
    return df


def nomina_mensual() -> pd.DataFrame:
    df = pd.DataFrame(NOMINA, columns=["Cargo", "Cantidad", "Salario base"])
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
FACTORES_LOC = [  # (factor, peso, {zona: calificación 1-10}, justificación)
    ("Preferencia de los encuestados", 0.25,
     {"Centro Histórico": 10, "Manga": 5, "Bocagrande": 3, "Getsemaní": 2},
     "Votos de la encuesta: 33 / 17 / 10 / 8"),
    ("Costo de arriendo por m²", 0.20,
     {"Centro Histórico": 3, "Manga": 8, "Bocagrande": 4, "Getsemaní": 6},
     "Mayor puntaje = arriendo más bajo"),
    ("Flujo de turistas y ejecutivos", 0.15,
     {"Centro Histórico": 10, "Manga": 5, "Bocagrande": 9, "Getsemaní": 8},
     "Cercanía a hoteles, centro de convenciones y oficinas"),
    ("Cercanía a proveedores (Bazurto, Mercado del Mar)", 0.10,
     {"Centro Histórico": 7, "Manga": 9, "Bocagrande": 6, "Getsemaní": 8},
     "Menor tiempo de traslado del pescado fresco"),
    ("Accesibilidad y parqueadero", 0.10,
     {"Centro Histórico": 4, "Manga": 8, "Bocagrande": 7, "Getsemaní": 5},
     "Vías, parqueo y acceso para proveedores"),
    ("Saturación de la competencia (menor = mejor)", 0.10,
     {"Centro Histórico": 4, "Manga": 6, "Bocagrande": 4, "Getsemaní": 6},
     "Número de restaurantes japoneses/nikkei cercanos"),
    ("Restricciones normativas para adecuar cocina (PEMP / POT)", 0.10,
     {"Centro Histórico": 4, "Manga": 8, "Bocagrande": 7, "Getsemaní": 5},
     "Centro y Getsemaní son zona patrimonial: limita extracción de humos y obras"),
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
