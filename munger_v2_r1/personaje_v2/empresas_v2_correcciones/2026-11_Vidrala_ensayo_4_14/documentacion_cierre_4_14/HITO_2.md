# Hito 2 · Munger v2 · 4.14 · decisiones aplicadas, tres expedientes y código i5

Fecha: 14-nov-2026. Base: ZIP de la 4.13 (SHA b1f747a1…). Instantánea de código: **i5**, que es i4 más 7 archivos (`instantaneas/i5/cambios_i5_frente_a_i4.diff`, `huellas.txt`).

**Separación.** Los **hechos** se dan con su evidencia. Las *interpretaciones* y las *propuestas* van marcadas como tales.

**Aptitud.** Ningún APROBADO de este hito acredita aptitud para dinero real. La verificación de las entradas es una condición necesaria, no suficiente. Las conclusiones son de uso supervisado y experimental.

## 1. Resultado por empresa

| Expediente | Decisiones aplicadas | Estado | Cubo · acción | Precio de Sí / objetivo | Auditoría | Condiciones de la persona responsable |
|---|---|---|---|---|---|---|
| `viscofan_decisiones/Viscofan` (motor B, V6.4.1) | D3 y E1 | concluido | Vigilar · esperar | 39,80 €, condicionado (18 variantes entre 38,13 y 42,98 €, todas «caro»); precio 54,70 € del 3-nov-2026 | APROBADO en el 2.º intento (SA-bdff49a38c72fabd). El 1.º fue REPETIR por un texto de la configuración | D3 a)–e): cumple (`auditoria_condiciones_D3.v2.md`) |
| `vidrala_decisiones/Vidrala` (motor B, V6.4) | E1 y E2, decididas; E3 y E4, supuestos de la orquestación | concluido | Vigilar · esperar | 56,00 €, condicionado (19 variantes entre 51,26 y 65,72 €, todas «caro»); precio 90,10 € | APROBADO (SA-fa0472f6bde97775) | E2 a)–f): cumple (`auditoria_condiciones_E2.md`) |
| `elis_decisiones/Elis` (motor A, V6.3) | E6 | pendiente_de_datos (reparto del capex no publicado) | Vigilar · sin acción | precio de Sí 7,30 € frente a 24,18 € (4-nov-2026), zona caro. **No es una conclusión utilizable** (F1). Réplica sin la doble cuenta: 11,08–21,89 €, todo «caro» | APROBADO (SA-d58921ca0d0cf0fa) | E6 a)–i): cumple (`auditoria_condiciones_E6.md`) |

**Ramas 4.14.** Se conservan sin cambios como expediente anterior y no se auditan, porque las sustituyen los expedientes de decisiones. Sus registros de entradas no eran aptos: las discrepancias que motivaron las decisiones (INCIDENCIAS I2).

## 2. Efectos separados (mecánicos, con las fases del expediente anterior fijas)

- **Viscofan** (`resultados/efecto_decisiones_viscofan.json`):
  - solo el denominador: 40,30282 → 39,85225 € (−0,45057);
  - solo la capitalización: −0,05466 €, por la r operativa (8,2603 → 8,2677 %);
  - las dos juntas: 39,79819 € (−0,50462);
  - E1: 0;
  - dilución potencial del plan, declarada aparte: 39,52748 / 39,39350 €.
- **Vidrala** (`resultados/efecto_correcciones_vidrala.md`):
  - frente a la rama: E2 alternativa +0,049 €, E3 pareja B +0,010 €, E1 y E4 0;
  - con las decisiones, el precio de Sí reproduce la rama (56,00201 €).
- **Elis** (`resultados/efecto_decisiones_elis_E6.md`): el anterior se reproduce exactamente (6,55634 €) y el caso «todo» reproduce exactamente el expediente nuevo (7,30206 €).
  - denominador C55 (259,077654 → 232,47681): +0,75020 €;
  - capitalización: 0;
  - pensiones I25:L25: 0, porque el motor A no las usa;
  - medias exactas: −0,00402 €;
  - entradas reexpresadas a 2025: 0;
  - todo: +0,74571 €.
  - Dilución potencial NO incorporada:
    - conversión de la OCEANE (acciones + 23,36 M y C48 sin el cupón de 8,55): −0,14650 €;
    - acciones de rendimiento: −0,08119 € (vivas) y −0,09721 € (al 120 %).

