"""Render dist/stats.svg: a night-blue GitHub activity card for the profile README.

Runs in the snake workflow with the repo's GITHUB_TOKEN, so the profile no longer
depends on third-party stats services. Counts include private contributions when
"Include private contributions on my profile" is enabled. Standard library only.

    GITHUB_TOKEN=... python3 scripts/stats.py <login> <out.svg>
    python3 scripts/stats.py --sample <out.svg>   # offline preview with fake data
"""
import datetime as dt
import json
import os
import random
import sys
import urllib.request

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      restrictedContributionsCount
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}"""

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"


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
    c = body["data"]["user"]["contributionsCollection"]
    days = [(d["date"], d["contributionCount"])
            for w in c["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    return {
        "total": c["contributionCalendar"]["totalContributions"],
        "commits": c["totalCommitContributions"] + c["restrictedContributionsCount"],
        "prs": c["totalPullRequestContributions"],
        "days": days,
    }


def sample():
    today = dt.date.today()
    days = [((today - dt.timedelta(n)).isoformat(), random.choice([0, 0, 1, 2, 3, 5, 8]))
            for n in range(363, -1, -1)]
    return {"total": sum(c for _, c in days), "commits": 300, "prs": 12, "days": days}


def streaks(days):
    counts = [c for _, c in days]
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


def render(s):
    W, H = 880, 250
    current, longest = streaks(s["days"])
    active = sum(1 for _, c in s["days"] if c)
    stats = [
        (f"{s['total']:,}", "contributions"),
        (f"{active}", "active days"),
        (f"{current}", "current streak"),
        (f"{longest}", "longest streak"),
    ]
    # weekly totals for the bar strip (last 52 weeks)
    counts = [c for _, c in s["days"]]
    weeks = [sum(counts[i:i + 7]) for i in range(max(0, len(counts) - 364), len(counts), 7)][-52:]
    peak = max(weeks) or 1

    css = (
        f"text{{font-family:{SANS}}}"
        "@keyframes up{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}"
        "@keyframes grow{from{transform:scaleY(0)}to{transform:scaleY(1)}}"
        ".b{transform-box:fill-box;transform-origin:bottom;animation:grow .7s cubic-bezier(.2,.8,.2,1) both}"
        "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"
    )
    out = [
        f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#030A1F"/>'
        f'<stop offset=".6" stop-color="#0A1A4F"/><stop offset="1" stop-color="#1238A8"/></linearGradient>'
        f'<linearGradient id="bar" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#1D4ED8"/>'
        f'<stop offset="1" stop-color="#60A5FA"/></linearGradient></defs>',
        f'<rect width="{W}" height="{H}" rx="18" fill="url(#g)"/>',
        f'<text x="32" y="40" font-size="15" font-weight="600" fill="#FFFFFF">GitHub activity</text>',
        f'<text x="{W-32}" y="40" font-size="12" fill="#93C5FD" text-anchor="end">last 12 months · '
        f'updated {dt.date.today().isoformat()}</text>',
    ]
    col = (W - 64) / 4
    for i, (num, label) in enumerate(stats):
        x = 32 + col * i
        out.append(
            f'<g style="animation:up .6s {0.1 + i * 0.12:.2f}s ease-out both">'
            f'<text x="{x:.0f}" y="100" font-size="40" font-weight="700" fill="#FFFFFF">{num}</text>'
            f'<text x="{x:.0f}" y="124" font-size="12" font-weight="600" fill="#93C5FD" '
            f'letter-spacing="1.5">{label.upper()}</text></g>')
    # weekly bar strip
    bx, by, bh = 32, 220, 62
    bw = (W - 64) / 52
    for i, v in enumerate(weeks):
        h = max(2, bh * v / peak)
        out.append(f'<rect class="b" x="{bx + i*bw + 1:.1f}" y="{by - h:.1f}" width="{bw - 2:.1f}" height="{h:.1f}" '
                   f'rx="2" fill="url(#bar)" fill-opacity="{0.35 if v == 0 else 1}" '
                   f'style="animation-delay:{0.5 + i*0.015:.3f}s"/>')
    out.append(f'<text x="32" y="{by+18}" font-size="11" fill="#93C5FD">weekly contributions</text>')
    out.append(f'<text x="{W-32}" y="{by+18}" font-size="11" fill="#93C5FD" text-anchor="end">'
               f'{s["commits"]:,} commits · {s["prs"]} pull requests</text>')
    label = (f"GitHub activity, last 12 months: {s['total']} contributions, {active} active days, "
             f"current streak {current} days, longest streak {longest} days")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'role="img" aria-label="{label}"><style>{css}</style>{"".join(out)}</svg>')


if __name__ == "__main__":
    if sys.argv[1] == "--sample":
        data, path = sample(), sys.argv[2]
    else:
        data, path = fetch(sys.argv[1], os.environ["GITHUB_TOKEN"]), sys.argv[2]
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    open(path, "w", encoding="utf-8").write(render(data))
    print(f"wrote {path}: {data['total']} contributions")
