# Informe de reparación · vigencia de las salidas oficiales (entrega 4.6.1, 9-nov-2026)

**Categorías:**
- **[Hecho]**: comprobado directamente por Claude o por un script del paquete.
- **[Antecedente externo]**: comprobado por otra parte.
- **[Pendiente]**: queda abierto.

**Criterio de cierre del encargo:** un contenido modificado después de la auditoría no puede publicarse ni seguir presentándose como aprobado por esa auditoría anterior, por ninguna de las rutas reparadas. **[Hecho] Se cumple en las tres rutas del caso reproducido y en los siete casos negativos de las pruebas.**

**Ningún número ha cambiado** (`resultados/comparacion_con_4_6.md`, 32 de 32).

## 1. Caso reproducido con el código 4.6 (`reproduccion/reproduccion_codigo_4_6.txt`)

[Hecho] Sobre una copia temporal del expediente aprobado de la 4.6, con su resumen, se hizo esta secuencia:

| Paso | Qué se hizo o se observó |
|---|---|
| 1 · Estado inicial | Paso 14, `concluido`, auditoría APROBADO. Ficha con cierre del material `74b94f8072dd58c1`. Fila del resumen `concluido / APROBADO` |
| 2 · Modificación | Se añadió una tesis de prueba a `fase_c.json → celdas.B101` (SHA-256 `4874c9b8…` → `9c36c656…`) |
| 3 · `pipeline.py --desde 14` | Código 4, «CIERRE RECHAZADO: el material cambió…» |
| 4 · Estado tras el rechazo | `ficha.json` seguía siendo oficial con `concluido`, `informe.md` seguía presente y la fila seguía en `concluido / APROBADO` |
| 5 · `informe.py` directo | Código 0. Publicó la tesis modificada en un informe con «Estado `concluido`» |
| 6 · `ficha.py --estado concluido` directo | Código 3, pero la ficha oficial anterior seguía presentando `concluido` |

**Las tres rutas reproducen el fallo.**

## 2. Qué cambia

**[Hecho] Regla nueva** (`scripts/cierre_v2.py`, sección 5; Anexo D, «Vigencia de las salidas oficiales»):
- **Registro del cierre:** al cerrar, `ficha.py` escribe `cierre_vigente.json` con el material aprobado y las huellas de la ficha y de la auditoría; `informe.py` añade la del informe.
- **Cuándo es vigente:** una salida oficial cerrada (ficha con `cierre`, o `concluido`) lo es solo si hay una aprobación válida del material actual y la ficha y el informe son los registrados.
- **Si no es vigente, se archiva** (`archivar_salidas`):
  - `ficha.json`, `informe.md` y `cierre_vigente.json` pasan a `historial_cierres/<n>_<material>/`;
  - se guarda también una copia de la auditoría de ese momento, si la había, y un `RETIRADA.json` con el material que aprobó, el actual, el motivo y una nota que distingue «aprobación histórica de otro material» de «ya no respaldada por una aprobación válida»;
  - la fila activa del resumen pasa a «SIN APROBACIÓN VIGENTE», y la anterior se conserva en `resumen_v2_historial.csv`. Las filas ajenas no se tocan;
  - el estado del pipeline deja de decir `concluido` y anota la retirada en `cierres_archivados`.
- **Lo que no cambia:** la auditoría que aprobó no se borra ni se modifica, y no se usa ningún estado financiero para representar la espera.

**Dónde se aplica:**
- `pipeline.py`: al empezar cada ejecución, antes de `--desde`; en el paso 11, que sustituye al antiguo renombrado a `.anterior`; y en el rechazo del paso 14.
- `ficha.py`: con un rechazo, archiva y termina con código 3. Una ficha oficial cerrada no se sobrescribe en silencio.
- `informe.py`: exige `ficha.json`. Con una ficha cerrada, exige además la vigencia; si falla, archiva y termina con código 3.
- `resumen.py`: con una ficha cerrada no vigente, archiva y termina con código 3.

**Rutas legítimas sin auditoría:** los estados tempranos se publican como antes, y el material provisional sigue identificado como provisional.

**[Hecho] La misma reproducción con el código 4.6.1** (`reproduccion/reproduccion_codigo_4_6_1.txt`):
- `--desde 14`: código 4. Ficha e informe archivados y fila «SIN APROBACIÓN VIGENTE».
- `informe.py`: código 3, sin publicar nada.
- `ficha.py`: código 3, sin ficha oficial.

