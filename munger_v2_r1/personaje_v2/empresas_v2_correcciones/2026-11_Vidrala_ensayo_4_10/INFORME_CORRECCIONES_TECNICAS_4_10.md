# Correcciones técnicas de la entrega 4.10 (encargo §3)

**Qué es.** Los cuatro hallazgos acotados de la revisión externa de la 4.9, cada uno con su reproducción antes y después y con sus pruebas. Las pruebas nuevas están en `personaje_v2/pruebas/test_trazabilidad_v2.py`, obligatoria en `verificar_paquete.sh completa`.

**Reproducción con el código de la 4.9.** Está en `tecnico/reproduccion/trazabilidad_con_codigo_4_9.txt` y `.json`: 26/69. El grupo L se interrumpe porque no existe `motivo_acreditacion_libro`, por eso hay 69 pruebas y no 74. La salida con el código de la 4.10 se recoge en `REGISTRO_ENTREGA_4.10.md` §6.

**Lo que no cambia:**
- `Pipeline.veredicto_auditoria` (H2) y sus dieciséis exigencias;
- D10, S-19 y los requisitos de una conclusión favorable;
- las solicitudes persistentes y las reglas de reanudación;
- el código 5 cuando queda una retirada pendiente;
- las fórmulas, los valores y los criterios financieros.

## 3.1 · ZIP portable

**[Hecho] La incidencia.**
- El ZIP de la 4.9 guarda `…/material_vigencia_2/ejecuciones/n4_paginas_reales_engaños.txt` con los bytes UTF-8 del nombre, pero sin el indicador UTF-8 (bit 11) y sin un campo Unicode alternativo (0x7075).
- Python `zipfile` lo extrae como `enga├▒os.txt`, porque interpreta el nombre en cp437: queda un ausente y un adicional en el manifiesto.
- `unzip` lo recupera bien.
- Reproducido en el arranque (`arranque/ARRANQUE_4_10.md`). El ZIP original no se ha modificado.

**[Corrección]** El nuevo productor, `scripts/empaquetar_zip.py`, escribe con `zipfile`, que marca con el bit 11 todo nombre no ASCII. Los nombres previstos y los bytes de los archivos históricos se conservan: no se ha renombrado ningún archivo de la 4.9.

**[Comprobación]** `--comprobar` hace lo siguiente:
- extrae el ZIP final dos veces, con Python predeterminado y con `unzip`;
- comprueba el manifiesto en las dos extracciones (cero modificados, ausentes y adicionales);
- comprueba que los dos árboles son idénticos byte a byte;
- comprueba que cada nombre no ASCII lleva el indicador.

Es la extracción real, no solo el encabezado. El resultado sobre el ZIP final está en el registro externo de verificación.

## 3.2 · BOM y transformaciones inocuas

**[Hecho] El defecto.**
- `cierre_v2.motivo_rechazo_cierre` decodificaba `auditoria.md` en UTF-8 sin quitar la marca BOM antes de H2 y del lector de material.
- Una respuesta aceptada que empezaba por «1. PASA» y a la que solo se añadía, o que ya traía, un BOM conservaba su huella fiel. Pero H2 leía «﻿1. PASA», no reconocía el punto 1 y daba REPETIR, así que las cuatro vías retiraban una aprobación legítima. Con «Material auditado» en la primera línea, el lector de material no la encontraba.
- El caso con preámbulo de la batería de la 4.9 no lo detectaba.

**[Corrección]**
- La lectura común, antes de H2 y de los lectores de solicitud y de material, es `texto_fiel`: solo las transformaciones inocuas ya declaradas (BOM, CRLF/CR, saltos finales y NFC/NFD). Se usa en el cierre y la vigencia (`motivo_rechazo_cierre`) y en la aceptación del paso 13 (`pipeline.py`).
- Las huellas de bytes siguen calculándose sobre los bytes reales, separadas de la huella fiel.
- No se amplía la normalización a palabras, orden, puntuación ni espacios.
- Los cierres sin huella fiel (los de la 4.8.1) siguen sujetos a sus bytes exactos.

