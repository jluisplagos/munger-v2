# Registro de pruebas · entrega 4.13

**Qué es.** Lo que se ejecutó de verdad, con qué código y con qué resultado. Lo que no se ejecutó se dice. Las salidas completas de las rondas están en el registro externo de verificación (fuera del ZIP) y en las carpetas que se citan.

## 1. Batería obligatoria de la integración V6.4 (`personaje_v2/pruebas/test_integracion_v64.py`)

| Grupo | Qué prueba | Pruebas |
|---|---|---|
| A | plantilla V6.4 y su referencia | 12 |
| B | 117 casos con la réplica independiente y el contraste numérico de las lecturas | 21 |
| C | pipeline con la V6.4 | 21 |
| D | cambio de base | 7 |
| E | vigencia y selección; desde la 4.13, tipos JSON erróneos en la primera llamada de las cuatro vías (`TIPOS_413`) y las correcciones R1 y R2 (`grupo_e_revision_413`), con tres combinaciones de la revisión del cambio de la ronda | 45 |
| F | materialidad y protocolos del objetivo; desde la 4.13, salto del protocolo, contrato de cobertura y R3/R4 (`grupo_f_revision_413`) | 53 |
| G | coherencia, variantes y fórmulas alteradas | 17 |
| H | (4.13) V6.4.1 experimental: plantilla, reconstrucción, compatibilidad, configuración, selección, huellas, variantes del perímetro, resumen propio, cobertura, avisos agrupados, R6, R12, R17 y pasadas del pipeline | 19 |
| **Total** | | **195** |

- `verificar_paquete.sh completa` exige ahora al menos 195 (antes, 127).
- La 4.13 añade 68 pruebas: en E, 15 de tipos, 14 de la revisión interna y 3 de la revisión del cambio de la ronda (13 → 45); en F, 4 del salto del protocolo, 9 de cobertura y 4 de la revisión interna (36 → 53); en H, 19.

## 2. Ejecuciones dirigidas durante el trabajo (código del momento)

- **Grupo E y F tras el Hito 1 y el contrato de cobertura:** 40/40 y 49/49 (el registro de avance decía 16 pruebas nuevas en E: eran 15; corregido, R9).
- **Grupo H:** 14/14 tras el Hito 3; 19/19 con las pruebas de R6, R12 y R17.
- **Grupos E y F de la revisión interna:** `grupo_e_revision_413` 14/14 y `grupo_f_revision_413` 4/4.
- **Grupos E, F y G con el código final de los expedientes:** 112/112, antes de la ronda general.

## 3. Sondas sobre el código final (`resultados/`)

Cada registro empieza por la huella de los scripts con que se ejecutó, y el control de la entrega la compara con la actual.
- **`sonda_tipos_4_13.txt` (§3).** 24 alteraciones × 4 vías = 96 primeras llamadas sobre copias del piloto 4.11, sin ninguna excepción.
  - 79 retiran la aprobación.
  - Las 17 restantes están explicadas, y el control de la entrega comprueba cada una:
    - con la solicitud como lista (no es material), no se retira nada;
    - con el registro de publicaciones ilegible, la retirada queda pendiente y visible (código 5) en las cuatro vías;
    - con el estado del pipeline como lista, cada vía se detiene con su motivo (pipeline código 6, «restaurarlo desde una copia»; ficha, informe y resumen, código 3) y el material no cambió;
    - con `ficha.json → decision` de otro tipo (la ficha no es material), `ficha.py` hace la sustitución W-d de la 4.7.1: código 0, aviso «la ficha nueva NO es vigente», el estado sin aprobación, la fila del resumen «SIN APROBACIÓN VIGENTE» y `motivo_vigencia` con motivo. Es lo que exigen las baterías de trazabilidad (M) e integridad. La primera corrección de R1 la convertía en una retirada sin ficha (por eso una sonda anterior daba 80), y rompía esas baterías (§5).
- **`sonda_salto_4_13.txt` (§4).**
  - Las tres fases C reales de la 4.12 se aceptan.
  - Sin protocolo, con la provisional «descartar» o «comprar», el tratamiento queda en «objetivo_sin_protocolo»: no hay objetivo oficial.
  - Con bloqueo, las dos se rechazan por contradicción.

## 4. Réplicas y comparaciones (solo lectura)

- **Réplica independiente de los libros finales:** Vidrala condicionado 21/21, Vidrala bloqueo 21/21, Viscofan 20/20. Control negativo: sin las altas, 9/20.
- **Compatibilidad V6.4.1 frente a V6.4:** 0 celdas distintas con el perímetro vacío, con «Caja» explícita y en heredado; réplica de las bases sin discrepancias.
- **Reproducción histórica de Viscofan con «Caja»:** idéntica a la 4.12.
- **Alternativas de acciones sobre el libro cerrado:** reproducen el caso activo.

## 5. Ronda general

