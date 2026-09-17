#!/usr/bin/env python3
"""Generate the SVG assets for the pauloes-btechs profile README.
Palette lifted from btechs.io: navy-black ground, Bitcoin orange accent, slate text."""
import math, random, os, html

OUT = os.path.join(os.path.dirname(__file__), "pauloes-btechs", "assets")
os.makedirs(OUT, exist_ok=True)

BG      = "#080D1A"
PANEL   = "#0C1324"
PANEL2  = "#101A30"
BORDER  = "#1E2A40"
TEXT    = "#E2E8F0"
MUTED   = "#94A3B8"
DIM     = "#475569"
ORANGE  = "#F7931A"
BLUE    = "#5B8DEF"
GREEN   = "#3FAE5E"
LINKEDIN= "#0A66C2"
SANS = "'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "'SFMono-Regular',SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

def esc(s): return html.escape(s, quote=True)

def grid_defs(step=40):
    return f'''<defs>
  <pattern id="grid" width="{step}" height="{step}" patternUnits="userSpaceOnUse">
    <path d="M {step} 0 L 0 0 0 {step}" fill="none" stroke="#94A3B8" stroke-opacity="0.07" stroke-width="1"/>
  </pattern>
  <radialGradient id="glow" cx="50%" cy="50%" r="50%">
    <stop offset="0%" stop-color="{ORANGE}" stop-opacity="0.35"/>
    <stop offset="100%" stop-color="{ORANGE}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="fade" x1="0" x2="1" y1="0" y2="0">
    <stop offset="0%" stop-color="{BG}" stop-opacity="0"/>
    <stop offset="100%" stop-color="{BG}" stop-opacity="1"/>
  </linearGradient>
</defs>'''

def write(name, svg):
    p = os.path.join(OUT, name)
    with open(p, "w") as f: f.write(svg)
    print("wrote", p)

