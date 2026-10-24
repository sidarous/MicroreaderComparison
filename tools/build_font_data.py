#!/usr/bin/env python3
"""Build the font data used by fonts.html.

Reads a CrossPoint firmware checkout and the published SD-font release, then
writes gzipped .cpfont files plus a catalog to ./fonts/:

  fonts/catalog.json                       metadata for every family
  fonts/<Family>/<Family>_<size>.cpfont.gz  downloadable fonts (byte-identical
                                            to the release files, gzipped)
  fonts/NotoSans/NotoSans_<size>.cpfont.gz  built-in reader font, converted
                                            from the firmware's C headers
  fonts/ui/Small_8.cpfont.gz               status-bar font (built-in)

Usage:
  python3 tools/build_font_data.py --firmware /path/to/crosspoint-reader

The firmware checkout must be at the tag the page describes (2.0.0rc).
Requires PyYAML.
"""

from __future__ import annotations

import argparse
import gzip
import json
import os
import re
import struct
import sys
import urllib.request
import zlib

import yaml

RELEASE = "sd-fonts-m1-b4"
RELEASE_URL = f"https://github.com/crosspoint-reader/crosspoint-fonts/releases/download/{RELEASE}/"
FIRMWARE_TAG = "2.0.0rc"
# Scripts whose fonts the browser covers; families needing RTL shaping or CJK are left out.
COVERED_SCRIPTS = {"latin", "cyrillic", "greek", "georgian", "armenian", "ethiopic"}
STYLE_NAMES = ["regular", "bold", "italic", "bolditalic"]
# sd-fonts.yaml files Alegreya under its Sans-serif heading, but its own description (and the
# crosspoint-fonts README) call it a serif.
CATEGORY_OVERRIDES = {"Alegreya": "Serif"}

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "fonts")


# --- .cpfont writer (format v4, mirrors fontconvert_sdcard.py) -------------

GLYPH_FMT = "<BBHhhH2xI"
TOC_FMT = "<B3xIIBhhHHBBBI4x"


def write_cpfont(styles: dict[int, dict]) -> bytes:
    """styles: style_id -> dict(intervals, glyphs, bitmap, advanceY, ascender, descender,
    kern_left, kern_right, kern_lcount, kern_rcount, kern_matrix, ligatures)."""
    sections = {}
    for sid, s in sorted(styles.items()):
        parts = [
            b"".join(struct.pack("<III", *iv) for iv in s["intervals"]),
            b"".join(struct.pack(GLYPH_FMT, *g) for g in s["glyphs"]),
            b"".join(struct.pack("<HB", cp, c) for cp, c in s["kern_left"]),
            b"".join(struct.pack("<HB", cp, c) for cp, c in s["kern_right"]),
            struct.pack(f"<{len(s['kern_matrix'])}b", *s["kern_matrix"]),
            b"".join(struct.pack("<II", p, l) for p, l in s["ligatures"]),
            bytes(s["bitmap"]),
        ]
        sections[sid] = b"".join(parts)
    offset = 32 + 32 * len(styles)
    toc = b""
    for sid, s in sorted(styles.items()):
        toc += struct.pack(TOC_FMT, sid, len(s["intervals"]), len(s["glyphs"]), s["advanceY"], s["ascender"],
                           s["descender"], len(s["kern_left"]), len(s["kern_right"]), s["kern_lcount"],
                           s["kern_rcount"], len(s["ligatures"]), offset)
        offset += len(sections[sid])
    header = struct.pack("<8sHHB19s", b"CPFONT\x00\x00", 4, 1, len(styles), bytes(19))
    return header + toc + b"".join(sections[sid] for sid in sorted(sections))


# --- Built-in font headers -> style data ------------------------------------

def _array(text: str, name: str) -> str | None:
    m = re.search(r"\b" + re.escape(name) + r"\[\d*\]\s*=\s*\{(.*?)\n\};", text, re.S)
    return m.group(1) if m else None


def _ints(body: str) -> list[int]:
    body = re.sub(r"//[^\n]*", "", body)
    return [int(x, 0) for x in re.findall(r"-?0x[0-9A-Fa-f]+|-?\d+", body)]


def _tuples(body: str, n: int) -> list[tuple[int, ...]]:
    vals = _ints(body)
    assert len(vals) % n == 0, (len(vals), n)
    return [tuple(vals[i:i + n]) for i in range(0, len(vals), n)]


