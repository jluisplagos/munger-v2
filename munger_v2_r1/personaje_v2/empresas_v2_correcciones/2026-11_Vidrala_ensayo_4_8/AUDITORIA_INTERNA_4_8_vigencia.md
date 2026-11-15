# Control de vigencia de la entrega 4.8 · Munger v2, piloto Vidrala

Hecho por el mismo auditor interno de Claude que la auditoría (`AUDITORIA_INTERNA_4_8.md`), el 10-nov-2026. Las convenciones son las mismas:
- **[hecho]**: comprobado con una ejecución o una lectura que se cita;
- **[interpretación]**;
- **[propuesta]**: lo decide la persona responsable.

Nada está comprobado externamente.

## 0. Material y huellas

| Comprobación | Momento | Resultado |
|---|---|---|
| `tail -n +2 MATERIAL_VIGENCIA_4_8.txt \| sha256sum -c --quiet` (39 archivos) | inicio (14:47:22 CET) | **todo OK** |
| la misma | final (15:04:14 CET) | **todo OK**: el material no cambió durante el control |

Todo se ejecutó en una copia `cp -a` del árbol final (`…/scratchpad/auditor/v48`), con `PYTHONDONTWRITEBYTECODE=1`, `python3 -I`/`-B` y las baterías con LibreOffice en secuencia. No se escribió nada en `trabajo48` ni en `base471`. El `AUDITORIA_INTERNA_4_8.md` incluido en el paquete es idéntico byte a byte al que entregó la persona auditora.

## 1. Pruebas ejecutadas

| Prueba | Resultado |
|---|---|
| `test_estados_v2.py` (código final) | **26/26**, mismas líneas que la salida conservada |
| `test_cierre_v2.py` y, después, `test_resumen_v2.py` | **55/55** y **45/45** |
| `test_comprobadores.py` · `test_pipeline_sintetico.py` | 114/114 · 30/30. Pero ver V-a: `test_comprobadores` registra ahora «pipeline --hasta 2 código **1**» donde la salida de referencia dice «código 0» |
| Controles de integración del verificador | 4.6.1 13/13 · 4.7 12/13 (como sobre el árbol 4.7.1) · 4.7.1 13/13 · 4.8 13/13 |
| Control de vigencia de la 4.6.1 | 23/23 |
| `comprobar_entrega_4_7_1.py` sobre el árbol final | 40/44: los cuatro que no cumplen son por diseño (huellas de código cambiado, la salida conservada del resumen, el material del control de vigencia de la 4.7.1 y que VERSION, CONTINUIDAD y PROMPT ya describen la 4.8) |
| `comprobar_entrega_4_8.py` | 35/36. No cumple «salidas pm1_*», y por una razón que no es el manifiesto (V-c) |
| `analisis_pm1.py --salida <temporal>` | código 0; las 7 salidas, idénticas byte a byte a las del paquete; el `financiero/` de la copia, intacto |
| Recomprobación aritmética propia sobre las salidas finales | ponderado, precio de Sí y Δ de 17 alternativas con error ≤ 0,0001; identidad del FCF en 510 filas; V por acción reconstruido con error ≤ 0,004 € (≤ 0,03 € en P2 y P4, por la cola del escudo fiscal) |
| Escenarios N1–N9 y N6b, más **N10–N13 nuevos** (código final) | ver §2 |
| `pipeline.py --desde 3 --hasta 3` con los códigos 4.7.1, 4.8 auditado y 4.8 final | 4.7.1: código 0, «estado final: None · paso 4». **4.8 auditado y final: código 1, `IndexError`** (V-a) |
| Manifiesto de la 4.7.1 frente al árbol real | ver §4 |

## 2. Cada corrección frente a su hallazgo

