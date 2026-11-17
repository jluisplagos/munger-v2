# F1-IMPL · motor A con el perímetro F1 · 4.15

Fecha: 17-nov-2026. Lo escribe el agente autor de F1-IMPL (Claude, Opus, esfuerzo alto) en la rama `f1/implantacion`, creada desde la
candidata `integracion/candidata-cierre-v2` @ `b129b36` (4.15 · hito 2). **Sin revisión independiente todavía**: la hará otro agente
(Fable). Aquí se distinguen **hechos** (comprobados con una prueba o un archivo), *interpretaciones* y ***propuestas***.

**Aptitud: uso supervisado experimental. No apto para decisiones con dinero real.** Superar estas guardas no acredita aptitud.
**Elis sigue en `pendiente_de_datos`.** Ningún cambio desbloquea una valoración.

Fuentes de lo que se implanta:
- decisiones registradas el 17-nov-2026: `munger-v2-evidencias-mistral`, `coordinacion/cierre_v2/DECISIONES_PARA_EL_USUARIO.md`:68–83;
- texto aprobado: la tabla única de `PROPUESTA_DECISIONES_F1.md` y `DECISIONES_F1_UNA_POR_UNA.md` (rama `auditoria/economica-f1-frente-e` @ `9cad78d`);
- guardas y pruebas: `ESPECIFICACION_F1_PROPUESTA.md` (E2–E5, E9: T1–T16).

## 1. Diseño técnico (qué se cambió y por qué así)

**Hecho.** El motor A del personaje es la plantilla V6.3 (Excel): `Historia C58` (f), `C53` (ancla de S2C) y la hoja `Motor`. Las reglas
del encargo prohíben cambiar las plantillas de referencia, y una plantilla nueva exigiría filas nuevas de la Historia, su extracción en la
fase 1, su verificación de entradas (4.15) y una referencia de integridad nueva: no cabe en un día con garantías.

**Diseño.** Una capa del motor A en Python, `personaje_v2/scripts/motor_a_f1.py`, que:
1. lee el libro V6.3 recalculado (Historia, Análisis, Palancas, Diagnóstico V6 y Control maestro L4) y una declaración del expediente,
   `motor_a_f1.json`, con lo que el libro no tiene (norma contable, perímetros, D&A ROU y PPA por año con su signo y su fuente, compras,
   transición, R estimada, ajustes N1);
2. **reproduce el libro** con las mismas ecuaciones (Convenciones V6.3 §1–§3 y §10) en el perímetro A0: f = C58, τ = C52, m0 = C48,
   ancla = C53 y los 33 flujos del Motor. Si no los reproduce, bloquea (`F1-REPLICA`): la capa y el libro son el mismo motor;
3. calcula f (E3), el ancla (E4), los flujos de los años 1–10 y del año 11 con los términos explícitos (E3) y el flujo sin crecimiento
   con el perímetro declarado y, como diagnóstico rotulado, con A0, A1, A2 y la cota B;
4. evalúa V-F1a…V-F1m con la severidad de E5 y unas guardas de implantación `F1-*` (§3);
5. hace la **comprobación K3** (§4);
6. el pipeline la ejecuta en el **paso 7** (antes de la fase B) y en el **paso 12** (con las palancas finales), solo con el motor A y en
   los expedientes que la exigen (§5). La ficha y el informe muestran el resultado.

**Consecuencia que hay que tener presente (límite principal, §6).** El libro V6.3 sigue calculando A0. Con cualquier otro perímetro (o con
N1), su valor no corresponde a la declaración, así que la conclusión del motor A queda bloqueada (`F1-LIBRO`) y los flujos F1 son un
diagnóstico. Hoy no cambia nada en la práctica, porque Elis está bloqueada por R; pero el siguiente caso NIIF 16 (Ahold) necesitará que
el valor se calcule con el perímetro F1 (***propuesta***: una plantilla V6.3.1 F1 o que la capa calcule también el valor, con su prueba).

## 2. Tabla decisión → cambio → prueba → resultado

`motor_a_f1.py` es `personaje_v2/scripts/motor_a_f1.py`; la batería es `personaje_v2/pruebas/test_motor_a_f1.py` (103 pruebas, sin
LibreOffice); la regresión de Elis es `scripts/regresion_elis_f1.py` de esta carpeta (36 comprobaciones sobre una copia).

