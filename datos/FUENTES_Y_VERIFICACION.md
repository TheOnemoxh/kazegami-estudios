# FUENTES Y VERIFICACIÓN DE LOS DATOS — KAZEGAMI

> Generado por `scripts/analizar_encuesta.py` desde `scripts/modelo_kazegami.py`. Consultas realizadas el 24 de octubre de 2026.
> **Verificado** = dato tomado de una fuente pública citada. **Estimación** = no existe dato público; valor razonado por el equipo con base en la investigación. **Decisión** = definición del proyecto.

**Resumen:** 72 datos verificados y 32 estimaciones.

## 1. Mercado, demanda, oferta y operación

| Dato | Valor | Estado | Fuente |
|:---|:---|:---|:---|
| Encuesta de mercado (todas las cifras de la encuesta) | n = 106, 31 columnas | Verificado | ResultadosEncuesta/*.xlsx (datos primarios del equipo) |
| Población de Cartagena 2024 / 2025 / 2026 / 2033 | 1.010.408 / 1.011.520 / 1.010.995 / 998.638 | Verificado | DANE vía El Universal (13-ago-2025): https://www.eluniversal.com.co/cartagena/2025/08/13/poblacion-de-cartagena-se-reducira-estas-son-las-proyecciones-del-dane/ |
| Población de 18 años y más (2025) | 719.615 (71,1 %) | Verificado | DANE vía Telencuestas: https://telencuestas.com/censos-de-poblacion/colombia/2025/bolivar/cartagena-de-indias |
| Viviendas en estratos 3 a 6 | 30 % (21 + 3 + 4 + 2) | Verificado | Cartagena Cómo Vamos vía El Universal (08-sep-2020): https://www.eluniversal.com.co/cartagena/2020/09/08/69-de-las-viviendas-en-cartagena-pertenece-a-estratos-1-y-ii/ |
| Turistas extranjeros 2024 / 2025 | 855.744 / 866.264 | Verificado | Migración Colombia vía El Universal (16-mar-2026): https://www.eluniversal.com.co/economica/2026/03/16/los-cinco-paises-que-mas-turistas-le-generaron-a-cartagena-durante-2025/ |
| Turistas que viajan por gastronomía | 11,3 % | Verificado | Corpoturismo vía El Universal (26-dic-2025) |
| Turistas extranjeros que consumen cocina japonesa | 10 % | Estimación | Aproximado al 11,3 % anterior; no existe dato específico |
| Ocupación hotelera 1.er trimestre 2025 | 70,5 % | Verificado | Cartagena Cómo Vamos: https://cartagenacomovamos.org/turismo-en-cartagena-primer-trimestre-2025/ |
| Salario mínimo 2026 y auxilio de transporte | $1.750.905 y $249.095 | Verificado | Decreto 1469 de 2025; Portafolio |
| Restaurantes japoneses en Cartagena | 37 (7 con ramen) | Verificado | Tripadvisor (24-oct-2026): https://www.tripadvisor.com/Restaurants-g297476-c27-Cartagena_Cartagena_District_Bolivar_Department.html |
| Platos del Top 3 vendidos por competidor al día | 50 | Estimación | Sin datos públicos de ventas; requiere observación de campo |
| Crecimiento de establecimientos de restaurantes 2024 | 2 % | Verificado | ACODRES vía Portafolio (23-feb-2025) |
| Crecimiento del gasto: total hogares / comidas fuera del hogar (dic-2024) | 2,02 % / 3,6 % | Verificado | Raddar vía Portafolio: https://www.portafolio.co/economia/finanzas/en-que-gastaron-mas-los-hogares-colombianos-en-el-2024-622923 |
| Crecimiento Sushi Master 2024 → 2025 (piezas) | 438.898 → 480.397 (+9,5 %) | Verificado | Valora Analitik (04-dic-2025): https://www.valoraanalitik.com/?p=532819 |
| Precios de rollos (Masaki Sushi Wok) | $40.000-$57.000 (prom. $49.550) | Verificado | Rappi: https://www.rappi.com.co/restaurantes/900039514-masaki-sushi-wok |
| Precios de ramen (Dame Ramen) | $35.000-$69.000 (prom. $45.667) | Verificado | https://dameramen.com/menu/ |
| Tempura de vegetales (Masaki) | $25.000 | Verificado | Rappi (ídem) |
| Food cost de restaurantes rentables | 28 %-35 % | Verificado | Gordon Food Service (Rivers, s.f.): https://gfs.com/es-us/?p=5384 |
| Rendimiento en filete del pescado | 46 % | Estimación | Mancera (2024): 46,15 % en cachama; se asume similar para pargo |
| Arriendo de locales ($/m² mediana): Manga / Centro / Bocagrande / Getsemaní | $75.295 / $110.000 / $130.000 / $83.333 | Verificado | Fincaraíz (24-oct-2026): https://www.fincaraiz.com.co/arriendo/locales/manga/cartagena |
| Tarifa de energía Afinia | $1.033,32/kWh (+20 % contribución comercial) | Verificado | El Universal (11-sep-2026); Ley 142 de 1994 |
| Consumo de energía del local | 2.600 kWh/mes | Estimación | Cálculo del equipo según equipos instalados |
| Factor prestacional | 1,38 | Verificado | Aleluya (2026): https://aleluya.com/blog/nomina/costo-de-un-empleado-en-colombia-2026/ |
| Salario de chef (promedio Colombia) | $1.947.429 | Verificado | Indeed Colombia (02-oct-2026) |
| Salario del administrador | 2 SMMLV | Estimación | Sin dato público verificable para Cartagena |
| Capacidad: puestos, rotación, utilización, platos por comensal | 56 / 3,5 / 50-80 % / 1,2 | Estimación | Parámetros de diseño del equipo |
| Calificaciones cualitativas de la microlocalización | 1-10 | Estimación | Juicio del equipo (flujo turístico, proveedores, acceso, competencia, normativa) |
| Precios de venta de Kazegami | $40.000 / $38.000 / $38.000 | Decisión | Método mixto: costo + food cost 28-35 % + precio de la competencia + disposición de pago |

## 2. Precios de insumos (recetas estándar)

| Insumo | Precio | Estado | Fuente |
|:---|:---|:---|:---|
| Arroz japonés para sushi (bulto Botan 50 lb) | $16.314/kg | Verificado | Global Gourmet Market Colombia, consulta 24-oct-2026: $370.000 / 50 lb |
| Vinagre de arroz (Kenko 750 ml) | $24.000/L | Verificado | Global Gourmet Market Colombia, consulta 24-oct-2026: $18.000 / 750 ml |
| Azúcar refinada (sazón del shari) | $3.820/kg | Verificado | SIPSA-DANE, Cartagena (Bazurto) (vía Agronegocios), consulta 24-oct-2026 |
| Sal (sazón del shari) | $1.100/kg | Verificado | SIPSA-DANE, Cartagena (Bazurto) (vía Agronegocios), consulta 24-oct-2026 |
| Alga nori (paquete de 100 hojas) | $980/und | Verificado | Global Gourmet Market Colombia, consulta 24-oct-2026: $98.000 / 100 hojas |
| Pargo rojo entero fresco (pesca artesanal; 56 g de filete, rinde 46 %) | $21.000/kg | Verificado | SIPSA-DANE, Cartagena (Bazurto) (vía Agronegocios), consulta 24-oct-2026 |
| Langostino 16-20 | $62.445/kg | Verificado | SIPSA-DANE, promedio nacional (vía Agronegocios), consulta 24-oct-2026 |
| Aguacate papelillo | $11.083/kg | Verificado | SIPSA-DANE, Cartagena (Bazurto) (vía Agronegocios), consulta 24-oct-2026 |
| Pepino cohombro | $2.367/kg | Verificado | SIPSA-DANE, Cartagena (Bazurto) (vía Agronegocios), consulta 24-oct-2026 |
| Mango de azúcar (toque caribeño) | $2.400/kg | Verificado | SIPSA-DANE, Cartagena (Bazurto) (vía Agronegocios), consulta 24-oct-2026 |
| Queso crema (Alpina 380 g) | $34.211/kg | Verificado | Mercasur, consulta 24-oct-2026: $13.000 / 380 g |
| Ajonjolí descortezado | $48.000/kg | Verificado | Global Gourmet Market Colombia, consulta 24-oct-2026: $12.000 / 250 g |
| Salsa de soya (Sakura 20 L) | $14.700/L | Verificado | Global Gourmet Market Colombia, consulta 24-oct-2026: $294.000 / 20 L |
| Wasabi en polvo (Waner 1 kg) | $115.000/kg | Verificado | Global Gourmet Market Colombia, consulta 24-oct-2026: $115.000 / kg |
| Jengibre encurtido – gari (340 g) | $44.118/kg | Verificado | Global Gourmet Market Colombia, consulta 24-oct-2026: $15.000 / 340 g |
| Mayonesa (base de la salsa spicy de la casa) | $18.490/kg | Verificado | SIPSA-DANE, Cartagena (Bazurto) (vía Agronegocios), consulta 24-oct-2026 |
| Fideo de trigo estilo chuka (Best Choice 400 g) | $38.750/kg | Verificado | Global Gourmet Market Colombia, consulta 24-oct-2026: $15.500 / 400 g |
| Espinazo de cerdo (caldo) | $12.750/kg | Verificado | SIPSA-DANE, región Caribe (vía Agronegocios), consulta 24-oct-2026 |
| Rabadillas de pollo (caldo) | $6.500/kg | Verificado | SIPSA-DANE, promedio nacional (vía Agronegocios), consulta 24-oct-2026 |
| Tocino de barriga de cerdo (chashu) | $18.170/kg | Verificado | SIPSA-DANE, promedio nacional (vía Agronegocios), consulta 24-oct-2026 |
| Huevo rojo A (ajitama) | $494/und | Verificado | SIPSA-DANE, Cartagena (Bazurto) (vía Agronegocios), consulta 24-oct-2026 |
| Miso (Hikari 1 kg) | $40.000/kg | Verificado | Global Gourmet Market Colombia, consulta 24-oct-2026: $40.000 / kg |
| Mirin (Kikkoman 375 ml) | $114.667/L | Verificado | Global Gourmet Market Colombia, consulta 24-oct-2026: $43.000 / 375 ml |
| Alga nori (½ hoja) | $980/und | Verificado | Global Gourmet Market Colombia, consulta 24-oct-2026: $98.000 / 100 hojas |
| Cebollín chino | $6.333/kg | Verificado | SIPSA-DANE, Cartagena (Bazurto) (vía Agronegocios), consulta 24-oct-2026 |
| Repollo blanco salteado | $2.077/kg | Verificado | SIPSA-DANE, Cartagena (Bazurto) (vía Agronegocios), consulta 24-oct-2026 |
| Ajo | $5.858/kg | Verificado | SIPSA-DANE, Cartagena (Bazurto) (vía Agronegocios), consulta 24-oct-2026 |
| Aceite de ajonjolí (Kuki 1.650 ml) | $83.939/L | Verificado | Global Gourmet Market Colombia, consulta 24-oct-2026: $138.500 / 1.650 ml |
| Berenjena | $1.333/kg | Verificado | SIPSA-DANE, Cartagena (Bazurto) (vía Agronegocios), consulta 24-oct-2026 |
| Ahuyama | $1.667/kg | Verificado | SIPSA-DANE, Cartagena (Bazurto) (vía Agronegocios), consulta 24-oct-2026 |
| Cebolla cabezona blanca | $2.408/kg | Verificado | SIPSA-DANE, Cartagena (Bazurto) (vía Agronegocios), consulta 24-oct-2026 |
| Harina para tempura (Best Choice 1 kg) | $23.000/kg | Verificado | Global Gourmet Market Colombia, consulta 24-oct-2026: $23.000 / kg |
| Fécula de maíz | $37.153/kg | Verificado | SIPSA-DANE, Cartagena (Bazurto) (vía Agronegocios), consulta 24-oct-2026 |
| Huevo rojo A (½ unidad) | $494/und | Verificado | SIPSA-DANE, Cartagena (Bazurto) (vía Agronegocios), consulta 24-oct-2026 |
| Aceite vegetal para freír (consumo + reposición) | $9.792/kg | Verificado | SIPSA-DANE, Cartagena (Bazurto) (vía Agronegocios), consulta 24-oct-2026 |
| Alga kombu (dashi para tentsuyu) | $160.000/kg | Verificado | Global Gourmet Market Colombia, consulta 24-oct-2026: $16.000 / 100 g |
| Rábano rojo rallado (en lugar de daikon) | $6.333/kg | Verificado | SIPSA-DANE, Cartagena (Bazurto) (vía Agronegocios), consulta 24-oct-2026 |

## 3. Maquinaria y equipos

| Equipo | Precio unitario | Estado | Fuente |
|:---|:---|:---|:---|
| Ultracongelador / abatidor −40 °C, 5 bandejas (TechGelato TG25BCF) | $15.990.000 | Verificado | Makfrio / America Food Solutions, oct-2026 |
| Nevera vertical industrial 2 puertas acero inoxidable (TG1400R2A) | $10.190.000 | Verificado | America Food Solutions, oct-2026 |
| Mesa refrigerada de preparación 1,50 m | $7.704.000 | Verificado | Makfrio, oct-2026 |
| Congelador horizontal ≈ 500 L | $3.900.000 | Estimado | Sin precio público consultable; requiere cotización |
| Vitrina refrigerada curva para sushi | $5.136.000 | Verificado | Makfrio, oct-2026 |
| Fabricador de hielo 65 kg | $4.990.000 | Verificado | Makfrio, oct-2026 |
| Nevera exhibidora de bebidas 2 puertas 1.100 L | $12.800.000 | Verificado | FrigoMaster, oct-2026 |
| Arrocera industrial a gas 10 L | $2.052.750 | Verificado | Pallomaro, oct-2026 |
| Estufa industrial de piso 36", 6 puestos (ETP-36) | $3.940.923 | Verificado | Pallomaro, oct-2026 |
| Quemador de piso para caldos + marmita 60 L | $2.800.000 | Estimado | Sin precio público consultable; requiere cotización |
| Freidora industrial a gas 20 L, 2 canastas | $5.089.000 | Verificado | Exhibir Equipos, oct-2026 |
| Campana extractora en acero inoxidable (3 módulos de 1 m) | $850.000 | Verificado | SMR Industriales, oct-2026 |
| Extractor centrífugo y ductería para la campana | $6.000.000 | Estimado | Sin precio público consultable; requiere cotización |
| Trampa de grasas en acero inoxidable | $2.500.000 | Estimado | Sin precio público consultable; requiere cotización |
| Mesas de trabajo en acero inoxidable (MAINOX2) | $2.535.000 | Verificado | Exhibir Equipos, oct-2026 |
| Pozuelo triple de lavado en acero inoxidable | $3.200.000 | Estimado | Sin precio público consultable; requiere cotización |
| Ollas de acero inoxidable 60 L | $650.000 | Estimado | Sin precio público consultable; requiere cotización |
| Balanzas digitales de precisión | $350.000 | Estimado | Estimación del equipo |
| Termómetros de punzón y data loggers de temperatura | $180.000 | Estimado | Estimación del equipo |
| Cuchillo yanagiba 270 mm Sekiryu | $441.200 | Verificado | Global Gourmet Market, oct-2026 |
| Cuchillo sashimi 240 mm | $150.000 | Verificado | Global Gourmet Market, oct-2026 |
| Utensilios menores (makisu, bandejas GN, coladores, tablas) | $3.500.000 | Estimado | Estimación del equipo |
| Vajilla japonesa (platos, bowls de ramen, palillos reutilizables) | $9.000.000 | Estimado | Estimación del equipo |
| Planta eléctrica diésel 18-20 kVA cabinada (respaldo de cadena de frío) | $53.300.000 | Verificado | Maquitec de Colombia, oct-2026 |

## 4. Mobiliario, adecuación y tecnología

| Ítem | Precio unitario | Estado | Fuente |
|:---|:---|:---|:---|
| Adecuación del local (obra civil, pisos, baños, redes de gas y eléctricas) | $85.000.000 | Estimado | Estimación del equipo; requiere presupuesto de obra |
| Barra de sushi en madera para 8 comensales | $12.000.000 | Estimado | Estimación del equipo |
| Mesas de madera para 4 personas | $650.000 | Estimado | Estimación del equipo |
| Sillas de comedor | $280.000 | Estimado | Estimación del equipo |
| Bancos altos de barra | $350.000 | Estimado | Estimación del equipo |
| Aire acondicionado minisplit 24.000 BTU | $4.067.900 | Verificado | Falabella Colombia, oct-2026 |
| Iluminación y decoración de inspiración japonesa | $15.000.000 | Estimado | Estimación del equipo |
| Aviso exterior y señalización | $4.500.000 | Estimado | Estimación del equipo |
| Sistema de sonido ambiental | $2.800.000 | Estimado | Estimación del equipo |
| Computador administrativo | $3.200.000 | Estimado | Estimación del equipo |
| Tablets comanderas para meseros | $1.100.000 | Estimado | Estimación del equipo |
| Impresoras térmicas de comandas y facturas | $650.000 | Estimado | Estimación del equipo |
| Cajón monedero y lector de código | $550.000 | Estimado | Estimación del equipo |
| Red WiFi y router empresarial | $900.000 | Estimado | Estimación del equipo |
| UPS para POS y red | $1.200.000 | Estimado | Estimación del equipo |
| Kit de cámaras de seguridad (4 cámaras + grabador) | $2.200.000 | Estimado | Estimación del equipo |

## 5. Nómina

| Cargo | Salario base | Fuente |
|:---|:---|:---|
| Chef ejecutivo / sushiman principal | $1.947.429 | Indeed Colombia: salario promedio de chef, act. 02-oct-2026 |
| Sushiman auxiliar (barra) | $1.750.905 | SMMLV 2026 (el promedio de Indeed para cocinero, $1.341.350, es inferior al mínimo legal) |
| Cocinero de línea caliente (ramen y tempura) | $1.750.905 | SMMLV 2026 (Indeed cocinero/a: $1.341.350 < mínimo legal) |
| Auxiliar de cocina y steward | $1.750.905 | SMMLV 2026 |
| Meseros | $1.750.905 | SMMLV 2026 (Indeed mesero/a: $1.524.922 < mínimo legal) |
| Anfitrión(a) y cajero(a) | $1.750.905 | SMMLV 2026 |
| Administrador(a) | $3.501.810 | Estimación: 2 SMMLV (sin dato público verificable para Cartagena) |

## 6. Qué falta para que todo sea dato real (trabajo de campo)

- Cotizar en tienda los equipos marcados como **Estimado** (congelador, quemador de caldos, extractor, trampa de grasa, pozuelo, ollas, utensilios, vajilla, mobiliario y tecnología).
- Pedir presupuesto de obra para la adecuación del local.
- Observar en 2 o 3 competidores cuántos platos venden en una hora pico, para reemplazar la estimación de 50 platos diarios.
- Confirmar en Bazurto el rendimiento real del pargo al filetearlo.
- Cotizar el software POS (Siigo, Alegra o Loggro) y la plataforma de reservas.
