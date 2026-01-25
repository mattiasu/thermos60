#!/usr/bin/env python3
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PHOTOS_DIR = ROOT / "public" / "photos"
OUT_FILE = ROOT / "public" / "photos.json"

VALID_EXT = {".jpg", ".jpeg", ".png", ".webp"}

def main():
  files = sorted([p for p in PHOTOS_DIR.iterdir() if p.suffix.lower() in VALID_EXT])
  items = []

  for p in files:
    with Image.open(p) as img:
      w, h = img.size

    items.append({
      "src": f"/photos/{p.name}",
      "w": w,
      "h": h
      # Optional: "thumb": f"/photos/thumbs/{p.name}"
    })

  OUT_FILE.write_text(json.dumps(items, indent=2), encoding="utf-8")
  print(f"Wrote {OUT_FILE} with {len(items)} photos.")

if __name__ == "__main__":
  main()