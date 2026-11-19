"""Builds the static KSN//OS panels into ../assets.

    python scripts/build_static.py

Edit the content constants below and re-run to regenerate.
"""

import math
import random

from hud import *  # noqa: F403  (palette + helpers)


# =========================================================================
# 1. BOOT HERO
# =========================================================================
BOOT_LOG = [
    ("mounting /dev/experience", "4+ yrs"),
    ("loading data-engineering.core", "aws · spark · kafka"),
    ("linking llm-runtime", "agentic"),
    ("calibrating sql-guardrails", "strict"),
    ("opening recruiter.uplink", "ready"),
]
GEO_NODES = [  # career geography (lat, lon)
    ("HYD", 17.4, 78.5), ("JAI", 26.9, 75.8), ("BAL", 39.3, -76.6),
    ("MLV", 40.0, -75.5), ("SEA", 47.6, -122.3), ("ATL", 33.7, -84.4),
]
IMPACT = [("+30%", .30, "PIPELINE SCALE"), ("−50%", .50, "DATA DISCREPANCY"), ("−15%", .15, "FRAUD FALSE +")]
CHIPS = ["4+ YRS · DATA & AI", "AWS CERTIFIED DATA ENGINEER", "M.P.S. DATA SCIENCE · UMBC"]


def boot():
    W, H = 1200, 520
    HZ = 345  # horizon
    rnd = random.Random(11)

    defs = bg_defs() + f"""
<linearGradient id="nameGrad" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="#FFFFFF"/><stop offset=".55" stop-color="{TEXT}"/><stop offset=".85" stop-color="{GOLD3}"/><stop offset="1" stop-color="{GOLD}"/>
</linearGradient>
<radialGradient id="globeFill" cx="38%" cy="32%" r="75%">
  <stop offset="0" stop-color="{SKY}" stop-opacity=".22"/><stop offset=".7" stop-color="{SKY}" stop-opacity=".04"/><stop offset="1" stop-color="{SKY}" stop-opacity="0"/>
</radialGradient>
<linearGradient id="floorFade" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{BG1}" stop-opacity="1"/><stop offset=".45" stop-color="{BG1}" stop-opacity="0"/>
</linearGradient>
<linearGradient id="horizon" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{GOLD}" stop-opacity="0"/><stop offset=".5" stop-color="{GOLD3}" stop-opacity=".9"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/>
</linearGradient>
<linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{SKY}" stop-opacity="0"/><stop offset="1" stop-color="{SKY}" stop-opacity=".28"/>
</linearGradient>
<clipPath id="floorClip"><rect x="0" y="{HZ}" width="{W}" height="{H - HZ}" rx="14"/></clipPath>
<clipPath id="typeSub"><rect x="56" y="250" height="30" width="900">{appear(3.0, .9, "width", 0, 900)}</rect></clipPath>
"""
    css = f"""
.name {{ font-family: {SANS}; font-weight: 800; letter-spacing: 4px; }}
"""
    b = [bg_body(W, H, grid=False, scan=False)]

    # ---- whole-scene CRT power-on flicker -------------------------------
    b.append('<g>')
    b.append('<animate attributeName="opacity" values="0;1;.25;1;.7;1" keyTimes="0;.2;.35;.5;.7;1" dur=".7s" fill="freeze"/>')

    # ---- perspective floor ----------------------------------------------
    floor = [f'<g clip-path="url(#floorClip)">{appear(.5, 1.0)}']
    vp = (600, 250)
    for k in range(-22, 23):
        xb = 600 + k * 74
        floor.append(f'<line x1="{vp[0]}" y1="{vp[1]}" x2="{xb}" y2="{H}" stroke="{SKY}" stroke-opacity=".22" stroke-width=".8"/>')
    n, dur = 12, 3.6
    for i in range(n):
        ts = [j / 20 for j in range(21)]
        ys = [f(HZ + (H - HZ) * t**2.3) for t in ts]
        ops = [f(.05 + .55 * t) for t in ts]
        begin = -i * dur / n
        y0 = ys[int(20 * ((i / n)))]  # static fallback spread
        floor.append(
            f'<line x1="0" x2="{W}" y1="{y0}" y2="{y0}" stroke="{SKY}" stroke-width="1" stroke-opacity=".3">'
            f'<animate attributeName="y1" values="{";".join(ys)}" dur="{dur}s" begin="{f(begin)}s" repeatCount="indefinite"/>'
            f'<animate attributeName="y2" values="{";".join(ys)}" dur="{dur}s" begin="{f(begin)}s" repeatCount="indefinite"/>'
            f'<animate attributeName="stroke-opacity" values="{";".join(ops)}" dur="{dur}s" begin="{f(begin)}s" repeatCount="indefinite"/>'
            f"</line>"
        )
    floor.append(f'<rect x="0" y="{HZ}" width="{W}" height="{H - HZ}" fill="url(#floorFade)"/>')
    floor.append("</g>")
    b += floor
    b.append(f'<rect x="40" y="{HZ - 1}" width="{W - 80}" height="2" fill="url(#horizon)" filter="url(#glow)">{appear(.6, .8)}</rect>')

    # ---- holographic globe ----------------------------------------------
    cx, cy, R = 935, 178, 104
    g = [f'<g>{appear(1.0, 1.0)}']
    # radar sweep
    g.append(
        f'<path d="M{cx} {cy}L{cx + R + 26} {cy}A{R + 26} {R + 26} 0 0 0 {f(cx + (R + 26) * math.cos(math.radians(-40)))} {f(cy + (R + 26) * math.sin(math.radians(-40)))}Z" fill="url(#sweep)">'
        f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="7s" repeatCount="indefinite"/></path>'
    )
    g.append(
        f'<circle cx="{cx}" cy="{cy}" r="{R + 26}" fill="none" stroke="{SKY}" stroke-opacity=".35" stroke-dasharray="2 7">'
        f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="40s" repeatCount="indefinite"/></circle>'
    )
    g.append(
        f'<circle cx="{cx}" cy="{cy}" r="{R + 38}" fill="none" stroke="{GOLD}" stroke-opacity=".35" stroke-dasharray="24 10 4 10">'
        f'<animateTransform attributeName="transform" type="rotate" from="360 {cx} {cy}" to="0 {cx} {cy}" dur="55s" repeatCount="indefinite"/></circle>'
    )
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="url(#globeFill)" stroke="{SKY}" stroke-opacity=".6" stroke-width="1.2"/>')
    for lat in (-60, -30, 0, 30, 60):
        y = cy - R * math.sin(math.radians(lat))
        rx = R * math.cos(math.radians(lat))
        col, op = (GOLD, .6) if lat == 0 else (SKY, .28)
        g.append(f'<ellipse cx="{cx}" cy="{f(y)}" rx="{f(rx)}" ry="{f(rx * .16)}" fill="none" stroke="{col}" stroke-opacity="{op}"/>')
    SPIN = 16.0
    steps = 48
    for m in range(6):
        ph = m * math.pi / 6
        vals = [f(R * abs(math.cos(ph + 2 * math.pi * s / steps))) for s in range(steps + 1)]
        g.append(
            f'<ellipse cx="{cx}" cy="{cy}" rx="{vals[0]}" ry="{R}" fill="none" stroke="{SKY}" stroke-opacity=".35">'
            f'<animate attributeName="rx" values="{";".join(vals)}" dur="{SPIN}s" repeatCount="indefinite"/></ellipse>'
        )
    for code, lat, lon in GEO_NODES:
        la, lo = math.radians(lat), math.radians(lon)
        xs, os_ = [], []
        for s in range(steps + 1):
            a = lo + 2 * math.pi * s / steps
            xs.append(f(cx + R * math.cos(la) * math.sin(a)))
            os_.append("1" if math.cos(a) > 0 else ".12")
        y = f(cy - R * math.sin(la))
        g.append(
            f'<circle cx="{xs[0]}" cy="{y}" r="3.2" fill="{GOLD2}" filter="url(#glow)" opacity="{os_[0]}">'
            f'<animate attributeName="cx" values="{";".join(xs)}" dur="{SPIN}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="{";".join(os_)}" dur="{SPIN}s" repeatCount="indefinite" calcMode="discrete"/></circle>'
        )
    # tilted orbit + satellite
    orx, ory = 172, 34
    g.append(f'<g transform="rotate(-16 {cx} {cy})">')
    g.append(f'<path id="orbit" d="M{cx - orx} {cy}A{orx} {ory} 0 1 1 {cx + orx} {cy}A{orx} {ory} 0 1 1 {cx - orx} {cy}" fill="none" stroke="{GOLD}" stroke-opacity=".45" stroke-dasharray="3 5"/>')
    g.append(
        f'<g opacity="0">{loop_values("opacity", [1, 1], 10)}'
        f'<circle r="4.5" fill="{GOLD3}" filter="url(#glow)"/>'
        f'<animateMotion dur="10s" repeatCount="indefinite"><mpath xlink:href="#orbit"/></animateMotion></g>'
    )
    g.append("</g>")
    g.append(f'<circle cx="{cx}" cy="{cy}" r="5" fill="{GOLD2}" class="pulse"/>')
    g.append(
        f'<text x="{cx}" y="{cy + R + 58}" text-anchor="middle" class="mono" font-size="10" fill="{DIM}" letter-spacing="1.5">'
        f'GEO-NODES ▸ {" · ".join(n[0] for n in GEO_NODES)}</text>'
    )
    g.append("</g>")
    b += g

    # ---- top bar ----------------------------------------------------------
    b.append(
        f'<text x="40" y="34" class="mono" font-size="11" letter-spacing="1.5"><tspan fill="{GOLD}" font-weight="700">KSN//OS</tspan>'
        f'<tspan fill="{DIM}">  v4.0 · HOLOGRAPHIC PROFILE INTERFACE</tspan></text>'
    )
    b.append(
        f'<text x="{W - 40}" y="34" text-anchor="end" class="mono" font-size="11" letter-spacing="1.5" fill="{DIM}">'
        f'NODE HYD-IN · UPLINK <tspan fill="{GREEN}">● STABLE</tspan></text>'
    )

    # ---- boot log (visible only during boot) ------------------------------
    b.append('<g opacity="0" class="mono" font-size="12.5">')
    b.append('<animate attributeName="opacity" values="1;1;0" keyTimes="0;.86;1" dur="2.2s" fill="freeze"/>')
    for i, (task, res) in enumerate(BOOT_LOG):
        y = 92 + i * 24
        dots = "." * (34 - len(task))
        b.append(
            f'<text x="56" y="{y}" fill="{MUTED}">{appear(.15 + .24 * i, .05)}<tspan fill="{GREEN}">[ OK ]</tspan> {task} '
            f'<tspan fill="{LINE}">{dots}</tspan> <tspan fill="{GOLD2}">{res}</tspan></text>'
        )
    b.append("</g>")

    # ---- identity ---------------------------------------------------------
    b.append(
        f'<text x="58" y="98" class="mono" font-size="11" letter-spacing="2" fill="{GOLD}">{appear(2.1, .2)}'
        f'▸ IDENTITY VERIFIED <tspan fill="{DIM}">// ACCESS LEVEL: PUBLIC</tspan></text>'
    )
    for line, y in (("KRISHNA SIDHVI", 168), ("NEKKANTI", 226)):
        # glitch ghosts
        for col, jit in ((SKY, "-7 1;5 -2;-3 2;6 0;-2 -1;0 0"), (ROSE, "6 -1;-5 2;4 0;-6 1;3 1;0 0")):
            b.append(
                f'<text x="56" y="{y}" class="name" font-size="56" fill="{col}" opacity="0">'
                f'<animate attributeName="opacity" values="0;0;.75;.75;0" keyTimes="0;.73;.75;.95;1" dur="3s" fill="freeze"/>'
                f'<animateTransform attributeName="transform" type="translate" values="0 0;{jit}" '
                f'keyTimes="0;.7;.76;.82;.88;.94;1" dur="3s" calcMode="discrete" fill="freeze"/>{line}</text>'
            )
        b.append(
            f'<text x="56" y="{y}" class="name" font-size="56" fill="url(#nameGrad)">'
            f'<animate attributeName="opacity" values="0;0;1;.1;1;.4;1" keyTimes="0;.73;.77;.82;.87;.92;1" dur="3s" fill="freeze"/>{line}</text>'
        )
    b.append(
        f'<text x="58" y="270" class="sans" font-size="16" letter-spacing="2.5" fill="{MUTED}" clip-path="url(#typeSub)">'
        f'FORWARD DEPLOYMENT AI ENGINEER <tspan fill="{GOLD}">◆</tspan> DATA &amp; LLM SYSTEMS <tspan fill="{GOLD}">◆</tspan> CLOUD DATA PLATFORMS</text>'
    )
    x = 58
    for i, chip in enumerate(CHIPS):
        w = len(chip) * 7.3 + 34
        col = SKY if i == 1 else GOLD
        b.append(
            f'<g transform="translate({f(x)} 290)">{appear(3.9 + .15 * i, .3)}'
            f'<rect width="{f(w)}" height="26" rx="13" fill="{BG2}" fill-opacity=".9" stroke="{col}" stroke-opacity=".55"/>'
            f'<circle cx="14" cy="13" r="3" fill="{col}" class="pulse"/>'
            f'<text x="25" y="17" class="mono" font-size="11" letter-spacing="1" fill="{SOFT}">{esc(chip)}</text></g>'
        )
        x += w + 10

    # ---- impact gauges (floor left) ---------------------------------------
    px, py, pw, ph = 40, 370, 430, 132
    b.append(f'<g>{appear(3.8, .5)}')
    b.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="10" fill="#050A16" fill-opacity=".88" stroke="{LINE}"/>')
    b.append(f'<text x="{px + 16}" y="{py + 20}" class="mono" font-size="10" letter-spacing="1.5" fill="{GOLD}">IMPACT TELEMETRY <tspan fill="{DIM}">// CAREER METRICS</tspan></text>')
    r = 27
    C = 2 * math.pi * r
    for i, (val, frac, cap) in enumerate(IMPACT):
        gx = px + 78 + i * 138
        gy = py + 70
        off = C * (1 - frac)
        b.append(f'<circle cx="{gx}" cy="{gy}" r="{r}" fill="none" stroke="{LINE}" stroke-width="5"/>')
        b.append(
            f'<circle cx="{gx}" cy="{gy}" r="{r}" fill="none" stroke="{GOLD2 if i != 1 else SKY}" stroke-width="5" stroke-linecap="round" '
            f'stroke-dasharray="{f(C)}" stroke-dashoffset="{f(off)}" transform="rotate(-90 {gx} {gy})" filter="url(#glow)">'
            f'{appear(4.2 + .2 * i, 1.2, "stroke-dashoffset", f(C), f(off))}</circle>'
        )
        b.append(f'<text x="{gx}" y="{gy + 5}" text-anchor="middle" class="sans" font-size="15" font-weight="800" fill="{TEXT}">{val}</text>')
        b.append(f'<text x="{gx}" y="{gy + 50}" text-anchor="middle" class="mono" font-size="9" letter-spacing="1" fill="{DIM}">{cap}</text>')
    b.append("</g>")

    # ---- live throughput (floor right) ------------------------------------
    px = W - 40 - 380
    b.append(f'<g>{appear(4.0, .5)}')
    b.append(f'<rect x="{px}" y="{py}" width="380" height="{ph}" rx="10" fill="#050A16" fill-opacity=".88" stroke="{LINE}"/>')
    b.append(f'<text x="{px + 16}" y="{py + 20}" class="mono" font-size="10" letter-spacing="1.5" fill="{SKY}">LIVE THROUGHPUT <tspan fill="{DIM}">// ETL STREAM</tspan></text>')
    for i in range(24):
        bx = px + 18 + i * 14.6
        hs = [rnd.randint(10, 82) for _ in range(6)]
        hs.append(hs[0])
        col = GOLD2 if i % 5 == 2 else SKY
        b.append(
            f'<rect x="{f(bx)}" y="0" width="9" height="{hs[0]}" rx="2" fill="{col}" fill-opacity=".75" transform="translate(0 {py + ph - 14}) scale(1 -1)">'
            f'{loop_values("height", hs, rnd.uniform(1.6, 2.8))}</rect>'
        )
    b.append("</g>")

    b.append(
        f'<text x="{W / 2}" y="{H - 22}" text-anchor="middle" class="mono" font-size="10.5" letter-spacing="2.5" fill="{GOLD3}">'
        f'{appear(5.0, .4)}<tspan class="pulse">◢ SCROLL TO BOOT MODULES ◣</tspan></text>'
    )

    # ---- scanline ---------------------------------------------------------
    b.append(
        f'<rect x="0" y="-6" width="{W}" height="3" fill="{GOLD3}" opacity=".12">'
        f'<animate attributeName="y" values="-6;{H + 6}" dur="5s" repeatCount="indefinite"/></rect>'
    )
    b.append("</g>")
    write("boot.svg", doc(W, H, "\n".join(b), defs, css,
                          "Krishna Sidhvi Nekkanti — Forward Deployment AI Engineer. Holographic boot screen."))


