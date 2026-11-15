# Registro de la entrega 4.8 · mantenimiento financiero (P-M1) y coherencia de estados (X-a, X-c)

Redactado por Claude (Opus, esfuerzo alto) el 10-nov-2026. El encargo vigente es «MUNGER V2 — ENTREGA 4.8: MANTENIMIENTO FINANCIERO Y COHERENCIA DE ESTADOS». La revisión posterior corresponde a ChatGPT.

**Convenciones de procedencia:**
- **[Claude]**: ejecutado o declarado por Claude;
- **[Fable]**: crítica independiente con Fable;
- **[auditor]**: auditoría interna de Claude con contexto separado;
- **[pendiente]**: sin hacer o sin comprobar.

Nada de esta entrega está comprobado externamente.

## 1. Partida

**Paquete:** `munger_v2_r1_entrega4.7.1_w1_y_n3.zip`. Comprobaciones [Claude]:
- el ZIP subido y la concatenación de sus seis partes dan el SHA-256 `8c3053ea…42d989`;
- cada parte coincide con `PARTES.txt`;
- se descomprimió en carpetas limpias y separadas de los adjuntos;
- `VERSION` dice entrega 4.7.1;
- manifiesto: 1.454 archivos, sin cambios, ausencias ni archivos de más;
- P1 conserva `b4e47afc…c445a4`.

**Verificación completa de partida** [Claude], sobre una descompresión limpia:
- `bash verificar_paquete.sh completa`: código 0, «RESULTADO GLOBAL: PASA», en 9 min 8 s;
- manifiesto, entorno y piloto (35) pasan;
- 114/114, 30/30 y nombres de la línea de base;
- resumen 45/45 y cierre 55/55.

**Baterías históricas** después, sobre la misma descompresión [Claude]: salida idéntica a la de referencia en todas.

| Batería | Resultado |
|---|---|
| 4.2 | 45 |
| 4.3 | 217/217 |
| 4.3.1 | 43/43 |
| 4.4 | 72/72 |
| 4.5 | 60/60 |
| 4.6 | 24/24 |
| 4.6.1 | 23/23 |
| 4.7 | 46/49, lo esperado sobre el árbol 4.7.1 |
| 4.7.1 | 44/44 |

**Discrepancias de partida** (declaradas, no corregidas en los documentos históricos):
- `CONTINUIDAD.md` §2 estima la verificación completa en 15–20 min; tardó 9 min.
- La cabecera de `comprobar_entrega_4_7_1.py` dice 4 min y tarda 1,2 (X-f).
- El recuento 40/41 de 44 que declaró la 4.7.1 (X-f) consta en su registro histórico. El control real es 44/44.

## 2. Trabajo hecho

| Parte | Qué | Dónde |
|---|---|---|
| X-a / X-c | Reproducción antes y después, corrección acotada en `pipeline.py` y `ficha.py`, batería nueva de 28 pruebas obligatoria en el verificador, mutaciones, Anexo D | `CIERRE_TECNICO_4_8.md`, `reproduccion/`, `personaje_v2/pruebas/test_estados_v2.py` |
| P-M1, fuentes | 94 datos reextraídos de los textos y del PDF español conservados; 11 documentos oficiales de la CNMV y 3 secundarios, con URL, fecha, huella y página | `financiero/pm1_evidencia.json`, `fuentes/fuentes_externas_pm1.json` |
| P-M1, conciliación | Por año 2016–2025 y por segmento 2018–2025 | `financiero/pm1_conciliacion_anual.csv`, `pm1_segmentos.csv` |
| P-M1, alternativas | Réplica de la 4.7.1 ejecutada sin cambios, con salidas idénticas byte a byte; 16 alternativas y una medida auxiliar, con su clase y fundamento; año a año; terminal; necesidades de caja | `scripts/analisis_pm1.py`, `financiero/pm1_*` |
| Decisiones y preguntas | D-N3b replanteada; D-N3c y D-N3d nuevas; Q-T1–Q-T3; Q-E1–Q-E7 (no enviadas); campos humanos vacíos | `financiero/decisiones_y_preguntas_4_8.json` |
| Informe | P-M1 completo | `INFORME_PM1.md` |
| Control | `comprobar_entrega_4_8.py` | `scripts/`, `resultados/` |

## 3. Fuentes externas y su acceso

- El entorno de Claude no puede descargar de la CNMV: el proxy devuelve 403 y `WebFetch` falla con esos PDF.
- Los documentos se leyeron con el **navegador integrado del equipo de la persona responsable**:
  - se calculó en la página la huella SHA-256 de los bytes servidos;
  - se extrajo el texto con pdf.js (cdnjs);
  - solo se trasladaron al contenedor las citas breves.
