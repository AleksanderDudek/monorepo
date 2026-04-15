import json
from datetime import datetime, timezone
from pathlib import Path


def write(output_root: Path, nip: str, result: dict, model: str) -> None:
    target = output_root / nip
    target.mkdir(parents=True, exist_ok=True)

    (target / "index.html").write_text(result["html"], encoding="utf-8")
    (target / "styles.css").write_text(result["css"], encoding="utf-8")
    (target / "meta.json").write_text(
        json.dumps(
            {
                "nip": nip,
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "model": model,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