# =========================================================================
# 2. NEURAL SKILL MAP
# =========================================================================
LAYERS = [
    ("LANGUAGES", SKY, ["Python", "SQL · T-SQL", "PySpark", "Bash"]),
    ("DATA PLANE", GOLD, ["Apache Kafka", "Apache Spark", "AWS Glue · Redshift", "Snowflake", "Databricks", "Azure Data Factory"]),
    ("INTELLIGENCE", VIOLET, ["LLM Orchestration", "LangChain", "Hugging Face", "Scikit-Learn", "TensorFlow · OpenCV"]),
    ("OUTCOMES", GREEN, ["Data Pipelines", "BI Dashboards", "ML Models", "AI Agents"]),
]
EDGES = {
    (0, 1): {0: [0, 1, 2, 4], 1: [2, 3, 4, 5], 2: [1, 4, 2], 3: [0, 5]},
    (1, 2): {0: [3], 1: [3, 4], 2: [0, 3], 3: [0, 1], 4: [2, 3, 4], 5: [0]},
    (2, 3): {0: [3, 1], 1: [3], 2: [3, 2], 3: [2, 1], 4: [2]},
    (1, 3): {0: [0], 1: [0], 2: [0, 1], 3: [1], 5: [0]},
}


def neural():
    W, H = 1200, 470
    rnd = random.Random(5)
    xs = [150, 450, 750, 1050]
    PW, PH = 196, 34
    pos = {}
    for li, (_, _, nodes) in enumerate(LAYERS):
        n = len(nodes)
        for ni in range(n):
            pos[(li, ni)] = (xs[li], 96 + (ni + .5) * (330 / n))

    b = [bg_body(W, H)]
    for li, (title, col, _) in enumerate(LAYERS):
        b.append(
            f'<text x="{xs[li]}" y="58" text-anchor="middle" class="mono" font-size="11" letter-spacing="3" fill="{col}">'
            f'{appear(.1 + .25 * li, .4)}L{li} · {title}</text>'
        )
        b.append(f'<line x1="{xs[li] - 60}" x2="{xs[li] + 60}" y1="68" y2="68" stroke="{col}" stroke-opacity=".4"/>')

    edges = []
    for (la, lb), mapping in EDGES.items():
        for a, targets in mapping.items():
            for t in targets:
                (x1, y1), (x2, y2) = pos[(la, a)], pos[(lb, t)]
                x1 += PW / 2
                x2 -= PW / 2
                mx = (x2 - x1) * .5
                d = f"M{f(x1)} {f(y1)}C{f(x1 + mx)} {f(y1)} {f(x2 - mx)} {f(y2)} {f(x2)} {f(y2)}"
                edges.append((d, LAYERS[la][1], lb - la > 1, la))
    for d, col, long_, la in edges:
        op = ".18" if long_ else ".32"
        dash = ' stroke-dasharray="3 5"' if long_ else ""
        b.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-opacity="{op}" stroke-width="1"{dash}>{appear(.5 + .3 * la, .6)}</path>')
    for d, col, long_, la in edges:
        dur = rnd.uniform(1.8, 3.2) * (1.6 if long_ else 1)
        begin = rnd.uniform(0, 3)
        b.append(
            f'<circle r="2.6" fill="{col}" filter="url(#glow)" opacity="0">'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.1;.85;1" dur="{f(dur)}s" begin="{f(begin)}s" repeatCount="indefinite"/>'
            f'<animateMotion path="{d}" dur="{f(dur)}s" begin="{f(begin)}s" repeatCount="indefinite"/></circle>'
        )
    for (li, ni), (x, y) in pos.items():
        _, col, nodes = LAYERS[li]
        label = nodes[ni]
        b.append(f'<g>{appear(.2 + .25 * li + .05 * ni, .4)}')
        b.append(f'<rect x="{f(x - PW / 2)}" y="{f(y - PH / 2)}" width="{PW}" height="{PH}" rx="{PH / 2}" fill="{BG2}" stroke="{col}" stroke-opacity=".6"/>')
        b.append(f'<circle cx="{f(x - PW / 2 + 16)}" cy="{f(y)}" r="4" fill="{col}" class="pulse" style="animation-delay:{rnd.uniform(0, 2):.2f}s"/>')
        b.append(f'<text x="{f(x + 6)}" y="{f(y + 4.5)}" text-anchor="middle" class="sans" font-size="13" font-weight="600" fill="{TEXT}">{esc(label)}</text>')
        b.append("</g>")
    b.append(
        f'<text x="{W / 2}" y="{H - 20}" text-anchor="middle" class="mono" font-size="10" letter-spacing="1.5" fill="{DIM}">'
        f"SIGNAL PATH ▸ language → data plane → intelligence → outcome   ·   each pulse = data in flight</text>"
    )
    write("neural.svg", doc(W, H, "\n".join(b), bg_defs(), "",
                            "Neural skill map: languages feed data platforms, which feed AI/ML, which produce pipelines, dashboards, models and agents."))


