# Informe de la prueba de traspaso · Munger v2 · entrega 4.14

Sesión nueva, sin historial, trabajando solo con el paquete. Descompresión en `/home/claude/traspaso_414/munger_v2_r1`; registros de esta sesión en `/home/claude/traspaso_414/_logs/` y `/home/claude/traspaso_414/relevo/`. Fable no se usó. Los hechos llevan su evidencia; las *interpretaciones* y las **propuestas** van marcadas.

---

## 1. Primera tarea: verificación del estado

### 1.1 Integridad y lectura
- **Hecho.** El SHA-256 del ZIP coincide con el del `.sha256`: `f9f888e3…4f5a24`. La extracción con `unzip` fue limpia. Los adjuntos no se modificaron.
- **Hecho.** `CONTINUIDAD.md` se leyó entero (347 líneas).
- **Hecho.** `PROMPT_NUEVA_VENTANA.md` coincide, por debajo de su línea separadora, con el mensaje de arranque recibido.
- **Versión** (`VERSION`): «munger_v2 · r1 · entrega 4.14 (cierre con verificación completa de las entradas financieras …) · 2026-11-14 · base SHA-256 61c70800…».

### 1.2 `bash verificar_paquete.sh completa`
Una sola ejecución: 20:24:17–21:00:26, unos 36 minutos. Resultado: **RESULTADO GLOBAL: PASA, código 0** (`_logs/verificacion_completa.txt`).

| Bloque | Resultado |
|---|---|
| Manifiesto | 6.694 archivos · 0 modificados · 0 ausentes · 0 de más · PASA |
| Entorno | PASA (autotest precio_de_si: 5 casos + propiedades) |
| Piloto Vidrala 2025 | 35 comprobaciones CUMPLEN · salida idéntica a la de referencia · PASA |
| `test_comprobadores.py` | 114/114 |
| `test_pipeline_sintetico.py` | 30/30 · mismos 30 nombres que la línea de base (faltan 0, nuevas 0) |
| Vigencia H5 | 59/59 |
| Juicio sobre el objetivo | 27/27 |
| Verificación de las entradas | 33/33 |
| Integración V6.4 | 198/198 |
| Trazabilidad | 78/78 |
| Integridad de la auditoría vigente | 103/103 |
| Solicitudes de auditoría | 55/55 |
| Coherencia de estados | 28/28 |
| Resumen | 45/45 |
| Cierre | 55/55 |

### 1.3 Control de la 4.14 (después de la verificación)
- **Hecho.** `comprobar_entrega_4_14.py`: **35/35 comprobaciones PASAN, código 0** (`_logs/control_4_14.txt`).

### 1.4 Controles históricos (`controles_historicos_4_13.py`, en secuencia, terminando por el de la 4.13)

**Incidencia de esta sesión.** La primera ejecución (21:01) se interrumpió con `OSError: No space left on device`:
- el disco tenía unos 4,5 GB libres al empezar;
- la verificación completa los redujo a unos 2 GB;
- el control `4_8_1_comparar_baterias…` necesita unos 2 GB en `/tmp`.

**Limpieza.** Se hizo con la regla 11.10 de CONTINUIDAD y las rutas quedan registradas en `_logs/LIMPIEZAS.txt`. Se borraron tres cosas, todas salidas de pruebas ya terminadas o un temporal de esta sesión:
- los `*.xlsx` de `personaje_v2/pruebas/_v64/`;
- `personaje_v2/pruebas/_v64/vigencia/`;
- `/tmp/bat471_v8aovwgv`.

Los controles excluyen `pruebas/_v64/` de sus recorridos. Se repitió la serie completa en una carpeta nueva, de 21:02:56 a 21:28:54 (`_logs/controles_historicos_2/`).

| Control | Resultado sobre el árbol 4.14 | Frente al LEEME de la 4.13 (árbol 4.13) |
|---|---|---|
| 4.2, 4.3 (217/217), 4.3.1 (43/43), 4.4 (72/72), 4.5 (60/60), 4.6.1 (23/23) | completos, código 0 | salida idéntica a la de referencia |
| 4.6 | 23/24, código 1 (Z-1) | idéntica |
| Comparaciones de baterías de la 4.8.1 y la 4.8 | «HAY DIFERENCIAS», código 1 | idénticas |
| 4.7 (45/49), 4.7.1 (38/44), 4.8 (32/36) | código 1 | idénticas |
| 4.8.1 (25/30), 4.9 (34/39), 4.10 (40/44), 4.10.1 (38/43), 4.11 (34/38), 4.12 (59/63) | mismo recuento que el LEEME, código 1 | **salida distinta**: 1 o 2 líneas de detalle de las listas «solo cambian los archivos declarados» o «archivos nuevos…», que ahora incluyen archivos de la 4.14 (`historia_anio.md`, `fase1_historia.py`, `cambiar_base.py`, `comprobar_gramatica.py`…) |
| **4.13 (último)** | **83 de 89, código 1** | **El LEEME exige 89/89 y lo clasifica como exigencia funcional** |

