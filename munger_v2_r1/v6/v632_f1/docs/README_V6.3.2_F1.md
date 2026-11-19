# Plantilla V6.3.2 F1 del motor A · normalización declarada del circulante

Escrita el 19-nov-2026 por el agente autor del cambio (Claude, Opus 5.5) en la rama `f1/circulante-normalizado`, desde `origin/examen/expedientes-f1`
@ `ebf47fc`. **Sin revisión independiente todavía**: la hará otro agente. El registro completo del cambio (decisión, reglas de la capa, pruebas,
diagnóstico de VINCI y cómo aplicarlo) está en
`personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_15/f1_circulante/F1_CIRCULANTE.md`.

**Aptitud: uso supervisado experimental. No apto para decisiones con dinero real.** La V6.3, la V6.3.1 F1 (`eaece01a…`), sus referencias y los
expedientes hechos con ellas **no cambian**.

## 1. Qué es y qué no es

**Hecho.** La V6.3.2 F1 es la V6.3.1 F1 (perímetro F1 de la reinversión, Historia C85:L89) con un solo cambio de modelo: la **normalización
declarada del circulante** de la reinversión, para la decisión V-CIRC (a) de la persona responsable (19-nov-2026, VINCI): si la caja base excluye el
circulante (Análisis C46), tampoco lo llevan la reinversión que calibra f ni la del ancla de S2C: ni entradas ni salidas de circulante.

| Normalización efectiva (Historia C97) | Circulante de la reinversión (fila 96) | Igual que |
|---|---|---|
| `ninguna` (C93 y C94:L94 vacías) | la fila 14 | la V6.3.1 F1 (y, con A0, la V6.3) |
| `circulante_a_cero` (C93 = «circulante_a_cero», C94:L94 = 1 en los años normalizados) | 0 en los años marcados; la fila 14 en los demás | — |
| `no reconocida` (otra regla, una marca distinta de 1, o marcas sin regla) | f, C76 y C53 vacías; Motor V05 DATOS INVÁLIDOS | — |

**Qué no es.** No decide nada: vacío = sin normalización = la V6.3.1 F1. La fila 14 (cifra publicada) y las demás series no cambian. La hoja no
comprueba que la caja base excluya el mismo circulante: lo comprueba la capa (`motor_a_f1.py`, guarda F1-CIRC) con el cálculo declarado de C46 del
expediente (`fase1_v63.json`), reproducido con sus fuentes y atado al libro (corrección C1 de la revisión independiente: una partida de
`conciliacion_fcf_base` sola no lo demuestra). Como la V6.3.1, no calcula `A3_estimado`, N1 ni los términos explícitos.

## 2. Archivos

| Archivo | Qué es |
|---|---|
| `entregables/Plantilla_V6.3.2_F1.xlsx` | La plantilla. SHA-256 `046b64fc7b7898c8a76d924ef72be43c17deb998f2433f43c06c0a18e07800fd` (en `referencia/SHA256_entregables_V6.3.2_F1.txt` y en el manifiesto). **No va en Git** (los `.xlsx` están excluidos): se reconstruye desde la V6.3 de la base con `python3 -I scripts/construir_v632_f1.py ../entregables/Plantilla_V6.3.xlsx entregables/Plantilla_V6.3.2_F1.xlsx` y tiene que dar la misma huella. |
| `referencia/referencia_V6.3.2_F1.json` | Referencia de integridad nueva: 10.996 fórmulas (21 más que la V6.3.1), 5.153 celdas fijas (13 más), 54 validaciones (2 más), 13 partes del paquete (las de la V6.3). |
| `scripts/construir_v632_f1.py` | La construye desde la V6.3, que no se modifica: aplica sin cambios la transformación de la V6.3.1 (`v6/v631_f1/scripts/construir_v631_f1.py`) y después la de la V6.3.2. Determinista. |
| `scripts/verificar_v632.py`, `generar_referencia.py`, `inventario_entradas.py`, `trasladar_entradas.py`, `comparar_libros.py`, `add_sliders.py` | Copias de las de la V6.3.1: `add_sliders.py` idéntico; en `verificar_v632.py` y `generar_referencia.py` cambia solo el docstring; el inventario añade Historia C93, C94:L94 y M93:S94; `comparar_libros.py` excluye la sección nueva (y, para comparar con la V6.3, también la de la V6.3.1). |
| `scripts/probar_v632_f1.py` | Pruebas `estructura` (sin LibreOffice), `a0` y `circ` (con LibreOffice). Resultados en `pruebas/`. |
| `scripts/prueba_pipeline_v632.py` | La V6.3.2 en el pipeline (LibreOffice). |

Selección: `personaje_v2/config_v2_v632_f1.json` (= la de la V6.3.1 salvo la plantilla, la versión y el resumen `resumen_v2_v632_f1.csv`).
Nunca es la de por defecto. `seleccion_plantilla.py`: `V632 = "V6.3.2 F1"`, de la familia V6.3.1 (`es_v631`): el paso 2 le aplica la declaración F1
(`f1_libro_v631.py aplicar`, que con un libro V6.3.2 escribe también C93:L94) y la capa es su oráculo. `plantilla_activa.json` fija sus huellas: un
expediente V6.3.1 no se ejecuta con la V6.3.2 ni al revés (cambiar de plantilla exige un expediente nuevo).

## 3. Cambios de fórmula frente a la V6.3.1 F1

- **Historia, sección nueva (filas 92–98).** C93 regla (lista de validación: «circulante_a_cero»); C94:L94 años normalizados (1 o vacío;
  validación); M93:S94 su procedencia; C95:L95 circulante excluido = `IF(AND($C$97="circulante_a_cero",N(x94)=1),N(x14),0)`; C96:L96 circulante que
  usa la reinversión = `IF(ISNUMBER(x14),x14-x95,"")`; C97 normalización efectiva; A98 nota.
