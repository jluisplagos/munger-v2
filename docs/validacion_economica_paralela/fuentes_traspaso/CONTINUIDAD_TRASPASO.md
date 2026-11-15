# CONTINUIDAD DEL TRASPASO · Munger v2 · después de la entrega 4.14

Fecha: 15-nov-2026, 11:00 (Europa/Ámsterdam). Lo escribe la orquestación (Claude, Opus) para continuar en una ventana nueva.

**Separación.** Los **hechos** se dan con su evidencia. Las *interpretaciones* y las *propuestas* van marcadas como tales.

**Estado del traspaso: preparado, NO completado.** Solo se dará por completado cuando el agente receptor confirme, en la ventana nueva, los cinco puntos del §11.

**Congelación.** El 15-nov a las 11:00 no había ninguna prueba ni ningún pipeline en ejecución (`pgrep`: ningún pipeline, LibreOffice, batería ni control). La última ejecución terminó el 14-nov a las 22:47 (controles históricos sobre la final). Este documento no modifica el paquete ni ningún expediente.

## 1. Base para continuar

| Dato | Valor |
|---|---|
| Versión | `munger_v2 · r1 · entrega 4.14 (cierre con verificación completa de las entradas financieras …) · 2026-11-14 · base SHA-256 61c70800d0faa7c4a98888b7413820ec8041153e53484c32b0c549b26b6af87d` (archivo `VERSION`) |
| ZIP | `munger_v2_r1_entrega4.14_cierre_verificacion_entradas.zip` |
| **SHA-256 del ZIP 4.14** | **`bb51942cefb848e409a4828e3faeb70f94aa4d29af39cda6d90cd0a97cb7b93e`** |
| Tamaño y contenido | 1.130.912.246 bytes; 6.799 entradas, de ellas 6.798 en `MANIFIESTO_SHA256.txt`, que se excluye a sí mismo |
| Partes | 54 de hasta 20 MiB (`.parte00` a `.parte53`); huellas y comandos de reconstrucción en `…zip.PARTES.txt` |
| Base anterior | entrega 4.13, ZIP SHA-256 `b1f747a18cd2123d71c0c1abdca0da049207b4c4eb215aa099f345aed4fbf22a` (incluida dentro de la 4.14) |
| Candidata (antecedente) | ZIP SHA-256 `f9f888e393bd90e699a031e66d9d553067d4f38c0e6414837fc1e0299b4f5a24`; no es la base |

**Ubicación.**
- **En los archivos de la persona responsable.** Las 54 partes, el `.PARTES.txt` y el `.sha256` se le enviaron en esta conversación el 14-nov (tandas 1–4; índice en `INDICE_ENTREGA_4_14.txt`).
- **El ZIP completo no se pudo enviar:** con 1078,5 MiB supera el límite de 500 MiB por archivo de la conversación. Se obtiene uniendo las partes.
- **En el contenedor de esta ventana**, que es efímero y no es accesible desde otra ventana: `/mnt/user-data/outputs/` (ZIP, partes y registros), `/home/claude/trabajo_4_14/candidata/munger_v2_r1` (el árbol empaquetado) y `/home/claude/trabajo_4_14/final_4_14/` (registros de la verificación final).

## 2. Cómo se accede a la base desde la ventana nueva

La ventana nueva no ve este contenedor. Hay dos vías.

**Vía A · Adjuntar archivos.** La persona responsable adjunta en la ventana nueva:
1. las 54 partes, `munger_v2_r1_entrega4.14_cierre_verificacion_entradas.zip.parte00` a `.parte53`;
2. `…zip.PARTES.txt` y `…zip.sha256`;
3. `PROMPT_NUEVA_VENTANA.md`, `ENCARGO_VIGENTE.md` y este `CONTINUIDAD_TRASPASO.md`;
4. si se quiere el registro de la verificación externa: `…VERIFICACION.txt`, `…INTEGRIDAD_Y_CREDENCIALES.txt` e `INDICE_ENTREGA_4_14.txt`.

Si la ventana nueva no admite tantos adjuntos de una vez, se envían en varios mensajes. No hace falta adjuntar el ZIP completo.

