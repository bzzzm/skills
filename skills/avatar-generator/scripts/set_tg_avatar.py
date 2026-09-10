#!/usr/bin/env python3
"""Set Telegram bot profile photo. Usage: python3 scripts/set_tg_avatar.py <image.png>"""
import io
import json
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
import uuid
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


def to_jpeg_bytes(img_path: Path) -> bytes:
    """Convert input image to JPEG bytes using PIL or ImageMagick convert."""
    try:
        from PIL import Image
        jpg = io.BytesIO()
        Image.open(img_path).convert("RGB").save(jpg, "JPEG", quality=95)
        return jpg.getvalue()
    except ImportError:
        pass

    if shutil.which("convert"):
        res = subprocess.run(
            ["convert", str(img_path), "jpg:-"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        return res.stdout

    raise RuntimeError("Pillow or ImageMagick 'convert' is required to convert image to JPEG.")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/set_tg_avatar.py <image.png>", file=sys.stderr)
        sys.exit(1)

    token = find_env_val("TELEGRAM_BOT_TOKEN")
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN not found in environment or .env file.", file=sys.stderr)
        sys.exit(1)

    img_path = Path(sys.argv[1]).resolve()
    if not img_path.is_file():
        print(f"Error: image file not found: {img_path}", file=sys.stderr)
        sys.exit(1)

    try:
        jpg_bytes = to_jpeg_bytes(img_path)
    except Exception as e:
        print(f"Error converting image: {e}", file=sys.stderr)
        sys.exit(1)

    boundary = uuid.uuid4().hex
    body = b""
    body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"photo\"\r\nContent-Type: application/json\r\n\r\n".encode()
    body += json.dumps({"type": "static", "photo": "attach://file"}).encode() + b"\r\n"
    body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"avatar.jpg\"\r\nContent-Type: image/jpeg\r\n\r\n".encode()
    body += jpg_bytes + b"\r\n"
    body += f"--{boundary}--\r\n".encode()

    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/setMyProfilePhoto",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    try:
        r = json.load(urllib.request.urlopen(req, timeout=60))
        print(json.dumps(r))
    except urllib.error.HTTPError as e:
        print("ERR:", e.read().decode()[:300], file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
