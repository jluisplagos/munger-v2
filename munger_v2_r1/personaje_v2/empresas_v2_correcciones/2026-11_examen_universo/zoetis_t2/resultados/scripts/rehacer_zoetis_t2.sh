#!/usr/bin/env bash
# zoetis_t2 · secuencia completa de la preparación del segundo tiempo (Claude orquestación, 19-nov-2026), desde munger_v2_r1/.
# Requiere: zoetis_t2/fuentes_release/ con las tres fuentes del T3 de la Release (huellas comprobadas) y la transcripción de Mistral, y DIR_TEXTO
# con zoetis-10k-fy2025.txt y los textos del T3 hechos como los hace cambiar_base.py (para generar la configuración antes de preparar).
# Uso: bash rehacer_zoetis_t2.sh DIR_TEXTO COMMIT_REGISTRO_T1D   (el expediente no debe existir: preparar nunca sobrescribe)
set -euo pipefail
EX=personaje_v2/empresas_v2_correcciones/2026-11_examen_universo
T2=$EX/zoetis_t2
python3 -I $T2/resultados/scripts/generar_cambio_zoetis_t2.py "$PWD" "$1" $EX/configuracion/cambio_zoetis_t2.json
python3 personaje_v2/scripts/cambiar_base.py preparar $EX/configuracion/cambio_zoetis_t2.json
( cd $T2 && python3 -I resultados/scripts/fuentes_zoetis_t2.py "$PWD" "$(git rev-parse --show-toplevel)" "$2" resultados/fuentes_zoetis_t2.json >/dev/null \
  && python3 -I resultados/scripts/corregir_registro_zoetis_t2.py Zoetis antecedentes resultados/registro_cambios_zoetis_t2.json \
  && python3 -I resultados/scripts/extracto_zoetis_t2.py Zoetis antecedentes resultados/extracto_zoetis_t2.json \
  && cat resultados/scripts/adenda_cambio_de_base.md >> resultados/cambio_de_base.md )
( flock /home/user/e_work/libreoffice.lock python3 personaje_v2/scripts/pipeline.py $T2/Zoetis --config personaje_v2/config_v2_v631_f1.json ) || test $? -eq 10
python3 personaje_v2/scripts/cambiar_base.py comprobar $EX/configuracion/cambio_zoetis_t2.json
