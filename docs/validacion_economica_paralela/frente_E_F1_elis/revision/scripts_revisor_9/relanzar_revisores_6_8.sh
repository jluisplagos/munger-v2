#!/bin/bash
# Revisión independiente n.º 9 · vuelve a ejecutar, sin cambios, los scripts de las revisiones n.º 6, n.º 7 y n.º 8 sobre
# C18 (versión anterior: C16, es decir, el worktree de C17) y compara cada salida con la que guarda el autor en
# resultados/revisor{6,7,8}_*_sobre_C18.txt. Los scripts se toman de la rama de revisión (commits 9711f04, d192cab y
# 3138a6b), no de la copia del autor.
#
# No se ejecutan barrido_7.py, clases_7.py ni lectura_filas_c14.py: necesitan PyMuPDF, que este entorno no tiene y que no
# se pudo instalar. clases_8.py se ejecuta sin --pylibs: su sección K sale sin la tipografía de MuPDF y se compara aparte.
#
# Uso: relanzar_revisores_6_8.sh <munger_v2_r1> <frente C17 (código de C16)> <frente C19 (código de C18)> \
#          <carpeta con los scripts de las revisiones (…/revision)> <carpeta de trabajo>
# Con SOLO_COMPARAR=1 no vuelve a ejecutar nada: compara las salidas que ya haya en la carpeta de trabajo.
set -u
RAIZ="$1"; C16="$2"; C18="$3"; REV="$4"; W="$5"
LIBRO="$RAIZ/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_14/elis_decisiones/Elis/Elis_v63_evaluada.xlsx"
PY="python3 -I -B"
mkdir -p "$W"
if [ "${SOLO_COMPARAR:-0}" != "1" ]; then
cd "$REV/scripts_revisor_8" || exit 1
$PY barrido_8.py --raiz "$RAIZ" --c14 "$C16" --c16 "$C18" --todas "$W/todas8.jsonl.gz" --salida "$W/revisor8_barrido_8.txt" > "$W/barrido_8.stdout" 2>&1
$PY clases_8.py --todas "$W/todas8.jsonl.gz" --raiz "$RAIZ" --c14 "$C16" --c16 "$C18" > "$W/revisor8_clases_8.txt" 2> "$W/clases_8.stderr"
$PY consultas_8.py --todas "$W/todas8.jsonl.gz" --raiz "$RAIZ" --c14 "$C16" --c16 "$C18" > "$W/revisor8_consultas_8.txt" 2> "$W/consultas_8.stderr"
$PY contraejemplos_8.py --raiz "$RAIZ" --version C16="$C16" --version C18="$C18" > "$W/revisor8_contraejemplos_8.txt" 2> "$W/contraejemplos_8.stderr"
$PY lectura_saldos_8.py --todas "$W/todas8.jsonl.gz" --raiz "$RAIZ" --c16 "$C18" > "$W/revisor8_lectura_saldos_8.txt" 2> "$W/lectura_saldos_8.stderr"
$PY sondas_8.py --autor "$C18" --libro "$LIBRO" > "$W/revisor8_sondas_8.txt" 2> "$W/sondas_8.stderr"
$PY reproduccion_8.py --raiz "$RAIZ" --autor "$C18" --c14 "$C16" --trabajo "$W/rep8" > "$W/reproduccion_8.stdout" 2> "$W/reproduccion_8.stderr"
cp "$W/rep8/reproduccion_8.txt" "$W/revisor8_reproduccion_8.txt"
cd "$REV/scripts_revisor_6" || exit 1
$PY barrido_6.py --raiz "$RAIZ" --anterior C16="$C16" --nueva C18="$C18" --todas "$W/todas6.jsonl.gz" --salida "$W/revisor6_barrido_6.txt" > "$W/barrido_6.stdout" 2>&1
$PY lectura_geometrica.py --raiz "$RAIZ" --autor "$C18" --todas "$W/todas6.jsonl.gz" --salida "$W/lectura6.jsonl.gz" --solo-grupo > "$W/lectura_geometrica.stdout" 2>&1
$PY clases_6.py --todas "$W/todas6.jsonl.gz" --lectura "$W/lectura6.jsonl.gz" --anterior C16 --nueva C18 > "$W/revisor6_clases_6.txt" 2> "$W/clases_6.stderr"
$PY contraejemplos_6.py --raiz "$RAIZ" --version C16="$C16" --version C18="$C18" > "$W/revisor6_contraejemplos_6.txt" 2> "$W/contraejemplos_6.stderr"
$PY cobertura_6.py --raiz "$RAIZ" --autor "$C18" --libro "$LIBRO" > "$W/revisor6_cobertura_6.txt" 2> "$W/cobertura_6.stderr"
$PY consultas_6.py --raiz "$RAIZ" --todas "$W/todas6.jsonl.gz" --anterior C16="$C16" --nueva C18="$C18" > "$W/revisor6_consultas_6.txt" 2> "$W/consultas_6.stderr"
$PY lectura_filas_c12.py --raiz "$RAIZ" --autor "$C18" > "$W/revisor6_lectura_filas_c12.txt" 2> "$W/lectura_filas_c12.stderr"
cd "$REV/scripts_revisor_7" || exit 1
$PY contraejemplos_7.py --raiz "$RAIZ" --version C16="$C16" --version C18="$C18" > "$W/revisor7_contraejemplos_7.txt" 2> "$W/contraejemplos_7.stderr"
$PY sondas_umbral_7.py --autor "$C18" --libro "$LIBRO" > "$W/revisor7_sondas_umbral_7.txt" 2> "$W/sondas_umbral_7.stderr"
$PY reproduccion_7.py --raiz "$RAIZ" --autor "$C18" --c13 "$C16" --trabajo "$W/rep7" > "$W/revisor7_reproduccion_7.txt" 2> "$W/reproduccion_7.stderr"
fi
S="$W/comparacion_6_8.txt"
echo "== Salidas de los scripts de las revisiones n.º 6, 7 y 8 sobre C18 frente a las que guarda el autor (resultados/*_sobre_C18.txt) ==" > "$S"
for n in revisor6_barrido_6 revisor6_clases_6 revisor6_contraejemplos_6 revisor6_cobertura_6 revisor6_consultas_6 revisor6_lectura_filas_c12 \
         revisor7_contraejemplos_7 revisor7_sondas_umbral_7 revisor7_reproduccion_7 \
         revisor8_barrido_8 revisor8_clases_8 revisor8_consultas_8 revisor8_contraejemplos_8 revisor8_lectura_saldos_8 revisor8_sondas_8 \
         revisor8_reproduccion_8; do
  g="$C18/resultados/${n}_sobre_C18.txt"
  if [ ! -s "$W/$n.txt" ]; then echo "  $n: SIN SALIDA (véase el .stderr en la carpeta de trabajo)" >> "$S"; continue; fi
  if cmp -s "$W/$n.txt" "$g"; then r="IDÉNTICA"; else r="DISTINTA ($(diff "$W/$n.txt" "$g" | grep -c '^[<>]') líneas de diferencia)"; fi
  echo "  $n: $(wc -l < "$W/$n.txt") líneas · $r" >> "$S"
  if ! cmp -s "$W/$n.txt" "$g"; then
    echo "    diferencias (< regenerada sobre el congelado · > guardada por el autor), primeras 40:" >> "$S"
    diff "$W/$n.txt" "$g" | grep '^[<>]' | head -40 | cut -c1-220 | sed 's/^/      /' >> "$S"
  fi
