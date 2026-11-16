#!/bin/bash
# Octava comprobación · registros reales con el código del árbol congelado (0a0020b), que solo se lee (python3 -I -B: no escribe .pyc):
#  1) diagnóstico de los tres registros finales (…_4_15/scripts/diagnostico_registros_4_14.py), como dice el encargo, y de los otros cuatro;
#  2) inventario de signo de los siete registros (…_4_15/hito2/scripts/inventario_signo_registros.py), llamado como en sondas7/registros_reales.sh;
#  3) PDF reales: parte B de q12_pdf.py (hito1/reproducciones_fable_tercera), copiado sin cambios a sondas8/ (usa pdftotext, no LibreOffice).
# El diagnóstico y q12 trabajan en copias temporales bajo TMPDIR (carpeta del revisor). Sustituto de soffice delante en el PATH.
F="$(cd "$(dirname "$0")/.." && pwd)"
C="$(cd "$F/.." && pwd)/munger_v2_r1"
export PATH="$F/bin:$PATH" PYTHONDONTWRITEBYTECODE=1 TMPDIR="$F/tmp/reales"; mkdir -p "$TMPDIR" "$F/salidas8/reales"
PVX="$C/personaje_v2"
E15="$PVX/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_15"
E14="$PVX/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_14"
O="$F/salidas8/reales"
( cd "$E14" && nice -n 10 python3 -I -B ../2026-11_Vidrala_ensayo_4_15/scripts/diagnostico_registros_4_14.py "$PVX" viscofan_decisiones/Viscofan vidrala_decisiones/Vidrala elis_decisiones/Elis ) > "$O/diagnostico_finales.json" 2> "$O/diagnostico_finales.err"; echo "diagnóstico finales rc=$?"
for exp in viscofan/Viscofan vidrala/Vidrala elis_motor_A/Elis vidrala_decisiones_INVALIDO_perdio_analisis/Vidrala; do
  n=$(echo $exp | tr '/' '_')
  ( cd "$E14" && nice -n 10 python3 -I -B ../2026-11_Vidrala_ensayo_4_15/scripts/diagnostico_registros_4_14.py "$PVX" $exp ) > "$O/diagnostico_${n}.json" 2> "$O/diagnostico_${n}.err"; echo "diagnóstico $exp rc=$?"
done
( nice -n 10 python3 -I -B "$E15/hito2/scripts/inventario_signo_registros.py" "$PVX" "$E14/vidrala_decisiones_INVALIDO_perdio_analisis/Vidrala" "$E14/elis_decisiones/Elis" "$E14/viscofan/Viscofan" "$E14/elis_motor_A/Elis" "$E14/vidrala_decisiones/Vidrala" "$E14/vidrala/Vidrala" "$E14/viscofan_decisiones/Viscofan" ) > "$O/inventario_signo.json" 2> "$O/inventario_signo.err"; echo "inventario rc=$?"
cmp "$F/sondas8/q12_pdf.py" "$E15/revision_independiente/hito1/reproducciones_fable_tercera/q12_pdf.py" && echo "q12_pdf.py de sondas8 == el entregado"
( cd "$F/sondas8" && PV="$PVX" nice -n 10 python3 -I -B "$F/sondas8/q12_pdf.py" B ) > "$O/q12_pdf_parteB.log" 2>&1; echo "q12 B rc=$?"
echo "--- comparación con lo entregado"
cmp "$O/diagnostico_finales.json" "$E15/hito2/resultados/diagnostico_registros_4_14_con_reglas_hito2.json" && echo "diagnóstico == entregado, byte a byte ($(sha256sum < "$O/diagnostico_finales.json" | cut -c1-64))"
cmp "$O/inventario_signo.json" "$E15/hito2/resultados/inventario_signo_registros_reales.json" && echo "inventario == entregado, byte a byte ($(sha256sum < "$O/inventario_signo.json" | cut -c1-64))"
for f in "$O"/*.err; do [ -s "$f" ] && { echo "stderr no vacío: $f"; head -5 "$f"; }; done
cat "$O/q12_pdf_parteB.log"
date -u +"%T fin"
