# pauloes-btechs/pauloes-btechs — Agent Guide

GitHub profile README repository. The repo is named after the username
(`pauloes-btechs`), must stay **public**, and its `README.md` renders on
github.com/pauloes-btechs. It is not an application: there is no server, no
database, and no runtime to keep healthy. "Local dev" means running the two
Python scripts that produce the SVG assets and activity cards.

## Stack

- **Runtime:** Python 3 (standard library only — zero third-party dependencies,
  no `requirements.txt`). CI pins Python 3.12; local 3.13 verified.
- **Tooling:** `gh` CLI (used by `publish.sh` only).
- **CI:** `.github/workflows/tracker.yml` — every 6 hours and on every push to
  `main`; rebuilds the stats/language/heatmap/commits/snake SVGs and publishes
  them to the `output` branch. The README embeds them from
  `raw.githubusercontent.com/pauloes-btechs/pauloes-btechs/output/`.

## Commands

```bash
# Rebuild the 20 hand-designed README SVGs (header, tabs, cards, sections).
# Path quirk: the script writes to <script_dir>/pauloes-btechs/assets, so it
# expects to live in the PARENT of a folder named pauloes-btechs. To run
# against this checkout:
cp gen_assets.py ../gen_assets.py && (cd .. && python3 gen_assets.py) && rm ../gen_assets.py

# Build the GitHub activity tracker SVGs into dist/ with mock data
# (no token needed — this is the local-dev mode):
GH_USER=pauloes-btechs python3 scripts/build_stats.py --mock

# Real build (CI does this; needs a token, network):
GITHUB_TOKEN=... GH_USER=pauloes-btechs python3 scripts/build_stats.py

# One-shot commit/publish helper (interactive; needs `gh auth login`):
bash publish.sh
```

## Environment variables

| Var | Required | Notes |
|---|---|---|
| `GH_USER` | no | defaults to `pauloes-btechs` |
| `GITHUB_TOKEN` / `GH_PAT` | no locally | CI injects them; `GH_PAT` additionally counts private repos |
| `OUT_DIR` | no | output dir for tracker SVGs, default `dist/` |

No secrets are needed for local development (`--mock` mode avoids the API).

## Workflow

1. Edit `gen_assets.py` (palette/design constants at the top), re-run it, and
   commit the regenerated SVGs in `assets/`. Assets are deterministic —
   regeneration is byte-identical when inputs are unchanged.
2. Edit `README.md` (content sections) directly; commit.
3. Tracker cards are never committed — CI rebuilds and pushes them to the
   `output` branch.

## Codebase map

See [codebase-map.md](codebase-map.md).

## Local verification

Verified during onboarding (2026-10-30):

```bash
python3 -m py_compile gen_assets.py scripts/build_stats.py   # pass
GH_USER=pauloes-btechs python3 scripts/build_stats.py --mock  # 4 SVGs in dist/, valid XML
# gen_assets.py: 20/20 SVGs regenerate byte-identical to committed assets
```

No lint, typecheck, or test suite exists in the repo. `convert` (ImageMagick)
is available to rasterize an SVG as a visual sanity check.

## Snapshot

- `snapshotId`: `r79z8hrytbl8cmrs9ggi:default`
- Captured: `2026-10-30T15:30:28Z`
- State: fresh checkout of `main` with Python 3.13 available; dev stack verified healthy.
