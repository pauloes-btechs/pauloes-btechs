#!/usr/bin/env python3
"""Build the GitHub activity tracker SVGs for the profile README.

Runs inside GitHub Actions with the repo's GITHUB_TOKEN (public data only — no PAT needed).
Writes four SVGs into dist/:
  stats.svg      — commits (YTD + all time), PRs, stars, public repos, followers
  languages.svg  — top languages by bytes across public repos
  heatmap.svg    — 52-week contribution grid
  commits.svg    — latest 5 commits (repo · message · date)

Usage:  GITHUB_TOKEN=... GH_USER=pauloes-btechs python3 scripts/build_stats.py [--mock]
"""
import os, sys, json, html, datetime as dt, urllib.request, urllib.parse, math, random

USER  = os.environ.get("GH_USER", "pauloes-btechs")
# GH_PAT (a personal token saved as a repo secret) unlocks private repos; GITHUB_TOKEN is the public-only fallback.
TOKEN = os.environ.get("GH_PAT") or os.environ.get("GITHUB_TOKEN", "")
PRIVATE_OK = bool(os.environ.get("GH_PAT"))
OUT   = os.environ.get("OUT_DIR", "dist")
MOCK  = "--mock" in sys.argv
os.makedirs(OUT, exist_ok=True)

BG, PANEL, PANEL2, BORDER = "#080D1A", "#0C1324", "#101A30", "#1E2A40"
TEXT, MUTED, DIM, ORANGE, BLUE, GREEN = "#E2E8F0", "#94A3B8", "#475569", "#F7931A", "#5B8DEF", "#3FAE5E"
SANS = "'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "'SFMono-Regular',Menlo,Consolas,'Liberation Mono',monospace"
HEAT = ["#101A30", "#3A2A14", "#8A5010", "#C7761A", "#F7931A"]
LANG_COLORS = {"TypeScript": "#3178C6", "JavaScript": "#F1E05A", "Python": "#3572A5", "HTML": "#E34C26",
               "CSS": "#563D7C", "Shell": "#89E051", "Go": "#00ADD8", "Rust": "#DEA584", "SQL": "#E38C00",
               "PLpgSQL": "#336790", "Dockerfile": "#384D54", "MDX": "#FCB32C", "Solidity": "#AA6746"}

def esc(s): return html.escape(str(s), quote=True)

# ----------------------------------------------------------------- data
def api(path, params=None):
    url = "https://api.github.com" + path + (("?" + urllib.parse.urlencode(params)) if params else "")
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json",
                                               "Authorization": f"Bearer {TOKEN}" if TOKEN else "",
                                               "User-Agent": "profile-stats"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def graphql(query, variables):
    req = urllib.request.Request("https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json", "User-Agent": "profile-stats"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)["data"]

def safe(fn, default):
    try:
        return fn()
    except Exception as e:  # keep the run alive; a card with zeros beats a red workflow
        print("warn:", e, file=sys.stderr)
        return default

