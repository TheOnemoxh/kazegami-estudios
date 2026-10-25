# CONTEXTO GLOBAL — KAZEGAMI RESTAURANTE

> **Verdad absoluta del proyecto.** Toda persona o IA que edite este repositorio debe leer este archivo y `datos/RESUMEN_ENCUESTA.md` antes de escribir una sola línea. Si algo aquí contradice otro archivo, **manda este archivo** (y los números de `scripts/modelo_kazegami.py`).

## 1. Datos académicos

| Campo | Valor |
|:---|:---|
| Universidad | Universidad de Cartagena · Facultad de Ingenierías · Programa de Ingeniería de Sistemas |
| Asignatura | Seminario Taller Creación de Empresas |
| Docente | Carla del Carmen de Ávila Altamiranda (cdeavilaa@unicartagena.edu.co) |
| Entregables | Taller No. 1 Estudio de Mercados y Taller No. 2 Estudio Técnico (Word) |
| Fecha de entrega | **25 de octubre de 2026, hasta las 11:59 p. m.** (enviar al correo de la docente) |
| Rúbrica | 10 % puntualidad · 10 % orden (normas, ortografía, coherencia) · 80 % pertinencia. **Plagio = 1,5** |
| Integrantes | Adrian Alberto Angulo Melgarejo · Samuel David Molina Romero · Edwin Esteban Cañas Jurado · Alejandro Jose Vergara Parra · Carlos Arturo Rodriguez Cochero |

## 2. El proyecto

**KAZEGAMI RESTAURANTE** — *"El espíritu de la brisa marina"* (kaze = viento/brisa, kami = espíritu). Restaurante de cocina japonesa en Cartagena de Indias con **técnica 100 % japonesa** e **insumos locales** de la pesca artesanal del Caribe y de los agricultores de Bolívar. Experiencia **100 % en el local** (sin domicilios). Ubicación elegida en el Estudio Técnico: **barrio Manga**.

### 2.1 Modelo Canvas (resumen)

| Bloque | Contenido |
|:---|:---|
| Segmento de clientes | Turismo gastronómico de clase alta, principalmente empresarios de alto nivel (+ residentes con capacidad de pago, según la encuesta) |
| Propuesta de valor | Del mar directo al plato; técnica 100 % japonesa con ingredientes locales; opciones vegetarianas/veganas; experiencia en barra de sushi, ambiente sereno, servicio cercano |
| Canales | Restaurante físico (único punto en Cartagena); Instagram, TikTok, WhatsApp; Google Maps, TripAdvisor |
| Relación con clientes | Atención personalizada en mesa y barra; fidelización; reservas por WhatsApp e Instagram; reseñas y encuestas |
| Fuentes de ingreso | Carta (almuerzo y cena); menú ejecutivo de mediodía; omakase por reserva; bebidas (sake, té, cerveza japonesa, cocteles); eventos privados |
| Recursos clave | Local con barra de sushi a la vista; chef sushiman; cocina y refrigeración; marca y recetario; POS y reservas |
| Actividades clave | Preparación diaria de sushi y ramen; control de calidad y cadena de frío; servicio en sala y barra; compras e inventario; redes |
| Socios clave | Pesca artesanal (Bazurto, Mercado del Mar); importadores japoneses (arroz, nori, soya, wasabi); agricultores de Bolívar; escuelas de gastronomía; empaques y medios de pago; hoteles y agencias |
| Estructura de costos | Arriendo y servicios; nómina; insumos y cadena de frío; importados; adecuación, equipos y mantenimiento; marketing, licencias, seguros e impuestos |

## 3. REGLA DE NEGOCIO N.º 1 — SOLO 3 PLATOS (TOP 3 DE LA ENCUESTA)

| Puesto | Plato | Menciones | % de encuestados | Peso en el portafolio | Precio de venta |
|:---:|:---|---:|---:|---:|---:|
| 1 | **Rollos de sushi** | 61 | 57,5 % | 44,9 % | $40.000 |
| 2 | **Ramen** | 40 | 37,7 % | 29,4 % | $38.000 |
| 3 | **Tempura** | 35 | 33,0 % | 25,7 % | $34.000 |

- Fichas técnicas, procesos, insumos, recetas, costos, precios y proyecciones: **únicamente** estos 3 platos.
- Los demás platos (pescado estilo japonés 26, sashimi 7, vegetarianos 6) **se descartan** del análisis técnico y de costos. En la gráfica general de la encuesta sí aparecen todos.
- Precios con impoconsumo del 8 % incluido.

## 4. Cifras exactas de la encuesta (n = 106, 31 columnas)