| Decisión | Cambio de código | Pruebas | Resultado |
|---|---|---|---|
| (1a) b: la reinversión que calibra f excluye la ROU; FCF base, C48 y C49 sin cambios | `DX_de` (perímetros A0, A1, A2, A3 de E2); f con D_X (E3); ancla con D_X (E4); terminal con la f del perímetro | T1, T2, T3, T3b(a) sobre el libro real (10⁻¹² en f, 10⁻⁹ en flujos y C53); T5; T2 control negativo del año 11 (205,363); regresión «+139,4» | PASA: A1 − A0 = **+139,381721** en la base 2025 |
| (1a) A0 solo sin arrendamientos; W3; V-F1a, V-F1b, V-F1e, V-F1m (E5) | guardas V-F1a (sin umbral: cualquier importe), V-F1m, V-F1b, V-F1e (invariantes, signo R415-SIGNO) | «G · W3» (cuatro casos), «V-F1a sin umbral» (0,001), V-F1b, V-F1e (tres), T9 | PASA |
| (1b) media 2023–25 como convención, sensibilidad al peso de 2025 a la vista | `sensibilidad_peso_arrendamiento_1b` en el resultado (serie declarada de pagos) | regresión de Elis | PASA: pagos −16,778; ROU +10,118; total −6,660 |
| (2) (i) la PPA no es reposición | `F1-2i`: A0 y A1 con PPA > 0 bloquean | «F1-2i» (dos sentidos), T6, AH | PASA |
| (2) (ii) gasto comercial en el margen, no en R | V-F1d exige `incluye_gasto_comercial: false` | «V-F1d … gasto comercial (P2f)» | PASA |
| (2) (iii) inversión propia por clientes sustituidos en R | V-F1d exige `reposicion_clientes` declarada | «V-F1d … sin fuente…» | PASA |
| (2) (iv) compras de cartera en R o término, nunca solo crecimiento | `reposicion_con_importe`: R_compras en D_X (A3) o término X_t = a·V_t fuera del ancla; V-F1j | T15 P2b, P2d; «V-F1j» (cuatro) | PASA |
| (2) (v) PPA y ROU como proporción constante; V-F1f, V-F1h | V-F1h (matriz de E2); V-F1f informa de los efectos de escala y del agotamiento | T15 P2g; «V-F1h» (tres); «V-F1f» (dos); regresión (PPA +4,206; ROU −10,118; 3,21 años) | PASA |
| (3a) R pendiente; R = R_propia + R_compras (+ transición); V-F1c, V-F1d | A3_estimado con R por año en tres partes; V-F1c parte a parte (AVISO con justificación, si no BLOQUEA); V-F1d; materialidad 736,0–867,2 informativa | «V-F1c» (cuatro, `guardas_V_F1c`), «V-F1d» (cuatro); Elis: V-F1d bloquea | PASA |
| (3b) (iv) mantener el bloqueo | sin cambio propio: sin estimación, V-F1d bloquea | regresión de Elis | PASA |
| (4a) un solo perímetro; V-F1g, V-F1k; bloque 10 con C179 (fila 178 = marginal − ROIC, W2) | V-F1g, V-F1k (perímetro, BLOQUEA); V-F1k numérico desde `Diagnóstico V6` B178:D178 y C179: AVISO solo si \|salto\| > C179; igualdad exacta con (1+g∞) informada | «V-F1g», «V-F1k» y seis casos W2 (±0,06, ±0,05 frontera, 0,0501, Elis) | PASA; Elis +0,47/+0,68/+2,41 ≤ 5: informa |
| (4b) opción A: compras pendientes hasta M6; V-F1j bloquea | V-F1j con `pendiente` o sin declarar | «V-F1j … pendientes»; Elis | PASA |
| (5a) N1 sin efecto fiscal, N2 pendiente, no deducir 27,936, V-F1l | `tasas_y_ebit`: EBIT − ajuste y τ = gasto ÷ (BAI − ajuste) con 4 decimales; m0 y τ de 5 años recalculados; V-F1l (fuente, regla fiscal, caja, BAI y gasto; N2 y otras reglas no aprobadas; el diagnóstico no se deduce; m_obj sin ajustes declarado) | T16 en la batería y en la regresión; «V-F1l» (cinco) | PASA: f 0,044900433; flujo 236,891 (−11,605); año 11 NORMAL −18,609 |
| (5b) por finalidad documentada; H > 10 bloquea (V-F1i) | términos explícitos X_t de E3 (años 1–H, fuera de Gordon con H ≤ 10); V-F1i (sin declarar, pendiente, H > 10, permanente como término, temporal en R, en R y término, término en el ancla, sin finalidad) | T15 P1b; «V-F1i» (siete) | PASA |
| E8.1 τ registrado de cinco años | `CONVENCION_TAU = "cinco_anios"` | réplica (τ = C52) y mutación m11 | PASA |
| Umbral de V-F1a: ninguno | `PARAMETROS_SIN_VALOR["umbral_v_f1a"]`; un umbral declarado no se aplica (`F1-PARAM`) | «umbral de V-F1a declarado» | PASA |
| Norma contable como entrada declarada; US GAAP | `F1-NORMA`: sin declarar, no NIIF o distinta de Control maestro L4 → bloquea; US GAAP → límite declarado | «F1-NORMA» (tres), «US · demostración», «US · …bloquea» | PASA |
| K3 automática | puente FCF base → flujo sin crecimiento (§4) en cada perímetro; `F1-K3` si no cuadra | «K3» (cuatro), «ELIS · K3», mutaciones m17–m18 | PASA (encontró un error de la cota B, corregido) |
| Generalidad NIIF 16 pesado (tipo Ahold) | sin código propio | «AH» (tres) | PASA |