# ---------------------------------------------------------------- header
def header():
    W, H = 1200, 320
    random.seed(7)
    hub = (860, 168)
    nodes = [(1040, 60), (1120, 220), (700, 40), (640, 262), (980, 290), (1150, 120), (560, 130)]
    lines, dots, signals = [], [], []
    for i, (x, y) in enumerate(nodes):
        lines.append(f'<line x1="{hub[0]}" y1="{hub[1]}" x2="{x}" y2="{y}" stroke="#94A3B8" stroke-opacity="0.28" stroke-width="1"/>')
        d = 2.2 + (i % 3) * 0.6
        dur = 2.4 + (i % 4) * 0.7
        dots.append(f'''<circle cx="{x}" cy="{y}" r="{d}" fill="{ORANGE}" fill-opacity="0.9">
      <animate attributeName="r" values="{d};{d+2.5};{d}" dur="{dur}s" begin="{i*0.35}s" repeatCount="indefinite"/>
      <animate attributeName="fill-opacity" values="0.9;0.35;0.9" dur="{dur}s" begin="{i*0.35}s" repeatCount="indefinite"/>
    </circle>''')
        if i % 2 == 0:
            signals.append(f'''<circle r="2.2" fill="{TEXT}">
      <animateMotion dur="{3+i*0.4}s" begin="{i*0.9}s" repeatCount="indefinite" path="M {hub[0]} {hub[1]} L {x} {y}"/>
      <animate attributeName="opacity" values="0;1;1;0" dur="{3+i*0.4}s" begin="{i*0.9}s" repeatCount="indefinite"/>
    </circle>''')
    # secondary edges between nodes for a mesh feel
    mesh = [(0,5),(1,4),(2,6),(3,6),(0,2)]
    for a,b in mesh:
        lines.append(f'<line x1="{nodes[a][0]}" y1="{nodes[a][1]}" x2="{nodes[b][0]}" y2="{nodes[b][1]}" stroke="#94A3B8" stroke-opacity="0.12" stroke-width="1"/>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Pauloes Berhe — technical product manager, founder, New York">
{grid_defs()}
<rect width="{W}" height="{H}" rx="18" fill="{BG}"/>
<rect width="{W}" height="{H}" rx="18" fill="url(#grid)"/>
<circle cx="{hub[0]}" cy="{hub[1]}" r="190" fill="url(#glow)"/>
<g>{''.join(lines)}</g>
<g>{''.join(dots)}</g>
<g>{''.join(signals)}</g>
<circle cx="{hub[0]}" cy="{hub[1]}" r="5" fill="{ORANGE}">
  <animate attributeName="r" values="5;8;5" dur="2.2s" repeatCount="indefinite"/>
</circle>
<circle cx="{hub[0]}" cy="{hub[1]}" r="5" fill="none" stroke="{ORANGE}" stroke-width="1.5">
  <animate attributeName="r" values="6;34" dur="2.2s" repeatCount="indefinite"/>
  <animate attributeName="stroke-opacity" values="0.8;0" dur="2.2s" repeatCount="indefinite"/>
</circle>
<rect x="0" y="0" width="{W}" height="{H}" rx="18" fill="none" stroke="{BORDER}" stroke-width="1"/>

<text x="56" y="86" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{ORANGE}">HELLO, WORLD  //  I'M</text>
<text x="54" y="150" font-family="{SANS}" font-size="58" font-weight="700" fill="{TEXT}" letter-spacing="-1">Pauloes Berhe</text>
<text x="56" y="188" font-family="{MONO}" font-size="13" letter-spacing="2.5" fill="{MUTED}">TECHNICAL PRODUCT MANAGER  ·  FOUNDER  ·  NEW YORK</text>
<text x="56" y="232" font-family="{SANS}" font-size="17" fill="{MUTED}">Product roadmaps and the infrastructure underneath them —</text>
<text x="56" y="256" font-family="{SANS}" font-size="17" fill="{MUTED}">Bitcoin, secure cloud, open-source public goods.</text>
<g font-family="{MONO}" font-size="11" letter-spacing="2" fill="{DIM}">
  <text x="56" y="296">BTECHS  ·  MIT DCI GLOBAL  ·  #STARTSMALL</text>
  <text x="{W-56}" y="296" text-anchor="end">STATUS: <tspan fill="{GREEN}">BUILDING</tspan></text>
</g>
<rect x="{W-50}" y="284" width="7" height="14" fill="{GREEN}">
  <animate attributeName="opacity" values="1;0;1" dur="1.1s" repeatCount="indefinite"/>
</rect>
</svg>'''
    write("header.svg", svg)

# ---------------------------------------------------------------- tab buttons
def tab(name, label, color, fill=True, sub=None, w=None):
    H = 46
    w = w or (len(label) * 9.6 + 70)
    w = int(w)
    txt = BG if fill else color
    bgc = color if fill else PANEL
    stroke = color
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{H}" viewBox="0 0 {w} {H}" role="img" aria-label="{esc(label)}">
<rect x="0.5" y="0.5" width="{w-1}" height="{H-1}" rx="10" fill="{bgc}" stroke="{stroke}" stroke-width="1.5"/>
<circle cx="22" cy="{H/2}" r="4" fill="{txt if fill else color}">
  <animate attributeName="fill-opacity" values="1;0.35;1" dur="2s" repeatCount="indefinite"/>
</circle>
<text x="36" y="{H/2+5}" font-family="{MONO}" font-size="13" font-weight="700" letter-spacing="1.5" fill="{txt}">{esc(label)}</text>
<text x="{w-16}" y="{H/2+5}" text-anchor="end" font-family="{MONO}" font-size="13" fill="{txt}">↗</text>
</svg>'''
    write(f"tab-{name}.svg", svg)

# ---------------------------------------------------------------- section label
def section(name, num, label, note=""):
    W, H = 1200, 54
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(label)}">
<rect width="{W}" height="{H}" fill="{BG}" rx="10"/>
<line x1="0" y1="{H-1}" x2="{W}" y2="{H-1}" stroke="{BORDER}"/>
<text x="20" y="34" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{ORANGE}">{num}</text>
<text x="66" y="35" font-family="{SANS}" font-size="20" font-weight="700" letter-spacing="1" fill="{TEXT}">{esc(label)}</text>
<text x="{W-20}" y="34" text-anchor="end" font-family="{MONO}" font-size="11" letter-spacing="2" fill="{DIM}">{esc(note)}</text>
<rect x="0" y="{H-3}" width="90" height="3" fill="{ORANGE}"/>
</svg>'''
    write(f"section-{name}.svg", svg)

# ---------------------------------------------------------------- project card
def card(name, title, kicker, lines, chips, link_label, accent=ORANGE, status="LIVE"):
    W, H = 580, 270
    body = "".join(f'<text x="28" y="{118 + i*22}" font-family="{SANS}" font-size="14.5" fill="{MUTED}">{esc(l)}</text>' for i, l in enumerate(lines))
    x = 28; chip_svg = []
    for c in chips:
        cw = int(len(c) * 7.2 + 22)
        chip_svg.append(f'<rect x="{x}" y="{H-72}" width="{cw}" height="24" rx="6" fill="{PANEL2}" stroke="{BORDER}"/>'
                        f'<text x="{x+cw/2}" y="{H-56}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{TEXT}">{esc(c)}</text>')
        x += cw + 8
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(title)}">
{grid_defs(30)}
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14" fill="{PANEL}" stroke="{BORDER}"/>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14" fill="url(#grid)"/>
<rect x="0" y="0" width="5" height="{H}" rx="2" fill="{accent}"/>
<text x="28" y="40" font-family="{MONO}" font-size="11" letter-spacing="2.5" fill="{accent}">{esc(kicker)}</text>
<g font-family="{MONO}" font-size="10.5" letter-spacing="2">
  <circle cx="{W-28-len(status)*7.5-14}" cy="36" r="3.5" fill="{GREEN if status=='LIVE' else (BLUE if status=='IN PROGRESS' else DIM)}">
    <animate attributeName="fill-opacity" values="1;0.3;1" dur="1.8s" repeatCount="indefinite"/>
  </circle>
  <text x="{W-28}" y="40" text-anchor="end" fill="{MUTED}">{esc(status)}</text>
</g>
<text x="28" y="80" font-family="{SANS}" font-size="26" font-weight="700" fill="{TEXT}" letter-spacing="-0.5">{esc(title)}</text>
{body}
<g>{''.join(chip_svg)}</g>
<line x1="28" y1="{H-30}" x2="{W-28}" y2="{H-30}" stroke="{BORDER}"/>
<text x="28" y="{H-11}" font-family="{MONO}" font-size="11" letter-spacing="1.5" fill="{accent}">{esc(link_label)}  ↗</text>
</svg>'''
    write(f"card-{name}.svg", svg)

