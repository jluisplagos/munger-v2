> **Nota de continuidad (entrega 3.1).** Las órdenes de este anexo usan las rutas de la sesión del diagnóstico (`diag/copia`, `diag/diagnostico`). Aquí, en `diagnostico/`, se incluyen las carpetas `pruebas/` y `resultados/`. La carpeta `trabajo/` (empresas sintéticas y libros recalculados) no se incluye: se regenera con las órdenes de la sección C. `diagnostico/` contiene también archivos de la fase del contrato, que este anexo no enumera:
> - `pruebas/h1_casos_contrato.py` y `pruebas/h2_casos_contrato.py`, con sus resultados `resultados/h1_casos_contrato*` y `resultados/h2_casos_contrato*` (línea de base de los casos nuevos con el código original);
> - `resultados/contrato_*.txt`: comprobación de que `fase_c.json` pasa el esquema de los dos turnos;
> - `resultados/h2_test_contra_codigo_original.txt`;
> - `resultados/manifiesto_zip_reextraido.sha256`: comprobación de que la copia coincidía con el ZIP original.

# Anexo reproducible · diagnóstico H1–H3 de Munger v2

Todo lo que figura aquí como resultado se ha ejecutado en esta sesión (8-nov-2026). Lo que no se ha ejecutado se indica expresamente como «no ejecutado» o «pendiente».

## A. Disposición y conservación de los originales

| Elemento | Ubicación |
|---|---|
| Adjuntos originales (no se han tocado) | `munger_v2_paquete.zip` (SHA-256 `61c70800d0faa7c4a98888b7413820ec8041153e53484c32b0c549b26b6af87d`) y el texto del encargo |
| Copia de trabajo (solo lectura durante las pruebas) | `diag/copia/` = el ZIP descomprimido (676 archivos, el mismo número que lista el ZIP) |
| Copia secundaria para la prueba de referencia del proyecto | `diagnostico/trabajo/copia_pruebas/` (duplicado de la copia; aquí escribe `test_pipeline_sintetico.py`) |
| Diagnóstico | `diagnostico/`: `pruebas/` (scripts), `resultados/` (salidas), `trabajo/` (carpetas sintéticas y libros recalculados) |

Integridad: `resultados/manifiesto_copia_inicial.sha256` (antes de las pruebas) y `resultados/manifiesto_copia_final.sha256` (después) son idénticos (`resultados/integridad_final.txt`); el SHA-256 de los adjuntos coincide antes y después.

**Ajustes para ejecutar:** ninguno en el código del proyecto. Para no crear `__pycache__` en la copia se usó `python3 -I -B`, y los scripts del proyecto se importaron con `sys.path.insert` desde `diagnostico/pruebas/`. Tampoco hizo falta ajustar rutas en `config_v2.json`: `comprobar_entorno.sh` dio código 0 en la copia secundaria.

## B. Entorno (`resultados/entorno.txt`)

Linux x86_64 · Python 3.13.18 · openpyxl 3.1.5 · lxml 6.1.3 · jsonschema 4.26.0 · LibreOffice 24.2.7.2 · pdftotext 24.02.0. Las ejecuciones de LibreOffice se hicieron en secuencia, nunca dos a la vez.

## C. Pruebas, comandos y resultados

Variables: `S=diag/copia/personaje_v2/scripts`, `E=diag/copia/personaje_v2/empresas_v2`, `D=diag/diagnostico`.

