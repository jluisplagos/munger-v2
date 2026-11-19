# F1 · normalización declarada del circulante de la reinversión (V-CIRC) · 4.15

Fecha: 19-nov-2026. Lo escribe el agente autor del cambio (Claude, Opus 5.5) en la rama `f1/circulante-normalizado`, creada desde
`origin/examen/expedientes-f1` @ `ebf47fc` (worktree `/home/user/e_work/wt_circulante`). **Revisión independiente** (otro agente, `fbb146d`;
`munger-v2-evidencias-mistral`, `coordinacion/cierre_v2/examen/revisiones/circulante_normalizado/REVISION.md`): **CONFORME CON CORRECCIONES**, con
una corrección que impide integrar (C1: F1-CIRC se podía burlar con dos partidas C46 que se compensan). Este documento recoge la corrección C1 en el
§9 y corrige lo que decía de más en los §3.4 y §8.2; queda pendiente de la ronda corta del mismo revisor. Se distinguen **hechos** (comprobados con
una prueba o un archivo), *interpretaciones del autor* y ***propuestas***.

**Aptitud: uso supervisado experimental. No apto para decisiones con dinero real.** Superar estas guardas no acredita aptitud. No se ha tocado ningún
expediente: el diagnóstico de VINCI y el ensayo de `vinci_b` se hicieron sobre copias.

## 1. La decisión y el problema

- **Decisión** (persona responsable, 19-nov-2026; `munger-v2-evidencias-mistral`, `coordinacion/cierre_v2/DECISIONES_PARA_EL_USUARIO.md`:134 y
  `examen/PREGUNTAS_PARA_LA_PERSONA.md`, V-CIRC): **(a)** «circulante a 0 también en la reinversión, con un mecanismo declarado (ni entradas ni salidas
  de circulante)», con cambio de producto, pruebas, revisión independiente y expediente nuevo de VINCI.
- **Problema** (`2026-11_examen_universo/vinci/resultados/diagnostico_k3c_vinci.md`; revisión del montaje, `examen/revisiones/vinci_montaje/REVISION.md`
  §3): la caja base de VINCI excluye el circulante (C46 = CFO − circulante, Control maestro M43) y la reinversión del motor A lo vuelve a contar (fila 30
  = capex − D_X + fila 14). f = (NOPAT − reinversión − C70) ÷ ventas absorbe 2.090 ÷ 71.687 = 2,9 puntos de ventas: la proyección equivale a una salida
  de circulante de ≈ 2.090/año. F1-K3c bloquea (reinversión media −1.514,333 con ventas al alza).

## 2. Qué se implanta (hechos)

**La declaración** (`motor_a_f1.json`, clave nueva `normalizacion_circulante`; vacía = sin declarar):

```json
"normalizacion_circulante": {
  "regla": "circulante_a_cero",
  "anios": [2021, 2022, 2023, 2024, 2025],
  "fundamento": "la decisión de la persona y dónde excluye la caja base el mismo circulante (p. ej. Control maestro M43; conciliacion_fcf_base, C46)",
  "registro": {"fecha": "…", "persona": "…", "motivo": "DECISIONES_PARA_EL_USUARIO.md:134 (V-CIRC)"}
}
```

Una sola regla, `circulante_a_cero`: en los años declarados el circulante no entra en la reinversión (ni entradas ni salidas). La fila 14 sigue siendo la
cifra publicada; el ajuste es −fila 14 y queda a la vista (en el resultado, el informe, la ficha y las filas 93–97 del libro V6.3.2 F1). Solo NIIF.

**En la capa** (`personaje_v2/scripts/motor_a_f1.py`):
- `leer_circulante` (la misma lectura que usa `f1_libro_v631.celdas`): la **forma** (regla, lista de años de la Historia sin repetir, sin claves
  desconocidas) y la norma NIIF deciden si la normalización se aplica; el fundamento, el registro, la cobertura y la coherencia con la caja base los
  examinan las guardas, como con un perímetro declarado.
- `WC_de`: con la normalización aplicable, 0 en los años declarados; en un año que usa la reinversión (la ventana de f y los cinco del ancla H–L) y no
  está declarado, no calculable (vacío ≠ 0: no se mezclan las dos definiciones); la fila 14 en los demás. Se aplica en f, en el ancla de S2C, en los
  flujos (a través de f) y en los diagnósticos por perímetro (A0, A1, A2 y la cota B).
- **F1-CIRC** (BLOQUEA): forma inválida (DATOS INVÁLIDOS) o incompleta (INCOMPLETO); US GAAP (MODELO NO APLICABLE); norma sin declarar; años de la ventana
  o de H–L sin declarar (INCOMPLETO); sin fundamento (INCOMPLETO); **la caja base no demuestra que excluye el circulante**: (i) ninguna partida
  completa de `conciliacion_fcf_base` del componente C46 (C46 − CFO medio, el que contrasta K3a) es la media de la fila 14 de la ventana (±0,0005)
  (DATOS INVÁLIDOS); la partida es una declaración y no basta; (ii) desde la corrección C1 (§9), el **cálculo declarado de C46 del expediente**
  (`fase1_v63.json`, `analisis.C46.calculo`) tiene que demostrarlo: que exista (si falta la carpeta, el archivo o el cálculo, INCOMPLETO), que se
  reproduzca con sus fuentes, que sea la media de la ventana de f con el CFO y la fila 14 sumados una vez, que el libro lo use (C46 y las filas 11 y
  14 de la ventana) y que ningún otro término, ni una combinación, devuelva el circulante (DATOS INVÁLIDOS). F1-REGISTRO si falta el registro.
