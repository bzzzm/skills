#!/usr/bin/env python3
"""Avatar generator: nano banana (gemini-3-pro-image-preview).

Generates seasonal or themed variants of Mihai's avatar, keeping the base
character consistent. Always edit from the base character image so identity
stays fixed.

Usage:
  python3 scripts/generate.py "prompt describing the theme" out_name.png
  python3 scripts/generate.py  # no args -> interactive prompt

Output goes to data/versions/<out_name>.png and is appended to data/history.json.
"""
import base64
import datetime
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_DATA_DIR = SKILL_DIR / "data" if (SKILL_DIR / "data").is_dir() else SKILL_DIR
DATA_DIR = Path(os.environ.get("AVATAR_DATA_DIR", DEFAULT_DATA_DIR))
BASE = Path(os.environ.get("AVATAR_BASE_IMAGE", DATA_DIR / "base_character.png"))
VERSIONS = DATA_DIR / "versions"
HISTORY = DATA_DIR / "history.json"


def find_env_val(key_name: str) -> str:
    """Find key in environment or search candidate .env files."""
    if key_name in os.environ:
        return os.environ[key_name]

    candidates = [
        Path.cwd() / ".env",
        SKILL_DIR / ".env",
        SKILL_DIR.parent / ".env",
    ]
    if "ENV_FILE" in os.environ:
        candidates.insert(0, Path(os.environ["ENV_FILE"]))

    for p in candidates:
        if p.is_file():
            try:
                with open(p, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("export "):
                            line = line[7:]
                        if "=" in line and not line.startswith("#"):
                            k, v = line.split("=", 1)
                            if k.strip() == key_name:
                                return v.strip().strip('"').strip("'")
            except OSError:
                continue
    return ""


def get_api_key() -> str:
    key = find_env_val("GOOGLE_API_KEY")
    if not key:
        raise RuntimeError("GOOGLE_API_KEY not found in environment or .env file.")
    return key


def get_base_image_path() -> Path:
    if BASE.is_file():
        return BASE
    fallback = SKILL_DIR / "base_character.png"
    if fallback.is_file():
        return fallback
    raise FileNotFoundError(
        f"Base character image not found at {BASE}. "
        f"Place base_character.png beside SKILL.md or set AVATAR_BASE_IMAGE."
    )


IDENTITY = (
    "Keep the character IDENTICAL: fair-skinned Caucasian woman, muted auburn "
    "(soft copper, not vivid) short hair, same face, confident smirk, raised "
    "eyebrow, same pose (hands on hips, head tilt), same flat vector art style "
    "with thick clean outlines, square 1:1. "
)


def generate(prompt: str, out_path: Path):
    base_path = get_base_image_path()
    with open(base_path, "rb") as f:
        b = base64.b64encode(f.read()).decode()

    key = get_api_key()
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-3-pro-image-preview:generateContent?key={key}"
    )

    body = json.dumps({
        "contents": [{"parts": [
            {"text": IDENTITY + prompt},
            {"inline_data": {"mime_type": "image/png", "data": b}},
        ]}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
    }).encode()

    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    r = json.load(urllib.request.urlopen(req, timeout=240))
    for part in r["candidates"][0]["content"]["parts"]:
        if "inlineData" in part:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            with open(out_path, "wb") as out_f:
                out_f.write(base64.b64decode(part["inlineData"]["data"]))
            return
    raise RuntimeError("No image in response: " + json.dumps(r)[:300])


def add_history(name: str, prompt: str, path: Path):
    h = {"entries": []}
    if HISTORY.is_file():
        try:
            with open(HISTORY, "r", encoding="utf-8") as f:
                old = json.load(f)
            h["base_character"] = old.get("base_character", "base_character.png")
            h["description"] = old.get("description", "")
            h["entries"] = old.get("entries", [])
        except (json.JSONDecodeError, OSError):
            pass

    try:
        rel_file = str(path.relative_to(SKILL_DIR))
    except ValueError:
        rel_file = str(path)

    h["entries"].append({
        "name": name,
        "prompt": prompt,
        "file": rel_file,
        "status": "generated",
        "created": datetime.datetime.now().isoformat(timespec="seconds"),
    })
    HISTORY.parent.mkdir(parents=True, exist_ok=True)
    with open(HISTORY, "w", encoding="utf-8") as f:
        json.dump(h, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    try:
        VERSIONS.mkdir(parents=True, exist_ok=True)
    except OSError:
        pass
    if len(sys.argv) >= 3:
        prompt, name = sys.argv[1], sys.argv[2]
    else:
        prompt = input("Theme prompt: ").strip()
        name = input("Name (e.g. christmas): ").strip()
    if not name.endswith(".png"):
        name = f"{name}.png"
    out = VERSIONS / name
    generate(prompt, out)
    add_history(Path(name).stem, prompt, out)
    print("saved", out)