# =========================================================================
# 3. MISSION TRAJECTORY
# =========================================================================
WAYPOINTS = [
    # x, y, when, org, role, label position
    (110, 342, "2021", "Amity University", "B.Sc. Technology", "up"),
    (290, 310, "JUL 2022", "Vanguard", "Data Analyst", "down"),
    (460, 272, "MAY 2023", "UMBC", "M.P.S. Data Science", "up"),
    (630, 228, "SEP 2023", "Amazon", "Data Engineer", "down"),
    (810, 180, "MAR 2024", "Global Payments", "Data Analytics Engineer", "up"),
    (985, 124, "MAY 2025", "Trida Labs", "Forward Deployment AI Eng.", "down"),
]
NEXT = (1130, 78)


def trajectory():
    W, H = 1200, 440
    rnd = random.Random(7)
    CYCLE, TRAVEL = 8.0, .78
    defs = bg_defs() + f"""
<linearGradient id="tail" x1="1" y1="0" x2="0" y2="0">
  <stop offset="0" stop-color="{GOLD3}" stop-opacity=".95"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/>
</linearGradient>
<linearGradient id="ground" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="{SKY}" stop-opacity=".12"/><stop offset="1" stop-color="{SKY}" stop-opacity="0"/>
</linearGradient>
"""
    b = [bg_body(W, H, grid=False)]
    # starfield
    for _ in range(110):
        x, y = rnd.uniform(20, W - 20), rnd.uniform(20, 380)
        r = rnd.choice([.5, .6, .8, 1, 1.3])
        if rnd.random() < .18:
            d = rnd.uniform(2, 5)
            b.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{r + .4}" fill="{TEXT}">{loop_values("opacity", [.15, 1, .15], d, rnd.uniform(0, 4))}</circle>')
        else:
            b.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{r}" fill="{MUTED}" opacity="{rnd.uniform(.15, .5):.2f}"/>')
    # ground + altitude scale
    b.append(f'<rect x="14" y="392" width="{W - 28}" height="34" fill="url(#ground)"/>')
    b.append(f'<line x1="40" x2="{W - 40}" y1="392" y2="392" stroke="{SKY}" stroke-opacity=".45"/>')
    for i in range(0, 41):
        x = 40 + i * (W - 80) / 40
        b.append(f'<line x1="{f(x)}" x2="{f(x)}" y1="392" y2="{398 if i % 5 else 404}" stroke="{SKY}" stroke-opacity=".4"/>')
    for i, y in enumerate(range(380, 60, -40)):
        b.append(f'<line x1="34" x2="{40 if i % 2 else 46}" y1="{y}" y2="{y}" stroke="{DIM}"/>')
    b.append(f'<text x="30" y="56" class="mono" font-size="9" letter-spacing="2" fill="{DIM}">ALT ▲</text>')
    b.append(f'<text x="{W - 40}" y="420" text-anchor="end" class="mono" font-size="9" letter-spacing="2" fill="{DIM}">TIME ▶</text>')

    pts = [(x, y) for x, y, *_ in WAYPOINTS]
    d, segs = catmull_rom(pts)
    lens = [seg_length(s) for s in segs]
    total = sum(lens)
    cum = [0.0]
    for L in lens:
        cum.append(cum[-1] + L)

    # future (dashed) leg
    fx, fy = NEXT
    lx, ly = pts[-1]
    b.append(f'<path d="M{lx} {ly}C{lx + 60} {ly - 20} {fx - 60} {fy + 30} {fx} {fy}" fill="none" stroke="{GOLD}" stroke-opacity=".5" stroke-width="1.5" stroke-dasharray="4 6"/>')
    b.append(f'<circle cx="{fx}" cy="{fy}" r="6" fill="none" stroke="{GOLD3}" class="blink"/>')
    b.append(f'<text x="{fx}" y="{fy - 16}" text-anchor="middle" class="mono" font-size="11" letter-spacing="2" fill="{GOLD3}">NEXT ▸ ?</text>')

    # flown path (base) + progress overlay synced with comet
    b.append(f'<path d="{d}" fill="none" stroke="{SKY}" stroke-opacity=".25" stroke-width="2"/>')
    b.append(
        f'<path d="{d}" fill="none" stroke="{GOLD2}" stroke-width="2.5" stroke-linecap="round" filter="url(#glow)" '
        f'stroke-dasharray="{f(total)}" stroke-dashoffset="0">'
        f'{loop_values("stroke-dashoffset", [f(total), 0, 0], CYCLE, key_times=[0, TRAVEL, 1])}</path>'
    )
    # waypoints
    for i, (x, y, when, org, role, side) in enumerate(WAYPOINTS):
        t = TRAVEL * cum[i] / total
        t1 = min(t + .015, .999)
        t2 = min(t + .12, .999)
        b.append(
            f'<circle cx="{x}" cy="{y}" r="16" fill="none" stroke="{GOLD2}" stroke-width="1.5" opacity=".35">'
            f'{loop_values("opacity", [0, 0, 1, .35, .35], CYCLE, key_times=[0, t, t1, t2, 1])}'
            f'{loop_values("r", [6, 6, 22, 14, 14], CYCLE, key_times=[0, t, t1, t2, 1])}</circle>'
        )
        b.append(f'<circle cx="{x}" cy="{y}" r="6" fill="{BG0}" stroke="{GOLD2}" stroke-width="2"/>')
        b.append(f'<circle cx="{x}" cy="{y}" r="2.5" fill="{GOLD3}"/>')
        if side == "up":
            ys = (y - 64, y - 46, y - 30)
        else:
            ys = (y + 34, y + 52, y + 68)
        b.append(f'<text x="{x}" y="{ys[0]}" text-anchor="middle" class="mono" font-size="10.5" letter-spacing="2" fill="{GOLD}">{when}</text>')
        b.append(f'<text x="{x}" y="{ys[1]}" text-anchor="middle" class="sans" font-size="15" font-weight="700" fill="{TEXT}">{esc(org)}</text>')
        b.append(f'<text x="{x}" y="{ys[2]}" text-anchor="middle" class="sans" font-size="12" fill="{MUTED}">{esc(role)}</text>')
    # you-are-here
    hx, hy = pts[-1]
    for k in range(3):
        b.append(
            f'<circle cx="{hx}" cy="{hy}" r="8" fill="none" stroke="{GREEN}" stroke-width="1.5" opacity="0">'
            f'{loop_values("r", [8, 34], 3, k)}{loop_values("opacity", [.8, 0], 3, k)}</circle>'
        )
    b.append(f'<text x="{hx + 14}" y="{hy - 14}" class="mono" font-size="9.5" letter-spacing="1.5" fill="{GREEN}">● YOU ARE HERE</text>')
    # comet
    b.append(
        f'<g opacity="0">{loop_values("opacity", [1, 1, 0, 0], CYCLE, key_times=[0, TRAVEL, TRAVEL + .01, 1])}'
        f'<polygon points="0,-3.5 -70,0 0,3.5" fill="url(#tail)"/><circle r="5.5" fill="{GOLD3}" filter="url(#glowBig)"/>'
        f'<animateMotion path="{d}" rotate="auto" dur="{CYCLE}s" repeatCount="indefinite" keyPoints="0;1;1" keyTimes="0;{TRAVEL};1" calcMode="linear"/></g>'
    )
    write("trajectory.svg", doc(W, H, "\n".join(b), defs, "",
                                "Career trajectory: Amity University 2021, Vanguard 2022, UMBC 2023, Amazon 2023, Global Payments 2024, Trida Labs 2025, next."))