- K3: el puente lleva la partida «− circulante de la ventana que la normalización declarada excluye» (clase `normalizacion_declarada`) y cuadra a 10⁻⁹.
- K3c mide la reinversión que calibra f, ya normalizada (la regla no cambia).
- Réplica (F1-REPLICA): con un libro V6.3 o V6.3.1 la del libro (fila 14 tal cual); con uno V6.3.2, la de su normalización efectiva (filas 93–97, no la
  declarada) y `replica_circulante` contrasta sus filas 95–97 con sus entradas.
- F1-LIBRO: con un libro V6.3 o V6.3.1 y la normalización con efecto, **límite declarado** (ninguno la calcula; la salida es la V6.3.2 F1 en un
  expediente nuevo). Con un libro V6.3.2, el oráculo (`f1_libro_v631.corresponde`) exige la misma normalización efectiva y los mismos años.
- El resultado lleva `normalizacion_circulante` (declarada, aplicada, años, excluido por año, partida de la caja base, `calculo_C46` con lo que lo
  demuestra y, para la revisión de entradas, cada componente de C46 con su fuente, su página y su cita; efecto sin normalizar → normalizado en f,
  reinversión, flujo sin crecimiento y ancla; libro), el informe una sección y la ficha el mismo bloque. **Sin la declaración no se añade nada** (ni la
  clave, ni la guarda, ni la partida de K3).

**En el libro** (plantilla nueva **V6.3.2 F1**, `v6/v632_f1/`; `docs/README_V6.3.2_F1.md`): la V6.3.1 F1 con la sección Historia filas 92–98 (C93 regla,
C94:L94 años, C95:L95 excluido, C96:L96 circulante de la reinversión, C97 efectiva); fila 30 = capex − D_X + fila 96; C58, C76 y C53 con «ninguna»
literalmente las de la V6.3.1. Selección `config_v2_v632_f1.json`; `seleccion_plantilla.V632`, de la familia V6.3.1 (el paso 2 le aplica la
declaración: `f1_libro_v631.aplicar` escribe C93:L94 si el libro es V6.3.2); resumen propio `resumen_v2_v632_f1.csv` (`cierre_v2`); la ficha
(`ficha.esquema.json`, `ficha.py`) y el informe (`informe.py`) dicen la normalización solo si existe; `datos_v63.md` (`volcar_datos_v63.py`) da a las
fases una nota con los años y lo excluido, solo con la normalización efectiva; la huella de entradas (`entradas_economicas.instantanea`) incluye C93 y
C94:L94 como configuración en los libros V6.3.2 (y con ello el universo de `verificacion_entradas.py`).

## 3. Decisiones de diseño (interpretaciones del autor, con su razón)

1. **El ajuste entra en el ancla de S2C, en los cinco años H–L** (VINCI: 5,960 → 2,323). Razones: (i) «ni entradas ni salidas de circulante»: un ancla
   que cuenta las entradas de circulante como reinversión negativa (5,96) las mete en el crecimiento a través de la palanca S2C, que las fases fijan con
   el ancla a la vista (Palancas F16 = Historia C53; referencias mecánicas); (ii) F1 (4a): un solo perímetro de la reinversión para f, el ancla y el ROIC
   (V-F1g); (iii) precedente D-US2: el ajuste del circulante de US GAAP se aplica «en f y en el ancla de S2C» y exige sus importes en la ventana y en
   H–L; (iv) un ancla con el circulante en unos años y sin él en otros (2,720, la opción «solo 2023–2025» del diagnóstico) mezcla dos definiciones en un
   mismo cociente: se rechaza (la cobertura de H–L es obligatoria; sin ella el ancla no se calcula y F1-CIRC bloquea). Era la consecuencia más
   material para las fases (más reinversión por euro de crecimiento) y una interpretación del autor. **La persona la confirmó después** (V-ANCLA (a),
   «7a», 19-nov-2026, `DECISIONES_PARA_EL_USUARIO.md`:135: el ancla de VINCI se calcula sin el circulante, ≈ 2,32 en lugar de 5,96; límite declarado: el
   capital del balance sigue incluyendo el circulante negativo, §8.1).
2. **La cobertura es obligatoria** en todos los años que usa la reinversión (ventana ∪ H–L). Años de más se admiten y no cambian nada.
3. **K3c no se debilita:** mide la reinversión que calibra f, ya normalizada; con capex − D_X negativo y ventas al alza sigue bloqueando (prueba «K3 ·
   K3c no se debilita»).
4. **K3a no cambia**; la coherencia con la caja base es una comprobación nueva de F1-CIRC. Sin ella, la normalización podría servir para silenciar K3c
   en una empresa cuya caja base **sí** cuenta el circulante (opción (b) del diagnóstico): contaría el circulante una vez, dentro de C70, como caja
   permanente. La prueba «G · caja base CON el circulante» lo muestra cuando la declaración no trae la partida: K3c dejaría de saltar y F1-CIRC bloquea.
   **Corregido (revisión C1):** la versión revisada decía aquí que K3a garantizaba que la partida C46 explica de verdad la diferencia entre C46 y el
   CFO. No es así: K3a solo comprueba que **la suma** de las partidas C46 la explica, y nada contrasta sus fuentes; otra partida C46 puede compensarla
   (−2.090 y +2.090) y la guarda la daba por buena. La partida es una declaración. Desde la corrección C1, F1-CIRC exige además la demostración con
   datos contrastados: el cálculo declarado de C46 del expediente (§9).
