#!/usr/bin/env python3
import re
import sys
from pathlib import Path

# Image extensions to consider (edit as needed)
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".heic"}

TARGET_RE = re.compile(r"^IMG_(\d{3})\.jpeg$")  # exact convention

def is_image(p: Path) -> bool:
    return p.is_file() and p.suffix.lower() in IMAGE_EXTS

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} /path/to/folder")
        sys.exit(2)

    folder = Path(sys.argv[1]).expanduser().resolve()
    if not folder.is_dir():
        print(f"Error: not a folder: {folder}")
        sys.exit(2)

    files = [p for p in folder.iterdir() if is_image(p)]

    # Find used IMG_###.jpeg numbers
    used_numbers = set()
    for p in files:
        m = TARGET_RE.match(p.name)
        if m:
            used_numbers.add(int(m.group(1)))

    def next_free(start_from: int) -> int:
        n = start_from
        while n in used_numbers or (folder / f"IMG_{n:03d}.jpeg").exists():
            n += 1
        return n

    next_num = next_free(max(used_numbers) + 1 if used_numbers else 1)

    # Pick files that are images but not already compliant
    to_rename = [p for p in files if not TARGET_RE.match(p.name)]
    # Stable order to make results deterministic
    to_rename.sort(key=lambda p: p.name.lower())

    if not to_rename:
        print("Nothing to rename.")
        return

    print(f"Folder: {folder}")
    print(f"Found {len(used_numbers)} existing IMG_###.jpeg files.")
    print(f"Renaming {len(to_rename)} files...")

    # 1) Move everything to temporary names to avoid collisions
    temp_map = {}
    for i, p in enumerate(to_rename, start=1):
        tmp = folder / f".__tmp__rename__{i}__{p.name}"
        if tmp.exists():
            print(f"Error: temp file already exists: {tmp}")
            sys.exit(1)
        p.rename(tmp)
        temp_map[tmp] = p

    # 2) Rename temp files to final IMG_###.jpeg names
    for tmp in sorted(temp_map.keys(), key=lambda p: p.name.lower()):
        n = next_free(next_num)
        target = folder / f"IMG_{n:03d}.jpeg"
        tmp.rename(target)
        used_numbers.add(n)
        next_num = n + 1
        print(f"{tmp.name} -> {target.name}")

    print("Done.")

if __name__ == "__main__":
    main()