| Hallazgo | Comprobación | Resultado |
|---|---|---|
| Z-a | N6 y N6b: código 5; con el destino recuperado, la siguiente ejecución publica la fila `pendiente_de_datos` («publicación pendiente del resumen: resumen.py → 0»). N12: con `--desde 2` también. N13: si el destino no se recupera, código 5 estable, sin bucle. Prueba A10 y mutación M6 | **resuelto** |
| Z-b | INFORME §1 y §7, D-N3b, DECISIONES.md y la tabla de mejora del registro: «hipótesis central», «indicios de 1,05 a 1,29», «ninguna es una cota» | **resuelto** |
| Z-c | En P3 MALO, años 9 y 10, la inversión fija es 8,0 y 13,4, el adicional se queda en 19,942 y la inversión bruta sube a 160,9 y 166,3. P3 da 68,85 / 62,87 (V MALO −0,32). Explicación corregida en §5.2 y §5.4 | **resuelto** |
| Z-d | Exceso propio 47,76 = 45,876 + (4,921 + 4,492) ÷ 5. La inversión bruta del año 1 de P5x es 188,503 (el nivel de 2025). P5 62,71 / 55,83 y P5x 57,68 / 51,05, iguales a la variante de la auditoría. El 51 % de doble cómputo se calcula con P5x0 (−10,21) | **resuelto** |
| Z-e | Registrado en el registro §7. Integración 4.6.1 13/13 y vigencia 4.6.1 23/23. El control de la 4.8 ejecuta los tres controles de integración. `LEEME_BATERIAS_HISTORICAS.md` está pendiente, como se anunció | **resuelto**, salvo lo que se genera al final |
| Z-f | N2: `ficha.py --estado pendiente_de_datos`, `modelo_no_aplicable` o `pendiente_de_investigacion` en el paso 14 ya no escribe `cierre` ni `cierre_vigente.json`. N7 (hipotético): ficha sin `cierre` y estado coherente. **Pero** la defensa de `salidas_finales` empeora el caso en que `ficha.py` no llega a escribir la ficha (V-b) | **resuelto en lo pedido; introduce V-b** |
| Z-g | N1: la línea FIN dice «fallo_de_implementacion: ficha.json no cumple su esquema…». N8: el aviso queda en el historial, no en el diagnóstico | resuelto (el segundo punto, solo en el historial; se acepta) |
| Z-h | N4 y N11: con `--desde`, el diagnóstico de un estado final pasa a `diagnostico.json.anterior` y no queda ninguno obsoleto | **resuelto** |
| Z-i | Los cambios están hechos (temporal, archivos añadidos, X41 exacto, integración). Hay un error nuevo en la comprobación de las salidas (V-c) | **resuelto en parte**; ver V-c |
| Z-j | Declarado en el cierre técnico §3 (M2 equivalente; M2b 21/26) | **resuelto** |
| Z-k | Marcas O\*/S\* en el informe; O1 marcada como posterior; `CRITICA_FABLE_PM1.md` transcrita | **resuelto**, en lo que puede resolverse |
| Z-l | P6i al 12 % con fundamento (O6, «around 12% of sales»): 61,33 / 55,53. El orden en que se fijaron las alternativas está declarado | **resuelto** |
| Z-m | Tabla del §6 con cartera y circulante del año 11. Comprobado: REF MALO, año 11, 166,2 − 16,4 − 2,1 = 147,7; P5 NORMAL, año 1, 214,8 − 28,3 − 4,3 + 4,5 − 19,5 = 167,2 | **resuelto** |

**Coherencia numérica [hecho].**
- No queda ninguna cifra anterior a la corrección (63,45; 56,55; 59,52; 52,80; 11,5 %; 64,07; 68,92 en P3; 713,6; 28,1) en INFORME_PM1, `decisiones_y_preguntas_4_8.json`, DECISIONES.md, CONTINUIDAD.md, VERSION, el registro, el cierre técnico ni el PROMPT. La única excepción es `CRITICA_FABLE_PM1.md`, que es la transcripción de la crítica de la primera versión, como corresponde.
- Las cifras nuevas coinciden con `pm1_salida.txt` y `pm1_alternativas.csv` en todos los documentos: 69,73–62,71 / 64,75–55,83; extremos 61,3 y 55,7; P1 68,92 / 63,00; P1b 69,25 / 63,72; P6m 67,36 / 61,80; P6i 61,33 / 55,53; P6x 55,70 / 50,25; P5 terminal 29,9 / 18,2 / 7,6; caja P5 160,6 / 113,8 / 704,2 / 176,2; P4 156,8 / 116,3 / 755,1 / 180,0.
- Los campos humanos de las decisiones siguen vacíos. Las constantes no cambian.

