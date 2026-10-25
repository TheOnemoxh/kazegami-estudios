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
| Fuentes de ingreso | Carta (horario continuo de 12:00 m. a 10:00 p. m., martes a domingo); menú ejecutivo de mediodía; omakase por reserva; bebidas (sake, té, cerveza japonesa, cocteles); eventos privados |
| Recursos clave | Local con barra de sushi a la vista; chef sushiman; cocina y refrigeración; marca y recetario; POS y reservas |
| Actividades clave | Preparación diaria de sushi y ramen; control de calidad y cadena de frío; servicio en sala y barra; compras e inventario; redes |
| Socios clave | Pesca artesanal (Bazurto, Mercado del Mar); importadores japoneses (arroz, nori, soya, wasabi); agricultores de Bolívar; escuelas de gastronomía; empaques y medios de pago; hoteles y agencias |
| Estructura de costos | Arriendo y servicios; nómina; insumos y cadena de frío; importados; adecuación, equipos y mantenimiento; marketing, licencias, seguros e impuestos |

## 3. REGLA DE NEGOCIO N.º 1 — SOLO 3 PLATOS (TOP 3 DE LA ENCUESTA)

| Puesto | Plato | Menciones | % de encuestados | Peso en el portafolio | Precio de venta |
|:---:|:---|---:|---:|---:|---:|
| 1 | **Rollos de sushi** | 61 | 57,5 % | 44,9 % | $40.000 |
| 2 | **Ramen** | 40 | 37,7 % | 29,4 % | $38.000 |
| 3 | **Tempura** | 35 | 33,0 % | 25,7 % | $38.000 |

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

## 5. Cifras del modelo (fuente: `scripts/modelo_kazegami.py`; verificación en `datos/FUENTES_Y_VERIFICACION.md`)

| Variable | Valor | Estado |
|:---|---:|:---|
| Demanda actual 2026 (3 platos, Cartagena) | 941.590 platos/año | Calculada con DANE, Cartagena Cómo Vamos, Migración Colombia y encuesta |
| Demanda base 2031 (g = 3,6 %, Raddar) | 1.119.734 platos/año | Escenarios con fuente: 2,02 % / 3,6 % / 9,5 % |
| Oferta 2026 → 2031 (37 restaurantes en Tripadvisor, +2 %/año ACODRES) | 629.000 → 694.467 platos/año | Ventas por local: estimación |
| Demanda insatisfecha base 2027 → 2031 | 333.187 → 425.267 platos/año | — |
| Puestos del local | 56 (12 mesas × 4 + 8 en barra) | Diseño |
| Capacidad diseñada / instalada | 73.382 / 58.706 platos/año | Diseño |
| Platos Kazegami 2027 → 2031 | 29.353 → 46.965 (8,8 % → 11,0 % de la DI) | — |
| Costo MP por porción: sushi (rollo de 10 piezas ≈ 320 g) / ramen / tempura | $11.087 / $12.120 / $11.953 | Precios SIPSA-DANE y proveedores (verificados) |
| Costo unitario total (formato Punto 6) | $11.768 / $13.189 / $12.687 | Food cost 29,9 % / 34,4 % / 34,0 % |
| Precios de venta | $40.000 / $38.000 / $38.000 | Promedio real de mercado (Rappi y dameramen.com, 24-oct-2026): rollos $49.684 (5 restaurantes), ramen $52.942 (4), tempura de vegetales $28.500 (2) |
| Inversión técnica inicial | $396.901.294 | Equipos mayormente verificados; obra y mobiliario estimados |
| Arriendo (Manga, mediana Fincaraíz) | $75.295/m² → $15.059.000/mes | Verificado |
| Microlocalización | Manga 6,91 · Centro Histórico 6,76 · Getsemaní 5,59 · Bocagrande 4,38 | Votos y arriendo cuantitativos; resto cualitativo |

| Horario | Martes a domingo, continuo de 12:00 m. a 10:00 p. m. (rotaciones 1,5 almuerzo + 0,5 tarde + 1,5 noche) | Diseño |
| Servicios públicos | Afinia (energía), Aguas de Cartagena (agua), Surtigas (gas natural), Pacaribe (aseo) | Cartagena Cómo Vamos 2023 |
| Compras a proveedores | Pescado y vegetales 2 veces/semana; carnes y secos nacionales semanal; importados y desechables mensual | WISK (2022): 4-6 pedidos de alimentos al mes |
| Tiempos de entrega | Rollos 15-20 min; ramen y tempura 12-15 min; mesa completa ≤ 20 min (≤ 25 en hora pico) | Estándar operativo del equipo |

**Regla:** toda cifra nueva necesita fuente; si no existe dato público, se escribe "Estimación" y se explica en qué se basa.

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
