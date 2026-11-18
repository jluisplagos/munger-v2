# Hoja resumen en lenguaje llano (`hoja_resumen.py`)

Una página por empresa para leer sin jerga: el veredicto, por qué, lo que lo haría falso, cuánto depende de la tasa y qué
predicciones se pueden comprobar (reorientación §7; criterios K5 y K9 de la lectura del informe).

## Uso

Desde `personaje_v2/`, sobre un expediente **cerrado** (paso 14 terminado, ficha oficial):

```
python3 -I scripts/hoja_resumen.py CARPETA_DEL_EXPEDIENTE            # escribe hoja_resumen.md y hoja_resumen.json en el expediente
python3 -I scripts/hoja_resumen.py CARPETA --salida OTRA_CARPETA     # o en otra carpeta
python3 -I scripts/hoja_resumen.py CARPETA --comprobar               # ¿la hoja sigue leyendo la ficha y el material vigentes?
python3 -I scripts/hoja_resumen.py CARPETA --verificar-origen        # ¿cada frase sale tal cual del texto del personaje?
```

Opciones: `--trabajo DIR` (copias temporales; se borran), `--lock ARCHIVO` (cerrojo de LibreOffice; por defecto
`/home/user/e_work/libreoffice.lock` o `$HOJA_RESUMEN_LOCK`), `--tasas 0.07,0.08,0.09,0.10,0.11`.

Códigos: 0 hecho · 2 uso · 3 expediente no cerrado o incoherente (no escribe nada) · 4 hoja desactualizada o frase sin origen ·
5 la sensibilidad a la tasa heredada no reproduce el precio de Sí oficial · 6 fallo del recálculo.

Tarda unos 25–30 s (cinco recálculos). LibreOffice va siempre bajo `flock`: no lanzarlo en paralelo con otro pipeline.

## Qué lee y qué escribe

- Lee: `ficha.json`, `informe.md`, `precio.json`, `resultados.json`, `fase_c.json`, `estado_pipeline.json`, el libro
  `<E>_v63_evaluada.xlsx` y, si están, `cierre_vigente.json`, `fase1_metadatos.json`, `fase1_fuentes.json`, `fase1_v63.json`.
- Antes de escribir comprueba que el pipeline terminó, que la ficha no es provisional, que la ficha y el informe son los de
  `cierre_vigente.json` (si existe) y que el libro evaluado es el de `ficha.hashes.libro_evaluado`. Si algo no cuadra, no escribe.
- Escribe solo dos archivos nuevos: `hoja_resumen.md` (la página) y `hoja_resumen.json` (huellas SHA-256 de todo lo leído,
  origen de cada frase y la tabla de sensibilidad con las cifras exactas). No cambia ningún otro archivo. No es una salida
  oficial ni forma parte del material auditado; la hoja no lleva línea «Material auditado» ni «Veredicto:».
- Si la ficha cambia después, `--comprobar` lo dice (código 4) y hay que regenerar la hoja; al regenerarla, avisa de la huella
  anterior.

## Cómo se hace cada parte

- **Veredicto:** estado, cubo, acción y precio de Sí de la ficha y de `precio.json`; la aptitud, tal como la declara la ficha
  (`aptitud_de_uso`). Si la ficha no la declara (salidas V6.3 anteriores), la hoja dice «experimental; no apto para dinero real»
  y que no se presume ninguna aptitud.
- **Texto llano:** frases del personaje, por una regla fija: tesis (B101) frases 1, 2 y última; tesis inversa (B102) primera
  frase con al menos seis palabras y última; «a No» de `cambiaria_de_cubo`, frase 1. Solo se quitan corchetes de fuente y
  referencias a celdas, filas o páginas (las citas de Munger se conservan). Cada frase lleva su número de origen.
- **Lo que lo haría falso:** `cambiaria_de_cubo` (a No, a Sí, a Demasiado difícil) y `decision.condiciones_revision`.
- **Sensibilidad a la tasa:** copia del libro evaluado con solo `Análisis!C56` cambiada, recálculo forzado (`recalc.sh`),
  lectura con `leer_resultados.py --exigir-recalculo-forzado` y escalera con `precio_de_si.calcular` (la misma k). A la tasa
  heredada debe reproducir exactamente el precio de Sí de `precio.json`; si no, código 5. «Firme» = la zona no cambia entre el 8 y
  el 10 %.
- **Predicciones:** `Palancas!A38:C40` de `fase_c.json`, cotejadas con `ficha.predicciones`.
- **Fechas:** análisis (ficha), datos base (último ejercicio), precio y acciones (`fase1_metadatos.json` o `fase1_v63.json`),
  fuentes (`fase1_fuentes.json` o los años de la Historia).

## Límites

- Cambiar solo la tasa deja quietas las demás celdas de juicio. Ejemplo: el ROIC de largo plazo, cuya referencia mecánica es la
  tasa del motor. La tabla dice cuánto pesa la tasa con el mismo juicio, no qué habría decidido el personaje con otra tasa.
- La hoja hereda los límites del libro y del expediente. Ejemplos: el motor A sin F1 en los libros V6.3 y la aptitud por entradas
  evaluada por la entrega que cerró el expediente. Nunca declara apto nada que la ficha no declare.
- La selección de frases es mecánica: no resume con palabras nuevas, así que alguna frase puede ser larga.
- Pruebas: `python3 -B pruebas/test_hoja_resumen.py`, sobre copias de Hermès (V6.3) y de Vidrala 4.14 (V6.4 experimental), con
  LibreOffice; tarda alrededor de 1 min. Todavía no está registrada en `verificar_paquete.sh`.
