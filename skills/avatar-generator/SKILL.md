---
name: avatar-generator
description: Generate themed variants of Mihai's avatar or update platform profile photos. Use when Mihai asks for avatar variants, seasonal character themes, or avatar updates.
---

# Avatar generator

Mihai's avatar project: flat vector female character with seasonal or themed variants.

## Locations

All paths are relative to this skill directory:

- Files: `base_character.png` (chosen base: variant B with headband), `versions/`, `history.json`, and `original_reference.png` sit beside `SKILL.md`. If `base_character.png` is missing, place the base character image in this directory before generating.
- Scripts: `scripts/generate.py`, `scripts/set_discord_avatar.py`, `scripts/set_tg_avatar.py`.
- Environment: `GOOGLE_API_KEY`, `DISCORD_BOT_TOKEN`, and `TELEGRAM_BOT_TOKEN` loaded from environment variables or a `.env` file in the current working directory or skill root.

## Usage

```bash
python3 scripts/generate.py "<theme prompt>" <name>.png
```

Output goes to `versions/<name>.png`, auto-appended to `history.json`.

## Rules

- Model: nano banana (`gemini-3-pro-image-preview`) via Google API.
- Always edit from `base_character.png` so identity stays consistent. If `base_character.png` is missing, obtain or supply the base character image first.
- Identity prompt is baked into the script: fair-skinned Caucasian woman, muted auburn short hair, confident smirk, raised eyebrow, hands on hips, head tilt, flat vector style, thick outlines, 1:1.
- Theme prompt only describes clothes, props, background, and expression tweaks.
- Avoid trademarked logos (generic red jersey for Liverpool, no crests).
- After generating: verify with vision (same character, theme present, no artifacts), then send the file to Mihai on Telegram with a MEDIA- path.
- Mark chosen variants as `"status": "CHOSEN"` in `history.json`.
- Chosen base so far: 'harvest' variant. Liverpool variant exists.

## Applying the avatar to platforms

- Discord: run `python3 scripts/set_discord_avatar.py <path/to/image.png>`. Uses `DISCORD_BOT_TOKEN`.
- Telegram: run `python3 scripts/set_tg_avatar.py <path/to/image.png>`. Uses `TELEGRAM_BOT_TOKEN`. Uses the `setMyProfilePhoto` Bot API method (requires JPEG; script converts via Pillow or ImageMagick `convert`).
- Verify both by reading back profile photo or avatar URL after the call.