# =========================================================================
# 4. CONSOLE (natural-language → SQL)
# =========================================================================
def console():
    W, H = 1200, 312
    O = -156  # vertical offset from original layout
    defs = bg_defs() + f"""
<linearGradient id="bar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#111C33"/><stop offset="1" stop-color="#0B1426"/></linearGradient>
<clipPath id="typeQ"><rect x="244" y="222" height="26" width="0">
  <animate attributeName="width" dur="14s" repeatCount="indefinite" values="0;0;400;400" keyTimes="0;.04;.18;1"/></rect></clipPath>
<clipPath id="typeSql"><rect x="86" y="278" height="26" width="0">
  <animate attributeName="width" dur="14s" repeatCount="indefinite" values="0;0;600;600" keyTimes="0;.25;.42;1"/></rect></clipPath>
"""
    css = f".kw {{ fill: {GOLD}; font-weight: 700; }} .id {{ fill: #E2E8F0; }} .tb {{ fill: {SKY}; }}"

    def show(t):
        return f'<animate attributeName="opacity" dur="14s" repeatCount="indefinite" values="0;0;1;1" keyTimes="0;{t};{t + .01:.2f};1"/>'

    prompt = f'krishna@github<tspan fill="{DIM}">:</tspan><tspan fill="{SKY}">~</tspan><tspan fill="{DIM}">$</tspan>'
    rows = [
        ("Forward Deployment AI Eng.", "Agentic AI · LLM systems", "Python · LangChain · Hugging Face · SQL"),
        ("Data Engineer", "Cloud ETL · data quality", "AWS Glue · Redshift · PySpark · Kafka"),
        ("Data Analyst", "BI · decision intelligence", "Tableau · Power BI · Microsoft Fabric"),
    ]
    b = [bg_body(W, H, scan=False), f'<g transform="translate(0 {O})">']
    b.append(f'<rect x="60" y="176" width="1080" height="282" rx="10" fill="#050810" fill-opacity=".9" stroke="{LINE}" stroke-width="1.2"/>')
    b.append(f'<path d="M70 176H1130A10 10 0 0 1 1140 186V206H60V186A10 10 0 0 1 70 176Z" fill="url(#bar)"/>')
    b.append(f'<line x1="60" y1="206" x2="1140" y2="206" stroke="{LINE}"/>')
    for i, c in enumerate(("#EF4444", GOLD, GREEN)):
        b.append(f'<circle cx="{82 + 18 * i}" cy="191" r="5" fill="{c}" fill-opacity=".85"/>')
    b.append(f'<text x="600" y="195" text-anchor="middle" class="mono" font-size="11" letter-spacing="1" fill="{DIM}">krishna — ask-in-plain-english.sql</text>')
    b.append('<g class="mono" font-size="14">')
    b.append('<animate attributeName="opacity" dur="14s" repeatCount="indefinite" values="1;1;0;0" keyTimes="0;.92;.97;1"/>')
    b.append(f'<text x="88" y="240" fill="{GREEN}">{prompt}</text>')
    b.append(f'<text x="246" y="240" fill="{TEXT}" clip-path="url(#typeQ)">ask <tspan fill="#34D399">"who is krishna, and what does he build?"</tspan></text>')
    b.append(f'<text x="88" y="268" fill="{DIM}">{show(.2)}-- parsing intent → generating SQL → validating against schema ✓</text>')
    b.append(
        '<text x="88" y="296" clip-path="url(#typeSql)"><tspan class="kw">SELECT</tspan><tspan class="id"> role, focus, stack </tspan>'
        '<tspan class="kw">FROM</tspan><tspan class="tb"> krishna.career </tspan><tspan class="kw">ORDER BY</tspan>'
        '<tspan class="id"> impact </tspan><tspan class="kw">DESC</tspan><tspan class="id">;</tspan></text>'
    )
    b.append(f'<g font-size="13"><g>{show(.46)}<rect x="80" y="310" width="1040" height="26" rx="4" fill="{GOLD}" fill-opacity=".1"/>')
    for x, h in ((94, "ROLE"), (370, "FOCUS"), (660, "STACK")):
        b.append(f'<text x="{x}" y="328" fill="{GOLD2}" font-weight="700" letter-spacing="1">{h}</text>')
    b.append("</g>")
    for i, (r1, r2, r3) in enumerate(rows):
        y = 356 + 28 * i
        b.append(
            f'<g>{show(.49 + .03 * i)}<text x="94" y="{y}" fill="#F1F5F9">{esc(r1)}</text>'
            f'<text x="370" y="{y}" fill="{SOFT}">{esc(r2)}</text><text x="660" y="{y}" fill="{MUTED}">{esc(r3)}</text>'
            + (f'<line x1="80" y1="{y + 9}" x2="1120" y2="{y + 9}" stroke="{LINE}"/>' if i < 2 else "")
            + "</g>"
        )
    b.append("</g>")
    b.append(
        f'<g>{show(.59)}<text x="88" y="444" fill="{DIM}" font-size="12.5">(3 rows) <tspan fill="{GREEN}">✓ validated</tspan> · <tspan fill="{GOLD2}">0.042s</tspan></text>'
        f'<text x="360" y="444" fill="{GREEN}" font-size="12.5">{prompt}</text>'
        f'<rect x="494" y="433" width="8" height="15" fill="{GOLD2}" class="blink"/></g>'
    )
    b.append("</g></g>")
    write("console.svg", doc(W, H, "\n".join(b), defs, css,
                             "Terminal: the question 'who is Krishna, and what does he build?' becomes SQL and returns his roles."))


