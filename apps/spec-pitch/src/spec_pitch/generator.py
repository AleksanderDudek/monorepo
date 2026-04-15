import json

import anthropic


def generate(row: dict, cfg) -> dict:
    prompt = cfg.prompt_template.format(
        name=row["name"],
        nip=row["nip"],
        url_or_none=row.get("url") or "brak",
        email_or_none=row.get("email") or "brak",
        phone_or_none=row.get("phone") or "brak",
        pkd_or_none=row.get("pkd") or "brak",
        notes_or_none=row.get("notes") or "brak",
    )

    client = anthropic.Anthropic(api_key=cfg.anthropic_api_key)
    msg = client.messages.create(
        model=cfg.model,
        max_tokens=8000,
        messages=[{"role": "user", "content": prompt}],
    )

    text = msg.content[0].text.strip()

    # Strip accidental markdown fences if the model wraps the JSON
    if text.startswith("```"):
        parts = text.split("```")
        text = parts[1] if len(parts) > 1 else text
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()

    data = json.loads(text)
    if "html" not in data or "css" not in data:
        raise ValueError(f"Response missing 'html' or 'css' keys (got: {list(data.keys())})")

    return data