**Vía B · Ordenador vinculado.** Si la ventana nueva está vinculada al ordenador de la persona responsable (app de escritorio de Claude, «Link to this computer»), basta con que las partes estén en una carpeta conectada: el receptor las copia a su espacio de trabajo.

**Reconstrucción y comprobación** (en el espacio de trabajo del receptor, en una carpeta nueva y vacía):
```bash
cat munger_v2_r1_entrega4.14_cierre_verificacion_entradas.zip.parte{00..53} > munger_v2_r1_entrega4.14_cierre_verificacion_entradas.zip
sha256sum munger_v2_r1_entrega4.14_cierre_verificacion_entradas.zip   # debe dar bb51942c…7b93e
mkdir base_4_14 && cd base_4_14 && unzip -q ../munger_v2_r1_entrega4.14_cierre_verificacion_entradas.zip
cat munger_v2_r1/VERSION
```
En Windows (cmd) la unión es la línea `copy /b …` de `…zip.PARTES.txt`.

Después, el receptor sigue `PROMPT_NUEVA_VENTANA.md`: leer `CONTINUIDAD.md` entero y ejecutar `bash verificar_paquete.sh completa`. Necesita unos 7 GB libres después de descomprimir (CONTINUIDAD §2, punto 5).

## 3. Trabajo terminado (hechos, con evidencia dentro del ZIP)

| Parte | Resultado | Evidencia |
|---|---|---|
| Reparación 4.13.1 (H5: vigencia, retirada y recuperación) | corregida; batería H5 59/59 | `documentacion_cierre_4_14/hito1/REGISTRO_REPARACION_4_13_1.md` |
| Materialidad §5 (juicio sobre el objetivo; S3 y S11) | contrato implementado; 27/27 | `scripts/objetivo_v64.py`, `pruebas/test_juicio_objetivo_414.py` |
| S4 (§7) | corregido en sus tres vías generativas | `hito1/HITO_1.md` |
| Verificación completa de las entradas (requisito) | puerta del paso 12, invalidación, revisor distinto del extractor; 33/33; los registros de los tres expedientes finales son aptos | `scripts/verificacion_entradas.py`; `comprobar_entrega_4_14.py` |
| Cambio de base con guardián y correcciones de extracción | grupo D 9/9 | `scripts/cambiar_base.py` |
| Viscofan (D3 y E1) | concluido · Vigilar · esperar · objetivo condicionado 39,80 € frente a 54,70 € · APROBADO (2.º intento) | `…_4_14/viscofan_decisiones/Viscofan` |
| Vidrala (E1 y E2; E3 y E4 son supuestos) | concluido · Vigilar · esperar · 56,00 € frente a 90,10 € · APROBADO | `…_4_14/vidrala_decisiones/Vidrala` |
| Elis, tercera empresa (E6, base 31-dic-2025, motor A) | pendiente_de_datos · Vigilar · sin acción · APROBADO. El precio de Sí (7,30 €) **no es utilizable** (F1) | `…_4_14/elis_decisiones/Elis` |
| Efectos separados y réplica independiente | diferencia 0 en los tres; réplica: 185 + 89 PASA, ninguna FALLA (revisión interna) | `resultados/efecto_*`, `revisiones/INFORME_REPLICA_4_14.md` |
| Descomposición de Viscofan (+1,5386 / −0,6623 €) | hecha | `DESCOMPOSICION_VISCOFAN_4_14.md` |
| Matriz del alcance, dictamen A–E, incidencias I1–I21 | escritos; **alcance original no completado** | `documentacion_cierre_4_14/` |
| Prueba de traspaso con un agente receptor sin historial | arranque, verificación y relevo real resueltos; la auditoría del relevo **no** fue de contexto separado | `documentacion_cierre_4_14/traspaso/` |
| Candidata y final | verificadas (§5) | `REGISTRO_PRUEBAS_4_14.md`; `…VERIFICACION.txt` |

## 4. Trabajo iniciado y no terminado

