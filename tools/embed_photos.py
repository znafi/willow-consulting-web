"""Embed photos/*.jpg into index.html so the page stays a single self-contained file.

Run after replacing any photo:   python tools/embed_photos.py

Expected files in photos/:
  <member>.jpg            full photo (drawer)      member = alvi, fatimah, kashifa, abby
  <member>-portrait.jpg   4:5 crop (bio panel)
  <member>-avatar.jpg     square face crop (menu, buttons)
  team.jpg                group photo
"""
import base64, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
photos = {}
for f in sorted((ROOT / 'photos').glob('*.jpg')):
    key, _, kind = f.stem.partition('-')
    uri = 'data:image/jpeg;base64,' + base64.b64encode(f.read_bytes()).decode()
    photos.setdefault(key, {})[kind or 'full'] = uri

page = ROOT / 'index.html'
html = page.read_text(encoding='utf-8')
block = '<script id="photo-data">window.PHOTOS=' + json.dumps(photos, separators=(',', ':')) + ';</script>'
html, n = re.subn(r'<script id="photo-data">.*?</script>', lambda m: block, html, flags=re.S)
if n != 1:
    raise SystemExit('photo-data placeholder not found in index.html')
page.write_text(html, encoding='utf-8')
print('embedded', {k: sorted(v) for k, v in photos.items()}, f'-> {len(html) / 1024:.0f} KB')
