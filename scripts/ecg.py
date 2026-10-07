"""Render dist/ecg.svg: the GitHub activity card drawn as a patient monitor.

Each of the last 42 days is one heartbeat on an ECG trace (QRS height grows with that
day's contributions, empty days flatline), with a sweeping gap that redraws the trace
like a bedside monitor. The side panel shows HR (contributions in the last 7 days),
current/longest streak and the 12-month total.

Runs in the profile workflow with the repo's GITHUB_TOKEN. Counts include private
contributions when "Include private contributions on my profile" is enabled.
Standard library only.

    GITHUB_TOKEN=... python3 scripts/ecg.py <login> <out.svg>
    python3 scripts/ecg.py --sample <out.svg>   # offline preview with fake data
"""
import datetime as dt
import json
import math
import os
import random
import sys
import urllib.request

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}"""

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
W, H = 880, 250
TRACE, SOFT, TEXT = "#60A5FA", "#93C5FD", "#FFFFFF"
DAYS = 42           # one beat per day on the trace
SWEEP = 7           # seconds for the sweep to cross the trace
X0, X1, BASE, AMAX = 32, 620, 172, 92

# P wave, QRS complex and T wave as (x fraction of the beat, y fraction of amplitude; negative = up)
PQRST = [(0, 0), (.16, 0), (.22, -.12), (.28, 0), (.36, 0), (.40, .10), (.46, -1.0),
         (.52, .28), (.57, 0), (.66, 0), (.75, -.22), (.84, 0)]


def fetch(login, token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        body = json.load(r)
    if "errors" in body:
        sys.exit(f"GraphQL error: {body['errors']}")
    weeks = body["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    return [(d["date"], d["contributionCount"]) for w in weeks for d in w["contributionDays"]]


def sample():
    today = dt.date.today()
    return [((today - dt.timedelta(n)).isoformat(), random.choice([0, 0, 1, 2, 3, 5, 8]))
            for n in range(364, -1, -1)]


def streaks(counts):
    longest = run = 0
    for c in counts:
        run = run + 1 if c else 0
        longest = max(longest, run)
    # current streak may end yesterday if nothing has been pushed yet today
    i = len(counts) - 1
    if counts and counts[i] == 0:
        i -= 1
    current = 0
    while i >= 0 and counts[i]:
        current += 1
        i -= 1
    return current, longest


def trace_points(values):
    """Polyline for the ECG. Square-root amplitude so one huge day doesn't flatten the rest."""
    w = (X1 - X0) / len(values)
    peak = max(values) or 1
    pts = []
    for i, c in enumerate(values):
        a = AMAX * (0.22 + 0.78 * math.sqrt(c / peak)) if c else 0
        for fx, fy in (PQRST if a else [(0, 0)]):
            pts.append((X0 + (i + fx) * w, BASE + fy * a))
    pts.append((X1, BASE))
    return pts


def path_d(pts):
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)


def head_motion(pts):
    """keyTimes/keyPoints that move the head dot at constant x speed, in step with the sweep gap."""
    clean = [pts[0]]
    for p in pts[1:]:
        if p[0] > clean[-1][0] + 1e-6:
            clean.append(p)
    cum = [0.0]
    for (ax, ay), (bx, by) in zip(clean, clean[1:]):
        cum.append(cum[-1] + math.hypot(bx - ax, by - ay))
    times = ";".join(f"{(x - X0) / (X1 - X0):.4f}" for x, _ in clean)
    points = ";".join(f"{c / cum[-1]:.4f}" for c in cum)
    return path_d(clean), times, points


def grid(x0, y0, x1, y1, step):
    lines = [f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y1}"/>' for x in range(x0, x1 + 1, step)]
    lines += [f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}"/>' for y in range(y0, y1 + 1, step)]
    return f'<g stroke="{TRACE}" stroke-opacity=".07">{"".join(lines)}</g>'