done
echo "" >> "$S"
echo "  No ejecutados (necesitan PyMuPDF): revisor7_barrido_7, revisor7_clases_7, revisor7_lectura_filas_c14" >> "$S"
echo "" >> "$S"
echo "== Scripts de las revisiones n.º 6 a 8: copia del autor (revision/scripts_revisor_N de C19) frente a la rama de revisión ==" >> "$S"
for d in scripts_revisor_6 scripts_revisor_7 scripts_revisor_8 resultados_revisor_8; do
  if diff -rq "$REV/$d" "$C18/revision/$d" > /dev/null 2>&1; then r="idénticos"; else r="DISTINTOS"; fi
  echo "  $d: $(ls "$REV/$d" | wc -l) archivos · $r" >> "$S"
done
if cmp -s "$REV/REVISION_INDEPENDIENTE_8.md" "$C18/revision/REVISION_INDEPENDIENTE_8.md"; then r="idéntico"; else r="DISTINTO"; fi
echo "  REVISION_INDEPENDIENTE_8.md: $r" >> "$S"
echo "" >> "$S"
echo "== Salidas guardadas por el autor de los scripts de las revisiones n.º 1 a 5: sobre C16 frente a sobre C18 (sin volver a ejecutarlos) ==" >> "$S"
for n in mutantes_revisor revisor3_prueba_mutantes_3 revisor3_prueba_mutantes_3b revisor3_sondas revisor4_contraejemplos_4 revisor4_paginas_sin_ancla \
         revisor5_barrido_tablas revisor5_clases_5 revisor5_cobertura_propia revisor5_contraejemplos_5; do
  a="$C18/resultados/${n}_sobre_C16.txt"; b="$C18/resultados/${n}_sobre_C18.txt"
  d=$(diff <(sed 's/C16/C18/g' "$a") "$b" | grep -c '^[<>]')
  echo "  $n: $(wc -l < "$b") líneas · líneas distintas tras igualar la etiqueta de versión: $d" >> "$S"
done
cat "$S"
