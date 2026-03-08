#!/usr/bin/env python3
"""Generate lightweight thumbnails for landing page.

- Scans assets/images/*/main.(jpg|jpeg|png|webp)
- Generates assets/images/<slug>/thumb.jpg (center-crop) at 900x675 (4:3) by default.
- Updates matching _recipes/<slug>.md front matter (optional):
    image.thumbnail -> /assets/images/<slug>/thumb.jpg

Usage:
  python scripts/generate_thumbnails.py
  python scripts/generate_thumbnails.py --size 900x675 --quality 75 --update-front-matter
"""

import argparse
import re
from pathlib import Path

from PIL import Image, ImageOps
import yaml

IMG_DIR = Path("assets/images")
RECIPES_DIR = Path("_recipes")

def find_main_images():
    exts = ["jpg", "jpeg", "png", "webp"]
    for slug_dir in IMG_DIR.glob("*"):
        if not slug_dir.is_dir():
            continue
        for ext in exts:
            p = slug_dir / f"main.{ext}"
            if p.exists():
                yield slug_dir.name, p
                break

def center_crop_resize(im: Image.Image, size):
    if im.mode in ("RGBA", "LA"):
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        im = bg
    else:
        im = im.convert("RGB")
    return ImageOps.fit(im, size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))

def update_recipe_front_matter(slug: str, thumb_web_path: str):
    md_path = RECIPES_DIR / f"{slug}.md"
    if not md_path.exists():
        return False, f"_recipes/{slug}.md introuvable"

    text = md_path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return False, "Front matter manquant"

    parts = text.split("---", 2)
    fm = parts[1]
    body = parts[2].lstrip("\n")

    data = yaml.safe_load(fm) or {}
    img = data.get("image") or {}

    img_path = img.get("path") or f"/assets/images/{slug}/main.jpg"
    img["path"] = img_path
    img["thumbnail"] = thumb_web_path

    photos = img.get("photos")
    if isinstance(photos, list) and len(photos) > 0:
        img["photos"] = photos
    else:
        img["photos"] = [img_path]

    data["image"] = img

    new_fm = yaml.safe_dump(data, sort_keys=False, allow_unicode=True).strip()
    md_path.write_text(f"---\n{new_fm}\n---\n\n{body}", encoding="utf-8")
    return True, "OK"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--size", default="900x675", help="thumbnail size like 900x675")
    ap.add_argument("--quality", type=int, default=75, help="JPEG quality 1-95")
    ap.add_argument("--update-front-matter", action="store_true", help="update _recipes/<slug>.md thumbnail path")
    args = ap.parse_args()

    m = re.match(r"^(\d+)x(\d+)$", args.size)
    if not m:
        raise SystemExit("Invalid --size format, expected 900x675")
    size = (int(m.group(1)), int(m.group(2)))

    IMG_DIR.mkdir(parents=True, exist_ok=True)

    generated, skipped = [], []
    updated = []

    for slug, main_path in find_main_images():
        thumb_path = main_path.parent / "thumb.jpg"
        if thumb_path.exists() and thumb_path.stat().st_mtime >= main_path.stat().st_mtime:
            skipped.append(slug)
            continue

        with Image.open(main_path) as im:
            thumb = center_crop_resize(im, size)
            thumb.save(thumb_path, format="JPEG", quality=args.quality, optimize=True, progressive=True)
        generated.append(slug)

        if args.update_front_matter:
            updated.append((slug, *update_recipe_front_matter(slug, f"/assets/images/{slug}/thumb.jpg")))

    print(f"Generated thumbnails: {len(generated)}")
    if skipped:
        print(f"Up-to-date thumbnails skipped: {len(skipped)}")
    if args.update_front_matter:
        ok = sum(1 for _, success, _ in updated if success)
        print(f"Front matter updated: {ok} / {len(updated)}")
        for slug, success, msg in updated:
            if not success:
                print(f" - {slug}: {msg}")

if __name__ == "__main__":
    main()
