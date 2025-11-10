#!/usr/bin/env python3
"""
Batch-export SVG icons to PNG.

Usage:
  python3 export_svgs.py --input assets/icons --output assets/icons/png --sizes 1024 512 192 128

This script will try, in order:
  1) Use the Python library `cairosvg` if installed.
  2) Fall back to CLI tools if available: `rsvg-convert`, `inkscape`, or ImageMagick `magick/convert`.

If no backends are available, it prints installation instructions.
"""

from __future__ import annotations
import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List


def find_backend() -> str | None:
    try:
        import cairosvg  # type: ignore
        return "cairosvg"
    except Exception:
        pass

    for cmd in ("rsvg-convert", "inkscape", "magick", "convert"):
        if shutil.which(cmd):
            return cmd
    return None


def convert_with_cairosvg(svg: Path, out: Path, size: int) -> None:
    import cairosvg  # type: ignore
    # cairosvg can take url or file object
    cairosvg.svg2png(url=str(svg), write_to=str(out), output_width=size, output_height=size)


def convert_with_rsvg(svg: Path, out: Path, size: int) -> None:
    subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size), "-o", str(out), str(svg)], check=True)


def convert_with_inkscape(svg: Path, out: Path, size: int) -> None:
    # modern inkscape CLI
    # inkscape input.svg --export-type=png --export-filename=out.png --export-width=512 --export-height=512
    subprocess.run([
        "inkscape",
        str(svg),
        "--export-type=png",
        "--export-filename",
        str(out),
        "--export-width",
        str(size),
        "--export-height",
        str(size),
    ], check=True)


def convert_with_magick(svg: Path, out: Path, size: int) -> None:
    cmd = "magick" if shutil.which("magick") else "convert"
    subprocess.run([cmd, "-background", "none", "-resize", f"{size}x{size}", str(svg), str(out)], check=True)


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def export_all(input_dir: Path, output_dir: Path, sizes: List[int], backend: str | None = None) -> int:
    svgs = sorted([p for p in input_dir.glob("*.svg")])
    if not svgs:
        print(f"No SVGs found in {input_dir}")
        return 1

    ensure_dir(output_dir)

    if backend is None:
        backend = find_backend()

    if backend is None:
        print("No available backend for SVG->PNG conversion found.")
        print("Install the Python package 'cairosvg' (recommended) or one of: rsvg-convert, inkscape, ImageMagick.")
        print("Example: pip install cairosvg")
        return 2

    print(f"Using backend: {backend}")

    for svg in svgs:
        name = svg.stem
        for size in sizes:
            out = output_dir / f"{name}-{size}.png"
            try:
                print(f"Exporting {svg.name} -> {out.name} ({size}x{size})")
                if backend == "cairosvg":
                    convert_with_cairosvg(svg, out, size)
                elif backend == "rsvg-convert":
                    convert_with_rsvg(svg, out, size)
                elif backend == "inkscape":
                    convert_with_inkscape(svg, out, size)
                elif backend in ("magick", "convert"):
                    convert_with_magick(svg, out, size)
                else:
                    # safety fallback try cairosvg if present
                    try:
                        convert_with_cairosvg(svg, out, size)
                    except Exception:
                        raise RuntimeError("Unsupported backend: %r" % backend)
            except subprocess.CalledProcessError as e:
                print(f"Command failed: {e}")
            except Exception as e:
                print(f"Failed to export {svg} @ {size}px: {e}")
    return 0


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Batch export SVG icons to PNG")
    p.add_argument("--input", "-i", default="assets/icons", help="Input folder with SVG files")
    p.add_argument("--output", "-o", default="assets/icons/png", help="Output folder for PNG files")
    p.add_argument("--sizes", "-s", nargs="*", type=int, default=[1024, 512, 192, 128], help="Sizes to export (px). Default: 1024 512 192 128")
    p.add_argument("--backend", "-b", choices=["cairosvg", "rsvg-convert", "inkscape", "magick", "convert"], help="Force a backend (optional)")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    input_dir = Path(args.input)
    output_dir = Path(args.output)
    sizes = args.sizes

    rc = export_all(input_dir, output_dir, sizes, backend=args.backend)
    sys.exit(rc)


if __name__ == "__main__":
    main()