5. **Solo NIIF.** Con US GAAP la fila 14 puede llevar tramos del arrendamiento operativo (D-US2, D-US2 bis); la combinación no está decidida: MODELO NO
   APLICABLE, no se aplica.
6. **La forma decide el cálculo; las demás condiciones son guardas** (como un perímetro declarado sin registro: se calcula y se bloquea). Así el libro
   (que `aplicar` escribe con la misma lectura) y la capa coinciden también cuando bloquean.
7. **Plantilla nueva y no un cambio de la V6.3.1:** la V6.3.1 F1 (`eaece01a…`) está fijada por `plantilla_activa.json` en los expedientes en curso
   (ahold_f3, jumbo_g, zoetis_t1c, vinci/Vinci); cambiarla los rompería. Precedente: V6.4 → V6.4.1.
8. **Propiedad, no elección:** excluir el circulante de la caja base **y** de la reinversión da la misma f que contarlo en las dos (por eso (a) y (b) del
   diagnóstico dan la misma f y el mismo flujo sin crecimiento; lo comprueba Q1/Q2 de la prueba del pipeline). Lo que cambia con (a) es la caja base que
   se enseña (C52 = 4.419) y el ancla.

## 4. Regla → código → prueba

| Regla | Código | Pruebas |
|---|---|---|
| lectura y forma | `motor_a_f1.leer_circulante`, `CLAVES_CIRCULANTE`, `_declaracion_bien_formada` | G (forma, 8 casos; vacío; no-objeto) · c13–c15 |
| circulante de la reinversión | `WC_de`, `_wc_normalizado`, `calcular` | VINCI, G (ventana, H–L), K3 · c01–c04 |
| F1-CIRC | `_guarda_circulante` | G (cobertura, fundamento, registro, caja base ×4, US GAAP, norma) · c07–c11, c16, c17 |
| F1-CIRC: la exclusión del circulante en C46, demostrada (corrección C1, §9) | `_c46_sin_circulante` (con `fase1_historia.calcular_entrada`), `_md_calculo_c46`; `ficha`, `informe` | CAJA (20), VINCI (cálculo de C46), MD; `probar_v632_f1.py circ` C9; `prueba_pipeline_v632.py` Q4 · c34–c51 |
| K3 y K3c | `calcular` (partida), K3c | K3 (5) · c05, c06 |
| réplica y oráculo | `_replica_v631`, `f1_libro_v631.normalizacion_del_libro`, `replica_circulante`, `corresponde`, `_f_vacia_v631` | LIBRO (15) · c18–c25, c28, c29 |
| libro | `f1_libro_v631.celdas(…, circulante=True)`, `aplicar`, `es_v632`; plantilla V6.3.2 | APLICAR (8), `probar_v632_f1.py` · c26, c27 |
| huella, selección, resumen, volcado | `entradas_economicas`, `seleccion_plantilla`, `cierre_v2`, `volcar_datos_v63`, `ficha`, `informe` | EE, SEL, DATOS, MD, `prueba_pipeline_v632.py` · c30–c33 |

## 5. Pruebas ejecutadas (hechos; resultados literales en `resultados/` y en `v6/v632_f1/pruebas/`)

Esta tabla es la de la **primera ronda** (código `eededd1`, el que revisó el revisor en `fbb146d`). Las de la corrección C1, con el código nuevo, están en
el §9.3; los archivos de `resultados/` y de `v6/v632_f1/pruebas/` que se repitieron llevan ya las cifras nuevas.