def panel(counts, x=652, top=56):
    week = sum(counts[-7:])
    current, longest = streaks(counts)
    year = counts[-365:]
    total, active = sum(year), sum(1 for c in year if c)
    out = [
        f'<line x1="{x - 24}" y1="{top - 4}" x2="{x - 24}" y2="{H - 28}" stroke="{TRACE}" stroke-opacity=".25"/>',
        f'<text x="{x}" y="{top + 12}" font-size="12" font-weight="700" fill="{SOFT}" letter-spacing="1.5">HR</text>',
        f'<g transform="translate({x + 34} {top + 2}) scale(.95)"><path class="hb" fill="#F87171" '
        'd="M0 3.2C-1.6-.6-7-.4-7 3.6-7 7.4-2.2 10 0 12.6 2.2 10 7 7.4 7 3.6 7-.4 1.6-.6 0 3.2Z"/></g>',
        f'<text x="{x + 196}" y="{top + 12}" font-size="11" fill="{SOFT}" text-anchor="end">per week</text>',
        f'<text class="n" x="{x}" y="{top + 70}" font-size="56" font-weight="700" fill="{TEXT}">{week}</text>',
    ]
    rows = [("STREAK", f"{current}", f"best {longest}"), ("YEAR", f"{total:,}", f"{active} active days")]
    for i, (label, big, small) in enumerate(rows):
        y = top + 104 + i * 46
        out += [
            f'<text x="{x}" y="{y}" font-size="11" font-weight="700" fill="{SOFT}" letter-spacing="1.5">{label}</text>',
            f'<text class="n" x="{x}" y="{y + 22}" font-size="20" font-weight="700" fill="{TEXT}">{big}</text>',
            f'<text x="{x + 196}" y="{y + 22}" font-size="11" fill="{SOFT}" text-anchor="end">{small}</text>',
        ]
    return "".join(out)


def render(days):
    counts = [c for _, c in days]
    window = days[-DAYS:]
    pts = trace_points([c for _, c in window])
    head_d, times, points = head_motion(pts)
    current, longest = streaks(counts)
    start = dt.date.fromisoformat(window[0][0]).strftime("%b %-d")

    css = (
        f"text{{font-family:{SANS}}}.n{{font-family:{MONO};font-variant-numeric:tabular-nums}}"
        "@keyframes beat{0%,100%{transform:scale(1)}12%{transform:scale(1.28)}24%{transform:scale(1)}}"
        ".hb{transform-box:fill-box;transform-origin:center;animation:beat 1.1s ease-out infinite}"
        "@media (prefers-reduced-motion:reduce){.mv{display:none}.hb{animation:none}}"
    )
    defs = (
        '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#030A1F"/>'
        '<stop offset=".6" stop-color="#0A1A4F"/><stop offset="1" stop-color="#1238A8"/></linearGradient>'
        '<filter id="glow" x="-5%" y="-30%" width="110%" height="160%"><feGaussianBlur stdDeviation="2.4" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
        # the sweep: a black bar in the mask erases the trace just ahead of the head dot
        f'<mask id="sweep" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">'
        f'<rect width="{W}" height="{H}" fill="#fff"/><rect class="mv" width="30" height="{H}" fill="#000">'
        f'<animateTransform attributeName="transform" type="translate" from="{X0 + 6} 0" to="{X1 + 6} 0" '
        f'dur="{SWEEP}s" repeatCount="indefinite"/></rect></mask></defs>'
    )
    body = [
        f'<rect width="{W}" height="{H}" rx="18" fill="url(#g)"/>',
        f'<text x="32" y="38" font-size="15" font-weight="600" fill="{TEXT}">GitHub activity</text>',
        f'<text x="173" y="38" font-size="11" font-weight="600" fill="{SOFT}" letter-spacing="1.2">'
        f'LEAD II · DAILY · 6 WEEKS</text>',
        f'<text x="{W - 32}" y="38" font-size="11" fill="{SOFT}" text-anchor="end">'
        f'updated {dt.date.today().isoformat()}</text>',
        grid(X0, 56, X1, 216, 20),
        f'<g mask="url(#sweep)"><path d="{path_d(pts)}" fill="none" stroke="{TRACE}" stroke-width="2" '
        f'stroke-linejoin="round" stroke-linecap="round" filter="url(#glow)"/></g>',
        f'<circle class="mv" r="3.6" fill="#FFFFFF" filter="url(#glow)"><animateMotion dur="{SWEEP}s" '
        f'repeatCount="indefinite" calcMode="linear" keyTimes="{times}" keyPoints="{points}" path="{head_d}"/></circle>',
        f'<text x="{X0}" y="{H - 14}" font-size="11" fill="{SOFT}">{start}</text>',
        f'<text x="{X1}" y="{H - 14}" font-size="11" fill="{SOFT}" text-anchor="end">today</text>',
        panel(counts),
    ]
    label = (f"GitHub activity as a heart monitor: {sum(counts[-7:])} contributions in the last 7 days, "
             f"{sum(counts[-365:])} in the last 12 months, current streak {current} days, longest {longest} days")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'role="img" aria-label="{label}"><style>{css}</style>{defs}{"".join(body)}</svg>')


if __name__ == "__main__":
    if sys.argv[1] == "--sample":
        days, path = sample(), sys.argv[2]
    else:
        days, path = fetch(sys.argv[1], os.environ["GITHUB_TOKEN"]), sys.argv[2]
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    open(path, "w", encoding="utf-8").write(render(days))
    print(f"wrote {path}: {sum(c for _, c in days[-7:])} contributions in the last 7 days")
