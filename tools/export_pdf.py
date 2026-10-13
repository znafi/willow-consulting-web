"""Export the scroll experience as a PDF of 1440x900 frames for the Canvas submission.

Usage:  pip install playwright pillow && python -m playwright install chromium
        python tools/export_pdf.py "Group 07"      ->  Group 07_Biographies_2WEBPAGE.pdf
"""
import asyncio, pathlib, sys
from playwright.async_api import async_playwright
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
GROUP = sys.argv[1] if len(sys.argv) > 1 else 'Group XX'
OUT = ROOT / f'{GROUP}_Biographies_2WEBPAGE.pdf'
# scroll progress per frame (1 unit = one section); 0.62 shows the portal window
FRAMES = [0.0, 0.62, 1.03, 2.03, 3.03, 4.03, 5.25]


async def main():
    shots = []
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'])
        pg = await b.new_page(viewport={'width': 1440, 'height': 900}, device_scale_factor=2)
        await pg.goto((ROOT / 'index.html').as_uri())
        await pg.wait_for_timeout(6000)
        for i, f in enumerate(FRAMES):
            await pg.evaluate(f'scrollTo(0, {f} * innerHeight * 1.3)')
            await pg.wait_for_timeout(5000)
            path = ROOT / f'.frame_{i}.png'
            await pg.screenshot(path=str(path))
            shots.append(path)
        await pg.click('#menu-btn')
        await pg.wait_for_timeout(1500)
        path = ROOT / '.frame_menu.png'
        await pg.screenshot(path=str(path))
        shots.append(path)
        await b.close()
    pages = [Image.open(s).convert('RGB') for s in shots]
    pages[0].save(OUT, save_all=True, append_images=pages[1:], resolution=200, quality=90)
    for s in shots:
        s.unlink()
    print('wrote', OUT)

asyncio.run(main())
