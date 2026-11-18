# Integración F1 · rama `examen/integracion-f1`

Fecha: 18-nov-2026. Integración técnica de tres ramas revisadas del producto, sin cambios de código propios. Este registro **no**
declara completa la migración, **no** inicia el pipeline financiero sobre expedientes reales y **no** otorga aptitud: la 4.15 sigue en
uso supervisado experimental, no apta para decisiones con dinero real. Superar estas baterías no sustituye a la revisión ni a la
conciliación propia del modelo A (F1).

## 1. Base y ramas fusionadas

- Base: `origin/examen/ahold-f1` @ `1c73f22` («zoetis_t1b: pipeline after phase B»), en el worktree nuevo `/home/user/e_work/wt_integracion`.
  La rama `examen/ahold-f1` y sus expedientes no se han tocado.
- Fusiones, en este orden, con commits de fusión (`--no-ff`, sin rebase):

| Orden | Rama · commit | Contenido | Revisión | Commit de fusión |
|---|---|---|---|---|
| 1 | `f1/series-escala` @ `a27788c` | F1-SERIES con escala y ceros (`test_f1_series_escala.py`, 80) | R2: conforme con límites | `9e7f17a` |
| 2 | `f1/usgaap` @ `267f8b0` | F1 con US GAAP (ASC 842), decisiones D-US1, D-US2, D-US2 bis y D-WM | R1 y R2; cierre con las pruebas de aceptación del revisor | `16dd06b` |
| 3 | `f1/perimetro-foso` @ `424a266` | P-FOSO (a) limitado a `A2_propio`; `A1_sin_ROU` pendiente de decisión | revisión con correcciones aplicadas en la ronda 2 | `1059a6c` |

Procedencia de las referencias: `origin/f1/series-escala` estaba en `a27788c`. `origin/f1/usgaap` estaba en `bcb6dc3`; `267f8b0` (el commit
pedido, descendiente de `bcb6dc3`) solo existía en la rama local `f1/usgaap`. `f1/perimetro-foso` no estaba publicada en `origin`; se
fusionó la rama local en `424a266`, el commit pedido. Las tres se fusionaron por su SHA.

## 2. Conflictos y resolución

- Único conflicto en las tres fusiones: `munger_v2_r1/MANIFIESTO_SHA256.txt` (archivo generado), en la 2 y en la 3. La fusión 1 no tuvo
  conflictos (Git combinó el manifiesto como texto). En las fusiones 2 y 3 se tomó provisionalmente la versión del primer padre. Tras
  la última fusión, y antes de su commit, se regeneró a partir de una copia limpia del árbol fusionado (el índice, `git write-tree`):
  `git archive` más los 1059 binarios del manifiesto que no están en Git. Esos binarios son idénticos (ruta y huella) en los manifiestos
  de las tres ramas. Se copiaron de `/home/user/e_work/wt_examen` comprobando su SHA-256 (`scripts/copia_limpia.py`). Después se calcularon
  las huellas de todos los archivos salvo el manifiesto, ordenadas por ruta, con el formato «huella  ruta» (`scripts/generar_manifiesto.py`).
  Resultado: 8885 archivos. El manifiesto de `perimetro-foso` listaba además dos textos de `zoetis_t1` (`Zoetis/ESPERANDO.md` y
  `ESPERANDO_FASE1.md`) que `examen/ahold-f1` borró después de `ab40e80`. No son binarios y no se copiaron.
- Sin conflicto (fusión automática de Git): `motor_a_f1.py` (las tres ramas), `informe.py` (US GAAP y perímetro), `metadatos_fase1.md`,
  `README_V6.3.1_F1.md`, `verificar_paquete.sh`, `CAMBIOS_ARCHIVOS.txt` y `VERSION` (estos dos últimos solo los cambia US GAAP).
  En `verificar_paquete.sh` quedan los bloques de las tres ramas con sus mínimos: US GAAP 290/26/16, gancho 8, V6.3.1 sin LibreOffice 29,
  F1-SERIES 80 y P-FOSO 66.
- Ningún conflicto en código: no se resolvió nada a mano.
- Al añadir este registro y sus resultados, el manifiesto se regeneró de nuevo del mismo modo (commit final).

## 3. Verificación sobre el árbol integrado (`1059a6c`)

Copia limpia de `1059a6c` (`git archive` + los 1059 binarios copiados con su huella) en una carpeta nueva, antes de ejecutar ninguna prueba.

**`flock /home/user/e_work/libreoffice.lock bash verificar_paquete.sh completa`**. Bloqueo obtenido a las 21:29:11 y fin a las 22:49:13
(80 min). Código 0. Salida completa en `resultados/verificacion_completa_1059a6c.txt`. Líneas literales:

