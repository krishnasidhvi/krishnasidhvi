"""Shared design system for the KSN//OS profile panels.

Animation rule used everywhere: an element's *static attributes* hold its
final, fully-visible state, and SMIL animations start at t=0 and pad their
delay with repeated values. Renderers that ignore SMIL (some mobile apps,
link previews) therefore still show a complete, readable panel.
"""

import math
import os

ASSETS = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "assets"))

# ---- palette -------------------------------------------------------------
BG0 = "#03060D"
BG1 = "#070D1A"
BG2 = "#0A1326"
LINE = "#1E293B"
GOLD = "#F59E0B"
GOLD2 = "#FBBF24"
GOLD3 = "#FDE68A"
SKY = "#38BDF8"
VIOLET = "#A78BFA"
ROSE = "#F43F5E"
GREEN = "#10B981"
TEXT = "#F8FAFC"
SOFT = "#CBD5E1"
MUTED = "#94A3B8"
DIM = "#64748B"

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"
MONO = "'SF Mono', 'Cascadia Code', 'Fira Code', Consolas, 'Courier New', monospace"

BASE_CSS = f"""
.sans {{ font-family: {SANS}; }}
.mono {{ font-family: {MONO}; }}
@keyframes pulse {{ 0%, 100% {{ opacity: .35; }} 50% {{ opacity: 1; }} }}
@keyframes blink {{ 0%, 49% {{ opacity: 1; }} 50%, 100% {{ opacity: 0; }} }}
.pulse {{ animation: pulse 2.6s ease-in-out infinite; }}
.blink {{ animation: blink 1s step-end infinite; }}
"""


def f(x):
    """Compact number formatting for SVG attributes."""
    return f"{x:.2f}".rstrip("0").rstrip(".")


def doc(w, h, body, defs="", css="", label=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="{label}">\n'
        f"<title>{label}</title>\n<defs>{defs}</defs>\n<style>{BASE_CSS}{css}</style>\n{body}\n</svg>\n"
    )


def write(name, content):
    path = os.path.join(ASSETS, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(content)
    print(f"wrote {os.path.relpath(path)} ({len(content):,} bytes)")


# ---- animation helpers ---------------------------------------------------
def appear(delay, length=0.35, attr="opacity", frm=0, to=1):
    """One-shot reveal that starts at t=0 (static attribute = final value)."""
    if delay <= 0:
        return f'<animate attributeName="{attr}" values="{frm};{to}" dur="{f(length)}s" fill="freeze"/>'
    total = delay + length
    k = delay / total
    return (
        f'<animate attributeName="{attr}" values="{frm};{frm};{to}" '
        f'keyTimes="0;{k:.4f};1" dur="{f(total)}s" fill="freeze"/>'
    )


def loop_values(attr, values, dur, begin=0.0, key_times=None):
    kt = f' keyTimes="{";".join(f"{t:.4f}" for t in key_times)}"' if key_times else ""
    vals = ";".join(str(v) for v in values)
    b = f' begin="{f(begin)}s"' if begin else ""
    return f'<animate attributeName="{attr}" values="{vals}"{kt} dur="{f(dur)}s"{b} repeatCount="indefinite"/>'


# ---- shared chrome -------------------------------------------------------
def bg_defs():
    return f"""
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="{BG0}"/><stop offset=".55" stop-color="{BG1}"/><stop offset="1" stop-color="#0D1830"/>
</linearGradient>
<radialGradient id="glowA" cx="88%" cy="0%" r="70%">
  <stop offset="0" stop-color="{GOLD}" stop-opacity=".16"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/>
</radialGradient>
<radialGradient id="glowB" cx="5%" cy="100%" r="60%">
  <stop offset="0" stop-color="#0284C7" stop-opacity=".16"/><stop offset="1" stop-color="#0284C7" stop-opacity="0"/>
</radialGradient>
<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">
  <path d="M32 0H0V32" fill="none" stroke="{LINE}" stroke-width=".6" stroke-opacity=".5"/>
</pattern>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
  <feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<filter id="glowBig" x="-50%" y="-50%" width="200%" height="200%">
  <feGaussianBlur stdDeviation="7" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
"""


def brackets(w, h, inset=10, size=22, color=GOLD, opacity=0.8):
    i, s = inset, size
    paths = [
        f"M{i} {i + s}V{i}H{i + s}",
        f"M{w - i - s} {i}H{w - i}V{i + s}",
        f"M{i} {h - i - s}V{h - i}H{i + s}",
        f"M{w - i - s} {h - i}H{w - i}V{h - i - s}",
    ]
    return "".join(
        f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2" stroke-opacity="{opacity}"/>' for d in paths
    )


def bg_body(w, h, grid=True, scan=True):
    out = [
        f'<rect width="{w}" height="{h}" rx="14" fill="url(#bg)"/>',
        f'<rect width="{w}" height="{h}" rx="14" fill="url(#glowA)"/>',
        f'<rect width="{w}" height="{h}" rx="14" fill="url(#glowB)"/>',
    ]
    if grid:
        out.append(f'<rect width="{w}" height="{h}" rx="14" fill="url(#grid)"/>')
    out.append(f'<rect x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" rx="13.5" fill="none" stroke="{LINE}" stroke-width="1.5"/>')
    out.append(brackets(w, h))
    if scan:
        out.append(
            f'<rect x="0" y="-6" width="{w}" height="2" fill="{GOLD2}" opacity=".10">'
            f'<animate attributeName="y" values="-6;{h + 6}" dur="6s" repeatCount="indefinite"/></rect>'
        )
    return "\n".join(out)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def bezier_point(p0, p1, p2, p3, t):
    u = 1 - t
    return (
        u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
        u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1],
    )


def catmull_rom(points, tension=0.5):
    """Smooth path through points; returns (d, list_of_cubic_segments)."""
    segs = []
    d = f"M{f(points[0][0])} {f(points[0][1])}"
    for i in range(len(points) - 1):
        p0 = points[i - 1] if i > 0 else points[i]
        p1, p2 = points[i], points[i + 1]
        p3 = points[i + 2] if i + 2 < len(points) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) * tension / 3, p1[1] + (p2[1] - p0[1]) * tension / 3)
        c2 = (p2[0] - (p3[0] - p1[0]) * tension / 3, p2[1] - (p3[1] - p1[1]) * tension / 3)
        segs.append((p1, c1, c2, p2))
        d += f" C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} {f(p2[0])} {f(p2[1])}"
    return d, segs


def seg_length(seg, n=40):
    pts = [bezier_point(*seg, i / n) for i in range(n + 1)]
    return sum(math.dist(pts[i], pts[i + 1]) for i in range(n))
