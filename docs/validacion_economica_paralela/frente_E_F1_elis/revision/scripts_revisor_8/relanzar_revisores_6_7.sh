#!/bin/bash
# Revisión independiente n.º 8 · vuelve a ejecutar, sin cambios, los scripts de las revisiones n.º 6 y n.º 7 sobre C16
# (versión anterior: C14, es decir, el worktree de C15) y compara cada salida con la que guarda el autor en
# resultados/revisor6_*_sobre_C16.txt y resultados/revisor7_*_sobre_C16.txt.
#
# Uso: relanzar_revisores_6_7.sh <munger_v2_r1> <frente C15 (código de C14)> <frente C17 (código de C16)> \
#          <carpeta con los scripts de las revisiones (…/revision)> <carpeta con pymupdf> <carpeta de trabajo>
# Los scripts se ejecutan con «python3 -I -B» para no dejar __pycache__ en la carpeta de los scripts.
# Con SOLO_COMPARAR=1 no vuelve a ejecutar nada: compara las salidas que ya haya en la carpeta de trabajo.
set -u
RAIZ="$1"; C14="$2"; C16="$3"; REV="$4"; LIBS="$5"; W="$6"
LIBRO="$RAIZ/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_14/elis_decisiones/Elis/Elis_v63_evaluada.xlsx"
PY="python3 -I -B"
mkdir -p "$W"
if [ "${SOLO_COMPARAR:-0}" != "1" ]; then
cd "$REV/scripts_revisor_6" || exit 1
$PY barrido_6.py --raiz "$RAIZ" --anterior C14="$C14" --nueva C16="$C16" --todas "$W/todas6.jsonl.gz" --salida "$W/revisor6_barrido_6.txt" > "$W/barrido_6.stdout" 2>&1
$PY lectura_geometrica.py --raiz "$RAIZ" --autor "$C16" --todas "$W/todas6.jsonl.gz" --salida "$W/lectura6.jsonl.gz" --solo-grupo > "$W/lectura_geometrica.stdout" 2>&1
$PY clases_6.py --todas "$W/todas6.jsonl.gz" --lectura "$W/lectura6.jsonl.gz" --anterior C14 --nueva C16 > "$W/revisor6_clases_6.txt" 2> "$W/clases_6.stderr"
$PY contraejemplos_6.py --raiz "$RAIZ" --version C14="$C14" --version C16="$C16" > "$W/revisor6_contraejemplos_6.txt" 2> "$W/contraejemplos_6.stderr"
$PY cobertura_6.py --raiz "$RAIZ" --autor "$C16" --libro "$LIBRO" > "$W/revisor6_cobertura_6.txt" 2> "$W/cobertura_6.stderr"
$PY consultas_6.py --raiz "$RAIZ" --todas "$W/todas6.jsonl.gz" --anterior C14="$C14" --nueva C16="$C16" > "$W/revisor6_consultas_6.txt" 2> "$W/consultas_6.stderr"
$PY lectura_filas_c12.py --raiz "$RAIZ" --autor "$C16" > "$W/revisor6_lectura_filas_c12.txt" 2> "$W/lectura_filas_c12.stderr"
cd "$REV/scripts_revisor_7" || exit 1
$PY barrido_7.py --raiz "$RAIZ" --c13 "$C14" --c14 "$C16" --pylibs "$LIBS" --todas "$W/todas7.jsonl.gz" --salida "$W/revisor7_barrido_7.txt" > "$W/barrido_7.stdout" 2>&1
$PY clases_7.py --todas "$W/todas7.jsonl.gz" --raiz "$RAIZ" --autor "$C16" --pylibs "$LIBS" > "$W/revisor7_clases_7.txt" 2> "$W/clases_7.stderr"
$PY contraejemplos_7.py --raiz "$RAIZ" --version C14="$C14" --version C16="$C16" > "$W/revisor7_contraejemplos_7.txt" 2> "$W/contraejemplos_7.stderr"
$PY lectura_filas_c14.py --raiz "$RAIZ" --autor "$C16" --pylibs "$LIBS" > "$W/revisor7_lectura_filas_c14.txt" 2> "$W/lectura_filas_c14.stderr"
$PY sondas_umbral_7.py --autor "$C16" --libro "$LIBRO" > "$W/revisor7_sondas_umbral_7.txt" 2> "$W/sondas_umbral_7.stderr"
# reproduccion_7.py vuelve a ejecutar la cadena del §13 sobre una copia; «C13» es aquí la versión anterior (C14)
$PY reproduccion_7.py --raiz "$RAIZ" --autor "$C16" --c13 "$C14" --trabajo "$W/rep7" > "$W/revisor7_reproduccion_7.txt" 2> "$W/reproduccion_7.stderr"
fi
# comparación con lo que guarda el autor
echo "== Salidas de los scripts de las revisiones n.º 6 y n.º 7 sobre C16 frente a las que guarda el autor ==" > "$W/comparacion_6_7.txt"
for n in revisor6_barrido_6 revisor6_clases_6 revisor6_contraejemplos_6 revisor6_cobertura_6 revisor6_consultas_6 revisor6_lectura_filas_c12 \
         revisor7_barrido_7 revisor7_clases_7 revisor7_contraejemplos_7 revisor7_lectura_filas_c14 revisor7_sondas_umbral_7 revisor7_reproduccion_7; do
  g="$C16/resultados/${n}_sobre_C16.txt"
  if cmp -s "$W/$n.txt" "$g"; then r="IDÉNTICA"; else r="DISTINTA ($(diff "$W/$n.txt" "$g" | grep -c '^[<>]') líneas de diferencia)"; fi
  echo "  $n: $(wc -l < "$W/$n.txt") líneas · $r" >> "$W/comparacion_6_7.txt"
  if ! cmp -s "$W/$n.txt" "$g"; then
    echo "    diferencias (< regenerada sobre el congelado · > guardada por el autor):" >> "$W/comparacion_6_7.txt"
    diff "$W/$n.txt" "$g" | grep '^[<>]' | cut -c1-200 | sed 's/^/      /' >> "$W/comparacion_6_7.txt"
  fi
done
echo "" >> "$W/comparacion_6_7.txt"
echo "== Salidas guardadas por el autor de los scripts de las revisiones n.º 1 a 5: sobre C14 frente a sobre C16 (sin volver a ejecutarlos) ==" >> "$W/comparacion_6_7.txt"
for n in mutantes_revisor revisor3_prueba_mutantes_3 revisor3_prueba_mutantes_3b revisor3_sondas revisor4_contraejemplos_4 revisor4_paginas_sin_ancla \
         revisor5_barrido_tablas revisor5_clases_5 revisor5_cobertura_propia revisor5_contraejemplos_5; do
  a="$C16/resultados/${n}_sobre_C14.txt"; b="$C16/resultados/${n}_sobre_C16.txt"
  d=$(diff <(sed 's/C14/C16/g' "$a") "$b" | grep -c '^[<>]')
  echo "  $n: $(wc -l < "$b") líneas · líneas distintas tras igualar la etiqueta de versión: $d" >> "$W/comparacion_6_7.txt"
done
cat "$W/comparacion_6_7.txt"