**Ninguna de las tres rutas se reproduce.**

## 3. Pruebas (`pruebas/test_cierre_v2.py`: 55 de 55)

**[Hecho] Pruebas nuevas.** Se añaden 15 a las 40 anteriores, que se conservan.

**Ampliada:** la prueba que solo comprobaba el código 4 tras cambiar el material ahora comprueba además las salidas, el archivo y el resumen.

**Siete casos negativos**, comprobando los archivos, el historial y el resumen después del rechazo:
1. `fase_c.json` modificado y `--desde 14`, con una fila ajena intacta.
2. `informe.py` directo tras modificar el material, sin pasar por el pipeline.
3. `ficha.py` directo.
4. Rechazo del pipeline seguido de `informe.py`.
5. Auditoría eliminada tras el cierre, con `informe.py` y con `--desde 14`.
6. Auditoría REPETIR y auditoría mal formada con salidas oficiales presentes.
7. Aprobación de otro material con una fila previa `concluido / APROBADO`.

Una prueba más verifica la conservación: la auditoría aprobatoria queda intacta y copiada, y la retirada dice de qué material era.

**Cinco casos positivos:**
1. **Sin cambios:** con aprobación vigente, `informe.py`, `ficha.py`, `resumen.py` y el pipeline regeneran sin archivar nada.
2. **Regeneración repetida:** da las mismas huellas, sin duplicados.
3. **Material modificado:** queda provisional y auditable.
4. **Auditoría nueva del material modificado:** el cierre es coherente y el anterior queda en el historial.
5. **Estado temprano sin auditoría (`pendiente_de_datos`):** no se bloquea.

**[Hecho] Con el código 4.6 la batería da 43 de 55** (`reproduccion/pruebas_aceptacion_con_codigo_4_6.txt`): las 12 pruebas negativas y de conservación nuevas fallan. Los cinco positivos pasan también con el código anterior, como corresponde a un comportamiento que ya existía y que la reparación conserva.

## 4. Integración en la verificación completa

**[Hecho] `verificar_paquete.sh completa`** ejecuta ahora la batería de cierre como bloque obligatorio. El resultado global es FALLA si:
- la batería falla;
- falta;
- se interrumpe sin su línea final;
- tiene menos de 55 pruebas;
- alguna prueba no pasa.

**El modo rápido** no la ejecuta y lo dice expresamente. La cabecera del verificador explica qué cubre cada modo y que ninguno sustituye a los controles de los expedientes reales ni a sus auditorías.

**[Hecho] `scripts/comprobar_integracion_verificador.py`** extrae el bloque real del verificador y lo ejecuta en los dos modos contra sustitutos de la batería: ausente, con fallo, interrumpida, con menos de 55, con una prueba en FALLA y correcta. Resultado: 13 de 13.

## 5. Expediente regenerado y auditoría nueva (`Vidrala/`)

[Hecho] Se copió el expediente aprobado de la 4.6 con su resumen; la 4.6 se conserva intacta. La auditoría 4.6 se renombró, sin cambios, a `auditoria_4_6_antecedente.md`.

**Al lanzar el pipeline con el código 4.6.1:**
- archivó las salidas oficiales de la 4.6 en `historial_cierres/01_74b94f8072dd58c1/` («no hay auditoria.md»), puso la fila del resumen en «SIN APROBACIÓN VIGENTE» y conservó la anterior en `resumen_v2_historial.csv`;
- regeneró el material provisional, que salió idéntico byte a byte al de la 4.6;
- se detuvo para pedir una auditoría nueva.

**Auditoría nueva:**
- La hizo un agente con contexto independiente, sin participación en la reparación ni en el análisis y sin leer las auditorías anteriores.
- Resultado: **16 de 16 en PASA, `Material auditado: 74b94f8072dd58c1`, APROBADO.** El identificador coincide con el de la 4.6 porque el material es idéntico, no porque se reutilice la auditoría anterior.
- Verificó expresamente:
  - el archivo y su `RETIRADA.json`;
  - la fila activa y el historial;
  - la ausencia de salidas oficiales antes de su auditoría;
  - el estado del pipeline;
  - las 18 huellas del material;
  - la marca, la etiqueta de C104 y los avisos de alcance de la 4.6.