- **S5 (§7 del encargo).** La vía generativa ya admite la cabecera F5 (`rellenar_fase1_v63.py`), pero **no se aplicó en Viscofan**, aunque `HITO_1.md` y `RAMAS_4_14.md` lo anunciaban. En `viscofan_decisiones/Viscofan/fase1_v63.json`, `control_maestro_textos` está vacío. Ver el hallazgo H-P1 del §7.
- **Relevos pendientes de expedientes sustituidos.** No hace falta resolverlos (CONTINUIDAD §2, punto 6):
  - `elis_motor_A` (paso 13, solicitud caducada);
  - las ramas `viscofan/` y `vidrala/` (paso 13, no se auditan);
  - `vidrala_decisiones_INVALIDO_perdio_analisis` (paso 6, inválido).
- **Ahold Delhaize (reserva de la tercera empresa).** El `.bat` está preparado, pero la persona responsable no lo ha ejecutado y no ha entregado el Excel de la etapa 1.
- **Fuentes oficiales materiales sin sus bytes** (doce documentos de `EVIDENCIA_ECONOMICA_4_14.md` §d). El 15-nov se consiguió la mayoría; falta la presentación «Beat'30», además de la transcripción de Vidrala y el PDF del informe de Viscofan de 2024; el estado y los enlaces están en el §6 (X5) y el §11. Ninguna se ha incorporado aún a un expediente.

## 5. Comandos y pruebas ejecutados sobre la final, con resultados (14-nov)

Sobre la descompresión con unzip del ZIP final, en secuencia:

| Comando | Resultado |
|---|---|
| `empaquetar_zip.py /home/claude/trabajo_4_14/candidata …zip --partes 20 --comprobar …` | CRC correcto; extracciones con Python y con unzip: 0 modificados, 0 ausentes, 0 adicionales; idénticas byte a byte; 54 partes. La concatenación da el mismo SHA-256 |
| `bash verificar_paquete.sh completa` (21:45–22:20) | **RESULTADO GLOBAL: PASA**, código 0 |
| `python3 -I -B …_4_14/scripts/comprobar_entrega_4_14.py` | **35/35**, código 0 |
| `python3 -I -B …_4_13/scripts/controles_historicos_4_13.py SALIDA` (22:20–22:47) | Los resultados que fija `resultados/LEEME_CONTROLES_HISTORICOS_4_14.md`; 18 de las 19 salidas son idénticas a las de la candidata, y la de la 4.9 cambia solo en la lista de archivos |
| Manifiesto después de las verificaciones | 6.798 archivos · 0 modificados · 0 ausentes (747 archivos de más escritos por las pruebas, como está documentado) |
| Escaneo de credenciales | 0 coincidencias del correo de la persona responsable y de los formatos de credenciales buscados |

**Detalle de la verificación completa:** comprobadores 114/114, sintética 30/30, H5 59/59, juicio sobre el objetivo 27/27, verificación de entradas 33/33, integración V6.4 198/198, trazabilidad 78/78, integridad 103/103, solicitudes 55/55, estados 28/28, resumen 45/45, cierre 55/55.

**Detalle de los controles históricos:** completos la 4.2, 4.3, 4.3.1, 4.4, 4.5 y 4.6.1. La 4.6 da 23/24. Las demás dan sus recuentos ligados a su versión: 4.7 45/49 … 4.12 59/63 y 4.13 83/89.

Los registros completos están en `…VERIFICACION.txt` y en `/home/claude/trabajo_4_14/final_4_14/` (este último, solo en este contenedor).

**El escáner de la plataforma no forma parte de estas comprobaciones y no se declara superado.**

## 6. Correcciones externas pendientes (del encargo vigente, aún no implementadas)

Referencia: `ENCARGO_VIGENTE.md` (texto 1 = encargo de cierre §; texto 2 = requisito §).

