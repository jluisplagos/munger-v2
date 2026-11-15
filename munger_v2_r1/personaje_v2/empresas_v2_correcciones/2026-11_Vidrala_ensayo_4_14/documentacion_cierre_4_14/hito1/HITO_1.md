# Munger V2 · encargo prioritario de cierre · Hito 1: primera instantánea técnica

Sábado 14-nov-2026. Base: `munger_v2_r1_entrega4.13_fiabilidad_motor_B_y_conciliacion_economica.zip`, SHA-256 `b1f747a18cd2123d71c0c1abdca0da049207b4c4eb215aa099f345aed4fbf22a`. Paquete pequeño: cambios frente a esa base y evidencia. No es una entrega integral: el ZIP completo se reserva para la candidata.

## 1. En breve

| Frente | Estado | Evidencia |
|---|---|---|
| A · H5 (reparación 4.13.1) | **Corregido; dos revisiones internas incorporadas; regresión completa sobre i4: todas las baterías pasan** | `REGISTRO_REPARACION_4_13_1.md`; batería `test_vigencia_h5.py` 59/59 |
| B · materialidad para el objetivo (§5) | **Contrato 4.14 implementado** (software). Los expedientes no se han regenerado todavía con él | `test_juicio_objetivo_414.py` 27/27; diseño del frente B |
| B · decisiones y evidencia económica (§6–§7) | **Paquete de decisiones enviado** (12, sin adoptar) | `DECISIONES_PENDIENTES_4_14.md`, `EVIDENCIA_ECONOMICA_4_14.md`, `DESCOMPOSICION_VISCOFAN_4_14.md` |
| §7 · S4 y S5 | **S4 corregido** en sus tres vías generativas. **S5:** la vía generativa ya admite la cabecera F5; falta aplicarlo en la rama de Viscofan | diff |
| Requisito nuevo · verificación completa de las entradas | **Mecanismo implementado y probado. Extracción y revisión independiente hechas: verificadas 210 de 232 (Viscofan) y 219 de 226 (Vidrala); ninguna apta por entradas** (27 discrepancias y 5 pendientes en total; tres pueden mover el valor del motor B) | `COBERTURA_ENTRADAS_4_14.md`; `evidencias/verificacion_entradas/`; `test_verificacion_entradas_414.py` 31/31 |
| C · alcance y tercera empresa | **Matriz del alcance en borrador.** Elis elegida por la persona responsable (Ahold Delhaize de reserva). **Expediente de la etapa 1 inventariado; fuentes que faltaban descargadas; Historia 2016–2025 construida** (10 años, 16 ceros pendientes de verificación); metadatos recogidos; precio contrastado con Euronext. Pipeline con agentes reales: siguiente paso | `SELECCION_TERCERA_EMPRESA.md`, `INVENTARIO_ELIS.md` |

## 2. Cambios (hechos; código congelado en la instantánea i4)

