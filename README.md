# Kazegami Restaurante · Estudios de Mercado y Técnico (Docs-as-Code)

Repositorio del grupo para el **Seminario Taller Creación de Empresas** (Universidad de Cartagena, profesora Carla del Carmen de Ávila Altamiranda). Los dos documentos se escriben en **Markdown**, se versionan con **Git** y se compilan a **Word** con **Pandoc**.

> **Entrega:** 25 de octubre de 2026 hasta las 11:59 p. m., al correo cdeavilaa@unicartagena.edu.co.
> Los Word listos están en `entregables_word/`.

## Clonar el repositorio (primera vez)

```bash
git clone https://github.com/TheOnemoxh/kazegami-estudios.git
cd kazegami-estudios
```

Acepta primero la invitación de colaborador que te llegó al correo de GitHub; sin ella no podrás hacer `git push`.

> La carpeta `EjemploDeOtroGrupo/` **no se sube** al repositorio público porque trae nombres y códigos de estudiantes de otro grupo. Si la necesitas, pídela por WhatsApp y cópiala dentro de tu carpeta local (Git la ignora).

## Estructura

| Carpeta / archivo | Qué contiene |
|:---|:---|
| `EjemploDeOtroGrupo/` | Referencia de otro grupo (solo local, no se publica; no copiar) |
| `FormatoDocumentos/` | Guías oficiales Taller No. 1 y No. 2 |
| `ModeloCanvasNuestraIdeaNegocio/` | Canvas de Kazegami |
| `ResultadosEncuesta/` | Excel con las 106 respuestas |
| `Punto6EstudioTecnicoImg/` | Fotos del tablero: formato de las tablas de insumos y factores de la oferta |
| `CONTEXTO_GLOBAL.md` | **Verdad del proyecto**: Top 3 platos, Canvas, cifras clave, formato Punto 6 y estilo |
| `CLAUDE.md` y `.cursorrules` | Reglas para la IA de cada integrante |
| `datos/RESUMEN_ENCUESTA.md` | Tablas de frecuencia de las 31 columnas y cruces (generado) |
| `datos/MODELO_PROYECCIONES.md` | Demanda, oferta, capacidad y costos (generado) |
| `assets/graficas/` | 36 gráficas PNG a 300 DPI (generadas) |
| `assets/diagramas/` | Diagramas de flujo, layout y canal de distribución (generados) |
| `assets/plantillas/` | Plantilla Word con estilos académicos |
| `01_estudio_mercado/` | **Documento 1**: Taller No. 1 Estudio de Mercados |
| `02_estudio_tecnico/` | **Documento 2**: Taller No. 2 Estudio Técnico |
| `scripts/` | Análisis, modelo, diagramas, plantilla y compilación |
| `entregables_word/` | Los `.docx` finales para enviar |

## Asignación de archivos por integrante

| Integrante | Archivos a cargo | Revisa además |
|:---|:---|:---|
| **Adrian Alberto Angulo Melgarejo** | `01_estudio_mercado/00_portada_e_introduccion.md`, `01_objetivos.md`, `02_identificacion_servicio.md` | Legislación (3.13) |
| **Samuel David Molina Romero** | `01_estudio_mercado/03_analisis_demanda.md`, `scripts/`, `datos/`, compilación final | Cifras de todo el repositorio |
| **Edwin Esteban Cañas Jurado** | `01_estudio_mercado/04_analisis_oferta.md`, `05_precio_comercializacion.md`, `99_bibliografia_y_anexos.md` | Competencia y precios |
| **Alejandro Jose Vergara Parra** | `02_estudio_tecnico/00_portada_y_objetivos.md`, `01_localizacion_y_tamano.md`, `02_proceso_productivo.md` | Diagramas (`scripts/generar_diagramas.py`) |
| **Carlos Arturo Rodriguez Cochero** | `02_estudio_tecnico/03_disponibilidad_insumos.md`, `04_costos_tecnicos.md`, `99_bibliografia.md` | Tablas Punto 6 y cotizaciones |

## Instalación (una sola vez)

| Herramienta | Windows | macOS / Linux |
|:---|:---|:---|
| Git | `winget install Git.Git` | `brew install git` / `sudo apt install git` |
| Python 3.10+ | `winget install Python.Python.3.12` | `brew install python` |
| Pandoc | `winget install JohnMacFarlane.Pandoc` | `brew install pandoc` / `sudo apt install pandoc` |
| Graphviz (diagramas) | `winget install Graphviz.Graphviz` | `brew install graphviz` / `sudo apt install graphviz` |
| Librerías Python | `pip install pandas openpyxl matplotlib seaborn python-docx` | igual |

## Flujo de trabajo con Git

```bash
git pull                                   # 1. trae lo último del grupo
git checkout -b mercado-oferta-edwin       # 2. (opcional) rama propia
# 3. edita SOLO tus archivos .md
python scripts/compilar_word.py            # 4. compila y verifica (debe decir TODO OK)
git add 01_estudio_mercado/04_analisis_oferta.md
git commit -m "docs(mercado): actualiza matriz de competidores"
git push                                   # 5. sube tus cambios
```

Si dos personas tocan el mismo archivo y aparece un conflicto, resuélvanlo juntos: no borren el trabajo del otro.

## Cómo regenerar todo

```bash
python scripts/analizar_encuesta.py        # encuesta → datos/*.md + 36 gráficas
python scripts/generar_diagramas.py        # diagramas de flujo, layout y canal
python scripts/generar_plantilla_word.py   # plantilla Word (solo si se borra)
python scripts/compilar_word.py            # Markdown → 2 Word en entregables_word/
python scripts/compilar_word.py --pdf      # opcional: también PDF (requiere LibreOffice)
```

Al abrir cada Word, acepta **"Actualizar campos"** para que aparezca la tabla de contenido con los números de página.

## Reglas del contenido (resumen)

1. Solo **Rollos de sushi, Ramen y Tempura** en fichas, procesos, insumos, costos, precios y proyecciones.
2. Ninguna estadística inventada: encuesta → `datos/RESUMEN_ENCUESTA.md`; modelo → `scripts/modelo_kazegami.py`.
3. Tablas de insumos con el formato del Punto 6 (ver `CONTEXTO_GLOBAL.md`, sección 6).
4. Tablas y gráficas antes que texto.
5. Normas APA 7 (Times New Roman 12, doble espacio, títulos y tablas en negro, notas con *Nota.*). El formato lo aplica el compilador automáticamente.