def compact(aligned: bytes, w: int, h: int) -> bytes:
    """Byte-aligned rows -> continuous 2-bit stream (FontDecompressor::compactSingleGlyph)."""
    stride = (w + 3) // 4
    out = bytearray()
    acc = 0
    n = 0
    for y in range(h):
        for x in range(w):
            px = (aligned[y * stride + x // 4] >> ((3 - x % 4) * 2)) & 3
            acc = (acc << 2) | px
            n += 1
            if n == 4:
                out.append(acc)
                acc = n = 0
    if n:
        out.append(acc << ((4 - n) * 2))
    return bytes(out)


def one_bit_to_two_bit(data: bytes, w: int, h: int) -> bytes:
    """1-bit glyph (UI fonts) -> 2-bit stream with ink at level 3, as the renderer paints it."""
    out = bytearray()
    acc = n = 0
    for i in range(w * h):
        px = 3 if (data[i >> 3] >> (7 - (i & 7))) & 1 else 0
        acc = (acc << 2) | px
        n += 1
        if n == 4:
            out.append(acc)
            acc = n = 0
    if n:
        out.append(acc << ((4 - n) * 2))
    return bytes(out)


def parse_builtin(path: str) -> dict:
    text = open(path, encoding="utf-8").read()
    name = re.search(r"\* name: (\w+)", text).group(1)
    bitmaps = bytes(_ints(_array(text, f"{name}Bitmaps")))
    glyphs = _tuples(_array(text, f"{name}Glyphs"), 7)
    intervals = _tuples(_array(text, f"{name}Intervals"), 3)
    groups_body = _array(text, f"{name}Groups")

    bitmap = bytearray()
    out_glyphs = []
    if groups_body:
        # Compressed 2-bit: inflate each group and repack its glyphs into one continuous bitmap.
        for comp_off, comp_size, raw_size, count, first in _tuples(groups_body, 5):
            raw = zlib.decompress(bitmaps[comp_off:comp_off + comp_size], -15)
            assert len(raw) == raw_size
            pos = 0
            for gi in range(first, first + count):
                w, h, adv, left, top, _, _ = glyphs[gi]
                size = ((w + 3) // 4) * h if w and h else 0
                packed = compact(raw[pos:pos + size], w, h) if size else b""
                pos += size
                out_glyphs.append((w, h, adv, left, top, len(packed), len(bitmap)))
                bitmap += packed
    else:
        # Uncompressed 1-bit (UI fonts): glyphs index the bitmap directly.
        assert "mode: 1-bit" in text
        for w, h, adv, left, top, length, off in glyphs:
            packed = one_bit_to_two_bit(bitmaps[off:off + length], w, h) if w and h else b""
            out_glyphs.append((w, h, adv, left, top, len(packed), len(bitmap)))
            bitmap += packed
    assert len(out_glyphs) == len(glyphs)

    # Trailing scalar fields of the EpdFontData initializer.
    init = text[text.rindex(f"static const EpdFontData {name} = {{"):]
    fields = [f.strip() for f in re.sub(r"//[^\n]*", "", init.split("{", 1)[1].rsplit("}", 1)[0]).split(",")]
    advance_y, ascender, descender = int(fields[4]), int(fields[5]), int(fields[6])
    lcount, rcount = int(fields[-5]), int(fields[-4])

    kern_left = kern_right = []
    matrix = []
    if _array(text, f"{name}KernLeftCodepoints"):
        kern_left = list(zip(_ints(_array(text, f"{name}KernLeftCodepoints")),
                             _ints(_array(text, f"{name}KernLeftClassIds"))))
        kern_right = list(zip(_ints(_array(text, f"{name}KernRightCodepoints")),
                              _ints(_array(text, f"{name}KernRightClassIds"))))
        rows = _ints(_array(text, f"{name}KernRowOffsets"))
        cols = _ints(_array(text, f"{name}KernSparseCols"))
        vals = _ints(_array(text, f"{name}KernSparseValues"))
        assert len(rows) == lcount + 1
        matrix = [0] * (lcount * rcount)
        for row in range(lcount):
            for i in range(rows[row], rows[row + 1]):
                matrix[row * rcount + cols[i]] = vals[i]
    else:
        lcount = rcount = 0
    ligs = _tuples(_array(text, f"{name}LigaturePairs"), 2) if _array(text, f"{name}LigaturePairs") else []

    return dict(intervals=intervals, glyphs=out_glyphs, bitmap=bitmap, advanceY=advance_y, ascender=ascender,
                descender=descender, kern_left=kern_left, kern_right=kern_right, kern_lcount=lcount,
                kern_rcount=rcount, kern_matrix=matrix, ligatures=ligs)


# --- Catalog -----------------------------------------------------------------

def categories(yaml_path: str) -> dict[str, str]:
    """Family name -> category, from the section comments in sd-fonts.yaml."""
    cats = {}
    current = None
    for line in open(yaml_path, encoding="utf-8"):
        m = re.match(r"\s*# ── (.+?) ─", line)
        if m:
            current = m.group(1).strip()
        m = re.match(r"\s*- name: (\S+)", line)
        if m and current:
            cats[m.group(1)] = current
    return cats


def fetch(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=120) as r:
        return r.read()


def write_gz(path: str, data: bytes) -> int:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        # mtime=0 keeps rebuilds byte-identical
        f.write(gzip.compress(data, compresslevel=9, mtime=0))
    return os.path.getsize(path)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--firmware", required=True, help="path to a crosspoint-reader checkout")
    ap.add_argument("--skip-download", action="store_true", help="reuse existing downloaded fonts")
    args = ap.parse_args()

    scripts_dir = os.path.join(args.firmware, "lib/EpdFont/scripts")
    builtin_dir = os.path.join(args.firmware, "lib/EpdFont/builtinFonts")
    sd_yaml = yaml.safe_load(open(os.path.join(scripts_dir, "sd-fonts.yaml"), encoding="utf-8"))
    yaml_by_name = {f["name"]: f for f in sd_yaml["families"]}
    cats = categories(os.path.join(scripts_dir, "sd-fonts.yaml"))
    manifest = json.loads(fetch(RELEASE_URL + "fonts.json"))
    labels = {g["tag"]: g["label"] for g in sd_yaml["scriptGroups"]}

    families = []

    # Built-in reader font: Noto Sans 12-18 in four styles.
    sizes = []
    for size in (12, 14, 16, 18):
        styles = {sid: parse_builtin(os.path.join(builtin_dir, f"notosans_{size}_{st}.h"))
                  for sid, st in enumerate(STYLE_NAMES)}
        data = write_cpfont(styles)
        gz = write_gz(os.path.join(OUT, "NotoSans", f"NotoSans_{size}.cpfont.gz"), data)
        sizes.append({"size": size, "path": f"fonts/NotoSans/NotoSans_{size}.cpfont.gz", "gzBytes": gz})
        print(f"built-in NotoSans {size}: {len(data)} bytes, {gz} gzipped")
    families.append({
        "name": "NotoSans", "builtin": True, "category": "Built in",
        "description": "Default reader font, built into the firmware (Latin, Cyrillic, Vietnamese)",
        "scripts": ["latin", "cyrillic"], "styles": STYLE_NAMES, "sizes": sizes,
        "source": "https://github.com/notofonts/latin-greek-cyrillic",
    })

    # Status-bar font (SMALL_FONT_ID): Noto Sans 8 regular.
    small = write_cpfont({0: parse_builtin(os.path.join(builtin_dir, "notosans_8_regular.h"))})
    write_gz(os.path.join(OUT, "ui", "Small_8.cpfont.gz"), small)

    # Downloadable families from the published release.
    for fam in manifest["families"]:
        if not set(fam["scripts"]) <= COVERED_SCRIPTS:
            continue
        name = fam["name"]
        y = yaml_by_name.get(name, {})
        sizes = []
        for f in fam["files"]:
            size = int(re.search(r"_(\d+)\.cpfont$", f["name"]).group(1))
            local = os.path.join(OUT, name, f["name"] + ".gz")
            if args.skip_download and os.path.exists(local):
                gz = os.path.getsize(local)
            else:
                data = fetch(RELEASE_URL + f["name"])
                assert len(data) == f["size"] and zlib.crc32(data) == f["crc32"], f["name"]
                gz = write_gz(local, data)
            sizes.append({"size": size, "path": f"fonts/{name}/{f['name']}.gz", "gzBytes": gz,
                          "file": f["name"], "bytes": f["size"], "url": RELEASE_URL + f["name"]})
            print(f"{f['name']}: {f['size']} bytes, {gz} gzipped")
        src = next(iter(y.get("styles", {}).values()), {})
        families.append({
            "name": name, "builtin": False, "category": CATEGORY_OVERRIDES.get(name, cats.get(name, "Other")),
            "description": fam["description"], "scripts": fam["scripts"], "styles": fam["styles"],
            "sizes": sorted(sizes, key=lambda s: s["size"]),
            "source": src.get("url"),
        })

    catalog = {
        "firmware": FIRMWARE_TAG,
        "release": RELEASE,
        "releaseUrl": f"https://github.com/crosspoint-reader/crosspoint-fonts/releases/tag/{RELEASE}",
        "scriptLabels": labels,
        "families": families,
    }
    with open(os.path.join(OUT, "catalog.json"), "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"{len(families)} families written to {OUT}")


if __name__ == "__main__":
    sys.exit(main())
