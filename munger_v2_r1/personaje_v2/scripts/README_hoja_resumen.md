# Hoja resumen en lenguaje llano (`hoja_resumen.py`)

Una página por empresa para estudiar sin jerga: qué concluye el análisis oficial (o por qué no concluye), por qué, qué le haría
cambiar de opinión, cuánto depende de la tasa y qué predicciones se pueden comprobar (reorientación §7; criterios K5 y K9 de la
lectura del informe). Versión 2.0: ronda 1 de su revisión crítica (`/home/user/e_work/revision_hoja/REVISION_HOJA.md`).

**La hoja no puede decir más que la ficha oficial.** No es una salida oficial ni una recomendación, y nunca dice que algo sea apto
para dinero real.

## Uso

Desde `personaje_v2/`, sobre un expediente **cerrado y vigente**:

```
python3 -I scripts/hoja_resumen.py CARPETA_DEL_EXPEDIENTE            # escribe hoja_resumen.md y hoja_resumen.json en el expediente
python3 -I scripts/hoja_resumen.py CARPETA --salida OTRA_CARPETA     # o en otra carpeta
python3 -I scripts/hoja_resumen.py CARPETA --comprobar               # ¿la hoja sigue siendo la del análisis oficial vigente?
python3 -I scripts/hoja_resumen.py CARPETA --verificar-origen        # ¿cada frase sale tal cual del texto del personaje?
python3 -I scripts/hoja_resumen.py CARPETA --antecedente             # análisis NO vigente: hoja rotulada «NO VIGENTE · ANTECEDENTE»
```

Opciones: `--trabajo DIR` (copias temporales; se borran), `--tasas 0.07,0.08,0.09,0.10,0.11` (siempre se añaden la tasa del
análisis y las dos que están un punto por encima y por debajo), `--lock ARCHIVO` (cerrojo de LibreOffice; por defecto
`$HOJA_RESUMEN_LOCK`, si no `/home/user/e_work/libreoffice.lock` cuando existe esa carpeta y, si no, uno en el directorio temporal),
`--espera-cerrojo S` (900 s por recálculo), `--cerrojo-ya-tomado` (o `HOJA_RESUMEN_CERROJO_YA_TOMADO=1`).

**Cerrojo.** El programa toma el cerrojo común con `flock -w` en cada recálculo. **No lo lances dentro de `flock` del mismo
cerrojo**: se esperaría a sí mismo (ahora termina con código 6 y un mensaje claro al agotar la espera, en vez de quedarse parado).
Si quien lo llama ya tiene el cerrojo (por ejemplo, `verificar_paquete.sh` bajo flock), usa `--cerrojo-ya-tomado`.

Códigos: 0 hecho (o hoja vigente con `--comprobar`) · 2 uso · 3 expediente no cerrado, no vigente, incompleto o mal formado ·
4 hoja desactualizada, no vigente, editada o ausente (`--comprobar`) / frase sin origen o contenido mínimo incumplido ·
5 la sensibilidad a la tasa del análisis no reproduce el precio de Sí de `precio.json` · 6 fallo del recálculo o del cerrojo.
**Con cualquier código distinto de 0 no se escribe hoja**, y la anterior, si la hay, se aparta como `hoja_resumen.NO_VIGENTE.md` /
`.json`.

## La puerta: cuándo hay hoja

La hoja usa la **misma comprobación que el cierre oficial**, `cierre_v2.motivo_vigencia`: auditoría APROBADO del material
vigente, material sin cambios desde la auditoría (también `fase_c.json`, `precio.json`, la declaración F1…), aprobación no retirada
(`aprobaciones_retiradas.json`, `historial_cierres/*/RETIRADA.json`) y, con el motor A y F1 exigido, una evaluación F1 vigente y
utilizable. Además exige un cierre registrado (`cierre_vigente.json`, `ficha.cierre.auditoria = APROBADO`), que el pipeline haya
terminado (`estado_pipeline.json → fin`), que la ficha y el informe sean los del cierre y que el libro evaluado sea el de la ficha.

- Los expedientes de `empresas_v2/` (Hermès, Nike…) **no son vigentes** para la vía oficial: sin `--antecedente` no tienen hoja.
- `--comprobar` repite la puerta completa, las huellas de todo lo leído y la huella de la propia página (`md_sha256`): una edición a
  mano, una aprobación retirada, F1 bloqueando o un `fase_c.json` cambiado después de la auditoría dan código 4 y el consejo de
  **retirar** la hoja. Una hoja `--antecedente` nunca es vigente.
- **Al retirar una aprobación** (`cierre_v2.archivar_salidas`, desde cualquier vía), la hoja se archiva con el antecedente como
  `historial_cierres/NN_…/hoja_resumen.NO_VIGENTE.*` (con `HOJA_RESUMEN_NO_VIGENTE.json`). **Al relanzar el pipeline** (`--desde N`
  o `--reiniciar`) se archiva en `historial_hojas_resumen/NN_relanzamiento_…/` y `fin` pasa a `fin_anterior`. Nunca se reactiva:
  una hoja nueva exige un cierre vigente nuevo. Una hoja escrita con `--salida` fuera del expediente no se archiva sola:
  `--comprobar` la da por no vigente.