| Archivo | Cambio | Frente |
|---|---|---|
| `scripts/cierre_v2.py` | H5: señal de publicación propia de la aprobación; invalidación sin salidas; rastro previo; tres señales de retirada; identidad heredada para los cierres anteriores a la 4.8.1; sin registro, destinos junto al expediente | A |
| `scripts/ficha.py`, `informe.py`, `resumen.py` | H5 en las vías manuales; S4 en la ficha; §5 en el informe §14 | A, B |
| `scripts/pipeline.py` | contrato 4.14 fijado por el pipeline en el paso 10; contraste mecánico para la fase C; reglas 4.13 del objetivo apartadas en `_objetivo_413`; adopción de la publicación registrada por `resumen.py` (D2-4) | A, B |
| `scripts/objetivo_v64.py` | `validar_juicio_objetivo` (V1–V8), `contraste_objetivo`, `escribir_contraste_objetivo`; `condicionantes` y la ficha leen el bloque | B |
| `esquema/fase_c.esquema.json`, `prompts/fase_c_turno1.md`, `prompts/verificacion.md` | bloque `juicio_objetivo`; instrucciones para la fase C; la auditoría revisa la pertinencia | B |
| `scripts/volcar_datos_v63.py`, `comprobar_gramatica.py` | S4: con el perímetro NIIF 16, el ancla del S2C de las referencias es B155 | §7 |
| `scripts/rellenar_fase1_v63.py` | S5: `control_maestro_textos` admite la cabecera F5 | §7 |
| `verificar_paquete.sh` | baterías obligatorias nuevas (H5 ≥ 59, juicio sobre el objetivo ≥ 27 y verificación de las entradas ≥ 27) | A, B, requisito |
| `pruebas/test_vigencia_h5.py`, `test_juicio_objetivo_414.py` | baterías nuevas | A, B |
| **Después de i3 (congelado en i4):** `scripts/verificacion_entradas.py` (nuevo), `pruebas/test_verificacion_entradas_414.py` (nuevo), `cierre_v2.py` (el registro entra en el material), `ficha.py` e `informe.py` (aptitud con la verificación de las entradas), `pipeline.py` (paso 12) | requisito de verificación de las entradas | requisito |
| `pruebas/agentes_sinteticos.py` | el agente sintético de las pruebas escribe el bloque `juicio_objetivo` cuando el pipeline fija el contrato 4.14 (era la causa de la regresión V6.4 135/181 sobre i3) | B |
| `pruebas/test_integracion_v64.py` | tres pruebas que alteran la fase C a mano la mantienen coherente con el contrato 4.14; las reglas 4.13 del objetivo se prueban sobre la vía 4.13 (la de los controles congelados), y se añade el control positivo 4.14 | B |
| `scripts/verificacion_entradas.py` (corrección) | un 0 publicado y una celda vacía ya no se dan por iguales; la cita tiene que contener el valor como cifra completa (no dentro de otra: el «0» de «2019»); ceros impresos como «-»; miles con espacio; hasta seis decimales (boletines de cotización) | requisito |
| `scripts/fase1_historia.py` | los importes con miles separados por espacio («1 512 764», «4 573,7»; informes en francés) se aceptan | C (Elis) |

El detalle está en `cambios_i4_frente_a_base.diff` (21 archivos; el de i3 en `evidencias/`) y los archivos nuevos en `codigo_nuevo/`. Huellas en `huellas_i4.txt` (i3 en `evidencias/`).

## 3. Pruebas ejecutadas (hechos)

- **Reproducción de H5 con el código 4.13:** reproducido como lo describió el revisor externo (`evidencias/sondas/sonda_h5_codigo_4_13.txt`).
- **Batería H5:** 59/59 (grupos A–J; §4 del encargo y los casos de las dos revisiones internas).
- **Juicio sobre el objetivo (4.14):** 27/27.
  - Legado: las tres fases C cerradas siguen siendo coherentes.
  - Control positivo.
  - S3: rechazo sin comparación; con «no determinada» condiciona; con comparación coherente se acepta; con un valor falso, rechazo.
  - S11: el criterio propio de 1,5 € no se admite como «calculada».
  - Contrato: Δ, cobertura, límites, política inventada, campos 4.13.
  - D10 y presentación.
  - Diagnóstico: con el contrato nuevo, en Viscofan condicionarían también N3.regla, PM1.convencion_anios y PM1.roic_terminal. Ningún estado cambia, porque todas las variantes siguen en «caro».
- **Verificación de las entradas:** 31/31 sobre un registro **sintético** (identificado como tal), incluidas las cuatro pruebas nuevas de esta ronda (vacío ≠ cero, cifra completa en la cita, miles con espacio, ceros impresos como «-»).
  - Cobertura, columna equivocada, unidades, signo, perímetro, derivado con origen pendiente, reutilización desactualizada y fuente cambiada.
  - Revisión no independiente, hipótesis como dato, cero, ausente y no aplicable, y cita fuera de la página.
  - Puerta en la ficha y el informe: nunca «apta para dinero real».
  - El registro es material: cambiarlo retira la aprobación.
