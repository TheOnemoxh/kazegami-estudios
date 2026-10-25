# Reglas para cualquier IA que trabaje en este repositorio (Kazegami)

Este repositorio genera dos documentos académicos en Word a partir de Markdown (Docs-as-Code). Lo editan 5 personas, cada una con su propia IA. Estas reglas son obligatorias.

## Antes de editar

1. **Lee primero** `CONTEXTO_GLOBAL.md`, `datos/RESUMEN_ENCUESTA.md` y `datos/FUENTES_Y_VERIFICACION.md` (qué está verificado y qué es estimación). Si vas a tocar cifras de demanda, oferta, capacidad o costos, lee también `datos/MODELO_PROYECCIONES.md`.
2. Haz `git pull` y revisa en `README.md` qué archivos le corresponden a la persona que te está pidiendo el cambio. No edites archivos de otro integrante sin que te lo pidan.

## Reglas de contenido (no negociables)

- **Solo 3 platos:** Rollos de sushi (61 menciones), Ramen (40) y Tempura (35). Ninguna ficha técnica, proceso, receta, tabla de insumos, costo, precio ni proyección puede incluir otros platos.
- **Prohibido inventar estadísticas.** Toda cifra de la encuesta debe salir de `datos/RESUMEN_ENCUESTA.md` (n = 106). Toda cifra del modelo debe salir de `scripts/modelo_kazegami.py`. Un dato externo nuevo necesita fuente verificable en APA 7; un supuesto se escribe como "supuesto del equipo".
- **Tablas de insumos con el formato de `Punto6EstudioTecnicoImg/`**: columnas `Insumos | Cantidad por mes | Proveedor (precio · calidad · postventa) | Precio | Total | Identificación del elemento | Total final`; los activos entran por depreciación = valor ÷ (vida útil × 12); costo unitario = total final ÷ unidades del mes.
- **Tablas y gráficos antes que párrafos.** El texto introduce y analiza; no repite lo que ya dice la tabla.
- **Redacción de los documentos:** cada tabla lleva un párrafo introductorio antes y un párrafo de cierre después (con la influencia en las decisiones del negocio cuando aplique). No usar rayas (—) como paréntesis: en el texto se usan paréntesis y en las tablas un guion (-). Las conclusiones se escriben en párrafos, no en tablas. El documento no menciona la clase, carpetas, archivos del repositorio ni "formatos del Punto 6": esas son instrucciones para el equipo, no contenido.
- Moneda COP (Cartagena, octubre de 2026), formato colombiano ($1.234.567 · 12,5 %). Español formal.
- No copiar texto de `EjemploDeOtroGrupo/` (el plagio se califica con 1,5). Usarlo solo como referencia de estructura y profundidad. Esa carpeta es solo local: está en `.gitignore` y nunca se debe subir al repositorio público (contiene datos de terceros). Sus hallazgos ya están resumidos en `CONTEXTO_GLOBAL.md`, sección 7.

## Si cambias un número

1. Cambia el supuesto en `scripts/modelo_kazegami.py` (fuente única de verdad).
2. Ejecuta `python scripts/analizar_encuesta.py` (regenera gráficas y `datos/*.md`).
3. Busca la cifra vieja en los `.md` (`git grep "cifra"`) y actualízala en todos los capítulos y en `CONTEXTO_GLOBAL.md`.

## Formato Markdown que entiende el compilador

- Títulos: `#` sección del taller (ej. `# 4. Demanda`), `##` subsección, `###` apartado.
- Tabla: línea `Table: Tabla N. Título`, línea vacía, tabla con pipes `|`, y debajo `*Fuente: ...*`.
- Figura: `![Figura N. Título](assets/graficas/archivo.png){width=15.5cm}` y debajo `*Fuente: ...*`.
- Salto de página: el bloque ```` ```{=openxml} ```` que ya existe en las portadas.
- No usar HTML ni LaTeX. El símbolo `$` se escribe tal cual (las matemáticas TeX están desactivadas).

## Archivos que NO se tocan

`EjemploDeOtroGrupo/`, `FormatoDocumentos/`, `ModeloCanvasNuestraIdeaNegocio/`, `ResultadosEncuesta/`, `Punto6EstudioTecnicoImg/` (insumos originales) y `entregables_word/` (se regenera con `python scripts/compilar_word.py`).

## Al terminar

Compila (`python scripts/compilar_word.py`), confirma que la verificación diga **TODO OK** y haz commit con un mensaje claro (`docs(mercado): ...`, `docs(tecnico): ...`, `fix(datos): ...`).