**[Pruebas]** Grupo B, 41 pruebas:
- una respuesta nueva aceptada con BOM ante «1. PASA», que cierra con código 0, en las cuatro vías;
- BOM añadido después del cierre con «1. PASA», «Material auditado» o «Solicitud de auditoría» como primera línea, en las cuatro vías;
- BOM con CRLF y BOM con NFD;
- el caso con preámbulo;
- regresiones negativas con BOM: una solicitud distinta, ausente o duplicada y las mismas palabras con el significado contrario, cada una retirada en la primera llamada con su diagnóstico;
- el cierre sin huella fiel, retirado al añadir un BOM;
- la huella de bytes registrada, que es la de los bytes reales.

**Antes y después.** Con el código de la 4.9 fallan las 5 de la respuesta aceptada con BOM, las 16 de BOM añadido con «1. PASA» o «Material auditado» en primera línea y con CRLF o NFD, las 4 negativas (retiran, pero por el motivo equivocado: «la auditoría dice REPETIR») y la del cierre sin huella fiel. Pasaban ya el caso con preámbulo y el de «Solicitud» en primera línea, como describía la revisión externa.

## 3.3 · Ficha que pierde sus marcadores de cierre

**[Hecho] El defecto.** Lo encontró la revisión externa y venía ya de la 4.8.1.
- En una ficha aprobada se elimina «cierre» y se cambia `estado_analisis` a `pendiente_de_datos`. Las vías la tomaban por «sin salida cerrada» aunque `cierre_vigente.json` registraba otra ficha.
- `informe.py` dejaba el CSV concluido/APROBADO y `resumen.py` publicaba pendiente_de_datos/APROBADO.
- Con `{}` se publicaba una fila sin empresa.
- Restaurar los bytes de la ficha reactivaba la aprobación.
- Modificar solo uno de los dos marcadores ya estaba protegido.

**[Corrección]**
- Con un cierre registrado (`cierre_vigente.json`, función `cierre_registrado`), la correspondencia se comprueba con independencia de los marcadores actuales (`motivo_vigencia`).
- `archivar_salidas` trata ese caso como una salida cerrada: retira el estado y la aprobación del pipeline y todas las publicaciones registradas, también si la ficha no dice su empresa.
- `ficha.py` comprueba la correspondencia antes de escribir y de que `registrar_cierre` actualice el registro. Si no corresponde, archiva, retira y no escribe (código 3, o 5 con una retirada pendiente).
- `informe.py`, `resumen.py` y la petición de una auditoría nueva en el pipeline usan la misma condición, comprobada localmente, sin depender de funciones nuevas de `cierre_v2.py`.
- `resumen.py` no escribe nunca una fila sin empresa, ni «APROBADO» para una ficha que no está cerrada.
- **(Revisión interna, R-1)** Si además se borra `cierre_vigente.json`, ya no queda ningún cierre registrado, pero el estado del pipeline sigue con APROBADO. Esa aprobación sin ficha cerrada (`aprobacion_sin_ficha_cerrada`, que exige además una publicación viva registrada, el rastro de un cierre publicado: así no afecta al cierre legítimo del paso 14) también es un motivo de retirada; las cuatro vías la comprueban, y `archivar_salidas` reinicia el estado. El defecto venía de la 4.9.
- Restaurar los bytes o regenerar la ficha no reactiva una aprobación retirada.

**[Pruebas]** Grupo M, 26 pruebas. Para cada uno de los cambios («cierre» eliminado, estado cambiado, ambos, `{}` y ambos con `cierre_vigente.json` borrado) se observa la primera llamada del paso 14, `ficha.py`, `informe.py` y `resumen.py`:
- retirada coherente en el destino predeterminado y en el configurado;
- historial conservado;
- ninguna aprobación incoherente.

Además:
- `ficha.json` ausente con un cierre registrado: el paso 14 archiva el resto y retira;
- restaurar o regenerar no reactiva;
- con un destino inaccesible, el código es 5;
- un estado temprano legítimo sin cierre previo se escribe sin retiradas;
- `{}` sin cierre registrado no publica ninguna fila.

**Contrato de códigos.** Es el de los casos comparables: paso 14 → 4; `ficha.py`, `informe.py` y `resumen.py` → 3; 5 si queda una retirada pendiente.

