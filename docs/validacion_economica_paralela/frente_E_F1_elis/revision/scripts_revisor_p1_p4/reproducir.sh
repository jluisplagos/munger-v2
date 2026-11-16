#!/usr/bin/env bash
# Reproducción · revisión dirigida a P1–P4 · propuesta de decisiones F1 · Elis.
# Script de revisión. No modifica el material del autor: escribe solo en la carpeta de salida que se le pasa.
#
# Uso: reproducir.sh <frente del autor en el commit congelado> <árbol materializado munger_v2_r1> <carpeta de salida>
#   <frente>  = .../docs/validacion_economica_paralela/frente_E_F1_elis de un worktree de 13f864f
#   <árbol>   = munger_v2_r1 de un worktree de main, materializado con tools/base_414.py y el ZIP de la Release base-4.14
# No ejecuta LibreOffice: contraste_f1.py consume el resultado conservado de la prueba de caja no nula.
set -u
FRENTE="$1"; BASE="$2"; OUT="$3"
AQUI="$(cd "$(dirname "$0")" && pwd)"
LIBRO="$BASE/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_14/elis_decisiones/Elis/Elis_v63_evaluada.xlsx"
mkdir -p "$OUT/tmp"
igual() { if cmp -s "$1" "$2"; then echo "    idéntico byte a byte: $(basename "$2")"; else echo "    DISTINTO: $(basename "$2")"; fi; }

echo "1. Manifiesto del autor"
( cd "$FRENTE" && sha256sum -c MANIFIESTO_SHA256.txt 2>&1 | awk '{print $NF}' | sort | uniq -c | sed 's/^/   /' )
echo "    líneas del manifiesto: $(wc -l < "$FRENTE/MANIFIESTO_SHA256.txt")"

echo "2. Libro de Elis"
echo "    sha256: $(sha256sum "$LIBRO" | cut -c1-64)"

echo "3. controles_sinteticos_f1.py (no necesita el libro)"
( cd "$FRENTE/scripts" && python3 -I controles_sinteticos_f1.py --salida "$OUT/tmp/controles_sinteticos_f1.json" > "$OUT/tmp/controles_sinteticos_f1.log" 2>&1; echo "    código de salida: $?" )
igual "$OUT/tmp/controles_sinteticos_f1.json" "$FRENTE/resultados/controles_sinteticos_f1.json"
igual "$OUT/tmp/controles_sinteticos_f1.log" "$FRENTE/resultados/controles_sinteticos_f1.log"
head -1 "$OUT/tmp/controles_sinteticos_f1.log" | sed 's/^/    /'

echo "4. copia_investigacion_f1.py"
( cd "$FRENTE/scripts" && python3 -I copia_investigacion_f1.py --cifras ../datos/cifras_fuente.csv --verificacion ../resultados/verificacion_cifras.json \
    --libro "$LIBRO" --contraste ../resultados/contraste_f1.json --salida "$OUT/tmp/copia_investigacion_f1.json" \
    --informe "$OUT/tmp/copia_investigacion_f1.md" 2>&1 | sed 's/^/    /'; echo "    código de salida: ${PIPESTATUS[0]}" )
igual "$OUT/tmp/copia_investigacion_f1.json" "$FRENTE/resultados/copia_investigacion_f1.json"
igual "$OUT/tmp/copia_investigacion_f1.md" "$FRENTE/resultados/copia_investigacion_f1.md"

echo "5. contraste_f1.py"
( cd "$FRENTE/scripts" && python3 -I contraste_f1.py --cifras ../datos/cifras_fuente.csv --verificacion ../resultados/verificacion_cifras.json \
    --libro "$LIBRO" --caja-no-nula ../resultados/caja_no_nula.json --salida "$OUT/tmp/contraste_f1.json" \
    --informe "$OUT/tmp/contraste_f1.md" 2>&1 | tail -1 | cut -c1-330 | sed 's/^/    /'; echo "    código de salida: ${PIPESTATUS[0]}" )
igual "$OUT/tmp/contraste_f1.json" "$FRENTE/resultados/contraste_f1.json"
igual "$OUT/tmp/contraste_f1.md" "$FRENTE/resultados/contraste_f1.md"
echo "    sha256 de contraste_f1.json: $(sha256sum "$OUT/tmp/contraste_f1.json" | cut -c1-64)"

echo "6. Scripts del revisor"
cd "$AQUI"
python3 -I recalculo_independiente.py --cifras "$FRENTE/datos/cifras_fuente.csv" --libro "$LIBRO" \
    --copia-autor "$FRENTE/resultados/copia_investigacion_f1.json" --salida "$OUT/recalculo_independiente.json" \
    --informe "$OUT/recalculo_independiente.txt" > /dev/null; echo "    recalculo_independiente.py: código $?; $(tail -1 "$OUT/recalculo_independiente.txt")"
python3 -I evidencia_pdf.py --base "$BASE" --fuentes "$FRENTE/datos/fuentes.json" --salida "$OUT/evidencia_pdf.json" \
    --informe "$OUT/evidencia_pdf.txt" > /dev/null; echo "    evidencia_pdf.py: código $?; $(tail -1 "$OUT/evidencia_pdf.txt")"
python3 -I sondas_caja.py --salida "$OUT/sondas_caja.json" --informe "$OUT/sondas_caja.txt" > /dev/null
echo "    sondas_caja.py: código $?; $(tail -1 "$OUT/sondas_caja.txt")"
python3 -I contraprueba_con_funciones_del_autor.py --scripts-autor "$FRENTE/scripts" \
    --controles-autor "$FRENTE/resultados/controles_sinteticos_f1.json" --salida "$OUT/contraprueba_con_funciones_del_autor.json" \
    --informe "$OUT/contraprueba_con_funciones_del_autor.txt" > /dev/null
echo "    contraprueba_con_funciones_del_autor.py: código $?; $(tail -1 "$OUT/contraprueba_con_funciones_del_autor.txt")"
rm -rf "$OUT/tmp"