- **Los PDF no se conservan en el paquete.** Si la persona responsable quiere conservarlos, puede adjuntarlos: sus huellas están en `fuentes_externas_pm1.json`.
- `vidrala.com` no respondió.
- No se envió ningún mensaje ni se contactó con nadie.

## 4. Uso de Fable (autorizado de forma selectiva)

**Motivo.** P-M1 es la hipótesis de mayor efecto potencial del ensayo (hasta −20 puntos en la 4.7.1), y el encargo señala la crítica independiente de las hipótesis de mantenimiento y terminal como aplicación pertinente. Se usó una sola vez, con un agente de contexto separado, de solo lectura y con cálculos propios en un temporal. No se ejecutó con Fable ninguna otra parte del procedimiento.

**Resultado** [Fable], resumido. El informe está transcrito en `CRITICA_FABLE_PM1.md`; aquí, sus hallazgos con su gravedad:
- **B1 (bloqueante).** El abanico estaba truncado: con λ = 1,10 y sin alternativas de nivel estructural, la conclusión «la reposición apenas mueve el valor» no se sostiene; la envolvente coherente va de −5 a −13 puntos. «Descartada» es excesivo para X41: parte de su efecto no es doble cómputo.
- **I1.** La regla del hueco es correcta, pero su suficiencia descansa en que el S2C sea causal. En la práctica, P-M1 se traslada al S2C y al ROIC_lp. La referencia ya invierte 1,21 × D&A el año 1 en el NORMAL.
- **I2.** El MALO mezcla dos lecturas reales (erosión de precio o caída de volumen). El terminal del MALO es frágil (holgura de 3,5 M€).
- **I3.** λ = 1,10 es el borde bajo; el indicio del Reino Unido es débil (The Park, reestructuración, ocho años). Propone central 1,15 y rango 1,10–1,25, con el contraste de balance 1 + π × valor neto ÷ dotación.
- **I4.** Falta la intensidad de inversión real (electrificación): propone un suelo de inversión en % de las ventas.
- **M1–M5.** Margen y D&A futura; escudo del MALO; límites de P0; convención de D&A; P3 irrelevante y P4 mal nombrada.

**Respuesta de Claude** [Claude]:
- se aceptan B1, I1–I4 y M1–M5;
- λ central pasa a 1,15, con rango 1,10–1,25;
- se añaden el indicio de balance y las alternativas P5, P5x, P6m, P6i y P6x;
- X41 pasa a «cerca de la mitad es doble cómputo»;
- P4 cambia de nombre;
- la conclusión se expresa como rango (`INFORME_PM1.md` §1, §6–§8).

**Discrepancia que queda.** La crítica estima en un 63 % el doble cómputo de X41, con un terminal plano. El guion da el 51 % con un adicional proporcional a las ventas en el terminal. Las dos cifras se presentan como dependientes de la convención.

## 5. Auditoría interna y control de vigencia

**Auditoría interna** [auditor]. Un agente de Claude con contexto separado revisó el material fijado por huellas (`MATERIAL_AUDITORIA_4_8.txt`, 32 archivos), con pruebas propias en copias. El informe completo está en `AUDITORIA_INTERNA_4_8.md`.

- **Material.** Al inicio, todo OK. Al final, 31 de 32 OK: `verificar_paquete.sh` cambió durante la auditoría. El cambio lo hizo el autor, lo declaró y el auditor lo revisó (Z-e).
- **Veredicto: sin bloqueantes.** Cinco hallazgos importantes (Z-a a Z-e) y ocho menores (Z-f a Z-m). X-a y X-c quedan reparados en las vías del encargo, sin aprobaciones indebidas. La regla H2 no cambia. La aritmética de P-M1 se reproduce de forma independiente.

**Respuesta a cada hallazgo** [Claude]. Todos se corrigen o se declaran después de la auditoría; los cambios los revisa el control de vigencia (§5b).