# =========================================================================
# 4b. DATA-FLOW ARCHITECTURE
# =========================================================================
FLOW_MAIN = [  # x-center, title, line1, line2, colour, shape
    (120, "SOURCES", "APIs · transactions", "event streams · files", SKY, "rect"),
    (345, "INGEST + TRANSFORM", "Kafka · AWS Glue", "PySpark · Azure DF", SKY, "rect"),
    (570, "WAREHOUSE", "Redshift · Snowflake", "PostgreSQL · Databricks", GOLD, "cyl"),
    (795, "QUALITY GATE", "validation · reconciliation", "RBAC · masking", GOLD, "hex"),
]
FLOW_OUT = [  # y-center, title, line, colour
    (92, "BI + DASHBOARDS", "Tableau · Power BI", GREEN),
    (196, "ML MODELS", "scikit-learn · TensorFlow", VIOLET),
    (300, "LLM LAYER", "plain English → validated SQL", SKY),
]


def dataflow():
    W, H = 1200, 400
    MY = 196
    NW, NH = 180, 84
    OX, OW, OH = 1065, 200, 62
    rnd = random.Random(3)
    b = [bg_body(W, H)]

    def packet(d, col, dur, begin, r=3):
        return (
            f'<circle r="{r}" fill="{col}" filter="url(#glow)" opacity="0">'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.08;.9;1" dur="{f(dur)}s" begin="{f(begin)}s" repeatCount="indefinite"/>'
            f'<animateMotion path="{d}" dur="{f(dur)}s" begin="{f(begin)}s" repeatCount="indefinite"/></circle>'
        )

    # main pipeline edges
    for (x1, *_), (x2, *_) in zip(FLOW_MAIN, FLOW_MAIN[1:]):
        d = f"M{x1 + NW / 2} {MY}H{x2 - NW / 2}"
        b.append(f'<path d="{d}" stroke="{GOLD}" stroke-opacity=".45" stroke-width="1.5" fill="none"/>')
        b.append(f'<path d="M{x2 - NW / 2 - 8} {MY - 5}L{x2 - NW / 2} {MY}L{x2 - NW / 2 - 8} {MY + 5}" stroke="{GOLD}" fill="none" stroke-width="1.5"/>')
        for k in range(3):
            b.append(packet(d, GOLD2, 1.8, k * .6 + rnd.uniform(0, .3)))
    # gate → outputs
    gx = FLOW_MAIN[-1][0] + NW / 2
    for y, _, _, col in FLOW_OUT:
        d = f"M{gx} {MY}C{gx + 60} {MY} {OX - OW / 2 - 60} {y} {OX - OW / 2} {y}"
        b.append(f'<path d="{d}" stroke="{col}" stroke-opacity=".5" stroke-width="1.5" fill="none"/>')
        for k in range(2):
            b.append(packet(d, col, 2.0, 1.0 + k * 1.0 + rnd.uniform(0, .4)))
    # reject loop: gate → back to ingest (underneath)
    ix = FLOW_MAIN[1][0]
    qx = FLOW_MAIN[-1][0]
    rd = f"M{qx} {MY + NH / 2 + 4}C{qx} {MY + 150} {ix} {MY + 150} {ix} {MY + NH / 2 + 4}"
    b.append(f'<path d="{rd}" stroke="{ROSE}" stroke-opacity=".6" stroke-width="1.3" stroke-dasharray="4 5" fill="none"/>')
    b.append(f'<path d="M{ix - 5} {MY + NH / 2 + 12}L{ix} {MY + NH / 2 + 4}L{ix + 5} {MY + NH / 2 + 12}" stroke="{ROSE}" fill="none" stroke-width="1.3"/>')
    b.append(packet(rd, ROSE, 3.2, 2.2, 3.2))
    b.append(
        f'<rect x="{(qx + ix) / 2 - 78}" y="{MY + 118}" width="156" height="22" rx="11" fill="{BG1}" stroke="{ROSE}" stroke-opacity=".6"/>'
        f'<text x="{(qx + ix) / 2}" y="{MY + 133}" text-anchor="middle" class="mono" font-size="10.5" letter-spacing="1.5" fill="#FCA5A5">✕ REJECT + ALERT</text>'
    )

    # main nodes
    for i, (x, title, l1, l2, col, shape) in enumerate(FLOW_MAIN):
        b.append(f"<g>{appear(.15 * i, .4)}")
        x0, y0 = x - NW / 2, MY - NH / 2
        if shape == "rect":
            b.append(f'<rect x="{x0}" y="{y0}" width="{NW}" height="{NH}" rx="10" fill="{BG2}" stroke="{col}" stroke-opacity=".6" stroke-width="1.3"/>')
        elif shape == "cyl":
            e = 9
            b.append(
                f'<path d="M{x0} {y0 + e}V{y0 + NH - e}A{NW / 2} {e} 0 0 0 {x0 + NW} {y0 + NH - e}V{y0 + e}" fill="{BG2}" stroke="{col}" stroke-opacity=".7" stroke-width="1.3"/>'
                f'<ellipse cx="{x}" cy="{y0 + e}" rx="{NW / 2}" ry="{e}" fill="#0E1A33" stroke="{col}" stroke-opacity=".7" stroke-width="1.3"/>'
            )
        else:  # hexagon gate with scanning beam
            s = 18
            pts = f"{x0},{MY} {x0 + s},{y0} {x0 + NW - s},{y0} {x0 + NW},{MY} {x0 + NW - s},{y0 + NH} {x0 + s},{y0 + NH}"
            b.append(f'<clipPath id="hexClip"><polygon points="{pts}"/></clipPath>')
            b.append(f'<polygon points="{pts}" fill="{BG2}" stroke="{col}" stroke-width="1.6" filter="url(#glow)"/>')
            b.append(
                f'<rect x="{x0}" y="{y0}" width="{NW}" height="3" fill="{GOLD3}" opacity=".35" clip-path="url(#hexClip)">'
                f'<animate attributeName="y" values="{y0};{y0 + NH};{y0}" dur="2.4s" repeatCount="indefinite"/></rect>'
            )
        b.append(f'<circle cx="{x0 + 16}" cy="{y0 + 16}" r="3.5" fill="{col}" class="pulse"/>')
        b.append(f'<text x="{x}" y="{MY - 8}" text-anchor="middle" class="mono" font-size="11.5" font-weight="700" letter-spacing="1.5" fill="{TEXT}">{title}</text>')
        b.append(f'<text x="{x}" y="{MY + 12}" text-anchor="middle" class="sans" font-size="11.5" fill="{MUTED}">{esc(l1)}</text>')
        b.append(f'<text x="{x}" y="{MY + 28}" text-anchor="middle" class="sans" font-size="11.5" fill="{MUTED}">{esc(l2)}</text>')
        b.append("</g>")
    # output nodes
    for i, (y, title, line, col) in enumerate(FLOW_OUT):
        b.append(f"<g>{appear(.7 + .15 * i, .4)}")
        b.append(f'<rect x="{OX - OW / 2}" y="{y - OH / 2}" width="{OW}" height="{OH}" rx="10" fill="{BG2}" stroke="{col}" stroke-opacity=".7" stroke-width="1.3"/>')
        b.append(f'<circle cx="{OX - OW / 2 + 16}" cy="{y - OH / 2 + 16}" r="3.5" fill="{col}" class="pulse"/>')
        b.append(f'<text x="{OX}" y="{y - 3}" text-anchor="middle" class="mono" font-size="11.5" font-weight="700" letter-spacing="1.5" fill="{TEXT}">{title}</text>')
        b.append(f'<text x="{OX}" y="{y + 16}" text-anchor="middle" class="sans" font-size="11.5" fill="{MUTED}">{esc(line)}</text>')
        b.append("</g>")
    b.append(
        f'<text x="40" y="44" class="mono" font-size="10.5" letter-spacing="2" fill="{GOLD}">RAW DATA → TRUSTED INSIGHT'
        f'<tspan fill="{DIM}">  // packets = records in flight · failed checks loop back</tspan></text>'
    )
    write("dataflow.svg", doc(W, H, "\n".join(b), bg_defs(), "",
                              "Data-flow architecture: sources, ingest and transform, warehouse, quality gate, then BI dashboards, ML models and an LLM layer; failed checks loop back to ingest."))