| Orden | Resultado |
|---|---|
| `cd personaje_v2 && python3 -B pruebas/test_circulante_f1.py` (grupos VINCI 13, G 25, K3 5, LIBRO 15, APLICAR 8, EE 2, SEL 6, DATOS 1, MD 2) | `77/77 pruebas de la normalización del circulante (V-CIRC) PASAN` |
| la misma batería contra el código anterior (`scripts/antes_y_despues.py ebf47fc`) | `pasan 8 de 77` (los ocho controles, marcados «(control)»: estado actual sin la declaración, la V6.3.1 sin cambios…); 77 de 77 con el actual (`resultados/antes_y_despues.txt`) |
| `python3 -I scripts/mutaciones_circulante.py` (33 líneas del producto cambiadas a propósito; baterías `test_circulante_f1`, `test_motor_a_f1`, `test_v631_f1`) | `33 de 33 mutaciones detectadas` (`resultados/mutaciones_circulante.txt`) |
| baterías sin LibreOffice que no pueden cambiar | motor A F1 `177/177`; US GAAP `294/294`; P-FOSO `72/72`; F1-SERIES `80/80`; redondeo `44/44`; V6.3.1 `29/29` |
| `probar_v632_f1.py estructura` · `a0` · `circ` (LibreOffice, con `flock`) | `26/26` · `39/39` · `16/16` |
| `prueba_pipeline_v632.py` (LibreOffice) | `8/8 pruebas de la V6.3.2 F1 en el pipeline PASAN` |
| regresión con la capa nueva (LibreOffice, en secuencia con `flock`) | `probar_v631_f1.py f1` `35/35`; `prueba_pipeline_v631.py` `9/9`; gancho F1 `prueba_pipeline_f1.py` `8/8`; `probar_libro_v631_usgaap.py` `18/18` (`resultados/regresion_v631/`; el registro de la V6.3.1 que reescribe `probar_v631_f1.py` se devolvió a su versión) |
| otras baterías sin LibreOffice de los módulos tocados | entradas dependientes `51/51`, acciones exactas `30/30`, verificación de entradas 4.15 `190/190` y 4.14 `33/33`, entrada efectiva `62/62`, vigencia H5 `59/59`, juicio sobre el objetivo `27/27` (`resultados/baterias_sin_libreoffice.txt`) |
| efecto nulo en los expedientes en curso (`scripts/comprobar_efecto_nulo.py`) | ahold_f3, jumbo_g, zoetis_t1c y vinci/Vinci: **idénticos** con el código anterior (`ebf47fc`) y con el actual (evaluación F1 completa salvo versión y fecha, informe .md, celdas que `aplicar` escribe en el libro V6.3.1, huella de entradas del libro evaluado y del de datos, vigencia F1; `resultados/efecto_nulo_expedientes.json`) |
| `flock … bash verificar_paquete.sh rapida` sobre una copia limpia de `f4b44e8` (`git archive` más los 1.060 binarios del manifiesto, copiados con su huella; 2 min) | manifiesto `9859 archivos · modificados 6 · ausentes 0 · de más 14`: son exactamente los 20 archivos de jumbo_g que `ebf47fc` añadió o cambió sin regenerar el manifiesto y que este cambio no acepta (ninguno de este cambio) → `RESULTADO manifiesto: FALLA`; los demás bloques PASAN: entorno, piloto, comprobadores `114/114`, normalización del circulante `77/77`, F1-SERIES `80/80`, redondeo `44/44`, acciones `30/30`, P-FOSO `72/72`, entradas dependientes `51/51`; `RESULTADO GLOBAL: FALLA (1 bloques)`, solo por el manifiesto de jumbo_g (`resultados/verificacion_rapida_f4b44e8.txt`). Después de `f4b44e8` solo cambian este documento, ese registro y el manifiesto |

Una mutación de la primera campaña (c29 antigua: la marca de un año admite cualquier número en `normalizacion_del_libro`) era **equivalente**: con la
normalización efectiva todas las marcas son 1, así que no cambia nada observable; se sustituyó por la mutación de la réplica (c29 actual). La c11
(coherencia con cualquier componente) no la detectaba ninguna prueba: se añadió «G · la partida del circulante declarada en otro componente».

## 6. Diagnóstico de VINCI sobre una copia (hechos; `resultados/diagnostico_vinci_circulante.{json,md}`)

Copia de `2026-11_examen_universo/vinci/Vinci` (sin `pdf/`), con la declaración del expediente más la normalización 2021–2025 escrita solo en la copia.
Antes de la fase A (sin palancas): es la previsión, no el paso 7. **Repetido con el código de la corrección C1** (§9): las mismas cifras; F1-CIRC
conforme porque lo demuestra el cálculo declarado de C46 de la copia (`fase1_v63.json`: media 2023–2025 de cfo + circulante + dividendos de
sociedades no consolidadas, con sus fuentes contrastadas en `texto/`; 9.327,333 = Análisis C46 del libro).

| | f | reinversión media | flujo sin crecimiento | ancla S2C | bloquean |
|---|---|---|---|---|---|
| libro V6.3.1 del expediente, sin la declaración (estado actual) | 4,4899 % | −1.514,333 | 3.016,069 | 5,9595 | F1-K3c |
| libro V6.3.1 del expediente, con la declaración | 1,5744 % | +575,667 | 5.190,977 | 2,3226 | F1-LIBRO (límite declarado: la V6.3.1 no normaliza) |
| libro V6.3.2 F1 (las entradas del expediente, la declaración aplicada como en el paso 2, LibreOffice) | 1,5744 % | +575,667 | 5.190,977 | 2,3226 | — |

Libro V6.3.2 recalculado: C58 = 0,0157439542453269, C53 = 2,3226451421801 (Palancas F16, el ancla que ven las fases), C76 = 575,667, C97
«circulante_a_cero», Motor V05 OK, ÍNTEGRO frente a su referencia; libro − capa: f −1·10⁻¹⁶, ancla 1·10⁻¹³. F1-CIRC conforme (la partida C46 −2.090 =
media de la fila 14 de 2023–2025); F1-K3c no salta (575,667 ≥ 0). Avisos que siguen: F1-SERIES-CERO (PPA de 2021 = 0, pendiente de revisor) y V-F1f
(efectos de escala). En el puente K3: FCF base 4.419,333 + nivel del EBIT 424,636 − τ 182,807 − f × Δventas 45,852 + reinversión neta propia y
circulante −1.514,333 + circulante excluido 2.090,000 = 5.190,977. Diagnóstico por perímetro con la normalización: A0 4.333,2 · A1 5.095,9 · A2
5.191,0 · cota B 4.591,9.

## 7. Cómo aplicarlo a VINCI (no hecho: lo hace la orquestación, con la decisión ya registrada)

