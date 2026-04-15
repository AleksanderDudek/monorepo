import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    anthropic_api_key: str
    csv_path: Path
    output_root: Path
    prompt_template: str
    model: str
    pages_base_url: str  # e.g. https://aleksanderdudek.github.io/monorepo


def load_config() -> Config:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY is not set")

    csv_path = Path(os.getenv("CSV_PATH", "prospects.csv"))
    output_root = Path(os.getenv("OUTPUT_ROOT", "../../spec-sites"))
    prompt_path = Path(os.getenv("PROMPT_PATH", "prompt.md"))
    model = os.getenv("MODEL", "claude-sonnet-4-6")
    pages_base_url = os.getenv("PAGES_BASE_URL", "").rstrip("/")

    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    prompt_template = prompt_path.read_text(encoding="utf-8")

    return Config(
        anthropic_api_key=api_key,
        csv_path=csv_path,
        output_root=output_root,
        prompt_template=prompt_template,
        model=model,
        pages_base_url=pages_base_url,
    )