## 3. Guardas de implantación (no están en E5; las añade F1-IMPL y hay que revisarlas)

| Id | Salta cuando | Severidad · efecto | Por qué |
|---|---|---|---|
| `F1-NORMA` | norma sin declarar; no NIIF; NIIF frente a un libro que dice otra cosa; US GAAP | BLOQUEA · INCOMPLETO, DATOS INVÁLIDOS o MODELO NO APLICABLE | la norma es entrada declarada (encargo, generalidad) |
| `F1-2i` | A0 o A1 con PPA > 0 en la ventana (o PPA vacía) | BLOQUEA · MODELO NO APLICABLE (o INCOMPLETO) | (2)(i) aprobada; E2 aún listaba A1 como coherente. *Interpretación*: con (2)(i) aprobada, A1 con PPA deja de estar cubierto. Para A0 sin arrendamientos y con PPA, (1a) lo admitiría y (2)(i) no: **combinación sin decidir, se para y se reporta** |
| `F1-PARAM` | se necesita un parámetro sin valor adoptado (alcance de N1 fuera de la ventana; actualización financiera del earnout; un umbral de V-F1a declarado) | BLOQUEA · INCOMPLETO | no se elige ningún valor; se calculan las variantes |
| `F1-REGISTRO` | una decisión declarada sin fecha, persona y motivo | BLOQUEA · INCOMPLETO | E2: «no la rellena el agente» |
| `F1-PERIMETRO` | perímetro sin declarar, no admitido o no calculable | BLOQUEA | — |
| `F1-DECLARACION` | claves desconocidas (p. ej. intentar declarar C48) | BLOQUEA · DATOS INVÁLIDOS | T10: las entradas registradas no se tocan |
| `F1-REPLICA` | la réplica A0 no reproduce el libro | BLOQUEA · fallo de implementación | la capa tiene que ser el mismo motor |
| `F1-K3` | el puente no cuadra | BLOQUEA · fallo de implementación | §4 |
| `F1-LIBRO` | perímetro distinto de A0, o N1, en un libro V6.3 | BLOQUEA · MODELO NO APLICABLE (límite declarado) | el libro calcula A0 sin normalizar |

Extensión declarada de V-F1b: con A0, C49 = 0 y la D&A ROU **vacía**, A0 no se admite (vacío ≠ 0; (1a) exige la ROU comprobada a cero).
*Interpretación*: también V-F1i bloquea una transición `en_R` con un perímetro de D&A (A1/A2), porque la D&A no la contiene de forma
comprobable.

## 4. K3: el flujo sin crecimiento frente a la caja base, partida a partida

Para cada perímetro, `K3.lineas` descompone exactamente el flujo sin crecimiento F₀ = V₀·[m₀(1 − τ) − f]:
FCF base (Historia C70) + nivel del EBIT del año base frente a la media, al τ de proyección + diferencia de τ de proyección frente al de cada
año − f aplicada a la diferencia de ventas + reinversión de la ventana que la proyección sin crecimiento no repite. Esa última se desglosa
en inversión neta propia y circulante, **− la ROU que D_X devuelve con los pagos ya dentro del FCF base** (clase `doble_computo`) y **− la
PPA que D_X devuelve como reposición** (clase `reposicion_no_monetaria`). La identidad tiene que cuadrar a 10⁻⁹ (`F1-K3`).

