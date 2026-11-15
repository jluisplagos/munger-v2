"""Recupera los binarios disponibles de la base 4.14, sin sobrescribir cambios."""
import argparse
import json
import os
from pathlib import Path
import shutil
import tempfile
import zipfile

import base_414 as base


def restore(bundle, metadata, data):
    if bundle.stat().st_size != metadata["bundle_size"] or base.sha_file(bundle) != metadata["bundle_sha256"]:
        raise ValueError("El paquete de binarios no coincide con su tamaño y SHA-256.")
    selected = [e for e in data["files"] if e["storage"] == "release_asset"]
    objects = {e["sha256"] for e in selected}
    included = set(metadata["objects"])
    if not included.issubset(objects):
        raise ValueError("El índice contiene objetos ajenos a la base.")
    with zipfile.ZipFile(bundle) as z:
        if len(z.namelist()) != len(set(z.namelist())) or set(z.namelist()) != {"objects/" + h for h in included}:
            raise ValueError("El ZIP no contiene exactamente los objetos declarados.")
        # Comprobar todo el paquete y todos los destinos antes de copiar.
        for h in included:
            with z.open("objects/" + h) as f:
                if base.sha_stream(f) != h:
                    raise ValueError("Objeto de binario alterado: " + h)
        for e in selected:
            if e["sha256"] not in included:
                continue
            target = base.destination(e["path"])
            if target.exists() and (not target.is_file() or base.sha_file(target) != e["sha256"]):
                raise ValueError("No se sobrescribe un archivo distinto: " + e["path"])
        restored = 0
        for e in selected:
            if e["sha256"] not in included:
                continue
            target = base.destination(e["path"])
            if target.exists():
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            fd, name = tempfile.mkstemp(prefix=".restore-", dir=target.parent)
            temp = Path(name)
            try:
                with os.fdopen(fd, "wb") as out:
                    with z.open("objects/" + e["sha256"]) as src:
                        shutil.copyfileobj(src, out, 1024 * 1024)
                if base.sha_file(temp) != e["sha256"]:
                    raise ValueError("La copia del binario no coincide.")
                temp.replace(target)
                restored += 1
            finally:
                temp.unlink(missing_ok=True)
    report = base.verify(data)
    report["binary_files_restored"] = restored
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="ZIP de binarios disponibles descargado de Releases")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    metadata = json.loads((base.REPO / "baselines/4.14_assets.json").read_text(encoding="utf-8"))
    report = restore(args.source, metadata, base.inventory())
    if args.report:
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: len(v) if isinstance(v, list) else v for k, v in report.items()}, ensure_ascii=False, indent=2))
    return 0 if report["complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
