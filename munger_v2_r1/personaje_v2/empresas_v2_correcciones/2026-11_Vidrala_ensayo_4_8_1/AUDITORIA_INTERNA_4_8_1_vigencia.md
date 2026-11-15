# Control de vigencia de la entrega 4.8.1 (contexto separado)

**Qué es este documento:**
- es el informe final del revisor del control de vigencia, un agente de Claude (Opus) con contexto separado;
- solo conoce el trabajo por sus documentos;
- es salida de un modelo, no una comprobación externa;
- **fecha:** 10-nov-2026, unos 15 minutos de ejecución. El revisor dejó constancia de su avance en un archivo de progreso, que se vigiló durante la ejecución;
- **material revisado:** `MATERIAL_VIGENCIA_4_8_1.txt`, con SHA-256 `d69532a5…2d5f102c6` y 36 archivos;
- **transcripción:** fiel; solo se ha ajustado el formato y se han abreviado algunas rutas.

Las correcciones posteriores de V-1 a V-10 están en `REGISTRO_ENTREGA_4.8.1.md` §7.

---

## 1. Material y huellas

- **Material:** la huella del archivo de material coincide con la esperada, y las 36 huellas que lista coinciden con el árbol al empezar y al terminar.
- **H2:** su huella es `9edf6252…5422`, la esperada.
- **El árbol no se tocó.** La lista de huellas de sus 2.537 archivos es la misma antes y después, y no se creó ningún `__pycache__`.
- **Archivos cambiados.** Frente al manifiesto de la 4.8 solo cambian los 11 archivos declarados; los originales, los expedientes anteriores y el libro de referencia no cambian.

## 2. Qué se ejecutó

No se ejecutó nada que use LibreOffice.

| Qué | Resultado |
|---|---|
| `test_auditorias_v2.py` | 43/43, con el mismo estado de cada prueba que la salida conservada |
| `reproducir_rt1.py` | Código 0. Los tres modos piden una auditoría nueva (código 10). La salida es idéntica salvo la etiqueta |
| `mutar_rt1.py` sobre una copia | 16 de 16 detectadas |
| `analisis_reinversion_4_8_1.py --salida` | Código 0, siete controles. Las cinco salidas son idénticas byte a byte |

**Sondas propias**, sobre copias del expediente 4.6.1:
- los casos K1, K2–K2d, K3, K4 y K6;
- casos cercanos: K1b–K1d, K2e–K2g, L1, L2, L4 y L5;
- el modo `--agentes-simulados`;
- la opción «no» de Q-T5, probada con M13 aplicada en una copia.

**No se ejecutó:**
- `comprobar_integracion_verificador_481.py`, porque no estaba en la lista de lo permitido;
- las baterías con LibreOffice;
- `--reiniciar`, que se simuló borrando el estado.

## 3. Hallazgos de la auditoría interna

| Hallazgo | Veredicto | Hecho que lo prueba |
|---|---|---|
| Y-a | **Resuelto en parte** | Se rechazan K2, K2b, K2c y K2d (código 10, «repite el contenido»). En cambio, K2e (la línea de material al principio), K2f (los 16 puntos en orden inverso) y K2g (sin tildes) se aceptan y cierran (V-1) |
| Y-b | **Resuelto en parte** | Se rechazan K1 y L5 (cierre válido, estado borrado y `--desde 13`: el registro persiste). En cambio, K1b (`Auditoria_4_6.md`), K1c (`auditoria_4_6.md.bak`) y K1d (`antecedentes/auditoria.md`) se aceptan y cierran (V-2) |
| Y-c | **Resuelto**, con defectos de documentación (V-3 a V-6) | den = 229,381 + 12,418 + 278,797 = 520,596, con un 53,6 % de circulante. SRF reproduce al auditor: 65,3842 / 59,9483 y 62,1000 / 55,3634. f pasa de 1,1684 a 1,1649 con den = 530,009. Las tablas coinciden con el CSV |
| Y-d | **Resuelto** | Δ conv. es −0,33 en S·L1.15 y −0,79 en S·T1.00. «Coherentes» queda matizado en §3.7 y `ORIGEN` está reclasificado. Residuo: la docstring del guion (V-3) |
| Y-e | **Resuelto en parte** | Las marcas de retirada están puestas. Pero en DECISIONES, l. 207, y en CONTINUIDAD, l. 6, sigue sin matiz «la sensibilidad de −20,6 puntos … contiene/contenía doble cómputo con el S2C» |
| Y-f | **Resuelto en parte** | Las cinco afirmaciones del auditor se han corregido o son ahora ciertas. Hay afirmaciones nuevas que el código no cumple: «con cualquier nombre», «con otro formato» y «ninguna puede responder» |
| Y-g | **Resuelto** | En K3 se archiva y `--desde 14` da código 4. K3c (CRLF en un cierre anterior a la 4.8.1) también archiva, como declara el «byte a byte» |
| Y-h | **Resuelto** | En K4 el cierre se archiva en la primera ejecución y `ficha.py` da código 3 |
| Y-i | **Resuelto** | En K6, guardar la respuesta con CRLF, restaurarla o añadirle BOM mantiene el cierre |
| Y-j | **Resuelto en parte** | 43 pruebas; M10 y M11 se detectan. Con el código 4.8, los grupos D, E y H se interrumpen con IndexError (2/25, declarado) |
| Y-k | **Resuelto** | — |
| Y-l | **No resuelto** (pendiente declarado) | Siguen «__N481__», REGISTRO §7 y §10 y las seis salidas sin escribir |
| Y-m | **Resuelto** | — |

