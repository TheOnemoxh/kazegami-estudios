# -*- coding: utf-8 -*-
"""
generar_diagramas.py
====================
Genera los diagramas del Estudio Técnico y de Comercialización en assets/diagramas/:

  * d01_flujo_rollos_sushi.png   · Diagrama de flujo del proceso de Rollos de sushi
  * d02_flujo_ramen.png          · Diagrama de flujo del proceso de Ramen
  * d03_flujo_tempura.png        · Diagrama de flujo del proceso de Tempura
  * d04_flujo_servicio.png       · Prestación del servicio en sala y barra
  * d05_layout_local.png         · Distribución en planta (layout) del local de 200 m²
  * d06_canal_distribucion.png   · Cadena de abastecimiento y canal de distribución

Requiere Graphviz (comando `dot`) y matplotlib.
Uso: python scripts/generar_diagramas.py
"""
from __future__ import annotations

import os
import shutil
import subprocess

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(RAIZ, "assets", "diagramas")
os.makedirs(OUT, exist_ok=True)

AZUL, NARANJA, AQUA, AMARILLO, GRIS, TINTA = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#b8b6ae", "#2b2b2b"

# Simbología ASME para cursogramas
TIPOS = {
    "O": ("○  Operación", "ellipse", "#d6e6f8", AZUL),
    "I": ("□  Inspección / control", "box", "#fde3d6", NARANJA),
    "T": ("⇨  Transporte", "cds", "#e3e1da", "#7a776e"),
    "D": ("D  Demora / espera", "box", "#fff1cc", AMARILLO),
    "A": ("▽  Almacenamiento", "box", "#d4f1e5", AQUA),
}


def flujo(nombre: str, titulo: str, pasos: list[tuple[str, str]]):
    """pasos: [(tipo, texto)] → diagrama vertical en dos columnas (zig-zag) para que quepa en la página."""
    lineas = [
        "digraph G {",
        'graph [rankdir=TB, splines=ortho, nodesep=0.35, ranksep=0.28, bgcolor="white", fontname="Liberation Sans", '
        f'label=<<B>{titulo}</B>>, labelloc=t, fontsize=18, pad=0.3, dpi=300];',
        'node [fontname="Liberation Sans", fontsize=11, width=3.2, height=0.55, style="filled,rounded", penwidth=1.6, margin="0.12,0.06"];',
        'edge [color="#52514e", penwidth=1.3, arrowsize=0.8];',
    ]
    mitad = (len(pasos) + 1) // 2
    for i, (t, txt) in enumerate(pasos):
        nombre_t, forma, fill, borde = TIPOS[t]
        estilo = '"filled"' if forma in ("invtriangle", "cds") else '"filled,rounded"'
        w, h = "3.2", "0.55"
        label = f"{nombre_t.split()[0]}  {i + 1}. {txt}"
        lineas.append(f'n{i} [label="{label}", shape={forma}, fillcolor="{fill}", color="{borde}", style={estilo}, width={w}, height={h}];')
    # dos columnas
    lineas.append("subgraph cluster_a { style=invis; " + " ".join(f"n{i};" for i in range(mitad)) + " }")
    lineas.append("subgraph cluster_b { style=invis; " + " ".join(f"n{i};" for i in range(mitad, len(pasos))) + " }")
    for i in range(len(pasos) - 1):
        if i == mitad - 1:
            lineas.append(f"n{i} -> n{i + 1} [constraint=false];")
        else:
            lineas.append(f"n{i} -> n{i + 1};")
    for i in range(1, mitad):
        if mitad + i < len(pasos) + 1:
            pass
    # Leyenda
    ley = "".join(
        f'<TR><TD BGCOLOR="{v[2]}" BORDER="1" COLOR="{v[3]}" WIDTH="18"> </TD><TD ALIGN="LEFT"> {v[0]}</TD></TR>' for v in TIPOS.values())
    lineas.append(f'leyenda [shape=plaintext, style="", label=<<TABLE BORDER="0" CELLSPACING="3"><TR><TD COLSPAN="2" ALIGN="LEFT"><B>Simbología ASME</B></TD></TR>{ley}</TABLE>>];')
    lineas.append(f"n{len(pasos) - 1} -> leyenda [style=invis];")
    lineas.append("}")
    dot = "\n".join(lineas)
    ruta_dot = os.path.join(OUT, nombre.replace(".png", ".dot"))
    with open(ruta_dot, "w", encoding="utf-8") as f:
        f.write(dot)
    subprocess.run(["dot", "-Tpng", ruta_dot, "-o", os.path.join(OUT, nombre)], check=True)
    os.remove(ruta_dot)