- **Regresiones:**
  - Sobre i1 (versión intermedia), las siete baterías obligatorias pasan: V6.4 195/195, trazabilidad 78/78, integridad 103/103, solicitudes 55/55, estados 28/28, resumen 45/45 y cierre 55/55.
  - **Sobre i3:** `verificar_paquete.sh completa` sobre una copia (32 min): todo pasa salvo la integración V6.4, 135/181. La causa era propia: el pipeline ya fija el contrato 4.14 y el agente sintético de las pruebas no escribía el bloque `juicio_objetivo`, así que su fase C se rechazaba. Corregido el agente sintético y adaptadas tres pruebas que alteran la fase C a mano (grupo F: 54/54 en el árbol). El manifiesto falla como se espera en un árbol modificado.
  - **Sobre i4 (final de este hito):** `verificar_paquete.sh completa` sobre una copia (36 min; `evidencias/pruebas/verificacion_completa_i4.txt`). **Pasan las doce baterías:** comprobadores 114/114, piloto 30/30, H5 59/59, juicio sobre el objetivo 27/27, verificación de las entradas 31/31, integración V6.4 196/196, trazabilidad 78/78, integridad 103/103, solicitudes 55/55, estados 28/28, resumen 45/45 y cierre 55/55. Ninguna escritura fuera de la copia.
    - El resultado global es «FALLA (1 bloque)» solo por el **manifiesto**, que falla como debe en un árbol modificado: se regenera en la candidata. No se presenta como superado.

## 4. Revisión (interna; la externa es la de este hito)

- **Dos revisiones internas independientes del autor** (subagentes de Claude, contexto separado; no son revisión externa):
  - primera: 1 bloqueante, 4 importantes, 3 menores y 3 observaciones;
  - segunda, sobre lo corregido: 2 importantes, 1 menor y 2 observaciones.
- Todo lo bloqueante e importante quedó resuelto con pruebas. Lo que queda declarado está en `REGISTRO_REPARACION_4_13_1.md` §5 y §7. Los informes completos están en `evidencias/revisiones/`.
- **Incidencia propia, declarada:** una versión intermedia de la corrección, al probarla, escribió una fila en una copia de trabajo antigua (fuera de la base y de la entrega). Se restauró desde la base, se corrigió la causa y se comprueba en cada ejecución que no se escribe fuera de las copias.

## 5. Requisito de verificación completa de las entradas: implementación, cobertura e impacto

**Implementado (software):**
- Universo: todas las celdas de entradas económicas del libro, una entrada por celda: 232 en Viscofan y 226 en Vidrala. Los datos de origen de los derivados se cuentan aparte.
- Registro `verificacion_entradas.json`, que forma parte del material auditado.
- Comprobaciones automáticas:
  - cobertura y vigencia: el valor del libro y el sha256 de la fuente;
  - cada campo del contraste;
  - escala frente a unidades;
  - período frente a la columna;
  - signo;
  - perímetro;
  - cita en la página citada y con la cifra;
  - derivados recalculados desde orígenes comprobados;
  - cero, ausente y no aplicable distintos;
  - revisor distinto del extractor y con la fuente examinada.
- **Puerta:** la ficha, el informe y el pipeline (paso 12) calculan la aptitud por entradas, y ninguna salida presenta la conclusión como apta para dinero real sin ella. Es condición necesaria, no suficiente: la entrega sigue siendo experimental.
- Los controles no demuestran la corrección semántica. Eso lo hace el revisor independiente examinando la fuente.

**Cobertura real conseguida** (detalle en `COBERTURA_ENTRADAS_4_14.md`):
- **Viscofan:** 210 de 232 verificadas; 21 discrepancias y 1 pendiente. Lo que puede mover el valor: pensiones de 2025 (≈ +0,13 €/acción) y el número de acciones (≈ −0,49 €/acción; decisión D3).
- **Vidrala:** 219 de 226 verificadas; 6 discrepancias y 4 pendientes. Lo que puede mover el valor: circulante y adquisiciones de 2024 por la venta de Italia (cotas groseras de hasta ≈ −0,8 y ≈ 0,25 €/acción).
- Ninguna de las dos es apta por entradas. Extractores y revisores son agentes Claude con contextos separados, no revisiones humanas.
- Los precios de Viscofan (boletín oficial de BME) y Vidrala (informe de gestión 2025) están verificados.