- **Fila 30** (y con ella la 31): `capex − D_X + N(fila 96)`. Sin normalización la fila 96 es la fila 14: el mismo valor.
- **C58 (f), C76 y C53:** `=IF($C$97="ninguna",<fórmula literal de la V6.3.1 F1>,IF($C$97="circulante_a_cero",<rama de D_X de la V6.3.1>,""))`.
  Con la normalización, f exige normalizados todos los años de la ventana (C94 = 1) y el ancla, los cinco años H–L con todo su denominador (filas
  12, 13, 14 y 88: E4) y normalizados los cinco: no se mezclan en una misma media o un mismo cociente la reinversión con circulante y sin él.
- **Motor E205 (V05):** al final, dos causas nuevas: normalización no reconocida (INV) y años de la ventana sin normalizar (INC).
- **Etiquetas de versión:** Panel A1, Análisis A1, Guía V6 A1 y Control maestro A3.

## 4. Pruebas (hechos; resultados literales en `pruebas/`)

| Orden (desde `v6/v632_f1/scripts/`) | Resultado |
|---|---|
| `python3 -I probar_v632_f1.py estructura` | `26/26 comprobaciones V6.3.2 F1 (estructura) PASAN` |
| `flock /home/user/e_work/libreoffice.lock python3 -I probar_v632_f1.py a0 <carpeta nueva fuera del repo>` | `39/39 comprobaciones V6.3.2 F1 (a0) PASAN` |
| `flock … python3 -I probar_v632_f1.py circ <carpeta nueva>` | `17/17 comprobaciones V6.3.2 F1 (circ) PASAN` |
| `flock … python3 -B prueba_pipeline_v632.py ../pruebas/resultado_pipeline_v632.txt` | `9/9 pruebas de la V6.3.2 F1 en el pipeline PASAN` |

- *estructura*: reconstrucción con el mismo SHA-256; la V6.3 y la V6.3.1 sin cambios; la referencia nueva difiere de la de la V6.3.1 exactamente en
  las celdas del §3 (ninguna fórmula o celda fija de la V6.3.1 quitada; formato condicional, nombres y partes del paquete idénticos); con «ninguna»,
  C53, C58 y C76 contienen literalmente la fórmula de la V6.3.1; el verificador nuevo acepta la plantilla y rechaza dos mutaciones (H96 = H14; C97
  fija); el de la V6.3.1 la rechaza.
- *a0*: libro de Elis (`d2593777…`) y los tres ejemplos de la V6.3, con el perímetro vacío y `A0_total` (y, en Elis, `A1_sin_ROU` y `A2_propio` con
  sus series): **0 celdas distintas de 39.950** frente a la V6.3.1 F1 con las mismas entradas, con igualdad exacta (tolerancia 0); con A0, 0 celdas
  distintas frente a la V6.3; C97 «ninguna», fila 95 = 0 y fila 96 = fila 14; los libros con las entradas, ÍNTEGROS.
- *circ*: caso tipo Vinci (las cifras de VINCI de `personaje_v2/pruebas/datos_circulante/vinci_libro_v631.json` sobre las entradas del ejemplo
  Empresa X): con la normalización 2021–2025, libro = capa en f (10⁻¹²: 0,0157439542), el ancla (2,32264514) y los 33 flujos del Motor (6,9·10⁻¹¹);
  F1-LIBRO, F1-REPLICA, F1-CIRC y F1-K3c no saltan; identidades con los valores del propio libro; sin la normalización, 0 celdas distintas frente a
  la V6.3.1 y K3c bloquea; solo la ventana → f sin ancla; sin un año de la ventana → f vacía, V05 INCOMPLETO; regla o marca no reconocidas → V05 DATOS
  INVÁLIDOS; A0 con la normalización; un libro V6.3.1 con la normalización declarada → F1-LIBRO; Elis (su caja base no excluye el circulante) → el
  libro la calcula y la capa bloquea con F1-CIRC. La carpeta lleva el expediente sintético tipo VINCI
  (`personaje_v2/pruebas/datos_circulante/expediente_tipo_vinci.py`: `fase1_v63.json` con el cálculo declarado de C46 y su texto); C9 (corrección C1):
  la sonda del revisor (caja base CON el circulante y dos partidas C46 que se compensan) → el libro calcula f −1,34 % y la capa bloquea con F1-CIRC.
- *pipeline*: Q1 empresa sintética con la caja base sin el circulante (C46 declarado con su cálculo en `fase1_v63.json`) y la normalización declarada →
  `plantilla_activa.json` V6.3.2, el paso 2 escribe C93:L94, F1 utilizable en los pasos 7 y 12, `concluido`, ficha con la versión y el bloque de la
  normalización, línea del informe, nota en `datos_v63.md`, resumen propio; Q2 sin normalización → «ninguna», `concluido`, sin bloque; Q3 la misma
  declaración con la V6.3.1 → paso 7 `no_entregable · límite del modelo` (F1-LIBRO); Q4 (corrección C1) Q1 con C46 sin su cálculo declarado → paso 7
  `pendiente_de_datos` con F1-CIRC INCOMPLETO.

## 5. Límites

- Todo el recálculo es LibreOffice; Excel real, sin probar.
- La normalización es por años completos (todo el circulante de un año); no hay normalización parcial.
- La fila 30 de los años que no se normalizan y no usa la reinversión (antes de H) se enseña con la fila 14 si no se declaran: no entra en f ni en
  el ancla.
- El capital invertido del balance (filas 32–33, C54–C55, y las medidas de P-FOSO) sigue llevando el circulante: la normalización es de los flujos
  de la reinversión, no del capital (ver F1_CIRCULANTE.md §8).
