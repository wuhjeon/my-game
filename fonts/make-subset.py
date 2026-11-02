#!/usr/bin/env python3
"""Rebuild the subset WOFF2 web fonts in this folder.

Usage:
    pip install fonttools brotli
    python3 fonts/make-subset.py <SOURCE_TTF_DIR> [--out <OUT_DIR>] [--repo <REPO_ROOT>]

SOURCE_TTF_DIR must contain the original TTFs from https://github.com/google/fonts :
    BlackHanSans-Regular.ttf          (ofl/blackhansans/)
    IBMPlexSansKR-Regular.ttf         (ofl/ibmplexsanskr/)
    IBMPlexSansKR-SemiBold.ttf        (ofl/ibmplexsanskr/)
    IBMPlexSansKR-Bold.ttf            (ofl/ibmplexsanskr/)

OUT_DIR defaults to the folder this script lives in (fonts/), REPO_ROOT to its parent.

Character set = union of
  a) printable ASCII U+0020-U+007E
  b) the 2,350 KS X 1001 Hangul syllables (EUC-KR 0xB0A1-0xC8FE)
  c) Hangul Compatibility Jamo U+3131-U+318E
  d) every character found in the repository's tracked *.html files
  e) common punctuation (· … – — ‘ ’ ‚ ‛ “ ” NBSP ×)
Characters a font does not contain are simply dropped by the subsetter.
"""
import argparse
import os
import subprocess
import sys

from fontTools import subset

FACES = [
    # (source TTF, output WOFF2)
    ("BlackHanSans-Regular.ttf", "BlackHanSans-400.woff2"),
    ("IBMPlexSansKR-Regular.ttf", "IBMPlexSansKR-400.woff2"),
    ("IBMPlexSansKR-SemiBold.ttf", "IBMPlexSansKR-600.woff2"),
    ("IBMPlexSansKR-Bold.ttf", "IBMPlexSansKR-700.woff2"),
]


def ksx1001_hangul():
    chars = set()
    for lead in range(0xB0, 0xC9):
        for trail in range(0xA1, 0xFF):
            try:
                chars.add(bytes([lead, trail]).decode("euc-kr"))
            except UnicodeDecodeError:
                pass
    return chars


def html_files(repo):
    try:
        out = subprocess.run(
            ["git", "-C", repo, "ls-files", "-z", "--", "*.html"],
            check=True, capture_output=True,
        ).stdout.decode("utf-8")
        files = [f for f in out.split("\0") if f]
        if files:
            return [os.path.join(repo, f) for f in files]
    except (OSError, subprocess.CalledProcessError):
        pass
    found = []
    for root, dirs, names in os.walk(repo):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        found += [os.path.join(root, n) for n in names if n.endswith(".html")]
    return found


def build_charset(repo):
    chars = set(chr(c) for c in range(0x20, 0x7F))                    # a
    chars |= ksx1001_hangul()                                         # b
    chars |= set(chr(c) for c in range(0x3131, 0x318F))               # c
    for path in html_files(repo):                                     # d
        with open(path, encoding="utf-8") as fh:
            chars |= set(fh.read())
    chars |= set("·…–— ×")              # e
    chars |= set(chr(c) for c in range(0x2018, 0x201E))
    return sorted(ord(c) for c in chars if ord(c) >= 0x20 and not 0x7F <= ord(c) < 0xA0)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src", help="directory containing the original TTF files")
    ap.add_argument("--out", default=here, help="output directory (default: this script's folder)")
    ap.add_argument("--repo", default=os.path.dirname(here), help="repository root to scan for *.html")
    args = ap.parse_args()

    unicodes = build_charset(args.repo)
    print(f"charset: {len(unicodes)} code points")

    for src_name, out_name in FACES:
        src = os.path.join(args.src, src_name)
        if not os.path.isfile(src):
            sys.exit(f"missing source font: {src}")
        opts = subset.Options()
        opts.flavor = "woff2"
        opts.layout_features = ["*"]
        opts.hinting = False
        opts.name_IDs = ["*"]
        opts.name_languages = ["*"]
        opts.notdef_outline = True
        opts.drop_tables += ["DSIG"]
        font = subset.load_font(src, opts)
        sub = subset.Subsetter(opts)
        sub.populate(unicodes=unicodes)
        sub.subset(font)
        out = os.path.join(args.out, out_name)
        subset.save_font(font, out, opts)
        kept = len(font.getBestCmap())
        print(f"{out_name}: {os.path.getsize(out):,} bytes, {kept} mapped chars")


if __name__ == "__main__":
    main()