**Excepción declarada.** Con un solo marcador cambiado, la ficha sigue «cerrada» y `ficha.py` mantiene la sustitución documentada en la 4.6.1 y la 4.7.1 (W-d): código 0 con aviso, cierre archivado, filas retiradas y una ficha nueva que no es vigente. Queda como la decisión pendiente de §9.5 de CONTINUIDAD.

**Antes y después.** Con el código de la 4.9 fallan 15: las 8 de «ambos» y `{}`, las 4 de R-1, la de `ficha.json` ausente, la de restaurar o regenerar y la de la fila sin empresa.

## 3.4 · P-N2: acreditar el libro final

**[Hecho] El defecto.** `verificar_todo.sh` escribía `verificacion_integridad.txt` antes de incorporar las cachés.
- En la 4.6.1 acredita un archivo de SHA-256 29ae55fa…, mientras que el libro entregado es 1020bb53….
- La verificación posterior nombraba el temporal `con_cache.tmp.xlsx`.

**[Corrección]** Al final de `verificar_todo.sh`, después de todas las escrituras del libro, `acreditar_libro.py` escribe un comprobante externo, `acreditacion_libro.json`. El libro no lleva su propio hash ni ninguna referencia circular. El comprobante distingue tres cosas:
- el libro de entrada;
- el libro evaluado verificado antes de las cachés (el que acredita `verificacion_integridad.txt`, que conserva su sentido histórico);
- el archivo final: su SHA-256, sus bytes y su propia verificación, `verificacion_libro_final.txt`.

Cómo se usa el comprobante:
- Ambos archivos entran en el material de la auditoría.
- `motivo_acreditacion_libro`, desde `motivo_rechazo_cierre`, impide confirmar un cierre y retira la vigencia en cuatro casos: el libro ya no es el acreditado; la ficha oficial o la provisional registran otro libro; el comprobante no nombra el libro evaluado («…_v63_evaluada.xlsx»); o su verificación final no es ÍNTEGRO (revisión interna, R-3). No se actualiza un cierre antiguo para conservar su aprobación.
- A un expediente sin comprobante (anterior a la 4.10) no se le atribuye uno nuevo.

**[Pruebas]** Grupo L, 7 pruebas:
- incorporación efectiva de cachés (el final es distinto del verificado antes y tiene valores);
- la ruta sin copia recalculada (el final es igual al verificado antes);
- una modificación posterior del libro, o una ficha que registra otro libro, invalidan la correspondencia;
- un comprobante que no es ÍNTEGRO, o que nombra otro `.xlsx`, no acredita nada;
- un cierre con el libro acreditado (el comprobante está en el material);
- una correspondencia rota después del cierre retira en la primera llamada;
- igualdad independiente del archivo final de los expedientes de la 4.10 con su comprobante. En la verificación del paquete, el árbol es el extraído del ZIP.

Con el código de la 4.9, la primera falla (no hay comprobante) y el grupo se interrumpe.

## Archivos cambiados (motivo)

- `personaje_v2/scripts/cierre_v2.py`: lectura común antes de H2 (3.2); `cierre_registrado`, `motivo_vigencia` y `archivar_salidas` (3.3); `motivo_acreditacion_libro` y el material (3.4).
- `personaje_v2/scripts/pipeline.py`: lectura común en el paso 13 (3.2); retirada al pedir una auditoría nueva con un cierre registrado (3.3).
- `personaje_v2/scripts/ficha.py`, `informe.py` y `resumen.py`: la condición de cierre registrado (3.3); en `resumen.py`, además, ninguna fila sin empresa.
- `personaje_v2/scripts/verificar_todo.sh` y el nuevo `acreditar_libro.py`: el comprobante del archivo final (3.4).
- `personaje_v2/pruebas/test_trazabilidad_v2.py` (nuevo) y `verificar_paquete.sh`: la batería obligatoria.

Los demás archivos se conservan con sus bytes.

## Límites

- R-V1 y estas correcciones siguen siendo una garantía de procedimiento: un agente que reescriba de forma coherente la ficha, `cierre_vigente.json` y el estado no se detecta.
- La sustitución de una ficha con un solo marcador sigue la decisión pendiente de §9.5.
- Los expedientes anteriores a la 4.10 no tienen comprobante del libro (P-N2 declarado).