En el control de la 4.13 no cumplen seis comprobaciones, todas de tipo «constata»:
1. los archivos de la 4.12 que cambian;
2. los archivos nuevos (los de la 4.14);
3. la ronda registrada de `verificar_paquete.sh`;
4. la sonda de tipos;
5. el contraejemplo del salto del protocolo (las tres anteriores, con `huellas_al_dia` falso porque la 4.14 cambió scripts);
6. «VERSION, CONTINUIDAD.md y PROMPT_NUEVA_VENTANA.md describen la 4.13».

*Interpretación.* Las seis están ligadas a las huellas o al texto de la versión 4.13, y no indican una regresión. Pero el paquete no documenta este resultado para el árbol 4.14.

### 1.5 Discrepancias entre CONTINUIDAD.md y los archivos o las pruebas
1. **Controles históricos.**
   - CONTINUIDAD §2.3, §11.4 y el mensaje de arranque remiten al LEEME de la 4.13, que describe el árbol 4.13.
   - En el árbol 4.14, el control de la 4.13 da 83/89, no 89/89, y seis salidas no son idénticas a las de referencia.
   - El resultado esperado sobre el árbol 4.14 no está en el paquete: `REGISTRO_PRUEBAS_4_14.md` §5 lo remite a un registro externo (`…VERIFICACION.txt`) que no se adjuntó.
2. **`MATRIZ_ALCANCE_4_14.md`**, que se declara «versión del hito 2», está desfasada frente a CONTINUIDAD y al registro:
   - dice que las auditorías de los expedientes de decisiones están «en curso»;
   - da la batería de entradas como 32/32 (no 33/33), la V6.4 como 196/196 sobre i4 y el grupo D como 8/8 (el registro dice 9/9);
   - atribuye a Vidrala las decisiones «E1 + E4» (el registro dice E1 y E2);
   - da por pendiente «Palancas!C47 en el registro de Vidrala», cuando I1 lo sitúa en Viscofan;
   - da como «en curso» la revisión de Elis;
   - cita la ruta `decisiones/HALLAZGO_MOTOR_A_NIIF16_4_14.md`, cuando el archivo está en `documentacion_cierre_4_14/`.

   `HITO_2.md` también da `elis_decisiones` como «en curso (fase C)».
3. **Número de baterías obligatorias.** §1 dice «12 baterías obligatorias» y §2 dice «Las diez baterías son obligatorias». *Interpretación:* 10 más la de comprobadores y la sintética; la redacción es ambigua.
4. **Secciones sin la 4.14.**
   - La cronología (§4) no tiene fila de la 4.14, y la fila de la 4.13 no tiene la columna «Dónde está».
   - El mapa del paquete (§7) no tiene fila del expediente de la 4.14.
   - La tabla de estado (§5) no tiene filas de la 4.12 a la 4.14.
5. **Duración de la verificación.** La guía del recorrido (§1.1) da unos 20–30 minutos; CONTINUIDAD da 25–45. Medido en esta sesión: 36 minutos.

---

## 2. Segunda tarea: relevo pendiente

### 2.1 Qué relevo se eligió y por qué
- **Hecho.** Expedientes de la 4.14 que esperan a un agente (`estado_pipeline.json → esperando`):
  - `elis_motor_A/Elis`: paso 13, auditoría, solicitud SA-ed5561eac1cc5897;
  - las ramas `viscofan/Viscofan` y `vidrala/Vidrala`: paso 13, con una auditoría presente no aceptada por estar ya usada;
  - `vidrala_decisiones_INVALIDO_perdio_analisis/Vidrala`: paso 6, fase A.
- **Elegido: `elis_motor_A/Elis`, relevo del agente de verificación (paso 13).** Motivos:
  - está sustituido por `elis_decisiones` (E6; `DECISIONES_ENTRADAS_4_14.md` línea 53);
  - la matriz lo da como «en curso» y su LEEME dice que «la auditoría se hace con agentes reales en este expediente», pero nunca se hizo;
  - es un relevo limpio, a la espera de su primera respuesta.