`vinci/Vinci` se preparó con la V6.3.1 F1 (`plantilla_activa.json`, `eaece01a…`) y está en el paso 6 (esperando la fase A): no puede pasar a la
V6.3.2 y no se toca (queda como antecedente; allí F1-K3c sigue bloqueando). Hace falta un **expediente nuevo `vinci_b`** con `cambiar_base.py`.
Ensayado entero sobre una copia del árbol en `/dev/shm` (resultado en el §7 bis):

1. `configuracion/cambio_vinci_b.json` = `cambio_vinci.json` con: `origen` `…/2026-11_examen_universo/vinci/Vinci` (lleva ya las correcciones de la
   revisión del montaje); `destino` `…/2026-11_examen_universo/vinci_b`; `conservar` + `"extracto_v63.md"` y `"motor_a_f1.json"` (como jumbo_g: no se
   repite la extracción del paso 5); `analisis` `{}` y `analisis_que_se_conservan` con C46, C47, C48, C49, C50, C42, C96 y C40 («entrada de vinci/Vinci
   sin cambio…»); el aviso de `alcance` con la V6.3.2 F1 y V-CIRC; lo demás igual (fechas, base, `entrada_efectiva` estricta, `textos_prohibidos`,
   `control_maestro_textos`).
2. Desde `munger_v2_r1/`: `python3 personaje_v2/scripts/cambiar_base.py preparar personaje_v2/empresas_v2_correcciones/2026-11_examen_universo/configuracion/cambio_vinci_b.json`.
3. En `vinci_b/Vinci/motor_a_f1.json` (la copia conservada) añadir **solo** el bloque `normalizacion_circulante` del §2, con `anios` 2021–2025, el
   fundamento (decisiones V-CIRC (a) y V-ANCLA (a), M43, el cálculo declarado de C46 y la partida C46 −2.090) y el registro de la decisión
   (`DECISIONES_PARA_EL_USUARIO.md:134`; propuesta en `resultados/ensayo_vinci_b/normalizacion_circulante_vinci_b.json`). Nada más cambia (en
   particular, no se declara `justificacion_reinversion_negativa`). Para F1-CIRC (corrección C1, §9) no hay que añadir nada: `cambiar_base.py`
   reconstruye `vinci_b/Vinci/fase1_v63.json` con `fase1_historia.py construir` desde las entradas conservadas, y C46 conserva su cálculo declarado
   (media 2023–2025 de cfo + circulante + dividendos de sociedades no consolidadas, con sus fuentes en `texto/`): es lo que demuestra que la caja base
   excluye el circulante. Si C46 llegara sin su cálculo, F1-CIRC bloquearía con INCOMPLETO en el paso 7.
4. Desde `munger_v2_r1/`, con LibreOffice en secuencia: `flock /home/user/e_work/libreoffice.lock python3 personaje_v2/scripts/pipeline.py
   personaje_v2/empresas_v2_correcciones/2026-11_examen_universo/vinci_b/Vinci --config personaje_v2/config_v2_v632_f1.json`. La primera ejecución
   registra `plantilla_activa.json` V6.3.2 F1; el paso 2 escribe en el libro el perímetro A2, las series y C93:L94; los pasos 3–5 recalculan,
   verifican y toman el `extracto_v63.md` conservado; el pipeline se detiene en el **paso 6** esperando `fase_a.json`.
5. Antes de la fase A, la previsión F1 sobre el libro de datos recalculado tiene que dar lo del §6 (V6.3.2): nada bloquea, f 1,5744 %, flujo sin
   crecimiento 5.190,98, ancla 2,3226.
6. **Fases pendientes (ninguna hecha en VINCI):** fase A (paso 6) → paso 7 (gancho F1: utilizable si nada más cambia); fase B (paso 8) → paso 9
   (recálculo de las entradas dependientes, si se declaran); fase C en dos turnos (paso 10) → paso 11 (material provisional) → paso 12 (recálculo,
   verificador y F1 con las palancas: 33 flujos contrastados con la capa) → paso 13 (solicitud de auditoría; auditor independiente) → paso 14 (cierre).
   Y lo del programa del examen: verificación de entradas (`verificacion_entradas.json`: ahora también Historia C93 y C94:L94, como hipótesis con el
   fundamento V-CIRC, y C94:L94 de 2016–2020 vacías con su justificación), contradictor y veredicto de la persona.
7. Lo que las fases verán distinto: el ancla de S2C pasa de 5,96 a 2,32 (Palancas F16 y referencias mecánicas del S2C), f de 4,49 % a 1,57 % y la
   reinversión neta orgánica de la Historia (filas 30–31) sin el circulante en 2021–2025; `datos_v63.md` lo explica con una nota.

### 7 bis. Ensayo de la receta sobre una copia