# =========================================================================
# 5. MODULE HEADERS
# =========================================================================
MODULES = {
    "00": "SYSTEM BRIEF",
    "01": "QUERY CONSOLE",
    "02": "NEURAL SKILL MAP",
    "03": "MISSION TRAJECTORY",
    "04": "MISSION LOGS",
    "05": "DATA-FLOW ARCHITECTURE",
    "06": "PROJECT ARCHIVE",
    "07": "ACTIVITY CONSTELLATION",
    "08": "CREDENTIALS",
    "09": "OPEN UPLINK",
}


def header(num, title):
    W, H = 1200, 58
    tw = len(title) * 16
    b = [
        f'<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="10" fill="{BG1}" stroke="{LINE}" stroke-width="1.5"/>',
        f'<path d="M.75 10.75A10 10 0 0 1 10.75 .75H120L104 {H - .75}H10.75A10 10 0 0 1 .75 {H - 10.75}Z" fill="{GOLD}" fill-opacity=".14"/>',
        f'<text x="22" y="36" class="mono" font-size="14" font-weight="700" letter-spacing="2" fill="{GOLD}">MOD.{num}</text>',
        f'<text x="134" y="37" class="sans" font-size="19" font-weight="800" letter-spacing="3.5" fill="{TEXT}">{title}</text>',
    ]
    lx1, lx2 = 150 + tw, W - 150
    b.append(f'<line x1="{f(lx1)}" x2="{lx2}" y1="29" y2="29" stroke="{LINE}" stroke-width="1.5"/>')
    b.append(
        f'<rect x="{f(lx1)}" y="27.5" width="60" height="3" rx="1.5" fill="{SKY}" filter="url(#glow)" opacity="0">'
        f'{loop_values("opacity", [1, 1], 3)}'
        f'<animate attributeName="x" values="{f(lx1)};{lx2 - 60}" dur="3s" repeatCount="indefinite"/></rect>'
    )
    b.append(f'<circle cx="{W - 120}" cy="29" r="4" fill="{GREEN}" class="pulse"/>')
    b.append(f'<text x="{W - 108}" y="33.5" class="mono" font-size="11" letter-spacing="2" fill="{GREEN}">ONLINE</text>')
    b.append(brackets(W, H, inset=4, size=10, opacity=.5))
    write(f"mod/{num}.svg", doc(W, H, "\n".join(b), bg_defs(), "", f"Module {num}: {title.title()}"))


