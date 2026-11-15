# Controles de las entregas sobre el árbol 4.14

**Qué es.** Lo que da cada control de una entrega anterior sobre el árbol de la 4.14, y por qué. Sustituye, para este árbol, a `…_4_13/resultados/LEEME_CONTROLES_HISTORICOS_4_13.md`, que sigue describiendo el árbol 4.13.

**Cómo se obtuvieron las referencias.** Sobre la descompresión del ZIP candidato 4.14 (SHA-256 `f9f888e3…4f5a24`) y **después** de `bash verificar_paquete.sh completa`, que dio PASA con código 0 (`bateria_completa_candidata_4_14.txt`). Se usó el mismo script: `python3 -I -B personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_13/scripts/controles_historicos_4_13.py CARPETA_SALIDA`. Las salidas están en `controles_historicos_en_arbol_4_14/`.

Un primer intento se detuvo por falta de espacio en el disco (INCIDENCIAS I17) y se repitió entero.

**Orden.** Primero, el control de la 4.14: `python3 -I -B personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_14/scripts/comprobar_entrega_4_14.py`. Da 35 de 35, código 0, y su salida está en `comprobar_entrega_4_14_candidata.txt`. Después, los controles históricos, uno detrás de otro.

## 1. Exigencias funcionales (resultado completo, igual que en el árbol 4.13)

| Control | Resultado sobre el árbol 4.14 |
|---|---|
| 4.2 | todas las comprobaciones esperadas se cumplen; idéntica a su referencia |
| 4.3 | 217 de 217; idéntica |
| 4.3.1 | 43 de 43; idéntica |
| 4.4 | 72 de 72; idéntica |
| 4.5 | 60 de 60; idéntica |
| 4.6.1 | 23 de 23; idéntica |
| **4.14** | 35 de 35 |

## 2. Exigencia funcional que cambia por una reparación declarada

- **4.6:** 23 de 24, código 1, igual que en los árboles 4.9 a 4.13 (Z-1, D-RV1c).

## 3. Controles ligados a las huellas, al texto o al código de su versión (que no den el resultado completo no es una regresión)

**Igual que en el árbol 4.13.** Las líneas de resultado son las mismas que sus salidas de referencia en `…_4_13/resultados/controles_historicos_en_arbol_4_13/`:
- la 4.7, 45 de 49;
- la 4.7.1, 38 de 44;
- la 4.8, 32 de 36;
- las dos comparaciones de baterías del resumen, «HAY DIFERENCIAS».

**Mismo recuento y mismas comprobaciones fallidas que en el árbol 4.13; solo cambia el detalle.** La lista de «archivos de más» que cambian frente a cada entrega es más larga, porque la 4.14 añade y cambia archivos:
- la 4.8.1, 25 de 30;
- la 4.9, 34 de 39;
- la 4.10, 40 de 44;
- la 4.10.1, 38 de 43;
- la 4.11, 34 de 38;
- la 4.12, 59 de 63.

**4.13: 83 de 89, código 1** (89 de 89 en su propio árbol). Las seis comprobaciones que no cumplen están ligadas, por diseño, al árbol 4.13:
1. los archivos de la 4.12 que cambian son exactamente los declarados: la 4.14 cambia otros;
2. los archivos nuevos están en el expediente 4.13: la 4.14 añade el suyo;
3. la ronda final registrada de la V6.4 es 195/195: en la 4.14 la batería tiene 198;
4. la sonda de tipos, que exige que las huellas del código coincidan con las de su registro: el código cambia en la 4.14;
5. el contraejemplo del salto del protocolo, también con huellas al día: por la misma razón;
6. VERSION, CONTINUIDAD.md y PROMPT_NUEVA_VENTANA.md describen la 4.13: ahora describen la 4.14.

**Lo funcional de la 4.13 se comprueba en la 4.14 por otro lado.** Lo cubren las baterías de `verificar_paquete.sh completa`: vigencia, guardas, coherencia de la acción, cobertura y la V6.4.1, dentro de la integración V6.4 (198/198), y la H5 (59/59).