| # | Exigencia externa | Estado | Siguiente acción |
|---|---|---|---|
| X1 | Revisión externa por hitos y de la candidata (encargo §1, §3 y §9) | **No hecha.** Ninguna revisión de ChatGPT ni externa ha llegado a esta sesión. Todas las revisiones existentes son internas, de Claude | La persona responsable traslada la final, o al menos el dictamen, la matriz y las incidencias, a una revisión externa, y entrega su resultado en la ventana nueva |
| X2 | S5: el Control maestro de Viscofan (D88 no declara C97; textos heredados F5, E88 y E100) (encargo §7) | **No aplicada en el expediente final.** Ampliado por el hallazgo H-P1 (§7) | Aplicarla en un expediente nuevo (copia), con la regla de rama, y regenerar desde la primera dependencia afectada, con auditoría nueva |
| X3 | Fundamento de P-M1; criterio de materialidad y política de salida (encargo §6) | Experimentales, sin adoptar. La suficiencia de k = 3 no está demostrada | Decisión o adopción humana con la evidencia de `DECISIONES_PENDIENTES_4_14.md`; no se firma por la persona responsable |
| X4 | Abstenerse si una incertidumbre material no se puede delimitar (encargo §6) | Viscofan y Vidrala muestran objetivos *condicionados* a convenciones no adoptadas. El encargo dice que eso no basta para declararla resuelta | Resolver X3 o, si no se resuelve, decidir si el objetivo debe abstenerse |
| X5 | Fuentes oficiales materiales con sus bytes (encargo §6) | 15-nov: se consiguieron 1–6, 9a, 9b, 10, 11 (presentación) y 12, y la nota de 2025 como apoyo del 8. Faltan la presentación del 8, la transcripción del 11 y el PDF del 7 (`REGISTRO_FUENTES_15NOV.txt`). Aún no se han incorporado a ningún expediente | El receptor los pide (§11). La persona responsable ejecuta `descargar_fuentes_pendientes_4_14.bat` y busca a mano el 8 y el 11; después se conservan con su SHA-256 en copias nuevas |
| X6 | Motor A con su propia validación (encargo §8) | Defecto F1 (NIIF 16 contado dos veces) sin corregir; **F1 sin respuesta** de la persona responsable; supuesto (a) | Decisión F1. Si es (b): especificación, referencia, réplica y recorrido |
| X7 | Motor C, entrada por instrucciones y alcance completo (encargo §8) | Sin recorrido real del motor C ni batería de la entrada por instrucciones | Empresa financiera real; batería dirigida |
| X8 | Traspaso con relevo real (encargo §10) | Hecho sobre la candidata, pero la auditoría del relevo no fue independiente | Repetir sobre la final con un auditor de contexto separado |
| X9 | Requisito §5: invalidación y bloqueo en todas las vías | Relevo caducado sin aviso (I19); la ficha V6.3 no muestra la aptitud por entradas (I20) | Implementar las propuestas de I19 e I20, con pruebas; cambian el código y las referencias |
| X10 | Requisito §4: corrección semántica | Revisión independiente interna (Claude), no humana ni externa. El comprobador no detecta un fundamento desfasado con un valor correcto (I13) | Revisión externa de las fuentes; propuesta de I13 |
| X11 | Supuestos de la orquestación (encargo §6, decisiones) | E3 y E4 (Vidrala), medias exactas en Elis y precio de Elis del 4-nov-2026 con las acciones de 2025: **supuestos, no decisiones** | Confirmación o cambio explícito de la persona responsable |

## 7. Cambios y hallazgos posteriores a la entrega

**Hecho: el ZIP 4.14 no ha cambiado.** No ha cambiado ningún archivo del árbol empaquetado ni de ningún expediente. Fuera del paquete:
- se editó `INDICE_ENTREGA_4_14.txt` en las salidas para anotar que el ZIP completo no se pudo enviar;
- se escribieron estos dos documentos;
- la carpeta del agente receptor de la prueba de traspaso (`/home/claude/traspaso_414/munger_v2_r1`, 1,9 GB, fuera del paquete) sigue en este contenedor, porque una comprobación de seguridad del entorno detuvo su borrado (I21).