- **Descartados.**
  - Las ramas: INCIDENCIAS I2 dice expresamente que «no se auditan».
  - El expediente INVALIDO: sus entradas de análisis son erróneas por diseño (I3).
- **Dónde se trabajó.** En una copia hermana, a la misma profundidad: `…/2026-11_Vidrala_ensayo_4_14/elis_motor_A_relevo_traspaso/` (`cp -a`, diferencia 0).
  - Así no se modifica un expediente anterior (regla 3 y §11.3).
  - Tampoco se rompe `comprobar_entrega_4_14.py`, que exige que `elis_motor_A` no tenga archivos posteriores a `elis_decisiones`.
  - Plantilla: `--config personaje_v2/config_v2.json` (V6.3, motor A, según su LEEME).

### 2.2 Qué se hizo (hechos)
1. **Reanudación sin salida.** Código 10. Sigue esperando SA-ed5561eac1cc5897 para el material 9e1a725d6432f548 (`relevo/pipeline_01_…txt`). Al relanzar, el prompt `13_verificacion.md` se regeneró con las rutas de esta descompresión; salvo las rutas, es igual al del paquete.
2. **El relevo pendiente estaba caducado.**
   - **Hecho.** `verificacion_entradas.json` se escribió a las 14:56, después de fijar el material (14:26). Está en `cierre_v2.MATERIAL_FIJO` (4.14).
   - **Hecho.** El material calculado hoy es 72f855cf…, no el fijado 9e1a…; la única diferencia es ese archivo.
   - *Interpretación* (por lectura del código de `pipeline.py` y `cierre_v2.motivo_auditoria_no_corresponde`; no ejecutado):
     - un APROBADO que nombrara 9e1a… se rechazaría con «el material cambió después de la auditoría»;
     - el pipeline volvería a pedir la auditoría con el mismo identificador, porque mientras espera no vuelve a fijar el material;
     - al agotar las correcciones terminaría en `no_entregable`.
   - Por eso se siguió la guía (`GUIA_RECORRIDO_SUPERVISADO.md` §8.7: «`--desde 12` para el registro de las entradas»).
3. **`pipeline.py … --desde 12`.** Código 10 (`relevo/pipeline_02_desde_12.txt`).
   - Paso 12: verificación de las entradas 184 de 193 celdas del universo, **apta por entradas: no** (9 entradas materiales sin comprobar, 8 discrepancias). Son las que motivaron E6.
   - Paso 13: material **de91ac881e63499f** y solicitud **SA-21babb1dd24901d1**, que sustituye a SA-ed5561…
   - Respecto al material anterior: se añade `verificacion_entradas.json`; cambian `resultados.json` (solo la ruta de origen) y `acreditacion_libro.json` (el libro final es ahora el verificado); la ficha y el informe provisionales no cambian.
4. **Relevo resuelto.** La sesión actuó como agente de verificación siguiendo `prompts_generados/13_verificacion.md`, con solo Read, Grep y Bash de lectura, sin internet y sin escribir nada más que la salida. No hicieron falta notas: la carpeta temporal `_notas_auditor/` quedó vacía y se eliminó.
   - Se comprobaron los 16 puntos: listas de herencia (34), datos ausentes (21 frente a 21), clases y apoyos, etiqueta de C104 contra la tabla §D.6, citas con grep en `munger.md` y `damodaran.md`, y hechos muestreados con `pdftotext` en las páginas citadas (URD 2025, p. 442 y 143; informe semestral de 2026, p. 46).
   - `auditoria.md`: **16 puntos en PASA, «Veredicto: APROBADO»**, con avisos:
     - las incoherencias F1 afectan al objetivo, que no se emite;
     - los hechos de 2026 vienen de `fuentes_2026/`;
     - el registro de entradas no es apto y la ficha V6.3 no lo muestra.
   - Antes de relanzar, el lector del pipeline lo leyó como APROBADO.
5. **Reanudación.** **Código 0: `[paso 14] FIN · estado pendiente_de_datos · auditoría APROBADO`** (`relevo/pipeline_03_tras_auditoria.txt`).

### 2.3 Qué dio el pipeline al reanudarlo
- **Hecho.** Paso 14, estado `pendiente_de_datos`. Solicitudes: SA-ed5561 sustituida y SA-21babb1d respondida.
- Se escribieron `ficha.json`, `informe.md`, `cierre_vigente.json`, `diagnostico.md` y la fila de `elis_motor_A_relevo_traspaso/resumen_v2.csv`.
- Contenido de la salida:
  - cubo Vigilar, acción ninguna, zona caro;
  - precio de Sí 6,56 €, MALO 5,01 € y ponderado 7,17 €, frente a 24,18 €;
  - causa: falta del reparto del capex entre reposición y crecimiento; continuar desde el paso 2;
  - `aptitud_de_uso = null`.