**Hecho** (`resultados/ensayo_vinci_b/`: la receta `cambio_vinci_b.propuesta.json`, el bloque `normalizacion_circulante_vinci_b.json`, el estado y la previsión). Sobre una copia del árbol en `/dev/shm` (con `vinci/Vinci` copiado de `wt_expedientes`; borrada después): `cambiar_base.py preparar` con la receta crea `vinci_b/Vinci` (20 archivos heredados a antecedentes; las 8 entradas `analisis` reconocidas como conservadas; entrada efectiva estricta); con el bloque añadido a la declaración conservada, `pipeline.py --config config_v2_v632_f1.json` registra `plantilla_activa.json` V6.3.2 F1 (`046b64fc…`), migra a la V6.3.2 (ÍNTEGRO), rellena la fase 1 en modo estricto (ÍNTEGRO), aplica la declaración (C85 = A2_propio, las series y C93:L94 con 2021–2025), pasa `comprobar_entrada_v63.py` (0 bloqueantes) y `volcar_datos_v63.py` (la nota de la normalización en `datos_v63.md`) y se detiene en el **paso 6** esperando `fase_a.json`. La previsión F1 sobre el libro de datos recalculado: **nada bloquea**, f = 1,5744 %, flujo sin crecimiento 5.190,98, ancla 2,3226, reinversión media +575,667; avisos V-F1f y F1-SERIES-CERO (la PPA de 2021, pendiente de revisor), como en `vinci/Vinci`.

**Repetido con el código de la corrección C1** (§9; `resultados/ensayo_vinci_b/ensayo_vinci_b.json`, con el bloque propuesto que ya cita V-ANCLA (a) y el cálculo de C46): `cambiar_base.py` reconstruye `vinci_b/Vinci/fase1_v63.json` con C46 = 9.327,333 **y su cálculo declarado** (media 2023–2025 de cfo + circulante + dividendos de sociedades no consolidadas); el pipeline llega al paso 6 igual; la previsión F1: nada bloquea, las mismas cifras, y F1-CIRC conforme porque lo demuestra ese cálculo (reproducido con sus fuentes en `texto/` de la copia y = C46 del libro).

## 8. Límites y preguntas para el revisor

1. **El capital invertido del balance sigue llevando el circulante** (negativo en VINCI): filas 32–33, C54–C55 (ROIC y S2C medios de todo el capital) y
   las medidas de P-FOSO. La normalización es de los flujos de la reinversión. El ROIC terminal (palanca de las fases) puede quedar alto si se ancla en
   un capital con circulante negativo; si la persona quiere el mismo criterio ahí, es otra decisión.
2. **Corregido (revisión C1).** La partida C46 de la caja base se reconoce por su componente y su importe (no por el rótulo), pero es una declaración:
   K3a solo comprueba que la **suma** de las partidas C46 explica C46 − CFO, y otra partida puede compensarla. La versión revisada decía que K3a
   garantizaba que la partida explica de verdad C46 − CFO; no lo garantiza. Lo que demuestra ahora la exclusión es el cálculo declarado de C46 del
   expediente, con sus fuentes y atado al libro (§9). Lo que sigue sin comprobarse por software está en el §9.4.
3. Normalización por años completos; no hay normalización parcial (una parte del circulante).
4. Con US GAAP no está definida (MODELO NO APLICABLE).
5. La V6.3.2 hereda los límites de la V6.3.1 (A3, N1 y términos explícitos fuera del libro; Excel real sin probar; el oráculo contrasta valores en caché).
6. Los encargos de las fases (`prompts/`) no se han cambiado: la nota de `datos_v63.md` es lo que les dice la normalización.
7. La decisión del ancla (§3.1) era del autor del cambio; la persona la confirmó (V-ANCLA (a), 19-nov-2026, `DECISIONES_PARA_EL_USUARIO.md`:135).

## 9. Corrección C1 de la revisión independiente (19-nov-2026)

### 9.1 Lo que encontró el revisor (hecho, reproducido)

`REVISION.md` §2: F1-CIRC solo buscaba una partida C46 de `conciliacion_fcf_base` cuyo importe fuera la media de la fila 14 de la ventana. K3a suma las
partidas por componente y nada contrasta sus fuentes. Con dos partidas C46 que se compensan («circulante excluido» −2.090 y «compensación» +2.090, las
dos con el documento «x», página 1), una empresa cuya caja base **sí** cuenta el circulante pasaba la normalización: K3a cuadraba, F1-CIRC daba por
buena la partida de −2.090 y K3c no saltaba. Con un libro V6.3.2, nada bloqueaba: f −1,3411 % y flujo sin crecimiento 7.365,885, un 42 % por encima del
caso genuino. Reproducido con el código revisado: la prueba nueva «CAJA · (C1) la misma sonda con un libro V6.3.2» da con `fbb146d` nada bloquea,
f −0,013410700269692 y flujo 7.365,884749419.

### 9.2 Qué cambia (hechos)

**(a) Los textos que decían de más**, ahora dicen lo que se comprueba:
- §3.4 y §8.2 de este documento (K3a solo garantiza la **suma** de las partidas C46; la partida es una declaración);
- la docstring de `_guarda_circulante`, punto (v) (`motor_a_f1.py`);
- el nombre de la prueba G «la misma con la normalización declarada y sin partida C46 del circulante» (`test_circulante_f1.py`; ya no dice que la
  normalización no sirva para ocultar entradas de circulante: eso lo prueban ahora las del grupo CAJA);
- y, en el mismo sentido: el mensaje de F1-CIRC cuando falta la partida («la conciliación de la caja base no declara que excluye el circulante», antes
  «la caja base no excluye»), la línea del puente K3 («la caja base tiene que excluirlo también: F1-CIRC», antes «la caja base ya lo excluye»), la
  docstring del módulo, la línea del informe (dice si lo demuestra el cálculo de C46), el §12 de `F1_IMPL.md` y el README de la V6.3.2.

