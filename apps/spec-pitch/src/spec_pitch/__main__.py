from datetime import datetime, timezone

from . import config as cfg_module
from . import csv_store, generator, writer


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def main() -> None:
    cfg = cfg_module.load_config()
    rows = csv_store.read(cfg.csv_path)
    pending = [r for r in rows if not r["done"]]

    if not pending:
        total = len(rows)
        done = sum(1 for r in rows if r["done"])
        print(f"Nothing to do. {done}/{total} already done.")
        return

    print(f"Processing {len(pending)} row(s) …")

    for row in pending:
        nip = row["nip"]
        name = row["name"]
        try:
            result = generator.generate(row, cfg)
            writer.write(cfg.output_root, nip, result, cfg.model)
            row["done"] = True
            row["generated_at"] = now_iso()
            row["output_path"] = f"spec-sites/{nip}"
            row["pages_url"] = (
                f"{cfg.pages_base_url}/spec-sites/{nip}/"
                if cfg.pages_base_url
                else ""
            )
            row["error"] = ""
        except Exception as exc:
            row["error"] = str(exc)[:500]

        csv_store.upsert(cfg.csv_path, row)
        status = "OK" if row["done"] else "FAIL"
        print(f"[{nip}] {status}: {name}")
        if not row["done"]:
            print(f"       └─ {row['error']}")

    rows = csv_store.read(cfg.csv_path)
    done = sum(1 for r in rows if r["done"])
    print(f"\nDone. {done}/{len(rows)} total.")


if __name__ == "__main__":
    main()
