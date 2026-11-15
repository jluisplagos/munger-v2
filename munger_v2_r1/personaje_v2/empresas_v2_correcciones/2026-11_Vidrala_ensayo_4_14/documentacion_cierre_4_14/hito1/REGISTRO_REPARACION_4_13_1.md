# Reparación 4.13.1 · H5: una aprobación publicada que pierde su respaldo deja de figurar vigente

Base: `munger_v2_r1_entrega4.13_fiabilidad_motor_B_y_conciliacion_economica.zip`, SHA-256 `b1f747a18cd2123d71c0c1abdca0da049207b4c4eb215aa099f345aed4fbf22a`.
Encargo: «encargo prioritario de cierre», §4. Instantánea probada: `i1`; las huellas de los scripts están en §6.

## 1. Reproducción del hallazgo externo (hecho)

Se ejecutó `sonda_h5.py` con el código de la 4.13 sin cambios; la salida es `sonda_h5_codigo_4_13.txt`.
- **Montaje:** una copia independiente del piloto cerrado de la 4.11 por cada vía, con el registro de publicaciones y su respaldo reubicados dentro de la copia; sin `ficha.json` ni `cierre_vigente.json`; `PM1.lambda` = 1,25.
- **Resultado, idéntico al descrito por el revisor externo:**
  - El pipeline limpia la aprobación interna, pero sin dejar ningún antecedente.
  - La ficha, el informe y el resumen retiran la fila pública y devuelven el código 3, pero conservan `APROBADO/concluido` en `estado_pipeline.json`.
- **Además:** solo sin `ficha.json` (con el cierre registrado), el informe y el resumen también conservaban la aprobación, porque salían por «no hay ficha.json» antes de comprobar la vigencia.

## 2. Causa compartida (hecho, en `cierre_v2.py`)

1. **`_motivo_vigencia`** daba por «estado temprano legítimo» la combinación sin ficha y sin cierre registrado. La única detección de una aprobación sin respaldo (`aprobacion_sin_ficha_cerrada`) exigía que `ficha.json` existiera.
2. **`archivar_salidas`** devolvía `None` sin tocar el estado cuando no quedaba ninguna salida oficial que archivar.
3. **`informe.py` y `resumen.py`**, sin `ficha.json`, sincronizaban las filas y salían sin aplicar la vigencia.

## 3. Corrección (versión final, instantánea i3)

- **Señal de publicación propia de la aprobación** (`senal_publicacion`, `aprobacion_publicada_sin_respaldo`). Se toma la publicación como hecha si consta alguna de estas señales:
  - una entrada «publicada» en el primer registro de publicaciones legible (o en su respaldo);
  - una entrada con la identidad de esta aprobación (solicitud y huella fiel de la respuesta aceptada), en cualquier estado;
  - el registro estructurado `publicaciones_de_la_aprobacion` del estado;
  - en el historial del estado, el FIN de un paso 14 que cierra (estado de cierre con APROBADO) después de consumir la respuesta a esta solicitud;
  - en un cierre anterior a la 4.8.1, cualquier FIN de cierre.

  No se busca ninguna fila por el nombre de la empresa. Un registro ilegible no es una señal: deja la retirada pendiente visible (código 5) y no hace perder una aprobación del intervalo legítimo.
- **Invalidar el estado aunque no queden salidas:** `archivar_salidas` crea el antecedente (`RETIRADA.json` con `archivos: []` y `sin_salidas_oficiales`), retira las publicaciones e invalida el estado.
  - Sin registro, retira los destinos que el propio estado registra, siempre junto a la ubicación actual del expediente, más el destino de la vía, a través de `retirar_publicaciones`. Un destino que no se puede escribir queda en `retirada_pendiente`, con código 5.
- **Rastro previo antes de sincronizar:** `rastro_previo/` con el estado y el registro tal como estaban, en todas las retiradas.
- **No depender de una carpeta archivada:** la identidad de la aprobación retirada se guarda en tres señales independientes, y `motivo_aprobacion_retirada` rechaza la aprobación si aparece en cualquiera:
  - `aprobaciones_retiradas.json`, que solo crece; si es ilegible, se ignora como fuente y no retira un cierre sano;
  - `RETIRADA.json`;
  - las entradas del registro que retiró una retirada de la aprobación, marcadas con `retirada_de_la_aprobacion`. Una retirada de filas de la sincronización no cuenta.

  Así, restaurar archivos antiguos, incluido el estado, no reactiva la aprobación. Los cierres anteriores a la 4.8.1 se identifican por la huella de su auditoría.
- **Las cuatro vías:**
  - el pipeline aplica la vigencia al empezar y adopta la publicación que registra `resumen.py`;
  - `ficha.py` comprueba la aprobación sin respaldo antes de leer el material;
  - `informe.py` y `resumen.py` aplican la vigencia antes de salir por «no hay ficha.json».
- **Intervalo legítimo entre el paso 13 y el paso 14:** no se toca. La aprobación nueva es de otra solicitud y no consta ningún FIN de cierre de ella.

## 4. Pruebas

**Sondas** (de diagnóstico): `sonda_h5_codigo_4_13.txt` reproduce H5 con el código de la 4.13, y `sonda_h5_corregido_v2.txt` y las salidas de `sondas_d1_w3/` y `sonda_d2_w6.txt` las repiten con el código corregido.

**Batería nueva `personaje_v2/pruebas/test_vigencia_h5.py`: 59/59, obligatoria en `verificar_paquete.sh completa`, con un mínimo de 59.**