**(b) La prueba de las partidas que se compensan:** grupo CAJA de `test_circulante_f1.py` (20 pruebas; la sonda del revisor con un libro V6.3.1 y con
uno V6.3.2) y C9 de `probar_v632_f1.py circ` (la misma sonda en un libro V6.3.2 recalculado por LibreOffice: el libro calcula f −1,34 % y la capa bloquea).

**(c) La guarda, endurecida** (`motor_a_f1._c46_sin_circulante`, desde `_guarda_circulante` cuando la normalización se aplica y la fila 14 de la
ventana no suma cero). La partida C46 se sigue exigiendo (no se debilita nada), pero ya no basta: la exclusión del circulante tiene que estar
**demostrada por el cálculo declarado de C46 del expediente** (`fase1_v63.json`, `analisis.C46.calculo`, la derivación registrada que
`fase1_historia.py construir` reproduce y `cambiar_base.py` conserva):
1. la carpeta del expediente, su `fase1_v63.json` y C46 con su cálculo; si falta cualquiera, **INCOMPLETO** («no se puede demostrar»: una partida
   de la conciliación no lo sustituye);
2. el cálculo se reproduce con sus fuentes: `fase1_historia.calcular_entrada` **con la carpeta**, el mismo contraste documental que las entradas
   (cada componente con su texto conservado en el expediente, la página PDF citada, la cita en ella y la cifra publicada con su signo; el valor
   declarado = el calculado). Un documento inexistente, una página que no existe o una cita que no está → **DATOS INVÁLIDOS**;
3. es la **media** de los años de la **ventana de f** y suma una vez el CFO y una vez la fila 14 (circulante): C46 = CFO + fila 14 + otros términos.
   Sin la fila 14, restándola o sumándola dos veces → DATOS INVÁLIDOS;
4. describe **este libro**: Análisis C46 = el cálculo, redondeado a los decimales con que el libro lo escribe (9.327,33 vale para 9.327,333…;
   9.327,34 no), y las filas 11 y 14 del libro en la ventana = la Historia con que se calcula → si no, DATOS INVÁLIDOS;
5. ningún otro término del cálculo, **ni una combinación de ellos**, devuelve en media el circulante que suma la fila 14 (±0,0005): ni la línea del
   circulante del estado de flujos, ni sus partes, ni una cifra cualquiera que lo iguale, aunque tengan fuente verdadera → DATOS INVÁLIDOS.

El resultado (`normalizacion_circulante.calculo_C46`), el informe de la capa y la ficha enseñan el cálculo y, **para la revisión de entradas**, cada
componente de C46 con su fuente, su página y su cita. *Por qué el cálculo y no las partidas* (interpretación del autor): «cualquier regla que mire solo
las partidas declaradas se cumple declarando partidas» (revisor). El cálculo de C46 es un dato contrastado con el texto del expediente, y F1-CIRC lo
vuelve a contrastar cada vez (no se fía de que se hiciera antes) y lo ata al libro. La primera vía del revisor (contrastar las fuentes de
`conciliacion_fcf_base`) no se ha hecho: en VINCI son texto libre (varios documentos y páginas en un campo, «URD2024 PDF 336; URD2025 PDF 358»),
necesitaría otro formato de la declaración en los expedientes, que no se tocan, y cerraría un hueco de K3a anterior a V-CIRC y común a todos los
componentes: es otro cambio.

### 9.3 Pruebas ejecutadas con el código nuevo (hechos; resultados literales en `resultados/` y en `v6/v632_f1/pruebas/`)

| Orden | Resultado |
|---|---|
| `python3 -B pruebas/test_circulante_f1.py` (VINCI 14, G 25, CAJA 20, K3 5, LIBRO 15, APLICAR 8, EE 2, SEL 6, DATOS 1, MD 2) | `98/98 pruebas de la normalización del circulante (V-CIRC) PASAN` |
| la misma batería con el código revisado (`scripts/antes_y_despues.py fbb146d --lista`) | `pasan 75 de 98`: no pasan las 19 nuevas del grupo CAJA que no son control, las dos de VINCI y la de MD que piden el cálculo de C46, y la de G cuyo mensaje se corrigió (`resultados/antes_y_despues_C1.txt`) |
| la misma batería con el código de partida de la rama (`antes_y_despues.py ebf47fc`) | `pasan 9 de 98` (los controles; `resultados/antes_y_despues.txt`) |
| `python3 -I scripts/mutaciones_circulante.py` (51 mutaciones: las 33 de antes y c34–c51 de la corrección C1) | `51 de 51 mutaciones detectadas` (`resultados/mutaciones_circulante.txt`) |
| baterías sin LibreOffice | motor A F1 `177/177`; US GAAP `294/294`; P-FOSO `72/72`; F1-SERIES `80/80`; redondeo `44/44`; V6.3.1 `29/29`; entradas dependientes `51/51`; acciones exactas `30/30` |
| `probar_v632_f1.py estructura` · `circ` (LibreOffice, con `flock`) | `26/26` · `17/17` (C1: el expediente sintético tipo VINCI, `pruebas/datos_circulante/expediente_tipo_vinci.py`; C9: la sonda del revisor) |
| `prueba_pipeline_v632.py` (LibreOffice) | `9/9` (Q1 con C46 declarado con su cálculo llega a `concluido`; Q4 sin el cálculo: paso 7 `pendiente_de_datos` con F1-CIRC INCOMPLETO) |
| gancho F1 del pipeline sin la normalización (`f1_impl/scripts/prueba_pipeline_f1.py`, LibreOffice) | `8/8 pruebas del gancho F1 del pipeline PASAN` (`resultados/regresion_v631/prueba_pipeline_f1_gancho_C1.txt`) |
| efecto nulo (`scripts/comprobar_efecto_nulo.py`, código `ebf47fc` frente al nuevo) | ahold_f3, jumbo_g, zoetis_t1c y vinci/Vinci **idénticos** salvo versión y fecha (`resultados/efecto_nulo_expedientes.json`) |
| diagnóstico de VINCI sobre una copia (§6) | las mismas cifras; F1-CIRC conforme con el cálculo de C46 (`resultados/diagnostico_vinci_circulante.{json,md}`) |
| ensayo de la receta de `vinci_b` sobre una copia del árbol (§7 bis) | paso 6; C46 con su cálculo en `fase1_v63.json`; previsión F1: nada bloquea, F1-CIRC conforme (`resultados/ensayo_vinci_b/`) |
| `flock … bash verificar_paquete.sh rapida` sobre una copia limpia de `3b971c4` (`git archive` más los 1.060 binarios del manifiesto, copiados con su huella; en `/dev/shm`, borrada después) | manifiesto `9863 archivos · modificados 6 · ausentes 0 · de más 14`: son exactamente los 20 archivos de jumbo_g de `ebf47fc` que este cambio no acepta → `RESULTADO manifiesto: FALLA`; los demás bloques PASAN: entorno, piloto, comprobadores `114/114`, normalización del circulante `98/98`, F1-SERIES `80/80`, redondeo `44/44`, acciones `30/30`, P-FOSO `72/72`, entradas dependientes `51/51`; `RESULTADO GLOBAL: FALLA (1 bloques)`, solo por el manifiesto de jumbo_g (`resultados/verificacion_rapida_3b971c4.txt`). Después de `3b971c4` solo cambian este documento, ese registro y el manifiesto |

