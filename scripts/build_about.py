#!/usr/bin/env python3
"""
Generates images/about.svg: an animated "terminal" that types out about.txt
character by character (SMIL animation, so it plays inside GitHub's <img> tags).

Usage:
    python3 scripts/build_about.py            # writes images/about.svg
    python3 scripts/build_about.py --static   # also writes images/about_preview.svg
                                              # (everything visible, no animation)

Edit the LINES list below, re-run, commit.  No dependencies beyond Python 3.
"""

import sys
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

# ---------------------------------------------------------------- content --
# each line is a list of (text, style) segments; an empty list is a blank line
TODAY = date.today().isoformat()

LINES = [
    [("err0ric", "user"), ("@", "sym"), ("toaster", "host"), (":", "sym"), ("~", "path"), ("$ ", "sym"), ("cat about.txt", "cmd")],
    [],
    [("handle:    ", "key"), ("Err0ric", "value")],
    [("location:  ", "key"), ("Pacific Northwest, USA", "value")],
    [("role:      ", "key"), ("Cybersecurity Lead", "value")],
    [("education: ", "key"), ("B.S. Cybersecurity (in progress)", "value")],
    [],
    [("building:", "header")],
    [("  - ", "dash"), ("darkwire.tech", "url"), ("   cybersecurity news + CVE feed", "item")],
    [("  - ", "dash"), ("crawlr.lol", "url"), ("      OSINT platform", "item")],
    [("  - ", "dash"), ("Remnant", "name"), ("         self-hosted AI usage monitoring ", "item"), ("(WIP)", "wip")],
    [],
    [("focus:", "header")],
    [("  - ", "dash"), ("OSINT & digital forensics", "item")],
    [("  - ", "dash"), ("AI security (MITRE ATLAS + ATT&CK)", "item")],
    [("  - ", "dash"), ("Network security & infrastructure hardening", "item")],
    [("  - ", "dash"), ("Security policy & compliance frameworks", "item")],
    [],
    [("hobbies:", "header")],
    [("  - ", "dash"), ("building tools nobody asked for", "item")],
    [("  - ", "dash"), ("CTF", "item")],
    [("  - ", "dash"), ("tinkering", "item")],
    [],
    [("err0ric", "user"), ("@", "sym"), ("toaster", "host"), (":", "sym"), ("~", "path"), ("$ ", "sym")],
]

# ---------------------------------------------------------------- styling --
COLORS = {
    "user":   "#34d399",   # green user
    "host":   "#34d399",
    "sym":    "#e2d9f3",
    "path":   "#60a5fa",   # blue path
    "cmd":    "#ffffff",
    "key":    "#a78bfa",   # purple keys
    "value":  "#f1ecfa",   # near-white values
    "header": "#8b5cf6",
    "dash":   "#5b4a8a",
    "item":   "#d8cdf0",
    "url":    "#c4b5fd",
    "name":   "#c4b5fd",
    "wip":    "#fbbf24",   # amber
}
UNDERLINE = {"url"}
FONT = "'Courier New','Lucida Console',monospace"
FONT_SIZE = 13
CHAR_W = 7.8          # advance width of Courier New at 13px
LINE_H = 21
PAD_X = 18
TITLE_H = 34
FIRST_BASELINE = 63
WIDTH = 680

# timing (seconds)
START_DELAY = 0.6
CHAR_T = 0.035
LINE_PAUSE = 0.15
BLANK_PAUSE = 0.08
END_HOLD = 6.0        # time the finished screen stays visible before looping