PROCESO_SUSHI = [
    ("T", "Recepción del pescado, martes y viernes (Bazurto / Mercado del Mar)"),
    ("I", "Control de recepción: T° ≤ 4 °C, olor, ojos, agallas"),
    ("O", "Eviscerado, fileteado y porcionado del pargo"),
    ("A", "Ultracongelación −35 °C × 15 h (control de parásitos)"),
    ("A", "Congelado −18 °C; descongelado diario 0-4 °C (PEPS)"),
    ("O", "Lavado del arroz japonés (3-4 aguas)"),
    ("D", "Reposo del arroz 30 min"),
    ("O", "Cocción del arroz en arrocera (20 min)"),
    ("O", "Sazonado del shari con vinagre y enfriado a 35 °C"),
    ("O", "Corte de vegetales y mise en place de barra"),
    ("O", "Armado del rollo (nori + shari + relleno) en makisu"),
    ("O", "Corte en 10 piezas y emplatado"),
    ("I", "Control de calidad del sushiman (forma, T°, presentación)"),
    ("T", "Entrega en barra o pase a mesa"),
]

PROCESO_RAMEN = [
    ("T", "Recepción de huesos, panceta y vegetales"),
    ("I", "Control de recepción: T° cárnicos ≤ 4 °C"),
    ("O", "Blanqueado de huesos (10 min) y lavado"),
    ("O", "Cocción del caldo a fuego lento (10-12 h)"),
    ("O", "Colado, desgrasado y ajuste del tare (soya/miso)"),
    ("A", "Enfriamiento rápido y refrigeración del caldo ≤ 4 °C"),
    ("O", "Marinado del huevo (ajitama) 12 h y horneado del chashu"),
    ("O", "Calentamiento del caldo al momento (≥ 85 °C)"),
    ("O", "Cocción del fideo 90 segundos y escurrido"),
    ("O", "Ensamble del bowl: tare + caldo + fideo + toppings"),
    ("I", "Control de calidad: T° ≥ 75 °C al servir y presentación"),
    ("T", "Pase a mesa en menos de 2 minutos"),
]

PROCESO_TEMPURA = [
    ("T", "Recepción de langostinos y vegetales"),
    ("I", "Control de recepción: langostino ≤ 4 °C, sin manchas"),
    ("O", "Pelado, desvenado y corte del langostino"),
    ("O", "Lavado, desinfección y corte de vegetales"),
    ("A", "Refrigeración de porciones (0-4 °C)"),
    ("O", "Preparación del batido con agua helada (al momento)"),
    ("I", "Control de T° del aceite (170-180 °C)"),
    ("O", "Rebozado y fritura (2-3 min por tanda)"),
    ("O", "Escurrido sobre rejilla y papel absorbente"),
    ("O", "Emplatado con salsa tentsuyu y rábano"),
    ("I", "Control de calidad: crocancia y color dorado claro"),
    ("T", "Pase a mesa inmediato"),
]

SERVICIO = [
    ("O", "Reserva por WhatsApp / plataforma web"),
    ("O", "Recepción y bienvenida del anfitrión"),
    ("T", "Ubicación en mesa o barra de sushi"),
    ("O", "Presentación de la carta (Top 3) y toma de pedido en tablet"),
    ("T", "Comanda digital a cocina y barra (POS)"),
    ("D", "Preparación de platos (12-20 min)"),
    ("T", "Servicio a la mesa"),
    ("I", "Verificación de satisfacción (2 min después)"),
    ("O", "Factura electrónica y cobro (tarjeta, QR, efectivo)"),
    ("O", "Despedida, invitación a reseña y fidelización"),
]