| Sonda del revisor (caja base que cuenta el circulante, normalización declarada y partidas C46 −2.090 / +2.090 del documento «x») | `fbb146d` | corrección C1 |
|---|---|---|
| libro V6.3.1 (prueba CAJA) | bloquea solo F1-LIBRO (límite declarado) | F1-CIRC DATOS INVÁLIDOS: el libro lleva C46 = 11.417,333 y el cálculo declarado de C46 da 9.327,333 |
| libro V6.3.2 (prueba CAJA, oráculo de la prueba) | nada bloquea: utilizable, f −1,3411 %, flujo 7.365,885 | F1-CIRC DATOS INVÁLIDOS, y solo F1-CIRC: no utilizable |
| libro V6.3.2 recalculado por LibreOffice (C9) | — | el libro calcula f −1,3411 % (= capa) y la capa bloquea con F1-CIRC |
| la misma, con el cálculo de C46 amañado de forma coherente: sin la fila 14; con un componente «compensación» de 2.090 del documento «x»; con la línea del circulante del estado de flujos (fuente verdadera); con el circulante repartido en dos componentes con fuente; con un componente que lo iguala en media | pasaba (F1-CIRC no leía el cálculo) | DATOS INVÁLIDOS en los cinco: «no suma la fila 14», «no se reproduce con sus fuentes», «devuelve el circulante» (×2) y «devuelven el circulante» |

### 9.4 Lo que sigue sin comprobarse por software (límites declarados)

1. **Un componente de C46 con fuente verdadera que sea circulante solo en parte** (p. ej. la variación de las provisiones corrientes) no se distingue
   de otro: F1-CIRC descarta los que lo compensan exactamente, solos o combinados, no los parciales. Eso lo ve la revisión de entradas (la persona y el
   revisor independiente), con la lista de componentes, fuentes y citas que enseñan el resultado, el informe y la ficha. En VINCI hay uno: los
   dividendos de sociedades no consolidadas (31 / 41 / 40; URD 2024 p. 348, URD 2025 p. 370), ya revisados en la revisión del montaje (§2).
2. **Las fuentes de `conciliacion_fcf_base` siguen sin contrastarse** (K3a; hueco anterior a V-CIRC y común a C46–C50 y C70 − C52). Con la
   normalización, C46 ya no depende de ellas, pero una partida de C47–C50 sin fuente verdadera podría inflar la caja base: es un fraude general, no
   del circulante; lo cerraría la primera vía del revisor.
3. **C46 tiene que declararse con su cálculo** (`fase1_historia`). Un expediente cuyo C46 sea una cifra de la etapa 1 o una derivación dependiente de
   una celda de juicio (`entradas_dependientes.py`, `derivacion.recalculo`, que no admite a la vez un `calculo`) no puede usar la normalización:
   F1-CIRC INCOMPLETO. Para usarla, se declara el cálculo en un expediente nuevo.
4. `fase1_v63.json` no lleva una huella sellada: F1-CIRC lo vuelve a contrastar cada vez con los textos del expediente y con el libro, así que un
   archivo editado tiene que seguir reproduciéndose con citas verdaderas y con las cifras del libro.
5. Las observaciones menores 1 (un solo criterio para reconocer la V6.3.2) y 2 (Motor E205 solo avisa de la ventana) de la revisión no se han
   tocado: no bloquean y quedan fuera de C1.
6. Nada de esto acredita aptitud económica ni por entradas. **No apto para dinero real.**