**Impacto en el plazo (estimación):**
- Unas 6–8 horas de agentes por empresa entre extracción y revisión, en paralelo entre empresas, más la corrección de lo que aparezca. Toda corrección exige recalcular solo lo afectado y una auditoría nueva.
- **Para Elis**, la verificación se añade a su recorrido completo y depende de que lleguen sus documentos.
- **Consecuencia:**
  - La candidata se retrasa del lunes a mediodía al lunes por la tarde.
  - El tercer expediente, Elis, es lo que más riesgo tiene de no quedar completo y verificado dentro de la ventana. Si no cabe, se entregará con el estado exacto de su verificación, sin presentarlo como apto.

## 6. Tercera empresa

La persona responsable eligió Elis, con Ahold Delhaize de reserva, por las características del negocio y la disponibilidad del expediente, antes de ver su valoración. Las reglas están fijadas en `SELECCION_TERCERA_EMPRESA.md`.

**Estado (hechos):**
- Recibidos `Elis_evaluada.xlsx` (SHA-256 `b775e6b0…`) y `Elis_respuesta.md` (`999c42d4…`), y los diez informes anuales 2016–2025 de la carpeta ELIS, copiados con sus bytes. Inventario en `INVENTARIO_ELIS.md`; la etapa 1 no se repite.
- El Excel V5.3 no tiene Historia de 10 años: se construye desde los diez informes, con el registro de verificación de las entradas.
- La documentación de 2026 que faltaba (semestral, presentación y comunicados) se descargó con `descargar_fuentes_elis.bat` en el ordenador de la persona responsable. Dos páginas web no se descargaron (comunicado H1 en GlobeNewswire y ajuste del ratio de la OCEANE en Euronext); no son imprescindibles, porque el informe semestral y el comunicado de la conversión cubren esos datos.
- Base propuesta: 31-dic-2025, con los datos de 2026 reexpresados o tratados como contraste (sin adoptar).
- Regla fijada: el lino propio que Elis alquila (inmovilizado) no es un derecho de uso NIIF 16.
- La fase A decidirá el motor. Si sale el motor A, se conserva y se evalúa la reserva.
- **Historia 2016–2025 construida** (`fase1_v63.json`): 10 años; 70 reexpresiones resueltas con la cifra más reciente y su fuente; 16 ceros pendientes de verificación. Los informes de 2016 y 2024 están en francés. Dudas de los extractores en `evidencias/ELIS_HISTORIA_DUDAS.md`.
- **Metadatos:**
  - precio 24,18 € del 4-nov-2026, contrastado con el histórico oficial de Euronext (no ajustado), leído en el navegador integrado;
  - Bund a 10 años 3,29 % (Investing.com; la curva del Bundesbank da 3,38 %, ambas anotadas);
  - acciones diluidas 2025: 259,08 M;
  - sector «Business & Consumer Services».
- **Aviso para la fase A:** las acciones diluidas ya incluyen 23,36 M de la conversión de las OCEANE. Si el puente del valor resta además las OCEANE como deuda, se cuentan dos veces. Relacionado con D3.

## 7. Decisiones pendientes (enviadas; ninguna adoptada)

Orden propuesto: D2 (delimitación de P-M1) → D1 (criterio de materialidad para el objetivo) → D7 (contraste con las probabilidades de referencia) → D5 → D3/D4.

Mientras no se decidan, los expedientes 4.14 se regenerarán con el contrato nuevo y la configuración vigente, sin adoptar nada, y los efectos se mostrarán por separado.

## 8. Siguiente

1. Correcciones de las entradas con discrepancia confirmada y reclasificación de los ceros inferidos, en las ramas 4.14; vuelta al revisor de lo cambiado (`COBERTURA_ENTRADAS_4_14.md` §6).
2. Ramas 4.14 de los tres expedientes:
   - fase C regenerada con el contrato 4.14;
   - S5 en Viscofan;
   - el registro de entradas verificado;
   - auditoría nueva del material final, con agentes reales;
   - de forma homogénea y separada del control congelado (precios de Sí de referencia: 56,0180901889 y 40,1640071815).
3. Elis: configuración y reglas propias congeladas, pipeline con agentes reales (la fase A decide el motor) y verificación de sus entradas.
4. Hito 2, esta noche: ramas 4.14 con las entradas corregidas, Elis y decisiones.