# =========================================================================
# 6. BUTTONS
# =========================================================================
BUTTONS = {
    "nav-console": ("01", "CONSOLE", GOLD),
    "nav-skills": ("02", "SKILL MAP", GOLD),
    "nav-trajectory": ("03", "TRAJECTORY", GOLD),
    "nav-projects": ("06", "PROJECTS", GOLD),
    "nav-uplink": ("09", "UPLINK", GOLD),
    "btn-linkedin": ("in", "LINKEDIN", SKY),
    "btn-email": ("@", "EMAIL", ROSE),
    "btn-github": ("{}", "GITHUB", TEXT),
    "btn-whatsapp": ("☏", "WHATSAPP", GREEN),
}


def button(name, glyph, label, col):
    W, H = 228, 52
    b = [
        f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="9" fill="{BG1}" stroke="{LINE}" stroke-width="1.5"/>',
        f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="9" fill="none" stroke="{col}" stroke-width="1.5" '
        f'stroke-dasharray="40 {2 * (W + H) - 40}" stroke-linecap="round" filter="url(#glow)">'
        f'<animate attributeName="stroke-dashoffset" values="0;-{2 * (W + H)}" dur="4s" repeatCount="indefinite"/></rect>',
        f'<rect x="10" y="10" width="32" height="32" rx="7" fill="{col}" fill-opacity=".12" stroke="{col}" stroke-opacity=".5"/>',
        f'<text x="26" y="31" text-anchor="middle" class="mono" font-size="{13 if len(glyph) > 1 else 16}" font-weight="700" fill="{col}">{esc(glyph)}</text>',
        f'<text x="56" y="32" class="mono" font-size="14" font-weight="700" letter-spacing="2.5" fill="{TEXT}">{label}</text>',
        f'<text x="{W - 16}" y="32" text-anchor="end" class="mono" font-size="13" fill="{col}"><tspan class="pulse">▸</tspan></text>',
    ]
    write(f"btn/{name}.svg", doc(W, H, "\n".join(b), bg_defs(), "", label.title()))