| # | Comando | Código de salida | Resultado | Salida |
|---|---|---|---|---|
| 1 | `python3 -I -B $D/pruebas/h1_comprobar_anio.py $S $D/trabajo $D/resultados/h1_resultados.json` | 0 | Acepta 1–7 y 10; rechaza 8, 9 y 11 | `h1_salida.txt`, `h1_resultados.json`; carpetas en `trabajo/h1/` |
| 2 | `python3 -I -B $S/fase1_historia.py comprobar-anio $D/trabajo/h1/1_revisor_capex_linea_inexistente 2025` | **0** (imprime «OK») | El caso del revisor pasa también por la línea de órdenes | `h1_cli_caso1.txt` |
| 3 | ídem con `8_control_numero_ausente` | 1 | Rechazo correcto | `h1_cli_caso8.txt` |
| 4 | `python3 -I -B $D/pruebas/h2_veredicto_auditoria.py $S $E $D/resultados/h2_resultados.json` | 0 | Ver tabla H2 | `h2_salida.txt`, `h2_resultados.json` |
| 5 | `bash $S/recalc.sh trabajo/h3/Aarsleff_v63_evaluada.xlsx trabajo/h3/recalc trabajo/h3/lo_perfil` (sobre una copia del libro) | 0 | Recálculo forzado | `h3_recalc.txt` |
| 6 | Control del recálculo: +1000 en `Historia!C11` de una copia, después recálculo | 0 | C35 pasa de −237,704 a 762,296, como se esperaba | `h3_control_recalculo.txt` |
| 7 | `python3 -I -B $D/pruebas/h3_aarsleff.py $E/Aarsleff trabajo/h3/recalc/Aarsleff_v63_evaluada.xlsx $D/resultados/h3_resultados.json` | 0 | 5 años negativos en las tres lecturas; 0 fórmulas dependientes; 27 apariciones de la frase | `h3_salida.txt`, `h3_resultados.json` |
| 8 | `python3 -I -B $D/pruebas/alcance.py $E $D/resultados/alcance_resultados.json` | 0 | Componentes, ceros y constructor de la Historia por empresa; afirmaciones del tipo «N años negativos» comparadas con la fila 35 | `alcance_salida.txt` |
| 9 | `python3 -I -B $D/pruebas/alcance_lineas.py $E $D/resultados/alcance_lineas.json` | 0 | 3.211 componentes: 3.205 con el número completo en su línea, 2 solo como subcadena (Hermès), 4 con formato «a + b» (Rational, válidos para su consolidador); concepto literal en la línea: 2.176; líneas con dos o más importes: 3.127 | `alcance_lineas_salida.txt`, `hermes_casos_reales_h1.md` |
| 10 | `bash scripts/comprobar_entorno.sh` (en la copia secundaria) | 0 | Dependencias y rutas correctas; autotest de `precio_de_si` PASA | `linea_base_comprobar_entorno.txt` |
| 11 | `python3 -B pruebas/test_pipeline_sintetico.py` (en la copia secundaria, línea de base) | 0 | **30/30 pruebas PASAN** (3 min 52 s, LibreOffice en secuencia), con la auditoría sintética de un solo punto que hay ahora. La reparación de H2 obliga a actualizarla | `linea_base_test_pipeline_sintetico.txt` |

### H1 · casos (resultado actual del código)

| Caso | Qué prueba | Resultado |
|---|---|---|
| 1 | Página «Revenue 123»; capex 123 con línea «Capital expenditure 123» (no existe) | ACEPTADO |
| 2 | capex con la línea real «Revenue 123» (otra partida) | ACEPTADO |
| 3 | «123» que solo aparece dentro de «91234» | ACEPTADO |
| 4 | Línea «Capital expenditure 150 123»; se declara 123 (ejercicio anterior) como actual | ACEPTADO |
| 5 | Página «Amounts in thousands»; el JSON declara «millones» | ACEPTADO |
| 6 | Cobro de 40 declarado con signo −1 | ACEPTADO |
| 7 | `cero` con motivo libre y página que solo dice «Revenue 123» | ACEPTADO |
| 8 | 999 ausente de la página | RECHAZADO |
| 9 | Página 7 inexistente | RECHAZADO |
| 10 | Línea y número presentes | ACEPTADO |
| 11 | `cero` con página inexistente | RECHAZADO |

### H2 · casos