def layout_local():
    zonas = [  # (nombre, x, y, w, h, color)
        ("Salón comedor\n12 mesas × 4 = 48 puestos", 0, 0, 9, 8, "#d6e6f8"),
        ("Recepción\ny espera", 0, 8, 4, 2, "#e3e1da"),
        ("Barra de bebidas\ny caja", 4, 8, 5, 2, "#fde3d6"),
        ("Circulación", 9, 0, 1.5, 10, "#f5f4f0"),
        ("Barra de sushi\n8 puestos (a la vista)", 10.5, 6, 4.5, 4, "#fbd2bf"),
        ("Preparación fría\n(mise en place)", 10.5, 3, 4.5, 3, "#d4f1e5"),
        ("Baños", 10.5, 0, 2.7, 3, "#e3e1da"),
        ("Oficina", 13.2, 0, 1.8, 3, "#e3e1da"),
        ("Cocina caliente\n(ramen y tempura)", 15, 5, 5, 5, "#fff1cc"),
        ("Cuarto frío y\nalmacén seco", 15, 2.6, 5, 2.4, "#c9e4f7"),
        ("Zona de lavado\n(steward)", 15, 0, 5, 2.6, "#e9e7f7"),
    ]
    fig, ax = plt.subplots(figsize=(10, 5.0))
    for nombre, x, y, w, h, c in zonas:
        ax.add_patch(Rectangle((x, y), w, h, facecolor=c, edgecolor=TINTA, lw=1.4))
        if nombre != "Circulación":
            dx = 0.35 if nombre.startswith("Barra de sushi") else 0
            ax.text(x + w / 2 + dx, y + h - 0.35, nombre, ha="center", va="top", fontsize=8.2, color=TINTA, fontweight="bold")
            ax.text(x + w / 2, y + 0.25, f"{w * h:.1f} m²".replace(".", ","), ha="center", va="bottom", fontsize=7.5, color="#52514e")
        else:
            ax.text(x + w / 2, y + h / 2, "Circulación  15 m²", rotation=90, ha="center", va="center", fontsize=8, color="#52514e")
    # mesas
    for i in range(4):
        for j in range(3):
            cx, cy = 1.3 + i * 2.1, 1.4 + j * 2.0
            ax.add_patch(Rectangle((cx - 0.45, cy - 0.45), 0.9, 0.9, facecolor="white", edgecolor=AZUL, lw=1))
            for dx, dy in [(-0.65, 0), (0.65, 0), (0, -0.65), (0, 0.65)]:
                ax.add_patch(Circle((cx + dx, cy + dy), 0.14, facecolor=AZUL, edgecolor="none"))
    # barra de sushi
    ax.add_patch(Rectangle((10.7, 6.15), 0.45, 3.3, facecolor="#8a5a2b", edgecolor="none"))
    for k in range(8):
        ax.add_patch(Circle((10.6 - 0.05, 6.35 + k * 0.42), 0.12, facecolor=NARANJA, edgecolor="none"))
    # puerta
    ax.annotate("Entrada principal", xy=(2, 10), xytext=(2, 11.0), ha="center", fontsize=8.5,
                arrowprops=dict(arrowstyle="->", color=TINTA))
    ax.annotate("Ingreso de proveedores", xy=(20, 1.3), xytext=(21.6, 1.3), va="center", ha="left", fontsize=8.5,
                arrowprops=dict(arrowstyle="->", color=TINTA))
    ax.set_xlim(-0.5, 25)
    ax.set_ylim(-0.6, 11.6)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Distribución en planta del local Kazegami (≈ 200 m², 20 m × 10 m)", loc="left", fontsize=12, fontweight="bold")
    fig.text(0.01, 0.06, "Escala aproximada. Flujo unidireccional: proveedores → almacén → preparación → cocina/barra → salón. "
             "Elaboración propia.", fontsize=7.5, color="#52514e")
    fig.savefig(os.path.join(OUT, "d05_layout_local.png"), dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return [(z[0].replace("\n", " "), round(z[3] * z[4], 1)) for z in zonas]


def canal_distribucion():
    dot = r'''
digraph G {
graph [rankdir=LR, bgcolor="white", fontname="Liberation Sans", nodesep=0.25, ranksep=0.6, dpi=300,
       label=<<B>Cadena de abastecimiento y canal de distribución directo de Kazegami</B>>, labelloc=t, fontsize=16, pad=0.3];
node [fontname="Liberation Sans", fontsize=11, shape=box, style="filled,rounded", penwidth=1.4, margin="0.15,0.08"];
edge [color="#52514e", penwidth=1.3];
subgraph cluster_p { label=<<B>Proveedores (socios clave)</B>>; style="rounded,dashed"; color="#b8b6ae"; fontsize=12;
  p1 [label="Pesca artesanal del Caribe\n(Bazurto / Mercado del Mar)", fillcolor="#d4f1e5", color="#1baf7a"];
  p2 [label="Agricultores de Bolívar\n(Montes de María, Turbaco)", fillcolor="#d4f1e5", color="#1baf7a"];
  p3 [label="Importadores de insumos\njaponeses (arroz, nori, soya)", fillcolor="#d6e6f8", color="#2a78d6"];
  p4 [label="Empaques, bebidas\ny medios de pago", fillcolor="#e3e1da", color="#7a776e"];
}
r [label="Recepción e inspección\ncadena de frío 0-4 °C / −35 °C", fillcolor="#fde3d6", color="#eb6834"];
k [label="Producción en cocina\ny barra de sushi\n(Rollos · Ramen · Tempura)", fillcolor="#fbd2bf", color="#eb6834"];
s [label="Servicio en sala y barra\n(único punto en Cartagena)", fillcolor="#fde3d6", color="#eb6834"];
c [label="Cliente final\n(residentes y turistas)", shape=ellipse, fillcolor="#2a78d6", fontcolor="white", color="#2a78d6"];
subgraph cluster_m { label=<<B>Promoción y reservas</B>>; style="rounded,dashed"; color="#b8b6ae"; fontsize=12;
  m1 [label="Instagram · TikTok", fillcolor="#fff1cc", color="#eda100"];
  m2 [label="Google Maps · TripAdvisor", fillcolor="#fff1cc", color="#eda100"];
  m3 [label="WhatsApp Business\n(reservas)", fillcolor="#fff1cc", color="#eda100"];
  m4 [label="Hoteles y agencias\nturísticas (alianzas)", fillcolor="#fff1cc", color="#eda100"];
}
p1 -> r; p2 -> r; p3 -> r; p4 -> r;
r -> k -> s -> c [penwidth=2.2, color="#eb6834"];
m1 -> c [style=dashed]; m2 -> c [style=dashed]; m3 -> c [style=dashed]; m4 -> c [style=dashed];
}
'''
    ruta = os.path.join(OUT, "d06.dot")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(dot)
    subprocess.run(["dot", "-Tpng", ruta, "-o", os.path.join(OUT, "d06_canal_distribucion.png")], check=True)
    os.remove(ruta)


def main():
    if not shutil.which("dot"):
        raise SystemExit("Falta Graphviz: instala 'graphviz' (sudo apt install graphviz / winget install graphviz)")
    flujo("d01_flujo_rollos_sushi.png", "Diagrama de flujo · Proceso productivo de Rollos de sushi", PROCESO_SUSHI)
    flujo("d02_flujo_ramen.png", "Diagrama de flujo · Proceso productivo de Ramen", PROCESO_RAMEN)
    flujo("d03_flujo_tempura.png", "Diagrama de flujo · Proceso productivo de Tempura", PROCESO_TEMPURA)
    flujo("d04_flujo_servicio.png", "Diagrama de flujo · Prestación del servicio en sala y barra", SERVICIO)
    areas = layout_local()
    canal_distribucion()
    print("OK · diagramas en assets/diagramas/")
    for a in areas:
        print(a)


if __name__ == "__main__":
    main()
