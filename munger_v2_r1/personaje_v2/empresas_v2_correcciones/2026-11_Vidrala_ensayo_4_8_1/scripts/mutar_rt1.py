#!/usr/bin/env python3
"""Mutaciones del código de R-T1 (entrega 4.8.1). Cada mutación tiene que hacer fallar al menos una prueba de
pruebas/test_auditorias_v2.py.

Uso: python3 -I mutar_rt1.py <COPIA de munger_v2_r1>
(M6 de la primera versión, «la huella del informe ya consumido no se anota», se retiró: tras la auditoría interna, Y-b, esa anotación
se sustituyó por la de todas las auditorías del expediente, M11.) Modifica la copia que recibe; nunca se ejecuta sobre el árbol entregado. Restaura el código de la copia al terminar.
"""
import os, shutil, subprocess, sys
RAIZ = sys.argv[1]  # copia de munger_v2_r1 en un temporal
P = os.path.join(RAIZ, "personaje_v2", "scripts", "pipeline.py"); C = os.path.join(RAIZ, "personaje_v2", "scripts", "cierre_v2.py")
ORIG = {P: open(P, encoding="utf-8").read(), C: open(C, encoding="utf-8").read()}
MUT = [
 ("M1 no se exige la línea de solicitud (cualquier informe nuevo vale)", P, [('elif ida is None:', 'elif False:'), ('elif ida != sol["id"]:', 'elif False:')]),
 ("M2 no se comprueba la huella de las auditorías ya usadas", P, [('if aprobaria and h in self.huellas_auditorias_usadas():', 'if False:')]),
 ("M3 la solicitud pendiente se sustituye en cada relanzamiento", P, [('if actual and actual.get("material") == mat:', 'if False:')]),
 ("M4 el paso 14 no mira las solicitudes pendientes", P, [('if pendientes else CIE.motivo_rechazo_cierre', 'if False else CIE.motivo_rechazo_cierre')]),
 ("M5 el cierre no compara la respuesta registrada", C, [('if (resp.get("contenido") or "") != huella_contenido(txt) and resp.get("sha256") != sha_archivo(p):', 'if False:')]),
 ("M7 identificador previsible (derivado solo del material)", C, [('semilla = f"{material_id}|{ahora}|{os.urandom(16).hex()}"', 'semilla = f"{material_id}"')]),
 ("M8 la respuesta aceptada no marca la solicitud como respondida", P, [('sol.update(estado="respondida", respuesta_sha256=h,', 'sol.update(respuesta_sha256=h,')]),
 ("M9 no se compara el contenido con el de las auditorías ya usadas", P, [('elif aprobaria and hc in self.contenidos_auditorias_usadas():', 'elif False:')]),
 # (auditoría interna de la 4.8.1, Y-a, Y-b, Y-g, Y-h, Y-i y Y-j)
 ("M10 la huella de contenido solo quita espacios (no puntuación, tildes ni forma Unicode)", C, [('palabras = re.findall(r"[^\\W_]+", _sin_diacriticos("\\n".join(lineas)).casefold())', 'palabras = "\\n".join(lineas).split()')]),
 ("M11 no se anotan las auditorías del expediente al registrar la solicitud", P, [('shas, conts = CIE.auditorias_del_expediente(self.c, self.veredicto_auditoria)', 'shas, conts = set(), set()')]),
 ("M12 el registro persistente no se consulta", P, [('set(self.st.get("anteriores_sha256") or []) | CIE.registro_auditorias(self.c)[0]', 'set(self.st.get("anteriores_sha256") or [])'),
                                                  ('set(self.st.get("anteriores_contenido") or []) | CIE.registro_auditorias(self.c)[1]', 'set(self.st.get("anteriores_contenido") or [])')]),
 ("M13 pedir una auditoría nueva no archiva el cierre vigente", P, [('        if CIE.ficha_cerrada(F):\n            # (Y-h)', '        if False:\n            # (Y-h)')]),
 ("M14 motivo_rechazo_cierre no mira las solicitudes pendientes", C, [('    if pend:\n        # (4.8.1, Y-h', '    if False:\n        # (4.8.1, Y-h')]),
 ("M15 el cierre anterior a la 4.8.1 no se compara con cierre_vigente.json", C, [('if cv.get("auditoria_sha256") and cv["auditoria_sha256"] != sha_archivo(p):', 'if False:')]),
 ("M17 la regla de reutilización se aplica también a las respuestas que no aprueban", P, [('aprobaria = self.veredicto_auditoria(txt) == "APROBADO"', 'aprobaria = True')]),
 # (control de vigencia de la 4.8.1, V-1, V-2 y V-9)
 ("M18 la huella de contenido depende del orden", C, [('return hashlib.sha256("\\n".join(sorted(palabras)).encode("utf-8")).hexdigest()', 'return hashlib.sha256("\\n".join(palabras).encode("utf-8")).hexdigest()')]),
 ("M19 la huella de contenido conserva las tildes", C, [('palabras = re.findall(r"[^\\W_]+", _sin_diacriticos("\\n".join(lineas)).casefold())', 'palabras = re.findall(r"[^\\W_]+", "\\n".join(lineas).casefold())')]),
 ("M20 solo se anotan los auditoria*.md", C, [('            if parece_auditoria(txt, veredicto):', '            if f.startswith("auditoria") and f.endswith(".md") and parece_auditoria(txt, veredicto):')]),
 ("M21 un registro ilegible se trata como vacío", C, [('        raise RegistroAuditoriasIlegible(', '        return set(), set()\n        raise RegistroAuditoriasIlegible(')]),
 # (tercera revisión de la 4.8.1, W-1 a W-3 y W-5e)
 ("M22 la huella de contenido vuelve a depender del corte de las líneas", C, [('palabras = re.findall(r"[^\\W_]+", _sin_diacriticos("\\n".join(lineas)).casefold())', 'palabras = [re.sub(r"[\\W_]+", "", _sin_diacriticos(l).casefold()) for l in lineas]')]),
 ("M23 solo se recorren la carpeta y historial_cierres/", C, [('dirs[:] = [d for d in dirs if d not in ("__pycache__", ".lo_perfil")]', 'dirs[:] = [d for d in dirs if d == "historial_cierres" or "historial_cierres" in raiz]')]),
 ("M24 solo se leen textos en UTF-8", C, [('for cod in ("utf-8-sig", "cp1252"):', 'for cod in ("utf-8",):'), ('if b[:2] in (b"\\xff\\xfe", b"\\xfe\\xff"):', 'if False:')]),
 ("M25 una respuesta que no es UTF-8 válido se consume", P, [('            if not utf8:', '            if False:')]),
 ("M26 el registro no valida los tipos", C, [('if not (isinstance(s, list) and isinstance(c, list) and all(isinstance(x, str) for x in s + c)):', 'if False:')]),
 ("M16 la respuesta registrada se compara solo por bytes", C, [('if (resp.get("contenido") or "") != huella_contenido(txt) and resp.get("sha256") != sha_archivo(p):', 'if resp.get("sha256") != sha_archivo(p):')]),
]
vivas = []
for nombre, f, cambios in MUT:
    for g, t in ORIG.items(): open(g, "w", encoding="utf-8").write(t)
    t = ORIG[f]
    for a, b in cambios:
        assert t.count(a) == 1, (nombre, a); t = t.replace(a, b)
    open(f, "w", encoding="utf-8").write(t)
    r = subprocess.run([sys.executable, "-B", "pruebas/test_auditorias_v2.py"], cwd=os.path.join(RAIZ, "personaje_v2"), capture_output=True, text=True)
    fin = (r.stdout.strip().splitlines() or [""])[-1]
    fallan = [l.split(" · ")[2][:70] for l in r.stdout.splitlines() if l.startswith("FALLA")]
    muerta = r.returncode != 0
    if not muerta: vivas.append(nombre)
    print(f"{nombre}: {'DETECTADA' if muerta else 'NO DETECTADA'} · {fin} · primeras que fallan: {fallan[:3]}")
for g, t in ORIG.items(): open(g, "w", encoding="utf-8").write(t)
print(f"RESULTADO: {len(MUT) - len(vivas)} de {len(MUT)} mutaciones detectadas")
sys.exit(0 if not vivas else 1)