| Hallazgo | Gravedad | Respuesta |
|---|---|---|
| Z-a · tras una retirada pendiente (código 5), el resumen no volvía a publicar el estado final | importante | **Corregido.** `salidas_finales` anota `resumen_pendiente` y la ejecución siguiente vuelve a publicar la fila una vez completadas las retiradas. Prueba nueva en la batería. Mutación M6 detectada |
| Z-b · λ presentado como «mínimo respaldado»; cota implícita entre P1 y P5 | importante | **Corregido** en el informe, en D-N3b, en `DECISIONES.md` y en la tabla de mejora: P1 es la hipótesis central; los indicios van de 1,05 a 1,29; ningún rango es una cota |
| Z-c · P3 = P1 por la regla del hueco | importante | **Corregido.** El hueco solo descuenta la inversión fija de R1. P3: 68,85 / 62,87 (V MALO −0,32); P4: 67,15 / 60,19. Explicación y dominio de la regla corregidos (§5.2 y §5.4) |
| Z-d · P5 y P5x medidos frente a la amortización total con P0 aplicado | importante | **Corregido.** El exceso se mide frente a la amortización que se repone: P5 62,71 / 55,83; P5x 57,68 / 51,05. El doble cómputo de X41 se mide con P5x0 |
| Z-e · el verificador fijado rompía el control de integración de la 4.6.1; faltaba registrarlo | importante | **Corregido y registrado** (§7). El bloque de estados va antes del del resumen; `comprobar_integracion_verificador_48.py` es nuevo; las baterías históricas sobre el árbol final constan en `resultados/LEEME_BATERIAS_HISTORICAS.md`; el control de la 4.8 ejecuta los controles de integración |
| Z-f · `cierre` en estados que la auditoría no aprobó; estado final sin ficha | menor | **Corregido.** `ficha.py` solo escribe `cierre` si el estado es el que propuso el material auditado, y rechaza `concluido` (código 3) si se propuso otro. `salidas_finales` no conserva un estado final sin ficha oficial |
| Z-g · FIN con tipos mezclados; fallo de esquema en `no_entregable` no declarado | menor | **Corregido.** FIN con la causa del diagnóstico y aviso en el historial |
| Z-h · diagnóstico obsoleto tras abandonar un estado final | menor | **Corregido.** Con `--desde`, el diagnóstico de un estado final pasa a `.anterior` |
| Z-i · lógica del control | menor | **Corregido.** P-M1 se ejecuta en un temporal (`--salida`); se detectan archivos añadidos en las zonas protegidas; la tolerancia de X41 es exacta; se ejecutan los controles de integración |
| Z-j · mutantes equivalentes | menor | **Declarado** en `CIERRE_TECNICO_4_8.md` §3. Con la defensa de Z-f, M2 también es equivalente; M2b (las dos defensas retiradas) da 22/28 en la batería final |
| Z-k · fuentes externas y crítica no comprobables | menor | **Corregido en parte.** Las citas O\* y S\* se marcan como declaradas y la O1 como posterior; la crítica está transcrita (`CRITICA_FABLE_PM1.md`). Los PDF de la CNMV siguen sin conservarse (§3) |
| Z-l · alternativas fijadas tras ver valores; P6i sin fundamento | menor | **Declarado y corregido.** El orden consta en §4 y en el informe §8. P6i pasa al 12 %, la previsión oficial de 2025 (O6) |
| Z-m · tabla por escenario | menor | **Corregido.** Columna de la cartera, circulante del año 11 y año 5 de P0 |

**§5b · Control de vigencia** [auditor, segunda revisión, contexto separado] (`AUDITORIA_INTERNA_4_8_vigencia.md`, material `MATERIAL_VIGENCIA_4_8.txt`, 39 archivos, OK al principio y al final).

**Veredicto: un bloqueante (V-a), dos importantes (V-b, V-c) y dos menores (V-d, V-e).** Comprobó que Z-a, Z-b, Z-c, Z-d, Z-e, Z-h, Z-j, Z-k, Z-l y Z-m están resueltos, Z-f y Z-g lo están en lo pedido, y Z-i en parte. Las cifras son coherentes entre todos los documentos.

| Hallazgo | Gravedad | Respuesta [Claude] |
|---|---|---|
| V-a · `pipeline.py` terminaba con `IndexError` (código 1) siempre que acababa sin estado final (p. ej. `--hasta`); `test_comprobadores.py` lo registraba sin fallar | **bloqueante** | **Corregido.** Ya estaba en el código de la primera auditoría y no se detectó entonces. Prueba nueva (parada con `--hasta`). Mutación M7 detectada. `test_comprobadores.py` vuelve a «código 0» |
| V-b · la defensa de Z-f dejaba sin estado un `no_entregable` legítimo cuando `ficha.py` no podía escribir la ficha (alcance ilegible) | importante | **Corregido.** La defensa solo actúa si en esa llamada se archivó una ficha. Prueba nueva. Mutación M8 detectada |
| V-c · el control exigía 8 salidas de P-M1 y el guion escribe 7 | importante | **Corregido** (7, los `pm1_*`) |
| V-d · faltaban pruebas de Z-f, Z-g, Z-h y `--hasta` | menor | **Corregido en parte.** Pruebas de `--hasta` (V-a), de la ficha que no se escribe (V-b) y de Z-h (subsanación). Z-g queda cubierto solo por las mutaciones de la causa en la última línea y del diagnóstico. Batería: 28 |
| V-e · restos documentales | menor | **Corregido.** «10 pruebas»; «16 alternativas y una medida auxiliar»; la clase de X41 remite a P5x0. P5x se describe como el nivel de 2025 en el año 1: después crece con la regla del hueco y la cartera; no afecta al valor |