def fetch():
    today = dt.date.today()
    year_start = dt.date(today.year, 1, 1)
    u = api(f"/users/{USER}")
    if PRIVATE_OK:
        # everything the token can see: own repos + org repos (private included), paginated
        repos, page = [], 1
        while True:
            chunk = api("/user/repos", {"per_page": 100, "page": page, "affiliation": "owner,collaborator,organization_member", "sort": "pushed"})
            repos += chunk
            if len(chunk) < 100: break
            page += 1
    else:
        repos = api(f"/users/{USER}/repos", {"per_page": 100, "type": "owner", "sort": "pushed"})
    repos = [r for r in repos if not r["fork"]]
    n_private = sum(1 for r in repos if r["private"])
    stars = sum(r["stargazers_count"] for r in repos)
    langs = {}
    for r in repos:
        try:
            for k, v in api(f"/repos/{r['full_name']}/languages").items():
                langs[k] = langs.get(k, 0) + v
        except Exception:
            pass
    commits_all = safe(lambda: api("/search/commits", {"q": f"author:{USER}", "per_page": 1}).get("total_count", 0), 0)
    commits_ytd = safe(lambda: api("/search/commits", {"q": f"author:{USER} author-date:>={year_start}", "per_page": 1}).get("total_count", 0), 0)
    prs = safe(lambda: api("/search/issues", {"q": f"author:{USER} type:pr", "per_page": 1}).get("total_count", 0), 0)
    latest = safe(lambda: api("/search/commits", {"q": f"author:{USER}", "sort": "author-date", "order": "desc", "per_page": 5}).get("items", []), [])
    # private repos never leak names or messages onto the public profile
    latest = [{"repo": "private repo" if c["repository"]["private"] else c["repository"]["full_name"],
               "msg": "commit in a private repository" if c["repository"]["private"] else c["commit"]["message"].splitlines()[0],
               "private": c["repository"]["private"],
               "date": c["commit"]["author"]["date"][:10], "url": c["html_url"]} for c in latest]
    # contribution calendar (public contributions) via GraphQL
    q = """query($u:String!){ user(login:$u){ contributionsCollection{ totalCommitContributions
             contributionCalendar{ totalContributions weeks{ contributionDays{ date contributionCount } } } } } }"""
    cal = safe(lambda: graphql(q, {"u": USER})["user"]["contributionsCollection"]["contributionCalendar"],
               {"totalContributions": 0, "weeks": []})
    days = [(d["date"], d["contributionCount"]) for w in cal["weeks"] for d in w["contributionDays"]]
    if not days:
        days = [((today - dt.timedelta(days=i)).isoformat(), 0) for i in range(364, -1, -1)]
    return dict(name=u.get("name") or USER, followers=u["followers"], public_repos=u["public_repos"],
                repos_total=len(repos), n_private=n_private, private_ok=PRIVATE_OK,
                stars=stars, langs=langs, commits_all=commits_all, commits_ytd=commits_ytd, prs=prs,
                latest=latest, days=days, total_contrib=cal["totalContributions"])

def mock():
    random.seed(3)
    today = dt.date.today()
    days = [((today - dt.timedelta(days=i)).isoformat(), max(0, int(random.gauss(1.2, 2.5)))) for i in range(364, -1, -1)]
    return dict(name="Pauloes Berhe", followers=12, public_repos=4, repos_total=7, n_private=3, private_ok=True, stars=9, commits_all=212, commits_ytd=188, prs=14,
                langs={"TypeScript": 412000, "JavaScript": 98000, "CSS": 61000, "Python": 44000, "Shell": 9000, "HTML": 7000},
                latest=[{"repo": "pauloes-btechs/portfolio", "msg": "v3.11: mobile hero stacking + role breadcrumbs", "date": "2026-09-16", "url": ""},
                        {"repo": "pauloes-btechs/pauloes-btechs", "msg": "Profile README: btechs.io palette, link tabs, featured projects", "date": "2026-09-16", "url": ""},
                        {"repo": "private repo", "msg": "commit in a private repository", "private": True, "date": "2026-09-12", "url": ""},
                        {"repo": "pauloes-btechs/portfolio", "msg": "OG image + metadataBase", "date": "2026-09-04", "url": ""},
                        {"repo": "pauloes-btechs/btechs", "msg": "Security page copy pass", "date": "2026-08-30", "url": ""}],
                days=days, total_contrib=sum(c for _, c in days))

