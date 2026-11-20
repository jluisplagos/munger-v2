#!/usr/bin/env bash
# vinci_b · secuencia completa de montaje hasta el relevo de la fase A (Claude orquestación, 20-nov-2026). LibreOffice siempre bajo flock.
# Uso: bash rehacer_vinci_b.sh DIR_GUIONES DIR_TRABAJO DIR_MISTRAL_FUENTES_MERCADO DIR_XLRD REGISTRO_MISTRAL.json
# (REGISTRO_MISTRAL.json = mistral/examen-vinci-entradas @ 737a8d8: resultados_examen/vinci/verificacion_entradas.json; DIR_MISTRAL_FUENTES_MERCADO = su fuentes_mercado/)
set -euo pipefail
G=$1; T=$2; MIS=$3; XLRD=$4; REGM=$5
R=/home/user/e_work/wt_expedientes/munger_v2_r1
U=$R/personaje_v2/empresas_v2_correcciones/2026-11_examen_universo
E=$U/vinci_b
REC=$R/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_15/f1_circulante/resultados/ensayo_vinci_b
MP=/home/user/e_work/fuentes_examen/mercado_persona
LOCK=/home/user/e_work/libreoffice.lock
test ! -e "$E"
cd /tmp
python3 -I $G/generar_cambio_vinci_b.py $REC/cambio_vinci_b.propuesta.json $MP $U/configuracion/cambio_vinci_b.json
cd $R
( flock $LOCK python3 personaje_v2/scripts/cambiar_base.py preparar personaje_v2/empresas_v2_correcciones/2026-11_examen_universo/configuracion/cambio_vinci_b.json ) > $T/preparar.log
mkdir -p $E/resultados/scripts
cp $G/generar_cambio_vinci_b.py $G/declarar_circulante_vinci_b.py $G/fuentes_mercado_vinci_b.py $G/vigencia_extracto_vinci_b.py $G/rehacer_vinci_b.sh $E/resultados/scripts/
cd /tmp
python3 -I $E/resultados/scripts/declarar_circulante_vinci_b.py $E/Vinci/motor_a_f1.json $REC/normalizacion_circulante_vinci_b.json $E/resultados/declaracion_circulante_vinci_b.json
( flock $LOCK python3 -I $E/resultados/scripts/fuentes_mercado_vinci_b.py $E/Vinci $MIS $MP $XLRD $T $E/resultados/fuentes_mercado_vinci_b.json ) > $T/fuentes.log
python3 -I $E/resultados/scripts/vigencia_extracto_vinci_b.py $E/Vinci $E/antecedentes $E/resultados/vigencia_extracto_vinci_b.json > $T/vigencia.log
cd $R
set +e
( flock $LOCK python3 personaje_v2/scripts/pipeline.py personaje_v2/empresas_v2_correcciones/2026-11_examen_universo/vinci_b/Vinci --config personaje_v2/config_v2_v632_f1.json ) > $T/pipeline.log 2>&1
echo "pipeline: código $?"
set -e
python3 personaje_v2/scripts/cambiar_base.py comprobar personaje_v2/empresas_v2_correcciones/2026-11_examen_universo/configuracion/cambio_vinci_b.json > $T/comprobar_cambio.log 2>&1 || true
tail -3 $T/comprobar_cambio.log
# registro de entradas (después del pipeline): plantilla regenerada fuera del expediente y registro de Mistral corregido (sin sellar)
python3 personaje_v2/scripts/verificacion_entradas.py plantilla personaje_v2/empresas_v2_correcciones/2026-11_examen_universo/vinci_b/Vinci
mv $E/Vinci/verificacion_entradas.plantilla.json $T/plantilla_vinci_b.json
python3 $E/resultados/scripts/registro_entradas_vinci_b.py $E/Vinci $REGM $T/plantilla_vinci_b.json $E/resultados/registro_entradas_vinci_b.json
python3 personaje_v2/scripts/verificacion_entradas.py comprobar personaje_v2/empresas_v2_correcciones/2026-11_examen_universo/vinci_b/Vinci > $E/resultados/comprobar_registro_vinci_b.txt || true
