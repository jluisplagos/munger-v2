#!/bin/bash
# Octava comprobación. Uso: run_bateria8.sh <árbol ligero (…/munger_v2_r1)> <batería.py> <salida.log> [partes de test_comprobadores…]
# Ejecuta una batería PERMITIDA como lo hace verificar_paquete.sh (cd personaje_v2 && python3 -B pruebas/…), con el sustituto de soffice
# delante en el PATH, TMPDIR propio y prioridad baja (hay una regresión completa en marcha en otra sesión). Nunca LibreOffice ni pipeline.py.
# test_comprobadores.py SOLO se admite con las partes h2, h1 y h3: h1_recorrido y h1_reutilizacion lanzan pipeline.py y LibreOffice.
F="$(cd "$(dirname "$0")/.." && pwd)"
arbol="$1"; bat="$2"; sal="$3"; shift 3
case "$bat" in
  test_verificacion_entradas_415.py|test_verificacion_entradas_414.py|test_entrada_efectiva_415.py) [ $# -eq 0 ] || { echo "sin argumentos"; exit 2; } ;;
  test_comprobadores.py) [ $# -ge 1 ] || { echo "test_comprobadores.py exige partes explícitas (h2 h1 h3)"; exit 2; }
     for p in "$@"; do case "$p" in h2|h1|h3) ;; *) echo "parte no permitida (LibreOffice/pipeline.py): $p"; exit 2;; esac; done ;;
  *) echo "batería no permitida: $bat"; exit 2;;
esac
export PATH="$F/bin:$PATH" PYTHONDONTWRITEBYTECODE=1
export TMPDIR="$F/tmp/$(basename "$sal" .log)"; mkdir -p "$TMPDIR"
t0=$(date +%s)
( cd "$arbol/personaje_v2" && nice -n 10 python3 -B "pruebas/$bat" "$@" ) > "$sal" 2>&1; rc=$?
echo "### rc=$rc segundos=$(( $(date +%s) - t0 )) soffice_en_PATH=$(command -v soffice)" >> "$sal"
exit $rc