## 4. Hallazgos nuevos

### V-1 · importante · Otros cambios solo de formato siguen acreditando una aprobación

**Hecho.** K2e, K2f y K2g dan código 0, concluido/APROBADO y fila APROBADO.

**Causa.** `huella_contenido` conserva el orden de las líneas y las marcas diacríticas.

**Por qué importa.** Es el mismo requisito que Y-a. El Anexo D y el REGISTRO dicen que se descarta «con otro formato».

**Interpretación.**
- Es importante y no bloqueante: hace falta reordenar o transcribir a propósito. Todas las variantes accidentales o de herramienta se rechazan.
- Con una lectura estricta del encargo, sería bloqueante.
- El argumento del registro para no detectar casi duplicados («reescribir solo la línea de material») es discutible: el pipeline pide que se repitan las dieciséis comprobaciones. L4 muestra que una respuesta con el material equivocado, cambiando solo esa línea y la de solicitud, se acepta y cierra.

**Propuesta:**
- una huella que no dependa del orden: el multiconjunto de líneas normalizadas;
- quitar las marcas diacríticas, con NFKD y descartando Mn;
- pruebas para K2e–K2g y su mutación;
- o, si no se hace, rebajar el texto a «dentro de cada línea».

### V-2 · importante · Las auditorías históricas que no se llaman `auditoria*.md` no se anotan

**Hecho.** K1b, K1c y K1d se aceptan y cierran.

**Causa.** El glob `auditoria*.md` distingue mayúsculas y solo mira la carpeta y `historial_cierres/`.

**Por qué importa:**
- el Anexo D y el código dicen «con cualquier nombre»;
- el límite declarado solo excluye las auditorías traídas de fuera del expediente.

**Propuesta:**
- anotar todo archivo de texto del expediente, en cualquier subcarpeta y sin distinguir mayúsculas, que H2 califique APROBADO o que tenga una línea «Material auditado»;
- o ajustar el texto a lo que hace el código;
- añadir pruebas.

### V-3 · menor · Cifras y textos desfasados

**Hecho:**
- INFORME §3.3 dice «las cuatro son hipótesis condicionadas», con cinco estructuras;
- INFORME §4 dice «68,92, frente a 61,63–63,69». 63,69 es el valor de la primera versión de f: hoy es 63,66, y SRF llega a 65,38;
- REGISTRO §2 dice «1.155 filas», cuando hoy son 1.386;
- la docstring del guion (punto 4) dice «se sustituye por SR1 y SR2 …, coherentes», sin SRF ni el matiz de Y-d.

**Propuesta.** Corregirlos.

### V-4 · menor · El control «SRF con ρ = 0 reproduce S» es tautológico

**Hecho.** Compara la misma llamada consigo misma: no pasa por `kw_estructura("SRF", …)`.

**Propuesta:**
- usar `kw_estructura("SRF", 0.0)`;
- añadir un control fila a fila de la inversión fija: la de SRF igual a la de S × (1 − Rh ÷ F).

### V-5 · menor · SRF publica un ROIC y un S2C que no son los efectivos