- **Interpretación.** Con F1 (el motor A cuenta dos veces los arrendamientos NIIF 16 y los intangibles comprados), los 6,56 € no son una conclusión utilizable. El expediente vigente de Elis sigue siendo `elis_decisiones` (7,30 €, APROBADO).
- **Hecho.** Después del relevo, el control de la 4.14 sigue dando 35/35. Los 126 archivos de `elis_motor_A/` original coinciden con el manifiesto: 0 modificados y 0 de más.
- **Hecho.** No hubo ningún relevo posterior: el pipeline llegó al final.

---

## 3. Dificultades de la documentación
1. **Ninguna lista de relevos vivos.** Ningún documento lista los relevos pendientes ni dice cuáles siguen vivos. CONTINUIDAD no menciona que `elis_motor_A`, `viscofan/` y `vidrala/` estén en el paso 13. La matriz dice «en curso», I2 dice «no se auditan» y el LEEME de `elis_motor_A` dice que la auditoría «se hace» en ese expediente.
2. **Un relevo caducado sin aviso.** El material se fijó antes de que la orquestación añadiera `verificacion_entradas.json`, que la 4.14 incluye en el material. Ni `ESPERANDO.md` ni el prompt lo advierten.
   - *Interpretación:* un auditor que siguiera el prompt al pie de la letra no podría cerrar el expediente.
   - La salida (`--desde 12`) solo se deduce de la guía §8.7.
   - **Propuesta:** que el paso 13 vuelva a fijar el material o emita una solicitud nueva cuando, mientras espera, aparece un archivo de `MATERIAL_FIJO`.
3. **Rutas absolutas del entorno original.** Los prompts de `prompts_generados/` y varios JSON (`resultados.json → origen`, `estado_pipeline.json`, `fase1_*.json`) llevan rutas de `/home/claude/trabajo_4_14/trabajo/…`.
   - Los prompts del paquete no se pueden usar tal cual; solo valen después de relanzar el pipeline, que los regenera.
   - Las plantillas de relevo de la 4.13 (`relevos_agentes_4_13.md`) también usan rutas antiguas y una carpeta temporal de otra sesión.
4. **Copia o expediente original.** El paquete no dice si un relevo de un expediente sustituido se reanuda en su sitio o en una copia. Las reglas prohíben modificar expedientes anteriores, y el control de la 4.14 falla si cambia una fecha de `elis_motor_A`, `viscofan/` o `vidrala/`. La sesión eligió una copia hermana.
5. **«Contexto limpio».** El procedimiento supone un agente nuevo. Esta sesión no disponía de herramienta para lanzarlo, así que hizo el relevo ella misma después de haber leído la documentación del paquete. Es una limitación declarada: la auditoría no es independiente en el sentido del prompt.
6. **Controles históricos sobre el árbol 4.14.** Los resultados esperados no están documentados dentro del paquete (ver 1.4 y 1.5.1).
7. **Espacio en disco.** No se documenta cuánto disco hace falta:
   - la verificación completa deja unos 1,7 GB en `pruebas/_v64/`;
   - el control `4_8_1_comparar_baterias` usa unos 2 GB en `/tmp`;
   - con unos 4,5 GB libres al empezar, la serie de controles se quedó sin espacio.

   I11 menciona unos 4 GB solo como contexto.
8. **«Apta por entradas» en la V6.3.** La guía §8.2 y CONTINUIDAD §11.9 dicen que la ficha y el informe muestran «apta por entradas: no». En la V6.3 (motor A), `ficha.py` solo escribe `aptitud_de_uso` en la vía V6.4. En este expediente, con el registro no apto, la ficha y el informe finales no lo dicen. *Interpretación:* es una laguna entre la documentación y el código, que no corrige esta sesión.
9. **Documentos de cierre desfasados.** La matriz del alcance y HITO_2 no reflejan el estado final de la 4.14 (ver 1.5.2).
10. **Redacciones menores.** «12» frente a «diez» baterías obligatorias, y la cronología y el mapa sin la 4.14 (ver 1.5.3 y 1.5.4).

**Archivos creados por esta sesión:**
- `_logs/*` (verificación, controles y limpiezas);
- `relevo/*`;
- la copia `…_4_14/elis_motor_A_relevo_traspaso/`, con su `auditoria.md` y las salidas del pipeline;
- este informe.

No se tocaron originales, adjuntos ni expedientes finales.
