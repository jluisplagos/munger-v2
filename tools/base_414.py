"""Materializa o comprueba la base exacta 4.14. Solo biblioteca estándar.
No acepta una base incompleta ni sobrescribe archivos modificados.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import tempfile
import zipfile

REPO = Path(__file__).resolve().parents[1]
INDEX = REPO / "baselines" / "4.14.json"
ROOT = REPO / "munger_v2_r1"


def sha_stream(stream):
    h = hashlib.sha256()
    for block in iter(lambda: stream.read(1024 * 1024), b""):
        h.update(block)
    return h.hexdigest()


def sha_file(path):
    with path.open("rb") as f:
        return sha_stream(f)


def inventory():
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    seen = set()
    for e in data["files"]:
        p = PurePosixPath(e["path"])
        if p.is_absolute() or ".." in p.parts or "\\" in e["path"] or e["path"] in seen:
            raise ValueError("Ruta insegura o repetida: " + e["path"])
        seen.add(e["path"])
    return data


def destination(name):
    p = ROOT / name
    if p.is_symlink() or not p.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError("Enlace o ruta de salida en el destino: " + name)
    return p


def verify(data, git_only=False):
    selected = [e for e in data["files"] if not git_only or e["storage"] == "git"]
    good, missing, changed = [], [], []
    for e in selected:
        p = destination(e["path"])
        if not p.is_file():
            missing.append(e["path"])
        elif sha_file(p) != e["sha256"]:
            changed.append(e["path"])
        else:
            good.append(e["path"])
    original = destination("MANIFIESTO_SHA256.txt")
    if not original.is_file():
        missing.append("MANIFIESTO_SHA256.txt")
    elif sha_file(original) != data["manifest_sha256"]:
        changed.append("MANIFIESTO_SHA256.txt")
    return {"scope": "git_files" if git_only else "full_baseline",
            "verified": len(good), "expected": len(selected),
            "missing": missing, "changed": changed,
            "complete": not missing and not changed}


class Source:
    def __init__(self, path, data):
        self.path, self.data, self.z = path, data, None
        if path.is_file():
            if path.stat().st_size != data["zip_size"] or sha_file(path) != data["zip_sha256"]:
                raise ValueError("El ZIP no coincide con tamaño y SHA-256 de la base4.14.")
            self.z = zipfile.ZipFile(path)
            names = self.z.namelist()
            if len(names) != len(set(names)):
                raise ValueError("ZIP con miembros repetidos.")
            for info in self.z.infolist():
                name = PurePosixPath(info.filename)
                if name.is_absolute() or ".." in name.parts or "\\" in info.filename:
                    raise ValueError("Ruta insegura en ZIP.")
                if (info.external_attr >> 16) & 0o170000 == 0o120000:
                    raise ValueError("No se admiten enlaces simbólicos.")
        elif path.is_dir():
            if not (path / "MANIFIESTO_SHA256.txt").is_file():
                self.path = path / "munger_v2_r1"
            if not self.path.is_dir():
                raise ValueError("No se encuentra la carpeta munger_v2_r1.")
        else:
            raise ValueError("La fuente debe ser el ZIP completo o una extracción.")

    def open(self, name):
        if self.z:
            return self.z.open(self.data["archive_prefix"] + name)
        p = self.path / name
        if p.is_symlink() or not p.resolve().is_relative_to(self.path.resolve()):
            raise ValueError("Enlace o ruta de salida en el origen: " + name)
        return p.open("rb")

    def close(self):
        if self.z:
            self.z.close()


def materialize(data, source_path, git_only):
    source = Source(source_path, data)
    selected = [e for e in data["files"] if not git_only or e["storage"] == "git"]
    try:
        # Verificar todo el origen antes de modificar la copia de trabajo.
        with source.open("MANIFIESTO_SHA256.txt") as f:
            if sha_stream(f) != data["manifest_sha256"]:
                raise ValueError("El manifiesto de origen no coincide.")
        for e in data["files"]:
            with source.open(e["path"]) as f:
                if sha_stream(f) != e["sha256"]:
                    raise ValueError("Origen incompleto o alterado: " + e["path"])
        selected += [{"path": "MANIFIESTO_SHA256.txt", "sha256": data["manifest_sha256"]}]
        for e in selected:
            target = destination(e["path"])
            if target.exists() and (not target.is_file() or sha_file(target) != e["sha256"]):
                raise ValueError("No se sobrescribe un archivo distinto: " + e["path"])
        added = 0
        for e in selected:
            target = destination(e["path"])
            if target.exists():
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            fd, temp_name = tempfile.mkstemp(prefix=".restore-", dir=target.parent)
            temp_path = Path(temp_name)
            try:
                with os.fdopen(fd, "wb") as out, source.open(e["path"]) as inp:
                    shutil.copyfileobj(inp, out, 1024 * 1024)
                if sha_file(temp_path) != e["sha256"]:
                    raise ValueError("No coincide el archivo recuperado: " + e["path"])
                os.replace(temp_path, target)
                added += 1
            finally:
                temp_path.unlink(missing_ok=True)
        print("Archivos recuperados:", added)
    finally:
        source.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["verify", "materialize"])
    parser.add_argument("--source", type=Path, help="ZIP completo o carpeta extraída de la base4.14")
    parser.add_argument("--git-only", action="store_true", help="Destino limitado a los archivos que se versionan en Git")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    data = inventory()
    if args.command == "materialize":
        if args.source is None:
            parser.error("materialize requiere --source")
        materialize(data, args.source, args.git_only)
    report = verify(data, args.git_only)
    if args.report:
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: len(v) if k in ("missing", "changed") else v for k, v in report.items()},
                     ensure_ascii=False, indent=2))
    return 0 if report["complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
