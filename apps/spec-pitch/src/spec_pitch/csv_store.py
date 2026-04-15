import csv
import os
import tempfile
from pathlib import Path

FIELDS = [
    "nip", "name", "url", "email", "phone", "pkd", "notes",
    "done", "generated_at", "output_path", "pages_url", "error",
]


def read(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        return [_normalize(r) for r in csv.DictReader(f)]


def write_all(path: Path, rows: list[dict]) -> None:
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    try:
        with os.fdopen(fd, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
            w.writeheader()
            for r in rows:
                w.writerow({**r, "done": "true" if r["done"] else "false"})
        os.replace(tmp, path)
    except Exception:
        os.unlink(tmp)
        raise


def upsert(path: Path, row: dict) -> None:
    rows = read(path)
    for i, r in enumerate(rows):
        if r["nip"] == row["nip"]:
            rows[i] = row
            break
    write_all(path, rows)


def _normalize(r: dict) -> dict:
    r["done"] = str(r.get("done", "")).strip().lower() == "true"
    return r