# ----------------------------------------------------------------- svg helpers
def frame(W, H, label, note, body, rx=14):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(label)}">
<defs><pattern id="g" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M 30 0 L 0 0 0 30" fill="none" stroke="#94A3B8" stroke-opacity="0.06"/></pattern></defs>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="{rx}" fill="{PANEL}" stroke="{BORDER}"/>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="{rx}" fill="url(#g)"/>
<rect x="0" y="0" width="5" height="{H}" rx="2" fill="{ORANGE}"/>
<text x="28" y="38" font-family="{MONO}" font-size="11" letter-spacing="2.5" fill="{ORANGE}">{esc(label)}</text>
<text x="{W-28}" y="38" text-anchor="end" font-family="{MONO}" font-size="10.5" letter-spacing="2" fill="{DIM}">{esc(note)}</text>
{body}
</svg>'''

def fmt(n):
    return f"{n/1000:.1f}k" if n >= 10000 else f"{n:,}"

# ----------------------------------------------------------------- cards
def stats_card(d, stamp):
    W, H = 580, 270
    tiles = [("COMMITS · " + str(dt.date.today().year), d["commits_ytd"], ORANGE),
             ("COMMITS · ALL TIME", d["commits_all"], TEXT),
             ("PULL REQUESTS", d["prs"], BLUE),
             ("STARS EARNED", d["stars"], ORANGE),
             ("REPOS · INCL. PRIVATE" if d.get("private_ok") else "PUBLIC REPOS", d["repos_total"] if d.get("private_ok") else d["public_repos"], TEXT),
             ("FOLLOWERS", d["followers"], GREEN)]
    body = []
    for i, (lab, val, col) in enumerate(tiles):
        x = 28 + (i % 3) * 178; y = 96 + (i // 3) * 86
        body.append(f'<rect x="{x}" y="{y-34}" width="164" height="68" rx="10" fill="{PANEL2}" stroke="{BORDER}"/>'
                    f'<text x="{x+14}" y="{y+2}" font-family="{SANS}" font-size="28" font-weight="700" fill="{col}">{fmt(val)}</text>'
                    f'<text x="{x+14}" y="{y+22}" font-family="{MONO}" font-size="9.5" letter-spacing="1.5" fill="{MUTED}">{esc(lab)}</text>')
    scope = "PUBLIC + PRIVATE" if d.get("private_ok") else "PUBLIC ONLY"
    body.append(f'<text x="28" y="{H-16}" font-family="{MONO}" font-size="10" letter-spacing="1.5" fill="{DIM}">{d["total_contrib"]} CONTRIBUTIONS IN THE LAST YEAR  ·  {scope}</text>')
    return frame(W, H, "GITHUB  ·  BY THE NUMBERS", "UPDATED " + stamp, "".join(body))

def languages_card(d, stamp):
    W, H = 580, 270
    total = sum(d["langs"].values()) or 1
    top = sorted(d["langs"].items(), key=lambda kv: -kv[1])[:6]
    body = []
    # stacked bar
    x = 28; bw = W - 56
    for name, b in top:
        w = bw * b / total
        body.append(f'<rect x="{x:.1f}" y="62" width="{max(w-2,1):.1f}" height="12" rx="3" fill="{LANG_COLORS.get(name, MUTED)}"/>')
        x += w
    for i, (name, b) in enumerate(top):
        cx = 28 + (i % 2) * 276; cy = 112 + (i // 2) * 44
        pct = 100 * b / total
        body.append(f'<circle cx="{cx+6}" cy="{cy-5}" r="6" fill="{LANG_COLORS.get(name, MUTED)}"/>'
                    f'<text x="{cx+22}" y="{cy}" font-family="{SANS}" font-size="15" font-weight="600" fill="{TEXT}">{esc(name)}</text>'
                    f'<text x="{cx+250}" y="{cy}" text-anchor="end" font-family="{MONO}" font-size="12" fill="{MUTED}">{pct:.1f}%</text>'
                    f'<rect x="{cx}" y="{cy+8}" width="250" height="3" rx="1.5" fill="{PANEL2}"/>'
                    f'<rect x="{cx}" y="{cy+8}" width="{250*pct/100:.1f}" height="3" rx="1.5" fill="{LANG_COLORS.get(name, MUTED)}"/>')
    if not top:
        body.append(f'<text x="28" y="120" font-family="{SANS}" font-size="15" fill="{MUTED}">No public code yet — check back soon.</text>')
    return frame(W, H, "TOP LANGUAGES  ·  PUBLIC REPOS", "BY BYTES", "".join(body))

def heatmap_card(d, stamp):
    W, H = 1200, 230
    days = d["days"][-364:]
    # align to weeks starting Sunday
    first = dt.date.fromisoformat(days[0][0])
    pad = (first.weekday() + 1) % 7
    cells = [None] * pad + days
    weeks = math.ceil(len(cells) / 7)
    cs, gap = 15, 4
    x0, y0 = 60, 66
    mx = max([c for _, c in days] + [1])
    body = []
    def level(c):
        if c == 0: return 0
        return min(4, 1 + int(3 * c / mx)) if mx > 3 else min(4, c)
    month_labels = {}
    for i, cell in enumerate(cells):
        w, dw = divmod(i, 7)
        if cell is None: continue
        date, c = cell
        dd = dt.date.fromisoformat(date)
        if dd.day <= 7 and w not in month_labels.values():
            month_labels[dd.strftime("%b").upper()] = w
        body.append(f'<rect x="{x0 + w*(cs+gap)}" y="{y0 + dw*(cs+gap)}" width="{cs}" height="{cs}" rx="3" fill="{HEAT[level(c)]}"><title>{date}: {c}</title></rect>')
    for lab, w in month_labels.items():
        body.append(f'<text x="{x0 + w*(cs+gap)}" y="{y0-10}" font-family="{MONO}" font-size="9.5" letter-spacing="1.5" fill="{DIM}">{lab}</text>')
    for lab, dw in (("MON", 1), ("WED", 3), ("FRI", 5)):
        body.append(f'<text x="{x0-10}" y="{y0 + dw*(cs+gap) + 11}" text-anchor="end" font-family="{MONO}" font-size="9" fill="{DIM}">{lab}</text>')
    # legend
    lx = W - 28 - 5 * 19 - 44
    body.append(f'<text x="{lx-10}" y="{H-14}" text-anchor="end" font-family="{MONO}" font-size="9.5" letter-spacing="1.5" fill="{DIM}">LESS</text>')
    for i, col in enumerate(HEAT):
        body.append(f'<rect x="{lx + i*19}" y="{H-25}" width="14" height="14" rx="3" fill="{col}"/>')
    body.append(f'<text x="{lx + 5*19 + 4}" y="{H-14}" font-family="{MONO}" font-size="9.5" letter-spacing="1.5" fill="{DIM}">MORE</text>')
    body.append(f'<text x="28" y="{H-14}" font-family="{MONO}" font-size="10" letter-spacing="1.5" fill="{DIM}">{d["total_contrib"]} PUBLIC CONTRIBUTIONS  ·  LAST 52 WEEKS</text>')
    return frame(W, H, "CONTRIBUTIONS  ·  52 WEEKS", "UPDATED " + stamp, "".join(body))

def commits_card(d, stamp):
    rows = d["latest"][:5]
    W, H = 1200, 70 + 44 * max(len(rows), 1) + 16
    body = []
    for i, c in enumerate(rows):
        y = 84 + i * 44
        msg = c["msg"] if len(c["msg"]) <= 78 else c["msg"][:77] + "…"
        priv = c.get("private")
        body.append(f'<line x1="28" y1="{y+16}" x2="{W-28}" y2="{y+16}" stroke="{BORDER}"/>'
                    f'<circle cx="36" cy="{y-5}" r="4" fill="{ORANGE if i == 0 else DIM}"/>'
                    f'<text x="52" y="{y}" font-family="{MONO}" font-size="12" fill="{DIM if priv else BLUE}">{"🔒 " if priv else ""}{esc(c["repo"].split("/")[-1])}</text>'
                    f'<text x="300" y="{y}" font-family="{SANS}" font-size="14.5" font-style="{"italic" if priv else "normal"}" fill="{MUTED if priv else TEXT}">{esc(msg)}</text>'
                    f'<text x="{W-28}" y="{y}" text-anchor="end" font-family="{MONO}" font-size="11" letter-spacing="1" fill="{MUTED}">{esc(c["date"])}</text>')
    if not rows:
        body.append(f'<text x="28" y="90" font-family="{SANS}" font-size="15" fill="{MUTED}">No public commits yet.</text>')
    return frame(W, H, "LATEST COMMITS", "UPDATED " + stamp, "".join(body))

if __name__ == "__main__":
    d = mock() if MOCK else fetch()
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    for name, fn in (("stats", stats_card), ("languages", languages_card), ("heatmap", heatmap_card), ("commits", commits_card)):
        with open(os.path.join(OUT, f"{name}.svg"), "w") as f:
            f.write(fn(d, stamp))
        print("wrote", os.path.join(OUT, f"{name}.svg"))