# ---------------------------------------------------------------- timeline
def timeline():
    W, H = 1200, 330
    items = [
        ("2025 → NOW", "Btechs", "Founder & Technical Lead",
         ["Bitcoin + AI workshops, secure", "cloud & security engineering.", "Leads MIT DCI Global Research Map."], ORANGE),
        ("2024 → 2026", "Bitcoin Innovation Hub", "Co-Founder & CEO",
         ["Bitcoinized settlement on", "BTCPayServer — fees cut 90%+", "for small businesses. #startsmall."], BLUE),
        ("2022 → 2024", "Bloomberg LP", "Sr. Technical Product Manager",
         ["20+ digital properties,", "1M+ monthly users,", "200+ features shipped."], GREEN),
        ("2014 → 2022", "City University of Seattle", "Technical Product Manager",
         ["Led the Azure migration and", "a $2.8M infrastructure", "program end to end."], MUTED),
    ]
    colw = (W - 80) / 4
    parts = []
    y_line = 92
    for i, (date, org, role, lines, col) in enumerate(items):
        x = 40 + i * colw
        cx = x + 14
        parts.append(f'''<circle cx="{cx}" cy="{y_line}" r="7" fill="{BG}" stroke="{col}" stroke-width="2"/>
<circle cx="{cx}" cy="{y_line}" r="3" fill="{col}"><animate attributeName="r" values="3;4.5;3" dur="2.4s" begin="{i*0.5}s" repeatCount="indefinite"/></circle>
<text x="{x}" y="{y_line-22}" font-family="{MONO}" font-size="11" letter-spacing="2.5" fill="{col}">{esc(date)}</text>
<text x="{x}" y="{y_line+44}" font-family="{SANS}" font-size="19" font-weight="700" fill="{TEXT}">{esc(org)}</text>
<text x="{x}" y="{y_line+68}" font-family="{MONO}" font-size="11" letter-spacing="1" fill="{MUTED}">{esc(role.upper())}</text>
''' + "".join(f'<text x="{x}" y="{y_line+100+j*21}" font-family="{SANS}" font-size="14" fill="{MUTED}">{esc(l)}</text>' for j, l in enumerate(lines)))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Career timeline">
{grid_defs()}
<rect width="{W}" height="{H}" rx="16" fill="{BG}"/>
<rect width="{W}" height="{H}" rx="16" fill="url(#grid)"/>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="16" fill="none" stroke="{BORDER}"/>
<line x1="40" y1="{y_line}" x2="{W-40}" y2="{y_line}" stroke="{BORDER}" stroke-width="2"/>
<line x1="40" y1="{y_line}" x2="{W-40}" y2="{y_line}" stroke="{ORANGE}" stroke-width="2" stroke-dasharray="6 14" stroke-opacity="0.6">
  <animate attributeName="stroke-dashoffset" values="0;-40" dur="2s" repeatCount="indefinite"/>
