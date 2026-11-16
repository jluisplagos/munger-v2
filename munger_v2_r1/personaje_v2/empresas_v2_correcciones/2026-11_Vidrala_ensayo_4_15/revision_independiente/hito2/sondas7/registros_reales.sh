#!/bin/bash
# Séptima comprobación · registros reales con el código de la candidata (copia = 45ff57c), con la corrección propuesta (fix7) y con el de
# la anterior (prev = 8196522):
#  1) diagnóstico de los tres registros finales (…_4_15/scripts/diagnostico_registros_4_14.py) y de los otros cuatro;
#  2) inventario de signo de los siete registros (…_4_15/hito2/scripts/inventario_signo_registros.py);
#  3) PDF reales: parte B de q12_pdf.py (hito1/reproducciones_fable_tercera), tal cual.
# Solo lee los expedientes (el diagnóstico trabaja en copias temporales bajo TMPDIR). Nunca LibreOffice (sustituto de soffice en el PATH).
# Uso: registros_reales.sh [códigos…]   (por defecto: copia fix7 prev)
F="$(cd "$(dirname "$0")/.." && pwd)"
C="$(cd "$F/.." && pwd)/munger_v2_r1"
export PATH="$F/bin:$PATH" PYTHONDONTWRITEBYTECODE=1 TMPDIR="$F/tmp/reales"; mkdir -p "$TMPDIR" "$F/salidas/reales"
E15="$C/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_15"
CODS="${@:-copia fix7 prev}"
for cod in $CODS; do
  PVX="$F/$cod/munger_v2_r1/personaje_v2"
  E14="$PVX/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_14"
  ( cd "$E14" && nice -n 5 python3 -I -B "$E15/scripts/diagnostico_registros_4_14.py" "$PVX" viscofan_decisiones/Viscofan vidrala_decisiones/Vidrala elis_decisiones/Elis ) > "$F/salidas/reales/diagnostico_finales_$cod.json" 2> "$F/salidas/reales/diagnostico_finales_$cod.err"; echo "diagnóstico finales $cod rc=$?"
  for exp in viscofan/Viscofan vidrala/Vidrala elis_motor_A/Elis vidrala_decisiones_INVALIDO_perdio_analisis/Vidrala; do
    n=$(echo $exp | tr '/' '_')
    ( cd "$E14" && nice -n 5 python3 -I -B "$E15/scripts/diagnostico_registros_4_14.py" "$PVX" $exp ) > "$F/salidas/reales/diagnostico_${n}_$cod.json" 2> "$F/salidas/reales/diagnostico_${n}_$cod.err"; echo "diagnóstico $exp $cod rc=$?"
  done
  ( nice -n 5 python3 -I -B "$E15/hito2/scripts/inventario_signo_registros.py" "$PVX" "$E14/vidrala_decisiones_INVALIDO_perdio_analisis/Vidrala" "$E14/elis_decisiones/Elis" "$E14/viscofan/Viscofan" "$E14/elis_motor_A/Elis" "$E14/vidrala_decisiones/Vidrala" "$E14/vidrala/Vidrala" "$E14/viscofan_decisiones/Viscofan" ) > "$F/salidas/reales/inventario_signo_$cod.json" 2> "$F/salidas/reales/inventario_signo_$cod.err"; echo "inventario $cod rc=$?"
  ( PV="$PVX" nice -n 5 python3 -I -B "$E15/revision_independiente/hito1/reproducciones_fable_tercera/q12_pdf.py" B ) > "$F/salidas/reales/q12_pdf_parteB_$cod.log" 2>&1; echo "q12 B $cod rc=$?"
  echo "--- $cod: comparación con lo entregado"
  cmp "$F/salidas/reales/diagnostico_finales_$cod.json" "$E15/hito2/resultados/diagnostico_registros_4_14_con_reglas_hito2.json" && echo "diagnóstico ($cod) == entregado, byte a byte"
  cmp "$F/salidas/reales/inventario_signo_$cod.json" "$E15/hito2/resultados/inventario_signo_registros_reales.json" && echo "inventario ($cod) == entregado, byte a byte"
  date -u +"%T fin $cod"
done