**Hecho (Elis, A0):** 307,933 + 39,600 − 7,965 − 9,872 + 136,767 − 132,500 − 85,467 = 248,496; K3 señala 139,382 de doble cómputo del
arrendamiento y 89,906 de PPA a la escala de 2025. En A2 no queda ninguna partida sin explicar. En el caso sintético tipo Ahold, 1.450 y 50.

Límite de K3: el puente es una identidad; detecta las partidas mal escritas (mutaciones m17 y m18) y nombra la amortización no monetaria
que la proyección cobra además de su caja. No detecta un doble cómputo que no pase por D_X (p. ej. un FCF base mal construido).

## 5. Integración en el pipeline, la ficha y el informe

- `pipeline.py`: método `motor_a_f1` y dos llamadas (paso 7, tras `comprobar_entrada_v63.py`; paso 12, tras el recálculo). Si una guarda
  BLOQUEA: `pendiente_de_datos` (falta de datos o de decisión), o `no_entregable` con `limite_del_modelo` (límite) o
  `fallo_de_implementacion` (réplica o K3). Escribe `motor_a_f1_resultado.json/.md` y `estado_pipeline.json → motor_a_f1`.
- **Exigencia** (`motor_a_f1.exigido`): con `motor_a_f1.json`, o en un expediente de la 4.15 con `entrada_efectiva.json` (que
  `cambiar_base.py` escribe en todo expediente nuevo). Sin declaración, un expediente nuevo con motor A bloquea en el paso 7 (no hay
  resultado silencioso). Los expedientes anteriores y la línea de base sintética v2.2 no cambian (sus cierres están ligados a su huella,
  la misma razón que en el hito 2, I20).
- `ficha.py`: bloque `motor_a_f1` solo si existe `motor_a_f1_resultado.json`; `esquema/ficha.esquema.json` lo describe.
  `informe.py`: una línea «Motor A · F1».
- `verificar_paquete.sh completa`: la batería nueva es obligatoria (mínimo 103).

## 6. Lo que no se implantó, y por qué

- **El valor del motor A con el perímetro F1** (por acción, escenarios, precio de referencia): el libro V6.3 calcula A0 y no se cambia la
  plantilla (`F1-LIBRO`). ***Propuesta***: plantilla V6.3.1 F1 construida por guion desde la V6.3 (como la V6.4.1), o el valor en la capa
  con réplica del Motor; las dos necesitan su prueba y su revisión.
- **H > 10 en la transición** (W1): bloquea (V-F1i); la fórmula de E3 con VP_pend no está implementada.
- **US GAAP** (Zoetis, Waste Management): **bloquea como límite declarado**. Demostración sintética (US1/US2 de la batería): con un
  arrendamiento operativo (coste lineal en el EBIT, pagos en el CFO, C49 = 0) y la amortización del derecho de uso dentro de la fila 8, la
  misma declaración F1 exige A1 si la variación del pasivo no está en la fila 14 y A0 si lo está. F1 no tiene esa clasificación, así que no
  hay una regla correcta con las entradas actuales. Haría falta declarar dónde están la amortización no monetaria y la variación del pasivo.
- **Lectura de las series nuevas desde la fase 1**: D&A ROU, PPA, pagos, BAI, gasto y ajustes N1 van en `motor_a_f1.json`, con documento y
  página, pero **no pasan por `verificacion_entradas.py`** (la verificación de entradas de la 4.15 no los cubre). En Elis salen del CSV
  verificado del frente E (estado OK, edición vigente; `datos/elis_cifras_f1.json`).
- **T12** (reproducción independiente del frente E), **T13** (caja no nula: la capa no usa C76) y la regeneración de los expedientes del
  motor A: fuera de este encargo.
- **T15**: no se ejecutan los 32 casos de `controles_sinteticos_f1.py` uno a uno (su formato no es el de la Historia); se prueban sus
  mecanismos con casos propios (P1b, P2b, P2d, P2g, P4d, P4f, V2b/V2g por el ancla, P2f, P1a, P1d, P2c por las guardas).
- `cambiar_base.py` no escribe una declaración F1 vacía en los expedientes nuevos (la exigencia por `entrada_efectiva.json` ya falla en
  cerrado).

