Activity icons for the booking/appointment mini-program

Contents
- `activity-calendar-check.svg` — Calendar with check badge (confirmation)
- `activity-ticket-clock.svg` — Ticket shape with clock (booking & time)
- `activity-pin-calendar.svg` — Map pin with small calendar (location + date)

Notes
- All icons use a 1024x1024 viewBox and are fully scalable (vector SVG).
- Colors are flat/modern; you can edit fills, gradients, and strokes directly in the SVG files.

Suggested export sizes
- App icons / store: 1024x1024
- Web & app assets: 512x512, 256x256, 192x192, 128x128, 96x96
- WeChat mini-program cover/icon: follow WeChat spec — use at least 512x512 for sharpness.

Exporting to PNG (macOS / zsh)
- Using Inkscape (recommended for high-quality export):

```bash
# export 512x512
inkscape assets/icons/activity-calendar-check.svg --export-type=png --export-filename=assets/icons/activity-calendar-check-512.png --export-width=512 --export-height=512

# export 192x192
inkscape assets/icons/activity-calendar-check.svg --export-type=png --export-filename=assets/icons/activity-calendar-check-192.png --export-width=192 --export-height=192
```

- Using rsvg-convert (librsvg):

```bash
rsvg-convert -w 512 -h 512 -o assets/icons/activity-calendar-check-512.png assets/icons/activity-calendar-check.svg
```

- Using ImageMagick (if installed):

```bash
magick -background none -resize 512x512 assets/icons/activity-calendar-check.svg assets/icons/activity-calendar-check-512.png
```

Customization tips
- Change the gradient stops or primary fill to match your brand color.
- For an outlined style, set fills to "none" and add stroke attributes.
- To create a dark-mode variant, swap the background rounded square fill to a dark gradient and invert foreground colors.

Next steps I can do for you
- Produce color variants (brand color, dark mode) and export PNGs for chosen sizes.
- Produce iOS/Android adaptive icon versions if you tell me target platform and colors.
- Create a rounded-square masked PNG for platform icon previews.

Tell me which variant(s) and sizes you want exported as PNG and any brand color or style preferences.

Python batch export
-------------------

I added a small Python script to batch-export the SVGs to PNG. Files:

- `assets/icons/export_svgs.py` — script to export SVGs to PNG (defaults: 1024, 512, 192, 128 px)
- `assets/icons/requirements.txt` — lists `cairosvg` as the recommended Python dependency

Usage (macOS / zsh):

1) Create a virtualenv and install requirements (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r assets/icons/requirements.txt
```

2) Run the exporter (default input/output and sizes):

```bash
python3 assets/icons/export_svgs.py
```

3) To customize sizes or output folder:

```bash
python3 assets/icons/export_svgs.py --input assets/icons --output assets/icons/png --sizes 1024 512 192 128
```

The script will try to use the Python package `cairosvg` if installed. If not available it will fall back to CLI tools (if present): `rsvg-convert`, `inkscape`, or ImageMagick (`magick`/`convert`). If no backend is available it will print instructions to install `cairosvg`.

If you want I can run the exporter here and add the generated PNGs to the repo — tell me which sizes you want and whether you want me to try installing dependencies locally (I can only proceed if the environment allows installing packages).