Estos cambios posteriores al control de vigencia los cubren la batería, las mutaciones y la verificación final sobre una descompresión limpia (§10). **No hay una tercera revisión independiente.** Se declara así para no presentar como auditado lo que no lo está.

## 6. Correcciones de documentos históricos (sin modificarlos)

- **X-e.** La depreciación de derechos de uso de 2025 es 6,760 y la de 2024 es 4,768. Está comprobado en el PDF español (p. 58) y en la versión inglesa [Claude]. El informe del N3 de la 4.7.1 citaba la de 2024 en «Límites en el otro sentido»; se corrige en `INFORME_PM1.md` §2–§3. La frase repetida del §6 de ese informe se señala aquí y no se toca.
- **X-f.** El control de la 4.7.1 tiene 44 comprobaciones y tarda en torno a 1,2 min, no 4.
- **Y-1 (nuevo).** La amortización de 2019 de la Historia (97,091) incluye el deterioro de 6,003; el resto de años no. Afecta a la ratio de 2019. No cambia ningún valor. El expediente vigente no se modifica.
- **Discrepancia documental en el PDF inglés de 2025:** la p. 69 rotula «as of 31 December 2024» importes de 2025.

## 7. Incidencias

- En pruebas locales se generaron cachés `__pycache__` en dos árboles de trabajo:
  - el de esta entrega, por una importación en proceso antes de fijar `PYTHONDONTWRITEBYTECODE` en la batería;
  - la copia de partida, por una importación sin `-B` para calcular la huella de la regla H2.

  Se borraron. Después, la copia de partida volvió a cumplir su manifiesto: 1.454 archivos más el propio manifiesto, sin cambios. La batería nueva fija la variable desde entonces.
- El primer guion de P-M1 terminaba sin salida porque el modelo de la 4.7.1 acaba con `sys.exit`. Se captura y se exige su código 0.
- **Verificador (Z-e).** El bloque de la batería de estados se escribió al final de `verificar_paquete.sh` (huella fijada `f2c14257…`). Así rompía la extracción por posición del control de integración de la 4.6.1: 7/13, y 22/23 en su control de vigencia.
  - Se movió, sin cambiar sus líneas, delante del bloque del resumen.
  - Después se subió su mínimo a 26, al añadir la prueba de Z-a.
  - Con el verificador final, los controles de integración de la 4.6.1, la 4.7.1 y la 4.8 dan 13/13, y las baterías históricas, su resultado esperado (`resultados/LEEME_BATERIAS_HISTORICAS.md`).

## 8. Tabla de mejora demostrada

| Ámbito | Qué error se corrige | Qué supuesto queda respaldado | Qué incertidumbre se reduce | Qué decisión sigue bloqueada |
|---|---|---|---|---|
| X-a | El estado del pipeline quedaba en `None` en la primera ejecución tras un cierre previo | Estado, ficha, informe, diagnóstico y resumen coherentes en la primera ejecución, también tras una retirada pendiente (10 pruebas) | Ya no hace falta relanzar para tener un estado coherente | — |
| X-c | Ficha `no_entregable` con `cierre`; rechazo atribuido a otra causa; paso 13 con estado final | Ninguna ficha `no_entregable` lleva `cierre`; diagnóstico y última línea con la causa y la vía (8 pruebas) | Subsanación clara: auditoría nueva desde el paso 13 | Q-T1 (código de salida), Q-T2 (X-b), Q-T3 (W-d) |
| X-e | Cifra de derechos de uso presentada en otro período | 6,760 (2025), comprobada en el PDF | — | — |
| P-M1 | La sensibilidad de −20,6 puntos contenía doble cómputo con el S2C (alrededor del 51 % de su efecto) | La amortización de la cartera no se repone (P0, respaldado). El desfase de inflación queda como hipótesis condicionada, con indicios de 1,05 a 1,29 y P1 = 1,15 como central | En lugar de una sensibilidad única de −20,6 con doble cómputo, alternativas fundamentadas de 69,7 a 62,7, con extremos explorados en 61,3 y 55,7; ninguna es una cota | D-N3b (y D-N3c, D-N3d): falta el desglose de la inversión y el calendario de hornos (Q-E1, Q-E2); valoración validada bloqueada |
| Y-1 | Definición distinta de la amortización de 2019, detectada y declarada | — | — | Corrección en un expediente futuro |

