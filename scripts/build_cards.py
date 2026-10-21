#!/usr/bin/env python3
"""
Generates one small animated project card per entry in PROJECTS:
    images/card_<slug>.svg
Each card is wrapped in its own <a> in README.md so it is clickable.

Usage:  python3 scripts/build_cards.py
"""

from pathlib import Path
from xml.sax.saxutils import escape

PROJECTS = [
    {
        "slug": "darkwire",
        "name": "darkwire.tech",
        "tag": "cybersecurity news + CVE feed",
        "status": "LIVE",
        "status_color": "#34d399",
        "lang": "FastAPI · PostgreSQL",
    },
    {
        "slug": "crawlr",
        "name": "crawlr.lol",
        "tag": "OSINT investigation platform",
        "status": "LIVE",
        "status_color": "#34d399",
        "lang": "FastAPI · Python",
    },
    {
        "slug": "remnant",
        "name": "Remnant",
        "tag": "self-hosted AI usage monitoring",
        "status": "BUILDING",
        "status_color": "#fbbf24",
        "lang": "shadow AI · agents · MCP",
    },
]

W, H = 290, 118
FONT = "'Courier New','Lucida Console',monospace"


def card(p: dict) -> str:
    sc = p["status_color"]
    return f"""<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
<defs>
  <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#140a2c"/>
    <stop offset="100%" stop-color="#0d0720"/>
  </linearGradient>
  <linearGradient id="bar" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%" stop-color="#6d28d9"/>
    <stop offset="50%" stop-color="#8b5cf6"/>
    <stop offset="100%" stop-color="#6d28d9"/>
  </linearGradient>
  <pattern id="scan" x="0" y="0" width="2" height="4" patternUnits="userSpaceOnUse">
    <rect width="2" height="1" fill="rgba(139,92,246,0.05)"/>
  </pattern>
</defs>
<style>
  @keyframes shimmer {{ 0%{{opacity:.55}} 50%{{opacity:1}} 100%{{opacity:.55}} }}
  @keyframes blink   {{ 0%,100%{{opacity:1}} 50%{{opacity:.25}} }}
  @keyframes sweep   {{ 0%{{transform:translateX(-{W}px)}} 100%{{transform:translateX({W}px)}} }}
  .bar  {{ animation: shimmer 3s ease-in-out infinite; }}
  .dot  {{ animation: blink 2s ease-in-out infinite; }}
  .sweep{{ animation: sweep 6s linear infinite; }}
</style>
<rect width="{W}" height="{H}" rx="8" fill="url(#bg)" stroke="#3b1680" stroke-width="1.5"/>
<rect width="{W}" height="{H}" rx="8" fill="url(#scan)"/>
<rect class="bar" x="0" y="0" width="{W}" height="3" rx="1.5" fill="url(#bar)"/>
<!-- faint light sweep -->
<rect class="sweep" x="0" y="0" width="60" height="{H}" fill="#8b5cf6" opacity="0.06"/>
<!-- bracket corner -->
<path d="M12,{H-12} L12,{H-28} M12,{H-12} L28,{H-12}" stroke="#8b5cf6" stroke-width="1.5" fill="none" opacity="0.5"/>
<path d="M{W-12},16 L{W-12},32 M{W-12},16 L{W-28},16" stroke="#8b5cf6" stroke-width="1.5" fill="none" opacity="0.5"/>
<!-- status -->
<circle class="dot" cx="20" cy="26" r="4" fill="{sc}"/>
<text x="30" y="30" font-family="{FONT}" font-size="10" fill="{sc}" letter-spacing="1.5">{escape(p['status'])}</text>
<!-- name -->
<text x="18" y="60" font-family="{FONT}" font-size="19" font-weight="700" fill="#ffffff">{escape(p['name'])}</text>
<!-- tagline -->
<text x="18" y="80" font-family="{FONT}" font-size="11" fill="#c4b5fd">{escape(p['tag'])}</text>
<!-- stack -->
<text x="18" y="{H-18}" font-family="{FONT}" font-size="9.5" fill="#7c6aa8">{escape(p['lang'])}</text>
<text x="{W-18}" y="{H-18}" font-family="{FONT}" font-size="9.5" fill="#7c6aa8" text-anchor="end">&gt;_</text>
</svg>
"""


if __name__ == "__main__":
    img = Path(__file__).resolve().parent.parent / "images"
    for p in PROJECTS:
        (img / f"card_{p['slug']}.svg").write_text(card(p), encoding="utf-8")
        print(f"wrote images/card_{p['slug']}.svg")