| Caso | Código | ¿Cumple el formato de 16 puntos? |
|---|---|---|
| 1 Solo «Veredicto: APROBADO» | APROBADO | No |
| 2 «8. FALLA · hecho material inventado» + APROBADO | APROBADO | No |
| 3a/3b/3c FALLA en el punto 1 / 11 / 16 + APROBADO | REPETIR | No |
| 4 Texto vacío · 5 «APROBADO con reservas» · 6 dos veredictos | REPETIR | No |
| 7 16 puntos, FALLA en el 8, APROBADO | APROBADO | Sí |
| 8 16 puntos, FALLA en los 11 no bloqueantes, APROBADO | APROBADO | Sí |
| 9 16 puntos, todos PASA, APROBADO | APROBADO | Sí |
| Auditorías reales (Aarsleff, Hermès, Nike, Rational, Vidrala, Viscofan) | APROBADO | Sí, 16/16 y ningún FALLA |

El caso 4 de bloqueo (punto 4) no se probó por separado. El código trata los puntos 1, 4, 11, 12 y 16 con la misma comparación (`actual in (1, 4, 11, 12, 16)`), y se comprobaron tres de ellos.

### H3 · datos

Fila 35 (2016–2025): −237,704 · −65,982 · 284,983 · 454,963 · 906,965 · −410 · −628 · −93 · 848 · 1.569. Diferencia máxima entre los valores guardados, el recálculo forzado y el recálculo en Python: 0. Suma: 2.629,2. Medias: 268,6 (2016–20) y 257,2 (2021–25). La frase aparece en `Análisis!B102` y `Control maestro!N30` del libro evaluado, así como en `fase_a.json` (3), `fase_a.md` (2), `fase_c.json` (1), `ficha.json` (3), `informe.md` (4), `celdas_A.json`, `celdas_C.json`, `citas_fase_a.md` (3), `citas_fase_c.md`, `observaciones_para_citas.md` (4), `datos_v63.json` y `resultados.json`.

## D. Dependencias ausentes y comprobaciones pendientes

- **`texto/` de las seis empresas (o los PDF de sus informes anuales): no incluidos.** Sin ellos no se puede pasar `comprobar_anio` (ni el actual ni el reparado) sobre los 3.211 componentes reales, ni contrastar ninguna cifra con su documento original. No se declara comprobada ninguna cifra contra el original.
- **Lotes de la etapa anterior (V5.3 + personaje v1) y base de datos: no incluidos.** Solo están los seis `etapa1/*_evaluada.xlsx`, que no se han examinado en profundidad. En el kit v1 (`kit_pipeline_munger/`), el veredicto de auditoría lo leía el modelo orquestador, no un código (`prompts/verificacion.md` del kit, línea 24). Por eso H2 no se aplica tal cual a esa etapa, y su calidad queda sin evaluar.
- **`Rational/fase1_partes/consolidar.py`:** evaluado por lectura del código, no ejecutado. Necesita `texto/AR_<año>.txt`.
- **Búsqueda tipo H3 en las otras empresas:** limitada a frases como «N años/ejercicios negativos». Otras formulaciones no se han revisado.
- **Fallos de ejecución:** ninguno.

## E. Archivos creados

`diagnostico/pruebas/`: `h1_comprobar_anio.py`, `h2_veredicto_auditoria.py`, `h3_aarsleff.py`, `alcance.py`, `alcance_lineas.py`.
`diagnostico/resultados/`: `entorno.txt`, `sha256_adjuntos_inicial.txt`, `sha256_adjuntos_final.txt`, `manifiesto_copia_inicial.sha256`, `manifiesto_copia_final.sha256`, `integridad_final.txt`, `h1_*`, `h2_*`, `h3_*`, `alcance_*`, `hermes_casos_reales_h1.md`, `linea_base_*`.
`diagnostico/trabajo/`: `h1/` (11 carpetas de empresa sintéticas), `h3/` (copia del libro, recálculo, control), `copia_pruebas/` (copia secundaria; excluida del ZIP de entrega por tamaño).