## 7. Parámetros sin valor adoptado (no se eligen; se calculan las variantes y bloquea `F1-PARAM`)

| Parámetro | Opciones | Elis (variación del flujo sin crecimiento por N1) |
|---|---|---|
| alcance de N1 a los ejercicios del τ fuera de la ventana | solo la ventana / también 2021–22 | −11,605 / −11,190 |
| actualización financiera del earnout de México | fuera / dentro del BAI que da el tipo | −11,605 / −12,396 (las dos: −11,980) |
| umbral de V-F1a | ninguno adoptado: bloquea con cualquier importe | materialidad mostrada: ROU media 132,5 = 43 % del FCF base |

Otras elecciones sin decidir encontradas (paradas, no resueltas): A0 sin arrendamientos y con PPA > 0 (`F1-2i`, §3); la declaración del
perímetro de Elis (las decisiones excluyen ROU y PPA y dejan R pendiente; la regresión usa A3_estimado sin estimación, con
`F1-REGISTRO` porque ese valor no está literalmente registrado).

## 8. Pruebas ejecutadas (hechos; código de producto de `eb193f8`)

| Orden | Resultado literal |
|---|---|
| `cd personaje_v2 && python3 -B pruebas/test_motor_a_f1.py` | `103/103 pruebas del motor A F1 (4.15) PASAN` |
| `python3 -I …/f1_impl/scripts/regresion_elis_f1.py <copia fuera del repo>` (desde `munger_v2_r1/`) | `36/36 PASAN` (`resultados/regresion_elis_f1.md`) |
| mutaciones de `motor_a_f1.py` (`resultados/mutaciones_motor_a_f1.txt`) | 17 de 18 detectadas; m16 explicada |
| `flock … python3 -B …/f1_impl/scripts/prueba_pipeline_f1.py …` (desde `personaje_v2/`, LibreOffice, sintética) | `5/5 pruebas del gancho F1 del pipeline PASAN` (`resultados/prueba_pipeline_f1.txt`) |
| `flock … bash verificar_paquete.sh completa` sobre una copia limpia de `eb193f8` (manifiesto 7780/7780) | `RESULTADO GLOBAL: PASA`, código 0 (`resultados/verificacion_completa_eb193f8.txt`): comprobadores 114/114, sintética 30/30 con los mismos nombres que la línea de base v2.2 (30 · faltan 0 · nuevas 0), vigencia H5 59/59, juicio 27/27, entradas 4.14 33/33, entradas 4.15 190/190, entrada efectiva 62/62, relevo 5/5, motor A F1 103/103, integración V6.4 199/199, trazabilidad 78/78, integridad 103/103, auditorías 55/55, estados 28/28, resumen 45/45, cierre 55/55 |

La prueba del gancho: P1, expediente 4.15 sin declaración → paso 7, `pendiente_de_datos`, diagnóstico F1, ficha con el bloque «no
utilizable»; P2, empresa sintética sin arrendamientos ni PPA con todo declarado → F1 no bloquea, el gancho corre en los pasos 7 y 12 y el
análisis llega a `concluido` con el bloque «utilizable»; P3, US GAAP → paso 7, `no_entregable` · `limite_del_modelo` con `F1-NORMA`.

Después de `eb193f8` solo cambian este documento, el script y la salida de la prueba del gancho, el registro de la regresión, el
manifiesto y el registro de cambios (sin código de producto).

## 9. Riesgos para el revisor

1. Que la capa F1 bloquee pero el libro siga dando un valor A0: la ficha y el informe muestran el bloque, y el pipeline termina; un uso
   manual del libro fuera del pipeline no queda protegido.
2. Las guardas `F1-2i` y la extensión de V-F1b son interpretaciones de (2)(i) y de (1a).
3. La exigencia depende de `entrada_efectiva.json`: un expediente nuevo preparado sin `cambiar_base.py` y sin declaración no la tendría,
   y relanzar el pipeline sobre un expediente de la 4.14 (sin ese archivo; p. ej. `elis_motor_A`) tampoco evalúa F1. El hito 2 ya exige
   regenerar esos expedientes con `cambiar_base.py`, que sí lo escribe.
4. La regla de signo de las series replica la de `verificacion_entradas.py` (lista de «ninguno») sin importar la función.
5. T15 por mecanismos, no por los 32 casos.