| Grupo | Qué prueba | Pruebas |
|---|---|---|
| A | cuatro primeras llamadas con el material cambiado, intacto e ilegible | 12 |
| B | ausencias individuales y combinadas | 16 |
| C | ninguna salida oficial restante | 4 |
| D | destino inaccesible | 4 |
| E | idempotencia | 4 |
| F | restaurar archivos antiguos | 4 |
| G | intervalo legítimo y cierre del paso 14 | 2 |
| H | recuperación con una auditoría nueva | 1 |
| I | casos D1-1 a D1-6 de la revisión interna | 8 |
| J | casos D2-1 a D2-3 de la segunda revisión | 4 |

**Regresiones:**
- Sobre i1, las siete baterías obligatorias pasan. Es una versión intermedia, superada después.
- Sobre i3: todas las baterías pasan salvo la integración V6.4 (135/181), por una causa ajena a H5 (el agente sintético de las pruebas no escribía el bloque del contrato 4.14).
- **Sobre i4, la final:** `verificar_paquete.sh completa` pasa las doce baterías, incluida H5 59/59 y V6.4 196/196. Solo falla el manifiesto, como corresponde a un árbol modificado.

## 5. Revisiones internas (subagentes de Claude, contexto separado; no son revisión externa)

- **Primera, sobre i1:** 1 hallazgo bloqueante, 4 importantes, 3 menores y 3 observaciones.
  - El bloqueante, D1-1: sin registro de publicaciones, una fila de otro expediente de la misma empresa bloqueaba un cierre legítimo.
  - Resueltos: D1-1 a D1-6, D1-8 y D1-10.
  - Declarados: D1-7, la restauración en espejo de todo el expediente; D1-9, `ficha.py --provisional`, que no publica salidas oficiales.
- **Segunda, sobre i2:** 2 importantes, 1 menor y 2 observaciones.
  - D2-1: la línea de publicación del historial truncada a 200 caracteres.
  - D2-2: una retirada de filas de la sincronización se tomaba por retirada de la aprobación.
  - D2-3: un FIN de no_entregable contaba como cierre.
  - D2-4: la publicación registrada por `resumen.py` no sobrevivía al estado de la memoria.
  - Resueltos en i3 con pruebas: D2-1 a D2-4. Declarado: D2-5, una entrada «publicada» de otra aprobación cuenta como señal, que es el lado seguro.
- **Incidencia durante la corrección (hecho):** una versión intermedia usaba la ruta absoluta del historial. Una sonda retiró así una fila en una copia de trabajo antigua de la 4.11 (`/home/claude/trabajo/…`), que no forma parte de la base, la entrega ni los originales.
  - Se restauró desde la base y se comprobó byte a byte.
  - Se corrigió: sin registro, solo se usan destinos junto a la ubicación actual del expediente.
  - En todas las ejecuciones posteriores, `find -newer` confirma que no se escribe nada fuera de las copias.

## 6. Huellas

**Instantánea i4 (final):**

```
0260b29edb01578d1c28126945a70e7d5b8d135cedfc3babda4b1de98d25f74c  personaje_v2/scripts/cierre_v2.py
ac8e6bbebf786cc27f5903ce01f230baea1ad41e599a235026f35e4add54da09  personaje_v2/scripts/ficha.py
10fd7bab9f689b8174dc3c4e634d0aadc852f7dc5f905bbeff550ef054a88d6d  personaje_v2/scripts/informe.py
6739881a8d7883b73a47ade1c5f18ae4052a4c9d482771b8ffb98fd5e1b722ab  personaje_v2/scripts/resumen.py
45a94fdf9b89dc4877aa6f020e3e51f9a9350be4324d678c2d212c17dc84e4b3  personaje_v2/scripts/pipeline.py
566cc87b8bfa37f3b6bd015c5ffc2af31f3a3a14324f851cc43e7bff927d4665  personaje_v2/pruebas/test_vigencia_h5.py
```

**Instantánea i1 (intermedia, superada):**

```
d4d41bb3a6288afa74b7bb29cbae67e9771f10df96561d5e082318c1fd58a351  personaje_v2/scripts/cierre_v2.py
33c4d6f9d78ae103276ab86cdb9990b9495ec0e244a0e0e850f2ada38b4e634c  personaje_v2/scripts/ficha.py
85a44b46a2026716823ca59368c2b61e015e6e9de896690e2dd968a799c0c495  personaje_v2/scripts/informe.py
6739881a8d7883b73a47ade1c5f18ae4052a4c9d482771b8ffb98fd5e1b722ab  personaje_v2/scripts/resumen.py
88bf2edf18a34eeffe209d6bc188ba492f6ea08678888e813dd6921034c822a7  personaje_v2/scripts/pipeline.py (sin cambios)
f4289b592323feb14337117fae55b4bfe94d1b189311febf42a7ea948c2bf294  personaje_v2/pruebas/test_vigencia_h5.py
```

## 7. Límites (declarados)

- **Restauración total:** si alguien restaura a la vez el estado, el registro de publicaciones, `aprobaciones_retiradas.json` y borra los antecedentes de `historial_cierres/`, el expediente vuelve a ser indistinguible del original. Equivale a restaurar una copia de seguridad completa, y eso no se puede detectar desde dentro del expediente.
- **Dos expedientes de la misma empresa en la misma carpeta:** la detección por la fila del resumen, que solo se usa sin registro ni respaldo, podría retirar por error la aprobación de uno en su intervalo legítimo. Es el lado seguro: la recuperación es una auditoría nueva.