**Hallazgo H-P1 (15-nov, al preparar este traspaso; no está en la documentación del ZIP).** Los textos de la hoja «Control maestro» de los tres expedientes finales siguen con el contenido de la etapa 1 y contradicen las decisiones aplicadas. Valores leídos con openpyxl de los `*_v63_evaluada.xlsx`:
- **Viscofan:** F5 «Pendiente de inversor: 5a (2021–25) / 3a (2023–25) / LTM jun-26»; D88 «Balance 30-jun-26; … precio 6-oct-26. Periodo de las medias DCF (C46–C50) pendiente de inversor.»; E88 «Fijar periodo C46–C50.»; E100 «C48 informado cuando se fije periodo.». El expediente usa el cierre de 2025, las acciones a 31-dic-2025 (D3) y el precio del 3-nov-2026.
- **Vidrala:** F5 y D88 dicen que las medias del DCF están «pendientes de decisión» y que las métricas son a LTM 30/06/2026.
- **Elis:** D88 dice «acciones 7-oct-26 (post-balance, coherente con C41/C42/C55)», mientras que E6 fijó las acciones a 31-dic-2025.
- *Interpretación:* son textos de control que no entran en el cálculo (la reproducción numérica es exacta), pero forman parte del material auditado y contradicen el expediente. Ninguna de las tres auditorías APROBADO lo detectó, y el comprobador de entradas tampoco (relacionado con I13). No cambia ningún precio de Sí, pero sí la fiabilidad documental del expediente.
- **No se ha corregido**, por la instrucción de no modificar el trabajo válido en el traspaso. *Propuesta:* corregirlo junto con X2, en expedientes nuevos, con auditoría nueva del material, y declararlo como I22 en la entrega siguiente.

**Fuentes subidas por la persona responsable que no están en el ZIP** (comparadas por SHA-256 con todo el árbol). Siguen en sus archivos originales: no se han borrado ni modificado.
- Viscofan, ediciones alternativas del mismo año: `annual-report-2020.pdf`, `2016_Annual_Integrated_Report_EN.pdf`, `2017_Cuentas_Anuales_Informe_Gestion.pdf`, `2018_Annual_Integrated_Report_EN.pdf`, `2019_Cuentas_Anuales_Informe_Gestion.pdf` y `2020_Informe_Anual.pdf`. De cada uno de esos años, el ZIP tiene otra edición.
- Viscofan, sin otra edición identificada en el ZIP: `2022_Informe_Anual.pdf` (*interpretación:* `ia_en.pdf` podría ser la de 2022; no se ha comprobado).
- Viscofan, otros: `BMadrid_boletin_20261103_seccion_9.pdf` (en el ZIP está la sección 16, la que sostiene el precio), `tabla.xls`, `HUELLAS_PRECIO.txt`.
- Elis: `LEEME.txt` y `descargas_2026/HUELLAS.txt`.
- *Propuesta:* incorporarlos a la entrega siguiente si alguno sostiene una cifra.

## 8. Decisiones y autorizaciones registradas (no volver a pedirlas)

Literales en `documentacion_cierre_4_14/DECISIONES_ENTRADAS_4_14.md`.
- **Decisiones:** E1, D3 (con condiciones), E2 (con reserva) y E6.
- **Autorización permanente de limpieza:** temporales y copias de pruebas reproducibles, si no hay ejecuciones activas, se conservan el código exacto, las evidencias y los archivos únicos, no se borran originales, fuentes ni entregables, y se registran las rutas. CONTINUIDAD §11.10.
- **Sin respuesta:** F1.

## 9. Archivos necesarios para continuar

