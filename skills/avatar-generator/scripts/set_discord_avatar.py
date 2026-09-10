#!/usr/bin/env python3
"""Set Discord bot avatar. Usage: python3 scripts/set_discord_avatar.py <image.png>"""
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent


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


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/set_discord_avatar.py <image.png>", file=sys.stderr)
        sys.exit(1)

    token = find_env_val("DISCORD_BOT_TOKEN")
    if not token:
        print("Error: DISCORD_BOT_TOKEN not found in environment or .env file.", file=sys.stderr)
        sys.exit(1)

    img_path = Path(sys.argv[1]).resolve()
    if not img_path.is_file():
        print(f"Error: image file not found: {img_path}", file=sys.stderr)
        sys.exit(1)

    with open(img_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()

    payload = json.dumps({"avatar": f"data:image/png;base64,{img_b64}"}).encode()
    req = urllib.request.Request(
        "https://discord.com/api/v10/users/@me",
        method="PATCH",
        data=payload,
        headers={
            "Authorization": f"Bot {token}",
            "Content-Type": "application/json",
        },
    )
    try:
        r = json.load(urllib.request.urlopen(req, timeout=60))
        print("OK:", r.get("avatar"))
    except urllib.error.HTTPError as e:
        print("ERR:", e.read().decode()[:300], file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