**Tras la aprobación,** el paso 14 escribió la ficha y el informe oficiales, idénticos byte a byte a los de la 4.6, y `cierre_vigente.json`. La fila volvió a `concluido / APROBADO`.

**Avisos del auditor, ninguno bloqueante:**
- **La nota de `RETIRADA.json` decía «otro material» y no había copia de la auditoría.** El material era el mismo y faltaba la auditoría. El Anexo D y el código se corrigieron después de la auditoría: la nota distingue ahora los dos casos y la copia se hace solo si hay auditoría. Ni el código ni el Anexo forman parte del material auditado.
- **Textos de la ejecución anterior en el expediente** (LÉEME y campos `fin` y `ficha_valida` de `estado_pipeline.json`): el LÉEME ya está actualizado y el cierre reescribió `fin`.
- **Avisos anteriores** sobre la etiqueta «2 pendientes» del libro y la sección 7.

**Contradicción normativa declarada:** el texto anterior del Anexo D sobre `RETIRADA.json`. Queda resuelta con la corrección descrita en el primer aviso.

**La aprobación del ensayo no es una validación financiera para invertir.**

## 6. Comparación numérica y regresión

**[Hecho] `scripts/comparar_con_4_6.py`: 32 de 32.** Son idénticos byte a byte frente a la 4.6:
- P1, fuentes y datos;
- las fases A, B y C;
- los libros de datos, evaluado y recalculado;
- `resultados.json`, `precio.json` y la escalera;
- el material provisional, la ficha y el informe oficiales.

El contraste entre motores, repetido sobre el libro 4.6.1, y su descomposición también son idénticos. Las únicas diferencias están en el estado del pipeline, el LÉEME, el prompt de la auditoría, la auditoría nueva y los registros de vigencia.

**[Hecho] Regresión:**
- `test_comprobadores.py` 114/114 y `test_pipeline_sintetico.py` 30/30, con los mismos nombres, dentro de `verificar_paquete.sh completa`;
- baterías de 45, 217, 43, 72, 60 y 24 sobre sus referencias intactas;
- `scripts/comprobar_vigencia_ensayo.py`: 23 de 23.

## 7. Archivos modificados y nuevos

**Modificados respecto a la 4.6:**
- `personaje_v2/scripts/cierre_v2.py`, `pipeline.py`, `ficha.py`, `informe.py` y `resumen.py`;
- `personaje_v2/pruebas/test_cierre_v2.py`;
- `personaje_v2/prompts/verificacion.md` (punto 1);
- `personaje_v2/ANEXO_D_salidas_y_formatos.md` y `personaje_v2/DECISIONES.md`;
- `verificar_paquete.sh`;
- `VERSION`, `CONTINUIDAD.md`, `PROMPT_NUEVA_VENTANA.md`, `CAMBIOS_ARCHIVOS.txt` y el manifiesto.

**Nuevo:** `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_6_1/`. La relación con huellas está en `CAMBIOS_ARCHIVOS.txt`.

**Sin cambios:** H1–H3, la regla estricta de H2 (`veredicto_auditoria`) y los expedientes anteriores.

## 8. Pendientes

- **[Pendiente] Financieros:** N1–N12 de la 4.5, sin cambios.
- **[Pendiente] Normativos:** P-N1 (los dos sentidos de «conclusión favorable») y P-N2 (la huella del libro en `verificacion_integridad.txt`), de la 4.6.
- **P-N3 queda resuelto:** la batería de cierre está en `verificar_paquete.sh completa`.
- **[Pendiente] Expedientes cerrados antes de la 4.6.1:** no tienen `cierre_vigente.json`. Si se vuelve a ejecutar sobre ellos el pipeline, `informe.py` o `resumen.py`, sus salidas se archivan hasta una auditoría nueva. Es la consecuencia buscada; no se ha ejecutado sobre ninguno.

**[Antecedente externo]** Según la persona responsable, la revisión independiente de la 4.6 comprobó la integridad, las 40 pruebas, las marcas y advertencias, la conservación financiera y el rechazo de una auditoría de material anterior.

**Modelos.** Opus en todo, con un agente de auditoría de contexto separado, también Opus. Fable no se usó.
