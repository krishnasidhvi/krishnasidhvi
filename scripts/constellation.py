"""Activity Constellation — turns a GitHub user's last-365-day contribution
calendar into a star chart. Every star is one real day; brightness is that
day's contribution count; each month's busiest days are joined into a
constellation.

    GITHUB_TOKEN=... python scripts/constellation.py --user krishnasidhvi --out dist/constellation.svg

Runs daily in .github/workflows/constellation.yml. Standard library only.
"""

import argparse
import datetime as dt
import hashlib
import json
import os
import random
import urllib.request

from hud import (DIM, GOLD, GOLD2, GOLD3, MUTED, SKY, TEXT,
                 bg_body, bg_defs, doc, f, loop_values)

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount weekday } }
      }
    }
  }
}"""

LEVEL_STYLE = [  # radius, color, opacity
    (1.05, "#475569", 0.6),
    (1.7, SKY, 0.85),
    (2.3, "#7DD3FC", 0.95),
    (3.0, GOLD2, 1.0),
    (3.8, "#FFFFFF", 1.0),
]


def fetch(user, token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": user}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json", "User-Agent": "ksn-os-constellation"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        payload = json.load(r)
    if "errors" in payload:
        raise SystemExit(f"GraphQL error: {payload['errors']}")
    cal = payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    days = [d for w in cal["weeks"] for d in w["contributionDays"]]
    return cal["totalContributions"], cal["weeks"], days


def jitter(date, axis):
    h = hashlib.sha1(f"{date}:{axis}".encode()).digest()
    return (h[0] / 255 - 0.5) * 2


def longest_streak(days):
    best = cur = 0
    for d in days:
        cur = cur + 1 if d["contributionCount"] > 0 else 0
        best = max(best, cur)
    return best


def render(user, total, weeks, days):
    W, H = 1200, 420
    x0, dx = 74, 20.6
    y0, dy = 104, 34
    counts = sorted(d["contributionCount"] for d in days if d["contributionCount"] > 0)

    def level(c):
        if c == 0 or not counts:
            return 0
        q = [counts[int(len(counts) * p)] for p in (0.25, 0.5, 0.75)]
        return 1 + sum(c > t for t in q)

    pos = {}
    for wi, w in enumerate(weeks):
        for d in w["contributionDays"]:
            x = x0 + wi * dx + jitter(d["date"], "x") * 6
            y = y0 + d["weekday"] * dy + jitter(d["date"], "y") * 9
            pos[d["date"]] = (x, y)

    rnd = random.Random(total)
    b = [bg_body(W, H, grid=False)]

    # faint background dust
    for _ in range(140):
        b.append(f'<circle cx="{f(rnd.uniform(16, W - 16))}" cy="{f(rnd.uniform(16, H - 16))}" r=".5" fill="{MUTED}" opacity="{rnd.uniform(.08, .3):.2f}"/>')

    # constellations: busiest days of each month, joined in date order
    by_month = {}
    for d in days:
        if d["contributionCount"] > 0:
            by_month.setdefault(d["date"][:7], []).append(d)
    for i, (month, ds) in enumerate(sorted(by_month.items())):
        top = sorted(sorted(ds, key=lambda d: -d["contributionCount"])[:5], key=lambda d: d["date"])
        if len(top) < 2:
            continue
        pts = " ".join(f"{f(pos[d['date']][0])},{f(pos[d['date']][1])}" for d in top)
        L = sum(((pos[a['date']][0] - pos[c['date']][0]) ** 2 + (pos[a['date']][1] - pos[c['date']][1]) ** 2) ** .5 for a, c in zip(top, top[1:]))
        delay = .4 + i * .12
        b.append(
            f'<polyline points="{pts}" fill="none" stroke="{GOLD}" stroke-opacity=".38" stroke-width=".9" '
            f'stroke-dasharray="{f(L)}" stroke-dashoffset="0">'
            f'<animate attributeName="stroke-dashoffset" values="{f(L)};{f(L)};0" keyTimes="0;{delay / (delay + 1.2):.3f};1" dur="{f(delay + 1.2)}s" fill="freeze"/>'
            f"</polyline>"
        )

    # stars
    brightest = {d["date"] for d in sorted(days, key=lambda d: -d["contributionCount"])[:14] if d["contributionCount"] > 0}
    for d in days:
        x, y = pos[d["date"]]
        lv = level(d["contributionCount"])
        r, col, op = LEVEL_STYLE[lv]
        title = f'<title>{d["date"]}: {d["contributionCount"]} contribution{"s" if d["contributionCount"] != 1 else ""}</title>'
        if d["date"] in brightest:
            tw = rnd.uniform(2.2, 4.5)
            b.append(
                f'<g filter="url(#glow)">{title}'
                f'<path d="M{f(x - 9)} {f(y)}H{f(x + 9)}M{f(x)} {f(y - 9)}V{f(y + 9)}" stroke="{GOLD3}" stroke-width=".8" opacity=".7">'
                f'{loop_values("opacity", [.2, .9, .2], tw, rnd.uniform(0, 3))}</path>'
                f'<circle cx="{f(x)}" cy="{f(y)}" r="{r}" fill="{col}"/></g>'
            )
        else:
            extra = loop_values("opacity", [op, op * .35, op], rnd.uniform(3, 7), rnd.uniform(0, 5)) if lv and rnd.random() < .3 else ""
            b.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{r}" fill="{col}" opacity="{op}">{title}{extra}</circle>')

    # month labels + weekday labels
    seen = set()
    for wi, w in enumerate(weeks):
        first = w["contributionDays"][0]["date"]
        m = first[:7]
        if m not in seen and int(first[8:]) <= 7:
            seen.add(m)
            label = dt.date.fromisoformat(first).strftime("%b").upper()
            b.append(f'<text x="{f(x0 + wi * dx)}" y="{y0 + 6 * dy + 34}" class="mono" font-size="9.5" letter-spacing="1.5" fill="{DIM}">{label}</text>')
    for wd, name in ((1, "MON"), (3, "WED"), (5, "FRI")):
        b.append(f'<text x="30" y="{y0 + wd * dy + 3}" class="mono" font-size="8.5" letter-spacing="1" fill="{DIM}">{name}</text>')

    # shooting star
    b.append(
        f'<g opacity="0">{loop_values("opacity", [0, 0, 1, 0, 0], 11, 0, [0, .6, .63, .7, 1])}'
        f'<line x1="0" y1="0" x2="-80" y2="-26" stroke="{GOLD3}" stroke-width="1.4" stroke-linecap="round"/>'
        f'<animateTransform attributeName="transform" type="translate" values="300 40;300 40;760 190;760 190" keyTimes="0;.6;.7;1" dur="11s" repeatCount="indefinite"/></g>'
    )

    # readout
    active = sum(1 for d in days if d["contributionCount"] > 0)
    peak = max(days, key=lambda d: d["contributionCount"])
    stats = [
        ("TOTAL", f"{total:,}"),
        ("ACTIVE DAYS", f"{active}"),
        ("LONGEST STREAK", f"{longest_streak(days)}d"),
        ("PEAK", f"{peak['contributionCount']} · {dt.date.fromisoformat(peak['date']).strftime('%d %b %Y').upper()}"),
    ]
    x = 40
    for k, v in stats:
        b.append(
            f'<text x="{x}" y="46" class="mono" font-size="10" letter-spacing="1.5" fill="{DIM}">{k}</text>'
            f'<text x="{x}" y="68" class="sans" font-size="18" font-weight="800" fill="{TEXT}">{v}</text>'
        )
        x += 190 if k != "LONGEST STREAK" else 210
    b.append(
        f'<text x="{W - 40}" y="46" text-anchor="end" class="mono" font-size="10" letter-spacing="1.5" fill="{GOLD}">SKY SURVEY // LAST 365 DAYS</text>'
        f'<text x="{W - 40}" y="66" text-anchor="end" class="mono" font-size="10" letter-spacing="1" fill="{DIM}">'
        f'1 star = 1 day · brightness = contributions</text>'
    )
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    b.append(
        f'<text x="{W / 2}" y="{H - 16}" text-anchor="middle" class="mono" font-size="9.5" letter-spacing="1.5" fill="{DIM}">'
        f'RENDERED {stamp} FROM github.com/{user} · REGENERATES DAILY</text>'
    )
    return doc(W, H, "\n".join(b), bg_defs(), "", f"Activity constellation for {user}: {total} contributions in the last year, one star per day.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit("GITHUB_TOKEN is not set")
    total, weeks, days = fetch(a.user, token)
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    with open(a.out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(render(a.user, total, weeks, days))
    print(f"wrote {a.out}: {total} contributions, {len(days)} days")


if __name__ == "__main__":
    main()