**Ronda A** (copia limpia del árbol con el código de los expedientes, 13-nov 16:41–17:21, 40 min). `bash verificar_paquete.sh completa`:
- **Pasan:** piloto 35; 114/114; 30/30; integración V6.4 **192/192**; solicitudes 55/55; estados 28/28; resumen 45/45; cierre 55/55.
- **FALLA, trazabilidad: 76/78.** Dos pruebas M: «cierre» eliminado y estado cambiado, con `ficha.py`.
- **FALLA, integridad: 102/103.** Una prueba H: cierre de la 4.6 con otra aprobación, con `ficha.py`.
  - **Causa:** una regresión introducida por la corrección R1. `ficha.py` comprobaba la vigencia completa (también la identidad de la ficha oficial) antes de leer el material. Por eso trataba como retirada la sustitución de una ficha cerrada (W-d, código 0 con aviso) y no decía el motivo «no consta».
  - **Corrección:** la comprobación previa mira solo la aprobación del material (`motivo_rechazo_cierre`) cuando hay una salida cerrada o un cierre registrado, y siempre dice el motivo. Las pruebas no se tocaron.
  - **Comprobación:** trazabilidad 78/78, integridad 103/103 y grupo E 42/42.
  - **Revisión del cambio** (Opus, contexto separado; `revision_interna/REVISION_CAMBIO_FICHA_RONDA_4_13.md`): el cambio no cubría combinaciones de un archivo ilegible con una ficha rota o sin marcadores y sin cierre registrado (H1, H2), ni un informe oficial cambiado a mano (H3). Corregido: vigencia completa en la rama de ilegibles, informe comprobado antes de leer el material, ilegibles comprobados otra vez antes de escribir (H4). Tres pruebas nuevas en E. Con el código corregido: E 45/45, trazabilidad 78/78, integridad 103/103. H5 (sin ficha ni cierre registrado, el estado del pipeline conserva APROBADO; la fila se retira) es igual en todas las versiones y queda declarado.
- **FALLA, manifiesto: 105 archivos de más.** Eran perfiles de LibreOffice que los recálculos del pipeline dejaron en las carpetas de los tres expedientes (`.lo_perfil/`). Se borraron del árbol; el empaquetado los excluye.

**Ronda B** (copia limpia del árbol final): 13-nov 17:42–18:50, con los scripts de las huellas que encabezan el registro.
- `bash verificar_paquete.sh completa`, 37 min: **RESULTADO GLOBAL: PASA**.
  - Piloto 35; 114/114; 30/30.
  - Integración V6.4 **195/195**.
  - Trazabilidad 78/78; integridad 103/103.
  - Solicitudes 55/55; estados 28/28; resumen 45/45; cierre 55/55.
- Manifiesto: 4568 archivos, ninguno modificado, ausente ni de más, antes y después de la verificación y los controles.
- Registro: `resultados/bateria_completa_4_13.txt`. Salida completa de la V6.4: `resultados/bateria_v64_detalle_4_13.txt`.

**Ronda C** (descompresión del ZIP final, verificación completa y controles): el resultado está en el registro externo de verificación, fuera del ZIP.

## 6. Control de la entrega y controles históricos

Controles de las entregas, en la ronda B, después de la verificación completa (31 min; `scripts/controles_historicos_4_13.py`). Los resultados y sus causas están en `resultados/LEEME_CONTROLES_HISTORICOS_4_13.md`, con las salidas de referencia en `resultados/controles_historicos_en_arbol_4_13/`:
- **4.2 a 4.6.1:** resultado completo, con la salida idéntica a su referencia. La 4.6 da 23 de 24, por la reparación declarada Z-1.
- **4.7, 4.7.1, 4.8 y las dos comparaciones de baterías:** salida idéntica a la del árbol 4.12.
- **4.9 a 4.12:** el mismo recuento que en el árbol 4.12, salvo la 4.12, que da 59 de 63. Cambian las listas de archivos de la 4.13, el mínimo de la batería y los documentos de versión.
- **4.8.1: 25 de 30 (27 en el árbol 4.12).** Dos reejecuciones con el código de la 4.8 montan un árbol mixto: el `pipeline.py` y el `cierre_v2.py` de la 4.8 con el `ficha.py` actual. Ese `ficha.py` usa `cierre_v2.leer_ficha_control`, que el `cierre_v2.py` de la 4.8 no tiene, y falla con `AttributeError`.
  - **Comprobación:** con el `ficha.py` de la 4.12 en la misma mezcla, la batería de estados da exactamente 27/28 y la reproducción de R-T1 sale idéntica a la conservada.
  - No es una regresión.
- **Control de la 4.13: 87 de 89 en la primera pasada.** Los dos casos eran defectos del propio control (LEEME, §3), no del motor:
  - buscaba en el registro de la batería la palabra «VEREDICTO», que `verificar_paquete.sh` no escribe;
  - exigía un árbol sin `__pycache__`, y esas carpetas las dejan la batería y los controles anteriores.
- **Corrección:** se corrigieron esas dos comprobaciones; sus subprocesos ya no escriben cachés. Después se volvieron a ejecutar solo los controles, sin la batería, sobre la misma copia, ya con el registro de la batería, este LEEME y el control corregido. Esa pasada dio **89 de 89** en la 4.13 y los demás controles igual que en la primera, y sus salidas son las referencias.

## 7. Lo que no se ejecutó

- Ninguna prueba de la revisión externa con material real fuera de los tres expedientes, ni ningún backtest (fuera del encargo).
- Fable no ejecutó ninguna prueba con LibreOffice en sus revisiones: leyó el código de `grupo_f_revision_413` y de las pruebas nuevas del grupo H.