## 3. Decisiones y supuestos

Las decisiones se recogen literalmente en `decisiones/DECISIONES_ENTRADAS_4_14.md`.

**Decisiones de la persona responsable:** E1, D3 (con sus condiciones), E2 y E6.

**Supuestos de la orquestación, reversibles con una decisión explícita:**
- E3 y E4;
- F1 = (a): el defecto del motor A con NIIF 16 se declara y no se corrige en esta entrega;
- medias exactas en Elis, por el precedente de E1;
- precio de Elis del 4-nov-2026 con las acciones de 2025, por el mismo criterio que D3.

## 4. Código (i5)

| Archivo | Cambio | Prueba |
|---|---|---|
| `scripts/verificacion_entradas.py` | Una hipótesis o convención material con la comprobación «pendiente» bloquea el apto (INCIDENCIAS I1). La cobertura del universo se cuenta aparte de los auxiliares (I9). | `test_verificacion_entradas_414.py` 33/33 |
| `scripts/cambiar_base.py` | `correcciones_fase1_partes`: corrección de extracción con el valor impreso esperado, la fuente, el motivo y la nota de la partida. El original va a antecedentes y la preparación se detiene si lo encontrado no es lo esperado (I10). | `test_integracion_v64.py` grupo D, 9/9 |
| `scripts/pipeline.py`, `scripts/informe.py` | El recuento «N de M» usa la cobertura del universo (I9) | — |
| `verificar_paquete.sh` | Mínimos obligatorios: verificación de entradas ≥ 33 e integración V6.4 ≥ 198 | — |

**Verificación completa sobre una copia de i5** (`ronda_i5/verificacion_completa.txt`; 17:51–18:27): pasan las 12 baterías, sin ninguna escritura fuera de la copia.
- Las baterías: comprobadores 114/114, piloto, sintético 30/30 (mismos nombres), H5 59/59, juicio sobre el objetivo 27/27, verificación de entradas 33/33, integración V6.4 198/198, trazabilidad 78/78, integridad 103/103, solicitudes 55/55, estados 28/28, resumen 45/45 y cierre 55/55.
- El manifiesto falla, como se espera en un árbol modificado: se regenera en la candidata.

## 5. Alcance

`MATRIZ_ALCANCE_4_14.md`: **el alcance original no está completado.**
- El motor A tiene un defecto declarado con NIIF 16 y no tiene validación propia.
- El motor C no tiene ningún recorrido real.
- No hay batería propia de la entrada por instrucciones.
- No se ha ejecutado ninguna publicación real.

## 6. Incidencias

`INCIDENCIAS_4_14.md`: de I1 a I10 en la fecha del hito, y de I1 a I21 en la final (I11–I17, limpiezas y controles de la candidata; I18–I21, prueba de traspaso). Entre las del hito: la puerta de las entradas, que aceptaba hipótesis pendientes; un texto desfasado de la configuración; el CAMBIO de Vidrala v1; errores propios en los informes de efectos; la re-extracción de Viscofan frente al encargo; y la limpieza de espacio autorizada por la persona responsable.

## 7. Después de este hito

La candidata y la final se describen en `REGISTRO_ENTREGA_4.14.md`, `REGISTRO_PRUEBAS_4_14.md`, `DICTAMEN_4_14.md` y el registro externo de verificación del ZIP. El traspaso se probó con un agente receptor sin historial sobre el ZIP candidato (`traspaso/LEEME_TRASPASO.md`). Arrancó, verificó el paquete, resolvió el relevo de `elis_motor_A` en una copia y reanudó el pipeline hasta el paso 14. Sus observaciones se corrigen en la final (I18), salvo dos que tocan código y se declaran (I19 e I20).