# =========================================================================
# 7. FOOTER — oscilloscope
# =========================================================================
def footer():
    W, H = 1200, 170
    defs = bg_defs() + f"""
<linearGradient id="wave" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{GOLD}" stop-opacity="0"/><stop offset=".2" stop-color="{GOLD2}"/><stop offset=".5" stop-color="{GOLD3}"/>
  <stop offset=".8" stop-color="{SKY}"/><stop offset="1" stop-color="{SKY}" stop-opacity="0"/>
</linearGradient>"""

    def wave(amp, freq, phase, decay):
        pts = []
        for i in range(121):
            x = 60 + i * (W - 120) / 120
            u = (x - W / 2) / (W / 2)
            env = math.exp(-decay * u * u)
            y = 62 + amp * env * math.sin(freq * u * math.pi + phase)
            pts.append(f"{f(x)} {f(y)}")
        return "M" + "L".join(pts)

    shapes = [wave(30, 6, 0, 3), wave(16, 9, 1.2, 2), wave(34, 4, 2.4, 4), wave(10, 14, .6, 1.5), wave(30, 6, 0, 3)]
    b = [bg_body(W, H, grid=True, scan=False)]
    b.append(f'<line x1="60" x2="{W - 60}" y1="62" y2="62" stroke="{LINE}" stroke-dasharray="2 6"/>')
    b.append(
        f'<path d="{shapes[0]}" fill="none" stroke="url(#wave)" stroke-width="2.2" filter="url(#glow)">'
        f'<animate attributeName="d" values="{";".join(shapes)}" dur="6s" repeatCount="indefinite" calcMode="spline" '
        f'keySplines="{";".join([".45 0 .55 1"] * (len(shapes) - 1))}"/></path>'
    )
    b.append(
        f'<text x="{W / 2}" y="122" text-anchor="middle" class="sans" font-size="15" font-weight="800" letter-spacing="6" fill="{TEXT}">'
        f'◢ END OF TRANSMISSION ◣</text>'
    )
    b.append(
        f'<text x="{W / 2}" y="146" text-anchor="middle" class="mono" font-size="10.5" letter-spacing="2" fill="{DIM}">'
        f'KSN//OS · SESSION PERSISTS · THANKS FOR SCANNING<tspan fill="{GOLD2}" class="blink"> _</tspan></text>'
    )
    write("footer.svg", doc(W, H, "\n".join(b), defs, "", "End of transmission"))


if __name__ == "__main__":
    boot()
    console()
    neural()
    trajectory()
    dataflow()
    for k, v in MODULES.items():
        header(k, v)
    for k, v in BUTTONS.items():
        button(k, *v)
    footer()