```
8885 archivos en el manifiesto · modificados 0 · ausentes 0 · de más 0
RESULTADO manifiesto: PASA
RESULTADO entorno: PASA
35 comprobaciones CUMPLEN · salida idéntica a resultados/contraste_salida.txt
RESULTADO piloto: PASA
114/114 comprobaciones PASAN
30/30 pruebas PASAN                                   (test_pipeline_sintetico.py; LibreOffice)
RESULTADO: PASA
59/59 pruebas de vigencia H5 (4.13.1) PASAN
27/27 pruebas del juicio sobre el objetivo (4.14) PASAN
33/33 pruebas de la verificación de las entradas (4.14) PASAN
190/190 pruebas de la corrección de la verificación de las entradas (4.15) PASAN
62/62 pruebas de la entrada efectiva (4.15) PASAN
5/5 pruebas del relevo caducado (4.15) PASAN
163/163 pruebas del motor A F1 (4.15) PASAN
8/8 pruebas del gancho F1 del pipeline PASAN
290/290 pruebas del motor A F1 con US GAAP PASAN
26/26 pruebas de F1 · US GAAP en el pipeline PASAN
16/16 comprobaciones de F1 · US GAAP sobre el libro V6.3.1 PASAN
29/29 pruebas V6.3.1 F1 (sin LibreOffice) PASAN
21/21 comprobaciones V6.3.1 F1 (estructura) PASAN
22/22 comprobaciones V6.3.1 F1 (a0) PASAN
35/35 comprobaciones V6.3.1 F1 (f1) PASAN
9/9 pruebas de la V6.3.1 F1 en el pipeline PASAN
80/80 pruebas de F1-SERIES con escala y ceros PASAN
199/199 pruebas de integración V6.4 PASAN
66/66 pruebas del perímetro F1 y la vara del foso (P-FOSO) PASAN
78/78 pruebas de trazabilidad de la 4.10 PASAN
103/103 pruebas de integridad de la auditoría vigente PASAN
55/55 pruebas de solicitudes de auditoría PASAN
28/28 pruebas de coherencia de estados PASAN
45/45 pruebas de aceptación del resumen PASAN
55/55 pruebas de aceptación del cierre PASAN
RESULTADO GLOBAL: PASA
```

Cada bloque imprime además su `RESULTADO …: PASA` (todos en PASA, ver el archivo).

**Baterías de las ramas fuera de `completa`**, o repetidas por separado. Se ejecutaron sobre una copia solo de Git de `1059a6c`, sin
LibreOffice y en paralelo con `completa`, en otra carpeta:

| Orden | Resultado literal |
|---|---|
| `cd personaje_v2 && python3 -B pruebas/test_f1_series_escala.py` | `80/80 pruebas de F1-SERIES con escala y ceros PASAN` |
| `cd personaje_v2 && python3 -B pruebas/test_motor_a_f1_usgaap.py` | `290/290 pruebas del motor A F1 con US GAAP PASAN` |
| `cd personaje_v2 && python3 -B pruebas/test_perimetro_foso.py` | `66/66 pruebas del perímetro F1 y la vara del foso (P-FOSO) PASAN` |
| `MUT_TRABAJADORES=2 python3 -I …/f1_usgaap/scripts/mutaciones_usgaap.py <salida>` | `112 de 112 mutaciones detectadas` (871 s; `resultados/mutaciones_usgaap_1059a6c.txt`) |

En esa copia sin binarios, `test_motor_a_f1.py` dio 151/152: falla el caso ELIS, «libro real de Elis disponible (materializar la base
4.14)», y faltan las pruebas que lo necesitan. `test_v631_f1.py` no arranca sin `Plantilla_V6.3.1_F1.xlsx`. Las dos son ausencias de
binarios en esa copia, no fallos del código. Con los binarios, en `completa`, dan 163/163 y 29/29.

**Resumen por lo pedido.** Series-escala 80. US GAAP 290 + 112 mutaciones, pipeline 26 y libro 16. Perímetro 66. F1 NIIF 163. V6.3.1
29/21. Gancho 8. a0 22 y f1 35. Pipeline V6.3.1 9. Pipeline sintético 30. Verificación de entradas 190. Todo en PASA. Hoja: no existe en
este árbol (la rama `examen/hoja-resumen` no forma parte de esta integración), así que no se ejecuta.

**RESULTADO GLOBAL: PASA** (`completa`, código 0).

## 4. Límites

- La integración comprueba que el código fusionado pasa las baterías de las tres ramas y las del paquete. No es una revisión nueva del
  contenido económico. Los límites declarados de cada rama siguen vigentes: los de `F1_USGAAP.md` §9, la decisión pendiente sobre
  `A1_sin_ROU` en P-FOSO y los límites de la revisión R2 de F1-SERIES.
- No se ha regenerado ningún expediente ni se han tocado fuentes ni huellas. Las copias de verificación se borraron al terminar.
- Los binarios de los expedientes del examen (PDF y libros de `2026-11_examen_universo/*`) siguen fuera del manifiesto, como en las tres ramas.