## 3. Hallazgos del control de vigencia

### V-a · **bloqueante** · regresión: `pipeline.py` termina con una excepción (código 1) siempre que acaba sin estado final

- **Evidencia [hecho].**
  - La última línea nueva de `main()` hace `dg = {}` cuando el estado es `None`. Después compara `dg.get("estado_analisis") == p.st.get("estado_analisis")`, que da `None == None`, es decir, verdadero. Entonces ejecuta `''.splitlines()[0]`, que lanza `IndexError`.
  - **Con `--hasta N`** (opción documentada en el uso del guion): `--desde 3 --hasta 3` sobre una copia del expediente da código 0 y «estado final: None · paso 4» con el código 4.7.1, y **código 1 con traza** con el código 4.8, tanto el auditado como el final.
  - El propio paquete lo deja ver: `test_comprobadores.py` (114/114, porque no comprueba ese código) registra ahora «pipeline --hasta 2 código 1», y su salida de referencia (`resultados_reparacion/entrega3_1_continuidad/test_comprobadores.txt`) dice «código 0».
  - La vía nueva de Z-f lleva también aquí (V-b).
- **Interpretación.** El estado se guarda antes de la excepción, así que no hay daño en los archivos. Pero el código de salida pasa a ser el de «fallo mecánico no previsto» en un uso normal y documentado. Esa es justo la clase de defecto (código y mensaje que no describen lo que ocurre) que la 4.8 debía corregir. La persona auditora no lo detectó en la auditoría: estaba en el código auditado y en su propia salida de `test_comprobadores` («código 1»), que no revisó.
- **Propuesta.** Exigir `dg` no vacío (`if dg and dg.get(...) == ...`) y usar `(detalle.splitlines() or [""])[0]`. Añadir a `test_estados_v2.py` una prueba con `--hasta` que observe el código 0 y la última línea, y hacer que `test_comprobadores.py` compruebe el código de `--hasta 2`.

### V-b · importante · la defensa de Z-f convierte un fallo de `ficha.py` en un estado no final, sin causa coherente

- **Evidencia [hecho].** N10: expediente vacío con `alcance_v2.json` ilegible, una sola ejecución.
  1. `ficha.py` termina con 1 sin escribir la ficha.
  2. La validación del esquema falla («no existe»), así que el estado pasa a `no_entregable` y el diagnóstico se escribe.
  3. La defensa nueva («un estado final sin ficha oficial no se conserva») pone `estado_analisis = None`, paso 1.
  4. La última línea cae en V-a: código 1 con traza. Una segunda ejecución repite lo mismo.
  - Al final, `estado_pipeline.json` dice `None` y `diagnostico.json` dice `no_entregable`. Con el código 4.7.1, la misma entrada terminaba con código 0, «estado final: no_entregable · paso 1» y un diagnóstico coherente.
- **Interpretación.** La defensa está pensada para cuando un generador **archiva** la ficha, que era el caso de N7. Pero también se activa cuando `ficha.py` **no llega a escribirla**. En ese caso el estado legítimo es `no_entregable` por fallo de implementación, no «sin estado».
- **Propuesta.** Aplicar la defensa solo si en esa llamada creció `cierres_archivados`, es decir, si hubo un archivo. Si no, conservar `no_entregable` con su diagnóstico. Añadir N10 a la batería.

### V-c · importante · la comprobación «salidas pm1_*» de `comprobar_entrega_4_8.py` no puede cumplirse nunca