</line>
{''.join(parts)}
<text x="{W-24}" y="{H-16}" text-anchor="end" font-family="{MONO}" font-size="10.5" letter-spacing="2" fill="{DIM}">11+ YEARS  ·  ENTERPRISE PLATFORM PRODUCTS  →  MISSION-DRIVEN BITCOIN VENTURES</text>
</svg>'''
    write("timeline.svg", svg)

# ---------------------------------------------------------------- footer
def footer():
    W, H = 1200, 110
    dots = "".join(f'<circle cx="{random.randint(30,W-30)}" cy="{random.randint(20,H-20)}" r="{random.choice([1,1.5,2])}" fill="{ORANGE}" fill-opacity="{random.choice([0.3,0.5,0.8])}"><animate attributeName="fill-opacity" values="0.2;0.9;0.2" dur="{random.uniform(2,5):.1f}s" repeatCount="indefinite"/></circle>' for _ in range(28))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Building resilient, self-sovereign digital infrastructure">
{grid_defs()}
<rect width="{W}" height="{H}" rx="16" fill="{BG}"/>
<rect width="{W}" height="{H}" rx="16" fill="url(#grid)"/>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="16" fill="none" stroke="{BORDER}"/>
{dots}
<text x="{W/2}" y="50" text-anchor="middle" font-family="{SANS}" font-size="20" font-weight="700" fill="{TEXT}">Building resilient, self-sovereign digital infrastructure.</text>
<text x="{W/2}" y="78" text-anchor="middle" font-family="{MONO}" font-size="11.5" letter-spacing="3" fill="{MUTED}">SECURE  ·  SCALE  ·  ADVANCE</text>
</svg>'''
    write("footer.svg", svg)

if __name__ == "__main__":
    header()
    tab("btechs",   "BTECHS.IO",     ORANGE, fill=True)
    tab("about",    "ABOUT", ORANGE, fill=False)
    tab("pauloes",  "PAULOES.COM",   BLUE,   fill=True)
    tab("linkedin", "LINKEDIN",      LINKEDIN, fill=True)
    tab("email",    "EMAIL ME",      GREEN,  fill=True)
    tab("org",      "@BTECHS-ORG",   MUTED,  fill=False)
    section("about",    "01", "What I'm building", "PRODUCT × INFRASTRUCTURE")
    section("projects", "02", "Featured projects", "SHIPPED & IN FLIGHT")
    section("portfolio","03", "Portfolio / experience", "11+ YEARS")
    section("stack",    "04", "What I build with", "TOOLS & PLATFORMS")
    section("stats",    "05", "GitHub activity", "COMMITS · STREAKS · LANGUAGES")
    card("btechs", "Btechs", "COMPANY  ·  FOUNDER & TECHNICAL LEAD",
         ["Bitcoin + AI workshops, digital infrastructure and",
          "security engineering for people, institutions and",
          "communities. Self-sovereign by design."],
         ["Next.js", "Google Cloud", "Bitcoin", "Security"], "btechs.io", ORANGE, "LIVE")
    card("dci", "DCI Global Research Map", "MIT DIGITAL CURRENCY INITIATIVE",
         ["Interactive map of the global Bitcoin research",
          "network — entities, researchers and programs.",
          "Supabase Auth + RLS hardening, Vercel deploys."],
         ["Vite", "React", "Express", "Supabase", "Vercel"], "dci-global-research-map.vercel.app", BLUE, "LIVE")
    card("portfolio", "pauloes.com", "PERSONAL PORTFOLIO  ·  OPEN SOURCE",
         ["Story-driven product portfolio: roles, programs,",
          "outcomes and the charts behind them. Clean, fast,",
          "recruiter-readable. MIT licensed."],
         ["Next.js 14", "React", "Canvas", "Vercel"], "pauloes.com  ·  source on GitHub", GREEN, "LIVE")
    card("t7f", "7eventh Foundation", "NONPROFIT  ·  CLIENT BUILD",
         ["Donation-facing site for the 7eventh Foundation.",
          "Resend email pipeline, Cloudflare DNS, DMARC/SPF",
          "hardening and a Vercel production deploy."],
         ["Next.js 16", "TypeScript", "Resend", "Cloudflare"], "7eventhfoundation.org", ORANGE, "LIVE")
    card("rwc", "Robots Will Cry", "MUSIC  ·  ART SITE  ·  BITCOIN COMMERCE",
         ["Cinematic boot sequence into a scrolling page-world",
          "for an EP release. DSP rail, sticky player, and a",
          "BTCPay-powered shop with checkout."],
         ["Next.js 15", "TypeScript", "BTCPay", "Resend"], "robotswillcry.com", BLUE, "IN PROGRESS")
    card("aegis", "AEGIS — CISO Auditor", "AI AGENT  ·  SECURITY TOOLING",
         ["Portable CISO-level security auditor skill: read-",
          "only recon, findings with file:line evidence, and",
          "a sequenced remediation plan for GCP/PaaS stacks."],
         ["Claude Skills", "Bash", "GCP", "Threat Modeling"], "private  ·  ask me about it", GREEN, "IN PROGRESS")
    timeline()
    footer()