1. Las 54 partes del ZIP 4.14, más el `.PARTES.txt` y el `.sha256`.
2. `PROMPT_NUEVA_VENTANA.md` (mensaje de arranque; también va dentro del ZIP).
3. `ENCARGO_VIGENTE.md` (este traspaso).
4. `CONTINUIDAD_TRASPASO.md` (este documento).
5. Recomendados: `…VERIFICACION.txt`, `…INTEGRIDAD_Y_CREDENCIALES.txt` e `INDICE_ENTREGA_4_14.txt`.
6. Para X5: `REGISTRO_FUENTES_15NOV.txt` y la carpeta `VISCOFAN SA\FUENTES_PENDIENTES_4_14\` (13 archivos y `HUELLAS.txt`). `descargar_fuentes_pendientes_4_14.bat` está en `VISCOFAN SA\`. Para Ahold: `descargar_fuentes_ahold.bat`. Los cuatro `.bat` anteriores también van dentro del ZIP, en `documentacion_cierre_4_14/descargas_bat/`.
7. Cualquier encargo o revisión de ChatGPT posterior al 14-nov a las 10:51, si existe.
8. `REGISTRO_FUENTES_15NOV.txt`: las fuentes conseguidas el 15-nov, con sus huellas, y las que faltan.

## 10. Reglas que siguen vigentes en la ventana nueva

Detalle en CONTINUIDAD §11.
- Trabajar sobre copias y conservar los originales con sus bytes. No modificar expedientes históricos: las correcciones van en expedientes nuevos, con la regla de rama.
- LibreOffice y los pipelines, nunca dos a la vez. No editar código mientras corre una batería.
- No contactar empresas ni terceros. No ejecutar operaciones financieras. No publicar.
- No inventar firmas ni adopciones. Ningún APROBADO, porcentaje o recuento acredita aptitud para dinero real.
- Antes de usar el modelo Fable, avisar a la persona responsable.

## 11. Siguiente acción concreta

**Del receptor, antes de cualquier otro trabajo.** Confirmar por escrito a la persona responsable estos cinco puntos. Hasta entonces, el traspaso no está completado.
1. El SHA-256 del ZIP reconstruido es `bb51942cefb848e409a4828e3faeb70f94aa4d29af39cda6d90cd0a97cb7b93e`.
2. `munger_v2_r1/VERSION` empieza por «munger_v2 · r1 · entrega 4.14».
3. Puede leer `CONTINUIDAD.md` y `PROMPT_NUEVA_VENTANA.md` del ZIP.
4. Puede leer `ENCARGO_VIGENTE.md` entero. Los dos bloques literales tienen los SHA-256 de su cabecera, sin el salto de línea final que añade el formato: `ad08d871…` y `70c1ac8d…`.
5. Ha leído este documento, y en especial el §6 (pendientes) y el §7 (hallazgo H-P1).

**Después:**
- ejecutar `bash verificar_paquete.sh completa` sobre su descompresión;
- preguntar a la persona responsable si existe una corrección de ChatGPT posterior al 14-nov y si responde F1;
- **fuentes pendientes (X5), estado al 15-nov a las 11:30:** hay 13 archivos con las huellas comprobadas (`REGISTRO_FUENTES_15NOV.txt`). Están en `…\INFORMACION ECONOMICA EMPRESAS\VISCOFAN SA\FUENTES_PENDIENTES_4_14\`, que es una carpeta conectada, y hay copia en esta sesión.
  - Los descargados a mano conservan el nombre que les dio el navegador: `ver.pdf` es la nota de 2025, `ver 2.pdf` la nota de 2021 (PDF de imagen: necesita OCR para citarlo), `ver 3.pdf` la nota de 2023, `ver 4.pdf` el informe semestral del 1S2026 y `1897_rns_….pdf` la presentación de Vidrala de 2024.
  - **Falta uno.** El receptor se lo pide a la persona responsable: la presentación «Resultados 2025 y Beat'30», https://public.viscofan.com/investor-relations/financialinformation/es/Presentaci%C3%B3n%20Resultados%202025%20y%20BEAT30_ES.pdf → `08_Viscofan_Beat30_presentacion_ES.pdf`. El 15-nov el servidor devolvía HTTP 500 y no está en la CNMV: hay que reintentar.
  - Siguen sin conseguirse: la transcripción oficial de Vidrala de 2024 (n.º 11; hay la presentación, no la transcripción) y el PDF del informe anual de Viscofan de 2024 (n.º 7; solo hay la página web).
  - Al incorporarlos: conservarlos con sus bytes en copias nuevas, declarar lo que falte y no sustituir un documento por texto web.

**Primer trabajo técnico** *(propuesta)*: X2 + H-P1. Corregir los textos del Control maestro de los tres expedientes finales en expedientes nuevos (copias, con la regla de rama). Regenerar desde la primera dependencia afectada, con verificación de entradas y auditoría nueva del material, y declararlo como I22.