- **Evidencia [hecho].** La comprobación exige `len(salidas) == 8`, pero `analisis_pm1.py --salida` escribe **7** archivos: los `pm1_*`. El octavo de `financiero/`, `decisiones_y_preguntas_4_8.json`, no lo genera el guion. La ejecución lo confirma: «NO CUMPLE · … · 7 archivos».
- **Interpretación.** El coordinador atribuye este fallo a que falta el manifiesto. Con el manifiesto regenerado seguiría fallando, y la verificación final sobre una descompresión limpia daría NO CUMPLE.
- **Propuesta.** Exigir los 7 `pm1_*`, o filtrar por `pm1_`. Hay que comprobarlo antes de generar `comprobar_entrega_4_8_salida.txt`.

### V-d · menor · huecos en las pruebas de las correcciones nuevas

- **Evidencia [hecho].** La batería solo añade A10 (Z-a). No cubre:
  - la defensa de `salidas_finales` (Z-f, que es la que produce V-b);
  - la línea FIN de Z-g;
  - el traslado del diagnóstico de Z-h;
  - el uso de `--hasta` (V-a).

  Z-c está comprobado en `comprobar_entrega_4_8.py`. N10 y `--hasta` habrían detectado V-a y V-b.
- **Propuesta.** Incorporar N10, `--hasta` y N11 (Z-h) a `test_estados_v2.py`.

### V-e · menor · restos documentales

- **Evidencia [hecho].**
  - La tabla de mejora del registro (§8, X-a) dice «9 pruebas»: ahora son 10 en el grupo A.
  - VERSION dice «16 alternativas»: `pm1_alternativas.csv` tiene 17 filas, con la medida auxiliar P5x0.
  - En `pm1_salida.txt`, la clase de X41 sigue diciendo «(la parte restante, en P5x)»: ahora es P5x0.
  - P5x se describe como «el nivel de inversión de 2025 en los diez años», pero en los años 6–10 su inversión bruta mostrada es 192,995. Es la convención de D&A constante: no afecta al FCF ni al valor, solo a la columna.
  - VERSION, CONTINUIDAD y el registro (§5b) ya mencionan este control de vigencia.
- **Propuesta.** Ajustar las cuatro primeras cosas al regenerar las salidas finales, y la quinta según el veredicto de este control.

## 4. Conservación de originales y expedientes previos

- [hecho] Comparado con las 1.454 huellas de `base471/MANIFIESTO_SHA256.txt`, en el árbol final solo difieren los archivos declarados: `pipeline.py`, `ficha.py`, `ANEXO_D`, `DECISIONES.md`, `verificar_paquete.sh`, `VERSION`, `CONTINUIDAD.md` y `PROMPT_NUEVA_VENTANA.md`.
- [hecho] No falta ningún archivo. Fuera de la carpeta 4.8 solo hay uno nuevo: `pruebas/test_estados_v2.py`. El manifiesto de la raíz sigue siendo el de la 4.7.1.
- [hecho] Los originales de `empresas_v2/` y los expedientes 4.4–4.7.1 están intactos, y no hay `__pycache__`.
- [hecho] `base471` sigue cumpliendo su manifiesto.

## 5. Veredicto

**Con un bloqueante (V-a).**
- Las correcciones de Z-a a Z-m resuelven sus hallazgos, con las salvedades de Z-f (V-b) y Z-i (V-c).
- Las baterías dan 26/55/45. Los controles de integración, su resultado esperado. P-M1 se reproduce y es coherente en todos los documentos.
- Pero la última línea de `pipeline.py`, introducida en la 4.8, termina con una excepción (código 1) en todo final sin estado final, como `--hasta`, que el propio paquete usa. Además, la defensa de Z-f lleva a ese camino cuando `ficha.py` falla.

La persona auditora recomienda:
1. corregir V-a (una guarda de dos líneas) y V-b;
2. añadir sus pruebas;
3. corregir la comprobación de V-c;
4. volver a ejecutar `test_estados_v2.py`, `test_comprobadores.py` (con «código 0» en `--hasta 2`) y `comprobar_entrega_4_8.py` antes de la verificación final.
