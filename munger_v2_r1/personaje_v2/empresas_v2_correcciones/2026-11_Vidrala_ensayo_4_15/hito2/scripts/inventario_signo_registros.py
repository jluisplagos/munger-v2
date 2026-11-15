"""(4.15, hito 2, R415-SIGNO) Inventario (no acredita nada): para cada entrada numérica con fuente local de texto de los registros
reales, el signo con que la página citada publica «valor_fuente» (verificacion_entradas._cita_cifra con el pasaje de la página).
Solo lee; no modifica ningún expediente.
Uso: python3 -I -B inventario_signo_registros.py <personaje_v2> <expediente> [<expediente> …] > SALIDA.json"""
import collections, json, os, sys
PV = os.path.abspath(sys.argv[1])
sys.path.insert(0, os.path.join(PV, "scripts"))
import verificacion_entradas as VE  # noqa: E402

out = {}
for exp in sys.argv[2:]:
    reg, err = VE.cargar(exp)
    if reg is None:
        out[exp] = {"error": err}
        continue
    cuenta, casos = collections.Counter(), []
    for e in reg["entradas"]:
        f = e.get("fuente") if isinstance(e.get("fuente"), dict) else {}
        vf = f.get("valor_fuente")
        if not VE._num(vf) or e.get("clase") not in ("dato_publicado", "cero_comprobado"):
            continue
        ruta = VE._ruta_fuente(exp, f.get("archivo")) if f.get("archivo") else None
        pag = None
        if ruta and str(ruta).lower().endswith(".txt"):
            est, txt = VE._pagina_examinable(ruta, f.get("pagina"))
            pag = txt if est == "ok" else None
        elif ruta and f.get("archivo_texto"):
            rt = VE._ruta_fuente(exp, f.get("archivo_texto"))
            est, txt = VE._pagina_examinable(rt, f.get("pagina")) if rt else ("", None)
            pag = txt if est == "ok" else None
        estado, det = VE._cita_cifra(f.get("cita"), vf, pag)
        clave = ("cero" if vf == 0 else "negativo" if vf < 0 else "positivo") + " · " + estado + (" · con página" if pag is not None else " · sin página")
        cuenta[clave] += 1
        if estado != "ok":
            casos.append({"celda": e.get("celda"), "valor_fuente": vf, "signo": f.get("signo"), "estado": estado, "detalle": det, "cita": f.get("cita")})
    out[os.path.relpath(exp, PV)] = {"recuento": dict(sorted(cuenta.items())), "no_ok": casos}
json.dump(out, sys.stdout, ensure_ascii=False, indent=1)