## 9. Pendientes que no cambian

- N4: 38 ceros, que la IA no confirma.
- N9: ruta B, E1–E7.
- N10: probabilidades.
- P-N1 y P-N2.
- N5–N8, N11 y N12.
- Los datos que faltan para N1–N2.
- H1–H3 siguen cerrados.
- La ruta desde cero y el inventario de las más de 100 empresas quedan fuera del alcance.

## 10. Verificación final del paquete 4.8

**Cómo se hizo.** Se verificó sobre una descompresión limpia del ZIP candidato. Su contenido es el mismo que el del final, salvo:
- este apartado;
- los archivos que dependen de él (`CAMBIOS_ARCHIVOS.txt` y el manifiesto).

El ZIP final se volvió a verificar del mismo modo. Sus huellas están en el `.sha256` y en `PARTES.txt` de la entrega, no aquí, porque escribirlas cambiaría el propio paquete.

**`bash verificar_paquete.sh completa`:** código 0 y «RESULTADO GLOBAL: PASA», en unos 9 minutos.
- manifiesto: 1.494 archivos, 0 modificados, 0 ausentes y 0 de más;
- entorno: pasa;
- piloto: 35 comprobaciones, salida idéntica;
- 114/114 y 30/30;
- batería de coherencia de estados: **28/28**, «RESULTADO estados: PASA»;
- batería del resumen: **45/45**, «RESULTADO resumen: PASA»;
- batería de cierre: **55/55**, «RESULTADO cierre: PASA».

**Aparte,** sobre la misma descompresión, después de la verificación completa y uno detrás de otro. Todos dieron una salida idéntica a la de referencia que fija `resultados/LEEME_BATERIAS_HISTORICAS.md`:
- con código 0: 45 de la 4.2, 217 de la 4.3, 43 de la 4.3.1, 72 de la 4.4, 60 de la 4.5, 24 de la 4.6 y 23 de la 4.6.1;
- 4.7: **46 de 49**, por diseño. Son los mismos tres controles que ya no cumplían sobre el árbol 4.7.1, con una salida idéntica byte a byte;
- 4.7.1: **40 de 44**, por diseño. Los cuatro que no cumplen miran las huellas de archivos que la 4.8 declara cambiados (LEEME §2);
- `comparar_baterias_4_7_1.py`: código 0. Las tres baterías del resumen de la 4.7.1 coinciden con lo conservado en el estado de cada prueba, el principio de las que fallan y la línea final (45/45, 35/45 y 36/45). Solo cambian las huellas de `ficha.py`, `pipeline.py` y `verificar_paquete.sh`;
- **4.8: 36 de 36**, código 0.

**Comprobaciones posteriores a las pruebas:**
- los 1.494 archivos del manifiesto siguen intactos;
- P1 conserva `b4e47afc…c445a4`.

**Respecto a la 4.7.1:**
- cambian 9 archivos: `pipeline.py`, `ficha.py`, `verificar_paquete.sh`, el Anexo D, `DECISIONES.md`, `VERSION`, `CONTINUIDAD.md`, `PROMPT_NUEVA_VENTANA.md` y `CAMBIOS_ARCHIVOS.txt`;
- se regenera el manifiesto;
- no desaparece ninguno;
- hay 40 nuevos: `personaje_v2/pruebas/test_estados_v2.py` y 39 en `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_8/`;
- son idénticos `cierre_v2.py`, `resumen.py`, `informe.py`, `test_resumen_v2.py`, `test_cierre_v2.py`, la regla H2, los 489 originales y los expedientes de la 4.4 a la 4.7.1.

**Cosa heredada.** `personaje_v2/pruebas/sintetico/EmpresaX_cero_pendiente/.lo_perfil/` venía ya en el ZIP de la 4.7.1. Son solo carpetas vacías, sin ningún archivo, y por eso no figuran en el manifiesto ni cuentan como «de más». Se conserva tal cual, para no alterar el material de partida.