# -------------------------------------------------------------- generator --
def build(static: bool = False) -> str:
    rows = len(LINES)
    height = FIRST_BASELINE + (rows - 1) * LINE_H + 30

    # 1) timeline: when does each character appear
    t = START_DELAY
    chars = []  # (x, y, char, color, appear_time)
    cursor_keys = []  # (time, x, y)
    for i, segs in enumerate(LINES):
        y = FIRST_BASELINE + i * LINE_H
        cursor_keys.append((t, PAD_X, y - 10))
        if not segs:
            t += BLANK_PAUSE
            continue
        col = 0
        for text, style in segs:
            color = COLORS[style]
            for ch in text:
                x = PAD_X + col * CHAR_W
                if ch != " ":
                    chars.append((x, y, ch, color, t, style in UNDERLINE))
                t += CHAR_T
                col += 1
                cursor_keys.append((t, x + CHAR_W, y - 10))
        t += LINE_PAUSE
    total = t + END_HOLD
    dur = round(total, 3)

    out = []
    out.append(
        f'<svg width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}" '
        f'xmlns="http://www.w3.org/2000/svg">'
    )
    out.append("""<defs>
  <linearGradient id="tg" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="#1a0a35"/>
    <stop offset="100%" stop-color="#2a1060"/>
  </linearGradient>
  <pattern id="scan" x="0" y="0" width="2" height="4" patternUnits="userSpaceOnUse">
    <rect width="2" height="1" fill="rgba(139,92,246,0.05)"/>
  </pattern>
</defs>""")
    # window chrome
    out.append(
        f'<rect width="{WIDTH}" height="{height}" rx="8" fill="#0d0720" stroke="#3b1680" stroke-width="1.5"/>'
    )
    out.append(f'<rect width="{WIDTH}" height="{height}" rx="8" fill="url(#scan)"/>')
    out.append(f'<rect width="{WIDTH}" height="{TITLE_H}" rx="8" fill="url(#tg)"/>')
    out.append(f'<rect y="20" width="{WIDTH}" height="14" fill="url(#tg)"/>')
    out.append(
        f'<line x1="0" y1="{TITLE_H}" x2="{WIDTH}" y2="{TITLE_H}" stroke="#3b1680" stroke-width="1" opacity="0.8"/>'
    )
    out.append('<circle cx="20" cy="17" r="5.5" fill="#ff5f57"/>')
    out.append('<circle cx="39" cy="17" r="5.5" fill="#febc2e"/>')
    out.append('<circle cx="58" cy="17" r="5.5" fill="#28c840"/>')
    out.append(
        f'<text x="{WIDTH/2}" y="22" font-family="{FONT}" font-size="11" fill="#a78bfa" '
        f'text-anchor="middle" opacity="0.75">terminal — about.txt</text>'
    )
    # live dot top-right
    out.append(
        f'<circle cx="{WIDTH-22}" cy="17" r="3.5" fill="#8b5cf6">'
        '<animate attributeName="opacity" values="0.9;0.25;0.9" dur="2s" repeatCount="indefinite"/></circle>'
    )

    # 2) characters
    for x, y, ch, color, at, ul in chars:
        if static:
            anim = ""
            op = "1"
        else:
            k_on = at / total
            k_off = (total - 0.01) / total
            anim = (
                f'<animate attributeName="opacity" values="0;0;1;1;0" '
                f'keyTimes="0;{k_on:.4f};{k_on + 0.0001:.4f};{k_off:.4f};1" '
                f'dur="{dur}s" repeatCount="indefinite" calcMode="linear"/>'
            )
            op = "0"
        out.append(
            f'<text x="{x:.1f}" y="{y}" font-family="{FONT}" font-size="{FONT_SIZE}" '
            f'fill="{color}" opacity="{op}"{" text-decoration=\"underline\"" if ul else ""}>{escape(ch)}{anim}</text>'
        )

    # 3) cursor
    if static:
        _, cx, cy = cursor_keys[-1]
        out.append(f'<rect x="{cx:.1f}" y="{cy}" width="8" height="12" rx="1" fill="#8b5cf6"/>')
    else:
        xs = ";".join(f"{x:.1f}" for _, x, _ in cursor_keys)
        ys = ";".join(f"{y}" for _, _, y in cursor_keys)
        kts = ";".join(f"{tt / total:.4f}" for tt, _, _ in cursor_keys)
        # keyTimes must start at 0 and end at 1
        xs = f"{cursor_keys[0][1]:.1f};" + xs + f";{cursor_keys[0][1]:.1f}"
        ys = f"{cursor_keys[0][2]};" + ys + f";{cursor_keys[0][2]}"
        kts = "0.0000;" + kts + ";1.0000"
        out.append(
            '<rect width="8" height="12" rx="1" fill="#8b5cf6">'
            f'<animate attributeName="x" values="{xs}" keyTimes="{kts}" dur="{dur}s" '
            'repeatCount="indefinite" calcMode="discrete"/>'
            f'<animate attributeName="y" values="{ys}" keyTimes="{kts}" dur="{dur}s" '
            'repeatCount="indefinite" calcMode="discrete"/>'
            '<animate attributeName="opacity" values="1;0;1" keyTimes="0;0.5;1" dur="1.1s" repeatCount="indefinite"/>'
            "</rect>"
        )
    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    img = root / "images"
    img.mkdir(exist_ok=True)
    (img / "about.svg").write_text(build(), encoding="utf-8")
    print("wrote images/about.svg")
    if "--static" in sys.argv:
        (img / "about_preview.svg").write_text(build(static=True), encoding="utf-8")
        print("wrote images/about_preview.svg")