## Qué dice la página

- **Qué concluye el análisis**, solo de la ficha: frase fija por estado («No comprar ahora; esperar a mejor precio», «La descarta»,
  «Compraría al precio del análisis. Es la conclusión del personaje, no una recomendación», «Sin conclusión: falta un dato», «Sin
  conclusión de compra: una hipótesis no se puede acotar con lo que hay»), el motivo (`causa_si_no_concluido`) y qué lo resolvería.
  **A qué precio compraría** = `decision.precio_objetivo` (u `objetivo.precio_objetivo_emitido`); si la ficha no emite precio
  (sin conclusión, objetivo bloqueado) lo dice, y si menciona la cifra de la hoja de cálculo dice por qué no es un precio de compra.
  Objetivo condicionado: «Es un precio provisional». **Precio usado en el análisis** con su fecha (no es el de hoy; aviso si es de
  más de 90 días antes del análisis).
- **Aptitud:** «Experimental: no vale para decidir con dinero real», y debajo, cuando existen en la ficha, los datos de entrada
  verificados (`verificacion_entradas`), el motor A · F1 (`motor_a_f1` y su vigencia actual) y la evaluación de la entrega
  (`aptitud_de_uso`). Si la ficha no dice nada: «no se presume ninguna». Una marca `apto_para_dinero_real = true` no se repite.
- **Salvedades de la ficha**, copiadas y recortadas: condición, objetivo, fundamento, «con datos de etapa 1 incompletos», alcance.
- **Por qué:** la tesis y la tesis inversa **enteras** (Análisis!B101 y B102, de `fase_c.json`), solo sin referencias a celdas y
  páginas. **Lo que le haría cambiar de opinión:** `cambiaria_de_cubo` y `decision.condiciones_revision`, con rótulos llanos.
  Contenido mínimo, o código 4 sin hoja: tesis y tesis inversa con texto, «a No» con texto real (salvo cubo No) y tres predicciones
  con fecha y probabilidad.
- **Cuánto cambia el resultado si se le pide más o menos rentabilidad:** copias del libro evaluado con solo `Análisis!C56`
  cambiada, recálculo forzado (`recalc.sh`), lectura con `leer_resultados.py --exigir-recalculo-forzado` y escalera con
  `precio_de_si.calcular` (la misma k). A la tasa del análisis debe reproducir exactamente `precio.json` (si no, código 5); el
  precio de Sí y el valor medio tienen que bajar al subir la tasa (si no, código 6: el libro no se recalculó). Cada fila dice si la
  tasa queda por debajo de la mínima de la hoja de cálculo y, en el motor B, con qué tasa descuenta. Avisos fijos: la tasa es
  provisional, el 10 % es solo una prueba, si el resultado cambia frente a la tasa (sin la palabra «firme»), el aviso A2 de la
  ficha, que la zona no es la conclusión, que el escenario malo no es un suelo, la regla experimental k = 3 y que lo demás se
  deja quieto. Sin conclusión, la tabla es «una lectura de la hoja de cálculo, no una conclusión».
- **Predicciones** (`Palancas!A38:C40`, cotejadas con la ficha), **fechas**, **glosario** con los términos que aparecen y, al pie,
  **para comprobar esta hoja** (huella de la ficha, origen de las frases, comprobación del cálculo y versiones).

## Límites

- Cambiar solo la tasa deja quietas las demás celdas de juicio (por ejemplo, el ROIC de largo plazo que el personaje fijó mirando la
  tasa). La tabla dice cuánto pesa la tasa con el mismo juicio, no qué habría decidido el personaje con otra tasa.
- Más corta que la versión 1.0 no es: la tesis inversa entera (hallazgo 5) pesa más que la brevedad. El texto del personaje
  conserva su jerga (se explica en el glosario) y su formato de cifras. Un resumen llano escrito por el personaje y auditado con
  el resto del material sería la solución de fondo; está fuera del alcance de esta ronda.
- La limpieza de referencias no quita un corchete de fuente dentro de un paréntesis sin dejar rastro («cálculo propio con)»).
- Pruebas: `python3 -B pruebas/test_hoja_resumen.py` (sin envolverla en flock; con `HOJA_RESUMEN_CERROJO_YA_TOMADO=1` si ya se
  tiene el cerrojo), sobre copias de Vidrala 4.10.1, Vidrala 4.14, Viscofan 4.14, Elis 4.14, Vidrala 4.13 bloqueo y Hermès, y una
  empresa sintética V6.3.1 F1 cerrada con el pipeline real; registrada en `verificar_paquete.sh completa`.