| Indicador | Valor |
|:---|---:|
| Consume o probaría comida japonesa/mariscos | 96,2 % (66 + 36) |
| Reside en Cartagena | 84,0 % (89) |
| Edad 18-25 años | 86,8 % (92) |
| Frecuencia promedio ponderada | 6,02 ocasiones/persona/año |
| Ocasión principal | Salida con amigos 41,5 %; cena en pareja 25,5 % |
| Lo que menos gusta de la competencia | Precios altos 67,0 %; porciones pequeñas 43,4 % |
| Concepto atractivo o muy atractivo | 82,9 % (de 105) |
| Disposición de pago por cena | $60.000-$100.000: 50,9 %; ≥ $60.000: 86,5 % (de 104) |
| Menú ejecutivo | $20.000-$30.000: 51,9 % |
| Omakase | 67,9 % algo interesado; 19,8 % muy interesado; $100.000-$200.000: 46,2 % |
| Zona preferida | Centro Histórico 33 · NS/NR 29 · Manga 17 · Bocagrande 10 · Getsemaní 8 |
| Canales de búsqueda | Instagram/TikTok 85,8 %; amigos y familia 63,2 %; Google Maps 44,3 % |
| Reserva | WhatsApp 53,8 %; web 33,0 % |
| Visitaría (probable + muy probable) | 74,0 % (de 104) |

Detalle completo, tablas por pregunta y cruces: `datos/RESUMEN_ENCUESTA.md`.

## 5. Cifras del modelo (fuente: `scripts/modelo_kazegami.py`)

| Variable | Valor |
|:---|---:|
| Demanda actual 2026 (3 platos, Cartagena) | 952.125 platos/año |
| Demanda base 2031 | 1.099.788 platos/año |
| Oferta 2026 → 2031 (45 locales, +2 %/año) | 765.000 → 844.622 platos/año |
| Demanda insatisfecha base 2027 → 2031 | 199.653 → 255.166 platos/año |
| Puestos del local | 56 (12 mesas × 4 + 8 en barra) |
| Capacidad diseñada / instalada | 73.382 / 58.706 platos/año |
| Platos Kazegami 2027 → 2031 | 29.353 → 46.965 (50 % → 80 % de la instalada) |
| Costo MP por porción: sushi / ramen / tempura | $10.952 / $11.270 / $10.545 |
| Costo unitario total (formato Punto 6) | $11.673 / $12.366 / $11.290 |
| Inversión técnica inicial | $389.371.491 |
| Microlocalización | Manga 6,70 · Centro Histórico 6,50 · Bocagrande 5,30 · Getsemaní 5,30 |

## 6. Formato obligatorio de las tablas de insumos (Punto6EstudioTecnicoImg/)

Las dos fotos del tablero de clase definen el formato. **Columnas exactas y en este orden:**

| Insumos | Cantidad por mes | Proveedor (precio · calidad · postventa) | Precio | Total | Identificación del elemento | Total final |
|:---|---:|:---|---:|---:|:---|---:|

Lógica del modelo (tablero):
1. Cada insumo se identifica como **Costo** (materia prima), **Costo o gasto** (servicios) o **Activo** (equipos).
2. Los activos **no** suman por su valor: entran como **gasto de depreciación** = valor ÷ (vida útil × 12). Ejemplo del tablero: $10.000.000 ÷ (2 × 12) ≈ $417.000.
3. **Total final mensual** = suma de costos + gastos + depreciación (ejemplo: $6.877.000).
4. **Costo unitario** = total final ÷ unidades del mes (ejemplo: $6.877.000 ÷ 400 = $17.192,5).

La segunda foto lista los **factores de la oferta**: 1. costos e insumos, 2. tecnología, 3. clima, 4. precios de los sustitutos, 5. capacidad instalada, 6. gobierno (aplicados en la sección 5.1 del Estudio de Mercados).

## 7. Hallazgos de EjemploDeOtroGrupo/ (PROTECNOVA)

| Lo que hace bien el ejemplo | Cómo lo aplicamos |
|:---|:---|
| Sigue al pie de la letra la numeración del taller (1 a 7, con 3.1-3.13) | Mismos títulos y numeración |
| Marco de Miranda (*Gestión de proyectos*) citado | Citado en introducción y métodos |
| Separa dato de supuesto (Anexo A) | Anexo A de supuestos y limitaciones |
| Embudo de demanda con fuentes públicas | Embudo con DANE + Migración + encuesta |
| Tres escenarios de proyección | Pesimista 1 %, base 3 %, optimista 5 % |
| Régimen de mercado sustentado | Competencia monopolística |
| Mucho texto y casi ninguna gráfica | **Nosotros: tablas y gráficas primero** |

## 8. Estilo de redacción

- **Tablas y gráficos > texto plano.** El texto solo introduce y analiza (párrafos cortos con **Lectura.**).
- Cada tabla: `Table: Tabla N. Título` + fuente en cursiva debajo. Cada figura: `![Figura N. Título](ruta){width=15.5cm}` + fuente.
- Español formal, tercera persona, números con formato colombiano: $1.234.567 y 12,5 %.
- Moneda COP de octubre de 2026 (Cartagena). Proyecciones 2027-2031 a precios constantes.
- Referencias en APA 7. Nada de copiar texto del ejemplo (plagio = 1,5).
- Supuestos siempre marcados como "supuesto del equipo".
