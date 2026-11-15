#!/usr/bin/env bash
# Pruebas de la reparación H1–H3 (contrato del 8-nov-2026). Ejecutar desde la raíz personaje_v2/:
#   bash pruebas/ejecutar_pruebas_reparacion.sh            (todas)
#   bash pruebas/ejecutar_pruebas_reparacion.sh rapidas    (sin la batería sintética, que tarda ~4 min con LibreOffice)
# Escribe las salidas en pruebas/resultados_reparacion/. Código 0 si todo PASA.
# La batería sintética crea carpetas en pruebas/sintetico/ (comportamiento normal del proyecto).
set -uo pipefail
cd "$(dirname "$0")/.."
export PYTHONDONTWRITEBYTECODE=1   # sin __pycache__ en scripts/ ni en v6/scripts/
OUT=pruebas/resultados_reparacion
mkdir -p "$OUT"
fallos=0

echo "== test_comprobadores.py"
python3 -B pruebas/test_comprobadores.py > "$OUT/test_comprobadores.txt" 2>&1; rc=$?
tail -1 "$OUT/test_comprobadores.txt"; [ $rc -eq 0 ] || fallos=$((fallos+1))

if [ "${1:-}" != "rapidas" ]; then
  echo "== test_pipeline_sintetico.py (LibreOffice, en secuencia)"
  python3 -B pruebas/test_pipeline_sintetico.py > "$OUT/test_pipeline_sintetico.txt" 2>&1; rc=$?
  grep -E "pruebas PASAN|comprobaciones" "$OUT/test_pipeline_sintetico.txt" | tail -1; [ $rc -eq 0 ] || fallos=$((fallos+1))
  echo "== mismos nombres de comprobación que la línea de base v2.2"
  python3 - "$OUT/test_pipeline_sintetico.txt" pruebas/linea_base/test_pipeline_sintetico_v2.2_nombres.txt > "$OUT/nombres_vs_linea_base.txt" 2>&1 <<'PY'
import re, sys
act = [m.group(2) for l in open(sys.argv[1], encoding="utf-8") if (m := re.match(r"^(PASA |FALLA) · (.*?)(?: · |$)", l.rstrip("\n")))]
base = [l.rstrip("\n") for l in open(sys.argv[2], encoding="utf-8") if l.strip() and not l.startswith("#")]
falt, sobr = [b for b in base if b not in act], [a for a in act if a not in base]
print(f"línea de base {len(base)} · ahora {len(act)} · faltan {len(falt)} · nuevas {len(sobr)}")
for x in falt: print("  falta:", x)
for x in sobr: print("  nueva:", x)
sys.exit(0 if not falt and not sobr and len(act) == len(base) else 1)
PY
  rc=$?; cat "$OUT/nombres_vs_linea_base.txt" | head -1; [ $rc -eq 0 ] || fallos=$((fallos+1))
fi

echo "RESULTADO: $([ $fallos -eq 0 ] && echo PASA || echo "FALLA ($fallos bloques)")"
exit $fallos