**Hecho:**
- en SRF·L1.15, terminal del NORMAL, se publica «ROIC 0,1100», pero la inversión fija para crecer es 28,91 frente a 41,22, y el ROIC efectivo sobre la inversión fija es de unos 0,157;
- en SRF·T1.00, con un factor de 0,0494, ese ROIC efectivo es de unos 2,23.

**Interpretación.** SRF con θ = 1 supone que el crecimiento casi no necesita inversión fija, también a perpetuidad. El informe no lo declara.

**Propuesta.** Publicar el ROIC y el S2C efectivos y declarar esa implicación.

### V-6 · menor · Una cifra atribuida al auditor no está en su informe transcrito

**Hecho.** El REGISTRO §6 cita «1,1442» como cifra del auditor, y esa cifra no aparece en `AUDITORIA_INTERNA_4_8_1.md`, cuya cabecera dice que la transcripción no cambia el contenido.

**Propuesta.** Citar de dónde sale o retirarla.

### V-7 · menor · La opción «no» de Q-T5 no es posible tal como se describe, y §9 no la lista

**Hecho.**
- Con M13 aplicada en una copia, la ficha cerrada sigue en esa ejecución.
- Pero la siguiente ejecución, sin `--desde`, la archiva, porque `auditoria` pasa a None al registrar la solicitud y `motivo_rechazo_cierre` rechaza con una pendiente.
- REGISTRO §9 no lista Q-T5.

**Propuesta.** Reescribir la opción «no» y añadir Q-T5 a §9.

### V-8 · menor · Documentación que no coincide con el código

**Hecho:**
- el LEEME espera «30/30» para la batería de solicitudes;
- el Anexo D y DECISIONES dicen «ninguna puede responder», cuando una REPETIR de contenido conocido sí responde;
- las docstrings de `pipeline.py` (cabecera y `agente_auditoria`) solo describen la comprobación por SHA-256.

**Propuesta.** Alinearlos con el código.

### V-9 · menor · Un `auditorias_conocidas.json` ilegible detiene el pipeline sin mensaje

**Hecho (L2).** Termina con una traza de `JSONDecodeError` y código 1.

**Por qué importa poco.** Falla del lado seguro.

**Propuesta.** Un mensaje y un código explícitos, y una prueba.

### V-10 · menor · La regla de contenido rechaza también una auditoría rehecha con el mismo texto

**Hecho:**
- **L1.** Tras un cierre válido y `--desde 13` sobre el mismo material, el auditor sintético rehízo la auditoría con el mismo texto: código 10, «repite el contenido». Basta añadir «Aviso: x» para que se acepte.
- **Modo simulado.** Con un `auditoria.md` simulado constante que nombra otro material, el pipeline acaba esperando con código 10. El Anexo D describe un agotamiento que termina en `no_entregable`.
- **Interpretación** (leído del código, no ejecutado con la 4.8): con la 4.8 ese caso terminaba en `no_entregable`.

**Propuesta:**
- documentarlo;
- valorar que una aprobación repetida cuente como corrección fallida.

## 5. Reglas permanentes

**Hecho:**
- la réplica de la 4.8 sale idéntica (7 de 7);
- R_OP, las probabilidades, el puente y las acciones coinciden; k y la caja vienen del guion de la 4.8, que no ha cambiado;
- solo cambian los archivos declarados;
- los campos humanos están a null;
- no se ha aplicado nada al libro de referencia.

## 6. Límites

- **Sin LibreOffice:**
  - no se ejecutaron las baterías que lo usan ni `verificar_paquete.sh`;
  - sus salidas conservadas tienen todas la misma hora (se copiaron juntas), así que no se puede comprobar que se ejecutaran con el código final;
  - no hay salida conservada de `verificar_paquete.sh completa`.
- **No ejecutado:**
  - `comprobar_integracion_verificador_481.py`;
  - `--reiniciar`, solo simulado.
- **Empaquetado (observación):**
  - unos 1.006 archivos del árbol de trabajo no están en el manifiesto de la 4.8, entre ellos `personaje_v2/pruebas/sintetico/` y `personaje_v2/.lo_perfil/`;
  - el manifiesto sigue siendo el de la 4.8;
  - es la verificación final pendiente.
- **Alcance:**
  - las sondas financieras son contrastes igual de condicionados que los de la entrega;
  - las variantes de formato y de nombre son ejemplos, no una búsqueda exhaustiva.
